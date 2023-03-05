# import pandas as pd
import psycopg2


# vps_list = ['Бутово','Дегунино','Ростокино','Куркино','Царицыно']
# Butovo = ['Гагарин', 'Леонов', 'Комаров']
# Degun = ['Титов', 'Терешкова', 'Крамаренко','Чкалов']
#
# vps_dict = {'Бутово': ['Гагарин', 'Леонов', 'Комаров'],
#             'Дегунино': ['Титов', 'Терешкова', 'Крамаренко', 'Чкалов'],
#             'Ростокино': ['Титов-p', 'Терешкова-p', 'Крамаренко-p', 'Чкалов-p'],
#             'Куркино': ['Титов-k', 'Терешкова-k', 'Крамаренко-k', 'Чкалов-k'],
#             'Царицыно': ['Цитов', 'Церешкова', 'ЦКрамаренко', 'ЦЧкалов'],
#             'Некрасовка': ['Нитов', 'НТерешкова', 'НКрамаренко', 'НЧкалов'],
#             }
#


my_db = psycopg2.connect(
  database="jurnal_db",
  user="postgres",
  password="1234",
  host="localhost",
  port="5432"
)


mycursor = my_db.cursor()



# mycursor.execute(f"insert into jurnal_tab (id_j, vps_j, fio_j, data_time, status) values ('555','{vps_name}','{fio}','{date_}', '{stat_tex}')");
# my_db.commit()

mycursor.execute(f"DELETE FROM spisok_vps WHERE name_vps = 'Дегунино' AND fio = 'Исправлен555'");
my_db.commit()
