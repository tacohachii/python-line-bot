import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()
    
def new_register(user_lineid):
    cursor.execute("INSERT INTO recipe(user_id) VALUES('{0}');".format(user_lineid))
    conn.commit()
    return

def reg_menu_name(user_lineid, menu_name):
    # 最新のユーザーを取ってきてメニュー名を入れている
    cursor.execute("UPDATE recipe SET name = '{0}' WHERE id = (SELECT id FROM recipe WHERE user_id= '{1}' ORDER BY id DESC LIMIT 1);".format(menu_name, user_lineid))
    conn.commit()
    return 

def reg_menu_recipe(user_lineid, menu_recipe):
    # 最新のユーザーを取ってきてレシピを入れている
    cursor.execute("UPDATE recipe SET recipe = '{0}' WHERE id = (SELECT id FROM recipe WHERE user_id= '{1}' ORDER BY id DESC LIMIT 1);".format(menu_recipe, user_lineid))
    conn.commit()
    return 

def db_search(user_lineid, menu_name):
    # 同じ名前で登録した場合は最新のものを取ってくる
    cursor.execute("SELECT recipe FROM recipe WHERE user_id= '{0}' and name= '{1}' and recipe IS NOT NULL ORDER BY id DESC LIMIT 1;".format(user_lineid, menu_name))
    hoge = cursor.fetchall()
    if len(hoge) == 0:
        return hoge
    else:
        return hoge[0][0]

# 最新のユーザーは登録が終わっているか？
# name も recipe も値を持っている ==> 登録終わっている/新規に追加可能
def finish_register(user_lineid):
    cursor.execute("SELECT * FROM recipe WHERE name IS NOT NULL and recipe IS NOT NULL and id = (SELECT id FROM recipe WHERE user_id= '{0}' ORDER BY id DESC LIMIT 1)".format(user_lineid))
    hoge = cursor.fetchall()
    if len(hoge) == 0:
        return False
    else:
        return True

def serch_user(user_lineid):
    cursor.execute("SELECT * FROM recipe WHERE user_id= '{0}'".format(user_lineid))
    hoge = cursor.fetchall()
    if len(hoge) == 0:
        return False
    else:
        return True

def check_latest_column(user_lineid, column):
    if column == 'name':
        # ユーザーの最新の情報から，nameが空でrecipeが空のものを抜き出す
        cursor.execute("SELECT * FROM recipe WHERE name IS NULL and recipe IS NULL and id = (SELECT id FROM recipe WHERE user_id= '{0}' ORDER BY id DESC LIMIT 1);".format(user_lineid))
    if column == 'recipe':
        # ユーザーの最新の情報から，nameに値があってrecipeが空のものを抜き出す
        cursor.execute("SELECT * FROM recipe WHERE name IS NOT NULL and recipe IS NULL and id = (SELECT id FROM recipe WHERE user_id= '{0}' ORDER BY id DESC LIMIT 1);".format(user_lineid))
    
    hoge = cursor.fetchall()
    if len(hoge) != 0:
        return False
    else:
        return True

