from flask import Flask,request,abort
from linebot import LineBotApi,WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent,TextMessage,TextSendMessage
import os
from db_line import new_register, reg_menu_name, reg_menu_recipe, find_latest_value, db_search

app = Flask(__name__)

# 環境変数の取得
# YOUR_CHANNEL_ACCESS_TOKEN = "yTBzjw46j2Jvaf6RiGPF92ZpDWdZiARi76/HVerrhILTowJ/1vYB+eWRsM9DRYvDgQgFd/DS4HKOOsoBjeOnyqWmCTi9njLPcqt4ZwmmsSeUxwPJ6yC/VuhKsesCtSWcC+WQNedupLjxrdptlyrPhAdB04t89/1O/w1cDnyilFU="
# YOUR_CHANNEL_SECRET = "23efb4818161eca47a07b09f6f58886b"
YOUR_CHANNEL_ACCESS_TOKEN = os.environ['YOUR_CHANNEL_ACCESS_TOKEN']
YOUR_CHANNEL_SECRET = os.environ['YOUR_CHANNEL_SECRET']
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

# LINEからメッセくるとここに入る
@app.route("/index", methods=["POST"])
def index():
    return

# LINEからメッセくるとここに入る
@app.route("/callback", methods=["POST"])
def callback():
    #絶対いる
    signature=request.headers["X-Line-Signature"]
    #情報をうけとる
    body=request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 検証に使う
    if event.reply_token == "00000000000000000000000000000000":
        return 
        
    # ここから下で処理を書く
    message = event.message.text
    user_lineid = event.source.user_id
    if message == "レシピを登録":
        new_register(user_lineid)
        return_message = '料理名を入力してください'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=return_message))
    elif message == "レシピを表示":
        return_message = '料理名を入力してください'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=return_message))
    else:
        if find_latest_value(user_lineid, message, 'user_id') == False:
            # user_idが見つからない => レシピを登録してないとき
            return_message = 'レシピがありません'
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=return_message))
        elif find_latest_value(user_lineid, message, 'recipe') == False:
            # 最新からmenu_recipeが見つからない => レシピを登録する
            menu_recipe = message
            reg_menu_recipe(user_lineid, menu_recipe)
            return_message = 'レシピが登録されました\nメニュー登録完了'
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=return_message))
        elif find_latest_value(user_lineid, message, 'name') == False:
            # 最新からmenu_nameが見つからない => 料理名を登録する
            menu_name = message
            reg_menu_name(user_lineid, menu_name)
            return_message = '料理名が登録されました\nレシピを入力してください'
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=return_message))
        elif len(db_search(user_lineid, menu_name)) == 0:
            # 全体でmenu_nameで検索したら見つかった => レシピを表示する
            return_recipe = db_search(user_lineid,menu_name)
            return_message = 'こちらがレシピです\n' + return_recipe
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=return_message))
        else: 
          return_message = '入力が間違っています'
          line_bot_api.reply_message(event.reply_token,TextSendMessage(text=message))

if __name__=="__main__":
    port=int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
