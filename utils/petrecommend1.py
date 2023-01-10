import pandas as pd
import numpy as np
import random
from sqlalchemy import create_engine, text  # pip install pymysql && python -m pip install mysql-connector
import json

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


def connect_my_sql():
    mysql_engine = create_engine('mysql+pymysql://root:root@localhost:3306/pet')
    return mysql_engine


# ----------------------------------以下為推薦系統----------------------------------

def read_pets_file(TypeIWant):
    # DataFrame
    sql_commend = 'select * from `pet_score`'
    mysql_engine = connect_my_sql()
    df = pd.read_sql(sql=sql_commend, con=mysql_engine)
    # print(df)
    #  column list and clean
    dlist = []
    for x in range(len(df.columns)):
        dlist.append(df.columns[x])

    # 各種類動物品種list
    dog_list = dlist[:-13]
    cat_list = dlist[-13:]
    all_list = dlist

    # dog df
    df_dogs = df.iloc[:, :-13]

    # cat df
    df_cats = df.iloc[:, -13:]

    # 檢查寵物種類
    if TypeIWant == '狗':
        return df_dogs, dog_list
    elif TypeIWant == '貓':
        return df_cats, cat_list
    else:
        return df, all_list


def random_pet_rec(my_condition):
    df, col = read_pets_file(my_condition['Type'])

    r = random.choice(col)

    compare_data = df[df[r] == 1]
    score_dict = {}
    for y in col:
        ratio_count = round(len(compare_data[compare_data[y] == 1]) / len(compare_data), 3)
        score_dict[y] = ratio_count

    sort_list = (sorted(score_dict.items(), key=lambda x: x[1], reverse=True))
    corr = random.choice(sort_list[1:4])
    for i in range(4, 7):
        corr += sort_list[i]
    corr_recommend = []
    for x in range(len(corr)):
        if x % 2 != 1:
            corr_recommend.append(corr[x])

    rand_recom_pets = [r] + corr_recommend
    return rand_recom_pets


def recommend_method(BreedIWant, my_condition):
    df, col = read_pets_file(my_condition['Type'])
    count = len(BreedIWant)
    r = random.choice(BreedIWant)

    compare_data = df[df[r] == 1]
    score_dict = {}
    for y in col:
        ratio_count = round(len(compare_data[compare_data[y] == 1]) / len(compare_data), 3)
        score_dict[y] = ratio_count

    sort_list = (sorted(score_dict.items(), key=lambda x: x[1], reverse=True))
    new_sort_list = []
    for j in sort_list:
        if j[0] not in BreedIWant:
            new_sort_list.append(j)

    corr = random.choice(new_sort_list[0:3])
    for i in range(3, 7 - count):
        corr += new_sort_list[i]
    corr_recommend = []
    for x in range(len(corr)):
        if x % 2 != 1:
            corr_recommend.append(corr[x])

    recom_pets = BreedIWant + corr_recommend

    return recom_pets


def recommend_final(BreedIWant, my_condition):
    # 串聯資料庫
    sql_commend = 'select * from `pet_adopt_list`'
    mysql_engine = connect_my_sql()
    df0 = pd.read_sql(sql=sql_commend, con=mysql_engine)
    final = []

    if my_condition['Type'] not in ['狗', '貓']:
        df1 = df0
    else:
        test1 = (df0['pet_category'] == my_condition['Type'])
        df1 = df0[test1]

    for i in BreedIWant:
        test2 = (df1['pet_variety'] == i)  # 選取推薦
        df2 = df1[test2]

        if len(df2) == 0:
            continue
        else:
            if my_condition['Sex'] not in ['公', '母']:
                try:
                    df3 = df2.sample(n=3)  # 隨機取3
                except ValueError:  # 小於三個則全選
                    df3 = df2
            else:
                test3 = (df2['pet_sex'] == my_condition['Sex'])
                try:
                    df3 = df2[test3].sample(n=3)  # 隨機取3
                except ValueError:  # 小於三個則全選
                    df3 = df2[test3]
            final += df3.to_dict('records')

    if len(final) < 15:  # 若沒有補滿15個推薦，則都推薦混種
        if my_condition['Sex'] not in ['公', '母']:
            df4 = df1
        else:
            test4 = (df1['pet_sex'] == my_condition['Sex'])
            df4 = df1[test4]
        if my_condition["Type"] == '狗':
            test5 = (df4['pet_variety'] == '混種狗')
            df5 = df4[test5].sample(n=15 - len(final))
        elif my_condition["Type"] == '貓':
            test5 = (df4['pet_variety'] == '混種貓')
            df5 = df4[test5].sample(n=15 - len(final))
        else:
            df5 = (df4[[('混種' in x) for x in df4['pet_variety']]]).sample(n=15 - len(final))
        final += df5.to_dict('records')

    return final


def show_recommend_pets(my_choice, my_condition):
    count = len(my_choice)
    if count == 0:
        rand_recom_pets = random_pet_rec(my_condition)
        final = recommend_final(rand_recom_pets, my_condition)
        result = json.dumps(final, ensure_ascii=False)
        return result
    elif count < 5 and count > 0:
        recom_pets = recommend_method(my_choice, my_condition)
        final = recommend_final(recom_pets, my_condition)
        result = json.dumps(final, ensure_ascii=False)
        return result
    else:
        final = recommend_final(my_choice, my_condition)
        result = json.dumps(final, ensure_ascii=False)
        return result


def recommend_insert_sql(data):
    engine = connect_my_sql()
    engine.execute(
        "CREATE TABLE IF NOT EXISTS `recommend` (`user_id` VARCHAR(100) PRIMARY KEY, `recommend_pets` VARCHAR(10000));")
    values = [json.loads(data)['user_id'], str(json.loads(data)['recommend']).replace("\'", "\"")]
    data_insert_sql = f"REPLACE INTO `recommend` (`user_id`,`recommend_pets`) VALUES ('{values[0]}','{values[1]}');"
    db.engine.execute(text(data_insert_sql))


def recommend_main(id):
    sql_command = f'select * from `userinfo` where user_id="{id}"'
    mysql_engine = connect_my_sql()
    df0 = pd.read_sql(sql=sql_command, con=mysql_engine)
    user_data = df0.to_dict('records')
    try:
        my_choice = user_data[0]['prefer_pet_variety'].split(',')
    except:
        my_choice = []
    my_condition = {'Type': user_data[0]['prefer_pet_category'], 'Sex': user_data[0]['prefer_pet_sex']}
    data = show_recommend_pets(my_choice, my_condition)
    resultdata = '{"user_id":' + f'"{id}"' + ', "recommend":' + data + '}'
    recommend_insert_sql(resultdata)
    return resultdata


if __name__ == "__main__":
    recommend_main('Gfo7AeUgV7KH4zEs7LXmCu')
