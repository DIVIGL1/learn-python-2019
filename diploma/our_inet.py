# -*- coding: utf-8 -*-
import datetime
import io
import pandas as pd
import requests

import our_utils
import our_constants

API_URL = "https://mfd.ru/export/handler.ashx/DataFile.txt?"

API_PARAMS = {
    "TickerGroup": "16",
    "Tickers": "330",
    "Alias": "False",
    "Period": "7",
    "timeframeValue": "1,",
    "timeframeDatePart": "day",
    "StartDate": "01.06.2019",
    "EndDate": "09.06.2019",
    "SaveFormat": "0",
    "SaveMode": "0", 
    "FileName": "FileWithData.txt",
    "FieldSeparator": ";",
    "DecimalSeparator": ".",
    "DateFormat": "yyyyMMdd",
    "TimeFormat": "HHmmss",
    "DateFormatCustom": "",
    "TimeFormatCustom": "",
    "AddHeader": "true",
    "RecordFormat": "0",
    "Fill": "false"
}

class Inet_connector():
    def get_stocks_prices_2df(self, mfd_id, id_period_type=our_constants.PERIOD_TYPES["День"], date_begin="", date_end=""):
        id_period_type = our_constants.PERIOD_TYPES["День"] # Принудительно выставим период в тип = День
        if not date_begin:
            date_begin = datetime.datetime.strptime('2000/01/01', "%Y/%m/%d")
        elif type(date_begin)==str:
            date_begin = datetime.datetime.strptime(date_begin, "%Y/%m/%d")

        if not date_end:
            date_end = datetime.datetime.now()
        elif type(date_end)==str:
            date_end = datetime.datetime.strptime(date_end, "%Y/%m/%d")
        
        API_PARAMS["Tickers"] = str(mfd_id)
        API_PARAMS["StartDate"] = datetime.datetime.strftime(date_begin,"%d.%m.%Y")
        API_PARAMS["EndDate"] = datetime.datetime.strftime(date_end,"%d.%m.%Y")
        API_PARAMS["Period"] = str(id_period_type)

        file_in_memory = io.StringIO(requests.get(API_URL,params=API_PARAMS).text)
        df = pd.read_csv(file_in_memory, sep=";")

        df = our_utils.prepare_df(df)
        return(df)

