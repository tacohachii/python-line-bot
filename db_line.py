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
    cursor.execute("UPDATE recipe SET recipe = '{0}' WHERE id = (SELECT id FROM recipe WHERE user_id= '{1}' ORDER BY id DESC LIMIT 1);".format(menu_recipe, user_lineid))
    conn.commit()
    return 

def db_search(user_lineid, menu_name):
    cursor.execute("SELECT * FROM recipe WHERE user_id= '{0}' and name= '{1}';".format(user_lineid, menu_name))
    hoge = cursor.fetchall()
    return hoge[0][0]

def serch_user(user_lineid):
      cursor.execute("SELECT * FROM recipe WHERE user_id= '{0}'".format(user_lineid))
      hoge = cursor.fetchall()
      if len(hoge) == 0:
          return False
      else:
          return True

def check_latest_column(user_lineid, column):
    if column == 'user_id':
        cursor.execute("SELECT * FROM recipe WHERE user_id= '{0}'".format(user_lineid))
    if column == 'name':
        # ユーザーの最新の情報から，nameが空でrecipeが空のものを抜き出す
        cursor.execute("SELECT * FROM recipe WHERE name IS NULL and recipe IS NULL and id = (SELECT id FROM recipe WHERE user_id= '{0}' ORDER BY id);".format(user_lineid))
    if column == 'recipe':
        # ユーザーの最新の情報から，nameに値があってrecipeが空のものを抜き出す
        cursor.execute("SELECT * FROM recipe WHERE recipe IS NOT NULL and recipe IS NULL and id = (SELECT id FROM recipe WHERE user_id= '{0}' ORDER BY id);".format(user_lineid))
    
    hoge = cursor.fetchall()
    if len(hoge) != 0:
        return False
    else:
        return True

