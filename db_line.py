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
    cursor.execute("UPDATE recipe SET name = '{0}' WHERE id = (SELECT id FROM recipe WHERE user_id= '{1}' ORDER BY id)".format(menu_name, user_lineid))
    conn.commit()
    return 
    
def reg_menu_recipe(user_lineid, menu_recipe):
    cursor.execute("UPDATE recipe SET recipe = '{0}' WHERE id = (SELECT id FROM recipe WHERE user_id= '{1}' ORDER BY id)".format(menu_recipe, user_lineid))
    conn.commit()
    return 

def db_search(user_lineid, menu_name):
    cursor.execute("SELECT * FROM recipe WHERE user_id= '{0}' and name= '{1}'".format(user_lineid, menu_name))
    hoge = cursor.fetchall()
    return hoge[0][0]

def find_latest_value(user_lineid, message, column):
    if column == 'user_id':
        cursor.execute("SELECT * FROM recipe WHERE user_id= '{0}'".format(user_lineid))
    if column == 'name':
        menu_name = message
        cursor.execute("SELECT * FROM recipe WHERE name = '{0}' and id = (SELECT id FROM recipe WHERE user_id= '{1}' ORDER BY id)".format(menu_name, user_lineid))
    if column == 'recipe':
        menu_recipe = message
        cursor.execute("SELECT * FROM recipe WHERE recipe = '{0}' and id = (SELECT id FROM recipe WHERE user_id= '{1}' ORDER BY id)".format(menu_recipe, user_lineid))
    
    hoge = cursor.fetchall()
    if len(hoge) == 0:
        return False
    else:
        return True

