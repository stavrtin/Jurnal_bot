from datetime import datetime
import view
import controller
import psycopg2
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)



def read_db(text_status):
    # text_status = 'где ВЫДАЁТСЯ ☏'
    # text_status = 'куда СДАЕТСЯ ☎'
    #------ СЧИТАЕМ ДАННЫЕ ИЗ бд ------------
    my_db = psycopg2.connect(
        # -------------
        database="jurnal_db",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432",
    )
    mycursor = my_db.cursor()

    vps_dict = {}

    # ---- готовый запрос на создание таблицы -----
    sql_all_rec = f"SELECT DISTINCT name_vps FROM spisok_vps" \
                  f" ORDER BY name_vps"
    mycursor.execute(sql_all_rec)
    result = mycursor.fetchall()
    vps_uniq_list = [i[0] for i in result]

    if text_status == 'где ВЫДАЁТСЯ ☏':
        status_chois = 'СДАЛ'
    elif text_status == 'куда СДАЕТСЯ ☎':
        status_chois = 'ПОЛУЧИЛ'

    for i in vps_uniq_list:
        # --------------status_chois - определяет текущий записанный в psw статус фио - вылан или сдан--
        sql_fio_from_vps = f"SELECT fio FROM spisok_vps " \
                           f"where name_vps = '{i}' and psw ='{status_chois}'" \
                           f" ORDER BY fio "
        mycursor.execute(sql_fio_from_vps)
        result_fio = mycursor.fetchall()
        fio_list = [j[0] for j in result_fio]
        vps_dict.update({i: fio_list})

    mycursor.close()
    my_db.close() #--------------- закрывашка БД ---------

    data_db = vps_dict
    logging.warning("считали БД")
    return data_db


    #///-------------------------------------попробуем засунуть в модель -

def record_contact(message, fio, vps_name, status):
    if message.text != None:
        view.start_menu(message)

    else:
        if message.contact is not None:  # Если присланный объект <strong>contact</strong> не равен нулю
            phone_number = message.contact.phone_number
            now = datetime.now()
            date_ = now.strftime("%d-%m-%Y %H:%M")
            # date_ = now.strftime("%Y-%m-%d %H:%M")

            doc = open('client.txt', 'a', encoding='utf-16')

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



def insert_data(vps_name, fio, phone_number, date_, stat_tex):
    # ----- добавление записи -----------

    # -------------------------------- считываем БД ----------
    my_db = psycopg2.connect(
        # -------------
        database="jurnal_db",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432",
    )
    mycursor = my_db.cursor()
    # --------------------------------------------------------

    mycursor.execute(     f"insert into jurnal_tab (vps_j, fio_j, phone_number_j, date_time, status) values "
                                                f"('{vps_name}','{fio}','{phone_number}','{date_}', '{stat_tex}')");
    my_db.commit()

    # -----------запись изменения статуса в таблицу spisok_vps ------
    mycursor.execute(     f"UPDATE spisok_vps SET psw = '{stat_tex}' WHERE name_vps = '{vps_name}' and fio = '{fio}'");
    my_db.commit()
    my_db.close() #--------------- закрывашка БД ---------
    mycursor.close()


def insert_new_record_to_db(message, vps_name):
    # ----- добавление записи -----------
    fio = message.text
    if fio == '↪️В меню':
        controller.bot.send_message(message.chat.id, "Добавление записи в БД отменено.")
        view.start_menu(message)
    else:
        # -------------------------------- считываем БД ----------
        my_db = psycopg2.connect(
            # -------------
            database="jurnal_db",
            user="postgres",
            password="1234",
            host="localhost",
            port="5432",
        )
        mycursor = my_db.cursor()
        # --------------------------------------------------------

        mycursor.execute(     f"insert into spisok_vps (name_vps, fio, psw) values "
                                                    f"('{vps_name}','{fio}','СДАЛ')");
        my_db.commit()
        my_db.close() #--------------- закрывашка БД ---------
        mycursor.close()

        view.confirm_new_fio_recording_by_chat(message, fio, vps_name)
        view.start_menu(message)


# message, fio, vps_name, status
def admin_drop_contact(message, fio, vps_name):
    if message.text != None:
        view.start_menu(message)

    else:
        if message.contact is not None:  # Если присланный объект <strong>contact</strong> не равен нулю
            drop_data(vps_name, fio)
            view.confirm_drop_records_by_chat(message, fio, vps_name)
            view.start_menu(message)


def drop_data(vps_name, fio):
    # -------------------------------- считываем БД ----------
    my_db = psycopg2.connect(
        # -------------
        database="jurnal_db",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432",
    )
    mycursor = my_db.cursor()
    # --------------------------------------------------------

    mycursor.execute(f"DELETE FROM spisok_vps WHERE name_vps = '{vps_name}' AND fio = '{fio}'");
    my_db.commit()

    my_db.close()  # --------------- закрывашка БД ---------
    mycursor.close()