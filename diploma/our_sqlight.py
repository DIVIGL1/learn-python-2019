# -*- coding: utf-8 -*-
import datetime
import os
import pandas as pd
import sqlite3 as sqlite
import sys
from tqdm import tqdm

import our_constants
import our_inet
import our_utils

class Data_handler():
    def __init__(self):
        self.get_connector()
        self.create_tables()

        # Добавим данные в справочники.
        # В PERIOD_TYPES:
        initual_data = our_constants.initual_data_PERIOD_TYPES
        self.add_rows_from_struct(initual_data)

        # В STOCKS:
        initual_data = our_constants.initual_data_STOCKS
        self.add_rows_from_struct(initual_data)

    def __del__(self):
        self._connector.close()
        print("Закрыли соединение с БД.")

    def get_connector(self):
        try:
            self._connector = sqlite.connect(our_utils.get_dbase_path())
        except (sqlite.Error):
            print("get_connector: Возникла проблема с подключением к базе данных.")
            if self._connector: self._connector.close()
        if self._connector:
            print("Установили соединение с БД.")
            return(True)
        else:
            print("get_connector: При установлении связи с БД возникли ошибки.")
            return(False)
    
    def add_rows_from_struct(self, data):
        ret_code = True
        for one_row in data["data"]:
            ret_code = self.add_row(data["table_name"], one_row, find_and_update_or_insert=data["find_and_update_or_insert"], id_column=data["id_column"], donot_commit=data["donot_commit"])
            if not ret_code: break
        return(ret_code)
        

    def add_row(self, table_name, data, find_and_update_or_insert=False, id_column="", donot_commit=False):
        if not self._connector:
            print("add_row: У данного объекта отсутствует коннектор.")
            return(False)
        
        table_name = table_name.replace(" ","").upper()
        cur = self._connector.cursor()
        if find_and_update_or_insert:
            # Ветка "НайдиИОбнови".
            # Предварительно нужно проверить, если такая запись уже есть, то её нужно не добавить а обновить.
            if id_column=="":
                print("add_row: Необходимо проверить наличие в таблице {} строки с идентификатором, а имя идентификатора не передано.".format(table_name))
                return(False)
            else:
                cur.execute("SELECT COUNT(*) FROM {} WHERE {}=?".format(table_name,id_column), ( data[id_column], ) )
                if cur.fetchone()[0]==1:
                    try:
                        cur = self._connector.cursor()
                        if table_name=="STOCKS":
                            cur.execute("UPDATE {} SET full_name=?, short_name=?, order_field=?, phidden=? WHERE {}=?".format(table_name,id_column), \
                                ( data["full_name"], data["short_name"], data["order_field"], data["phidden"], data["trade_kod"] ) )
                        elif table_name=="PERIOD_TYPES":
                            cur.execute("UPDATE {} SET period_name=?, phidden=? WHERE {}=?".format(table_name,id_column), \
                                ( data["period_name"], data["phidden"], data["id"] ) )
                        elif table_name=="STOCKS_PRICES":
                            print("add_row: Попытка обновить данные в таблице: " + table_name + ". Эта операция не предусмотрена структурой данных.")
                            return(False)
                        else:
                            print("add_row: Попытка обновить данные в несуществующей таблице: " + table_name)
                            return(False)
                    except:
                        print("add_row: При обновлении существующей строки в таблице {} возникла ошибка.".format(table_name))
                        self._connector.rollback()
                        return(False)
                    if not donot_commit: self._connector.commit()
                    # Так как это была ветка "НайдиИОбнови" и ошибок не произошло, то на этом завершаем работу и выходим с True.
                    return(True)

        # Ветка "ДобавьНовыеДанные"
        try:
            if table_name=="STOCKS":
                cur.execute("INSERT INTO STOCKS (trade_kod, mfd_id, full_name, short_name, order_field, phidden) VALUES(?, ?, ?, ?, ?, ?)", \
                    ( data["trade_kod"], data["mfd_id"], data["full_name"], data["short_name"], data["order_field"], data["phidden"] ) )
            elif table_name=="PERIOD_TYPES":
                cur.execute("INSERT INTO PERIOD_TYPES (id, period_name, phidden) VALUES(?, ?, ?)", \
                    ( data["id"], data["period_name"], data["phidden"] ) )
            elif table_name=="STOCKS_PRICES":
                cur.execute("INSERT INTO STOCKS_PRICES (mfd_id, price_dt, id_period_type, price_open, price_min, price_max, price_close, vol) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", \
                    ( data["mfd_id"], data["price_dt"], data["id_period_type"], data["price_open"], data["price_min"], data["price_max"], data["price_close"], data["vol"] ) )
            else:
                print("add_row: Попытка добавить данные в несуществующую таблицу: " + table_name)
                return(False)
        except:
            print("add_row: При добавлении строки в таблицу {} возникла ошибка.".format(table_name))
            self._connector.rollback()
            return(False)
        
        if not donot_commit: self._connector.commit()
        # Так как ошибок не было, то выходим с True
        return(True)

    def create_tables(self):
        if not self._connector:
            return(False)
        
        cur = self._connector.cursor()
        try:
            cur.execute("CREATE TABLE IF NOT EXISTS STOCKS (trade_kod TEXT NOT NULL PRIMARY KEY, mfd_id INTEGER NOT NULL, full_name TEXT NOT NULL, short_name TEXT NOT NULL, order_field INTEGER NOT NULL, phidden INTEGER NOT NULL)")
        except:
            print("create_tables: При создании таблицы STOCKS возникла ошибка.")
            return(False)
        try:
            cur.execute("CREATE TABLE IF NOT EXISTS PERIOD_TYPES (id INTEGER PRIMARY KEY, period_name TEXT, phidden INTEGER)")
        except:
            print("create_tables: При создании таблицы PERIOD_TYPES возникла ошибка.")
            return(False)
        try:
            cur.execute("CREATE TABLE IF NOT EXISTS STOCKS_PRICES (mfd_id INTEGER NOT NULL, price_dt TIMESTAMP NOT NULL, id_period_type INTEGER NOT NULL, price_open REAL NOT NULL, price_min REAL NOT NULL, price_max REAL NOT NULL, price_close REAL NOT NULL, vol INTEGER NOT NULL)")
            cur.execute("CREATE TRIGGER IF NOT EXISTS trig_STOCKS_PRICES_befor_insert BEFORE INSERT ON STOCKS_PRICES FOR EACH ROW BEGIN DELETE FROM STOCKS_PRICES WHERE mfd_id=NEW.mfd_id AND price_dt=NEW.price_dt AND id_period_type=NEW.id_period_type; END")
            cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS unique_combination ON STOCKS_PRICES (mfd_id, price_dt, id_period_type)")
        except:
            print("create_tables: При создании таблицы STOCKS_PRICES возникла ошибка.")
            return(False)
        # Так как ошибок не было, то выходим с True
        return(True)
    
    def get_stocks_list(self):
        if not self._connector:
            return(False)
        
        cur = self._connector.cursor()
        try:
            cur.execute("SELECT * FROM STOCKS WHERE phidden==0 ORDER BY order_field")
            return(cur.fetchall())
        except:
            print("get_stocks_list: При попытке получить выборку из таблицы STOCKS_PRICES возникла ошибка.")
            return(False)
        # Так как ошибок не было, то выходим с True
        return(True)

    def get_period_types_list(self):
        if not self._connector:
            return(False)
        
        cur = self._connector.cursor()
        try:
            cur.execute("SELECT * FROM PERIOD_TYPES WHERE phidden==0 ORDER BY id")
            return(cur.fetchall())
        except:
            print("get_stocks_list: При попытке получить выборку из таблицы STOCKS_PRICES возникла ошибка.")
            return(False)
        # Так как ошибок не было, то выходим с True
        return(True)

    def load_stock_prises_from_file2df(self, file_name):
        if not os.path.isfile(file_name):
            print("load_stock_prises_from_file: Файл '{}' не найден.".format(file_name))
            return(False)
        
        print("Получаем данные о стоимости акций из текстового файла '{}'".format(file_name))
        df = pd.read_csv(file_name, sep=";")
        # Полученную таблицу нужно причесать:
        return(our_utils.prepare_df(df))

    def load_stock_prises_from_df2db(self, mfd_id, id_period_type, df):
        try:
            rows_ko_bo = df.shape[0]
        except:
            print("load_stock_prises_from_df2db: Проблема с исходными данными.")
            return(False)
        print("Загрузка цен на акции в DBase. Количество строк для загрузки: {}".format(rows_ko_bo))
        if rows_ko_bo==0:
            return(0)
        else:
            p_all_transactions_good = True
            for _, row in tqdm(df.iterrows(), total=df.shape[0]):
                # Добавим строчки по одной в STOCKS_PRICES:
                initual_data = {"table_name": "STOCKS_PRICES", "find_and_update_or_insert": False, "id_column": "", "donot_commit": True,
                                "data":
                                [ { 
                                    "mfd_id": mfd_id, 
                                    "id_period_type": id_period_type, 
                                    "price_dt": row[0].to_pydatetime(), 
                                    "price_open": row[1], 
                                    "price_min": row[2], 
                                    "price_max": row[3], 
                                    "price_close": row[4], 
                                    "vol": row[5]
                                } 
                                ]
                            }
                if not self.add_rows_from_struct(initual_data):
                    p_all_transactions_good = False
                    break
        
            if p_all_transactions_good: self._connector.commit()
            else: self._connector.rollback()
            return(p_all_transactions_good)

    def load_stock_prises_from_file2db(self, file_name, mfd_id, id_period_type):
        return(
                self.load_stock_prises_from_df2db( 
                    mfd_id, id_period_type, self.load_stock_prises_from_file2df(file_name)
                                                 )
              )

    def get_stocks_prices_pd(self, mfd_id, id_period_type=our_constants.PERIOD_TYPES["День"], price_type="MAX", dt_begin="", dt_end=""):
        if not self._connector:
            return(False)
        if not dt_end:
            dt_end = datetime.datetime.now()
        elif type(dt_end)==str:
            dt_end = datetime.datetime.strptime(dt_end, "%Y/%m/%d" if len(dt_end)==10 else "%Y/%m/%d %H:%M:%S")
        if not dt_begin:
            dt_begin = datetime.datetime.strptime('2000/01/01 9:00:00', "%Y/%m/%d %H:%M:%S")
        elif type(dt_begin)==str:
            dt_begin = datetime.datetime.strptime(dt_begin, "%Y/%m/%d" if len(dt_begin)==10 else "%Y/%m/%d %H:%M:%S")
        
        cur = self._connector.cursor()
        try:
            cur.execute("SELECT price_dt, price_{} AS price, vol FROM STOCKS_PRICES WHERE id_period_type=? AND price_dt BETWEEN ? AND ? ORDER BY price_dt".format(price_type.lower()),(id_period_type, dt_begin, dt_end))
            return(pd.DataFrame(cur.fetchall(),columns=["price_dt","price","vol"]))
        except:
            print("get_stocks_list: При попытке получить выборку из таблицы STOCKS_PRICES возникла ошибка.")
            return(False)

    def get_stocks_prices_min_max_dates(self, mfd_id, id_period_type=our_constants.PERIOD_TYPES["День"], dt_begin="", dt_end=""):
        if not self._connector:
            return(False)
        if not dt_end:
            dt_end = datetime.datetime.now()
        elif type(dt_end)==str:
            dt_end = datetime.datetime.strptime(dt_end, "%Y/%m/%d" if len(dt_end)==10 else "%Y/%m/%d %H:%M:%S")
        if not dt_begin:
            dt_begin = datetime.datetime.strptime('2000/01/01 9:00:00', "%Y/%m/%d %H:%M:%S")
        elif type(dt_begin)==str:
            dt_begin = datetime.datetime.strptime(dt_begin, "%Y/%m/%d" if len(dt_begin)==10 else "%Y/%m/%d %H:%M:%S")
        
        cur = self._connector.cursor()
        try:
            cur.execute("SELECT MIN(price_dt), MAX(price_dt) FROM STOCKS_PRICES WHERE id_period_type=? AND price_dt BETWEEN ? AND ? ORDER BY price_dt",(id_period_type, dt_begin, dt_end))
            return(cur.fetchall())
        except:
            print("get_stocks_list: При попытке получить максммальную и минимальную даты из таблицы STOCKS_PRICES возникла ошибка.")
            return(False)
    
    def load_stock_prises_from_inet(self, mfd_id, id_period_type=our_constants.PERIOD_TYPES["День"], price_type="MAX", date_begin="", date_end=""):
        if not self._connector:
            return(False)

        if not date_end:
            date_end = datetime.datetime.now().date()
        elif type(date_end)==str:
            date_end = datetime.datetime.strptime(date_end, "%Y/%m/%d").date()

        if not date_begin:
            date_begin = datetime.datetime.strptime('2000/01/01', "%Y/%m/%d").date()
        elif type(date_begin)==str:
            date_begin = datetime.datetime.strptime(date_begin, "%Y/%m/%d").date()

        # так как нам нужно найти последнюю дату в БД,
        # а там хратися DateTime, а у нас в переменной Date
        # то преобразуем дату в соотвествии с примером:
        # 20/01/2019 --> 20/01/2019 23:59:59
        dt_end = datetime.datetime(date_end.year, date_end.month, date_end.day) + datetime.timedelta(days=1) - datetime.timedelta(seconds=1)
        # При этом dt_begin будет типа 01/01/2019 00:00:00
        dt_begin = datetime.datetime(date_begin.year, date_begin.month, date_begin.day)

        ret_value = \
                self.get_stocks_prices_min_max_dates( 
                                    mfd_id=mfd_id, 
                                    id_period_type=id_period_type, 
                                    dt_begin=dt_begin, 
                                    dt_end=dt_end
                                                    )
        if ret_value==[(None, None)]:
            # В БД нет данных для данной акции и для данного типа периода.
            date_max = date_begin - datetime.timedelta(days=1)
            date_min = date_max
        else:
            date_min = datetime.datetime.strptime(ret_value[0][0], "%Y-%m-%d %H:%M:%S").date()
            date_max = datetime.datetime.strptime(ret_value[0][1], "%Y-%m-%d %H:%M:%S").date()

        inet_connector = our_inet.Inet_connector()
        if date_begin<date_min:
            df = inet_connector.get_stocks_prices_2df( 
                                                        mfd_id=mfd_id, 
                                                        id_period_type=id_period_type, 
                                                        date_begin=date_begin, 
                                                        date_end=date_min-datetime.timedelta(days=1)
                                                     )
            if not df.shape[0]==0:
                print("Подгружаем данные за период с {} по {}.".format(date_begin, date_min-datetime.timedelta(days=1)))
                self.load_stock_prises_from_df2db(mfd_id=mfd_id, id_period_type=id_period_type, df=df)

        if date_max<date_end:
            df = inet_connector.get_stocks_prices_2df( 
                                                        mfd_id=mfd_id, 
                                                        id_period_type=id_period_type, 
                                                        date_begin=date_max+datetime.timedelta(days=1), 
                                                        date_end=date_end
                                                     )
            if not df.shape[0]==0:
                print("Подгружаем данные за период с {} по {}.".format(date_max+datetime.timedelta(days=1), date_end))
                self.load_stock_prises_from_df2db(mfd_id=mfd_id, id_period_type=id_period_type, df=df)





