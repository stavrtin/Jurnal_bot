from datetime import datetime
import view
import controller
import psycopg2


# vps_list = ['Бутово','Дегунино','Ростокино','Куркино','Царицыно']
#
# vps_dict = {'Бутово':['Гагарин', 'Леонов', 'Комаров'],
#             'Дегунино'  :['Дитов', 'Дерешкова', 'Драмаренко','Дкалов'],
#             'Ростокино' :['Титов-p', 'Терешкова-p', 'Крамаренко-p','Чкалов-p'],
#              'Куркино'   :['Титов-k', 'Терешкова-k', 'Крамаренко-k','Чкалов-k'],
#             'Царицыно'  :['Цитов', 'Церешкова', 'ЦКрамаренко','ЦЧкалов', 'ЦКожедуб', 'ЦПокрышкин'],
#              'Некрасовка':['Нитов', 'НТерешкова', 'НКрамаренко','НЧкалов'],
#              'Перово':['Питов', 'ПТерешкова', 'ПКрамаренко','ПЧкалов'],
#             }

my_db = psycopg2.connect(
    # -------------
    database="jurnal_db",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"

)

mycursor = my_db.cursor()


def read_db_for_criate_button_vps():
    # ----------- считываем БД со списком сотруднико, табл "spisok" -------
    # my_db = psycopg2.connect(
    #     database="jurnal_db",
    #     user="postgres",
    #     password="1234",
    #     host="localhost",
    #     port="5432"
    # )
    #
    # mycursor = my_db.cursor()

    vps_dict = {}

    # ---- готовый запрос на создание таблицы -----
    sql_all_rec = f"SELECT DISTINCT name_vps FROM spisok_vps"
    mycursor.execute(sql_all_rec)
    result = mycursor.fetchall()
    vps_uniq_list = [i[0] for i in result]

    for i in vps_uniq_list:
        sql_fio_from_vps = f"SELECT fio FROM spisok_vps " \
                           f"where name_vps = '{i}'"
        mycursor.execute(sql_fio_from_vps)
        result_fio = mycursor.fetchall()
        fio_list = [j[0] for j in result_fio]
        vps_dict.update({i: fio_list})

    return vps_dict


def read_db_for_criate_fio(status):

    vps_dict = {}

    # ---- готовый запрос на создание таблицы -----
    sql_all_rec = f"SELECT DISTINCT name_vps FROM spisok_vps"
    mycursor.execute(sql_all_rec)
    result = mycursor.fetchall()
    vps_uniq_list = [i[0] for i in result]

    for i in vps_uniq_list:
        sql_fio_from_vps = f"SELECT fio FROM spisok_vps " \
                           f"where name_vps = '{i}'"  # ------ если в другой таблице status <> status !!!!
        mycursor.execute(sql_fio_from_vps)
        result_fio = mycursor.fetchall()
        fio_list = [j[0] for j in result_fio]
        vps_dict.update({i: fio_list})

    return vps_dict



def record_contact(message, fio, vps_name, status):
    if message.text != None:
        view.start_menu(message)

    else:
        if message.contact is not None:  # Если присланный объект <strong>contact</strong> не равен нулю
            phone_number = message.contact.phone_number
            now = datetime.now()
            date_ = now.strftime("%d-%m-%Y %H:%M")

            doc = open('client.txt', 'a', encoding='utf-16')
            # doc.write(f"\nВПС - {vps_name} - ФИО - {fio} Телефон - {phone_number} Получен - {date_}" )
            if status == 'где ВЫДАЁТСЯ ☏':
                stat_tex = 'ПОЛУЧИЛ'

            elif status == 'куда СДАЕТСЯ ☎':
                stat_tex = 'СДАЛ'


            doc.write(f"\n{vps_name};{fio};{phone_number};Получен;{date_}")
            insert_data(vps_name, fio, phone_number, date_, stat_tex)
            doc.close()
            view.confirm_recording_by_chat(message, fio, stat_tex, phone_number, vps_name, date_)
            # controller.bot.send_message(message.chat.id, f'{fio} {stat_tex} {phone_number} в {vps_name} - {date_}') # -- вывод сообщ на экран телеф
            view.start_menu(message)

vps_dict = read_db_for_criate_button_vps()

vps_dict_for_take = read_db_for_criate_fio('СДАЛ')
vps_dict_for_return = read_db_for_criate_fio('ПОЛУЧИЛ')




def insert_data(vps_name, fio, phone_number, date_, stat_tex):
    # ----- добавление записи -----------
    # mycursor = read_db()
    mycursor.execute(     f"insert into jurnal_tab (vps_j, fio_j, phone_number_j, date_time, status) values "
                                                f"('{vps_name}','{fio}','{phone_number}','{date_}', '{stat_tex}')");
    my_db.commit()
