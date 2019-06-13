import our_constants
import our_sqlight
import our_utils


dbase_connector = our_sqlight.Data_handler()

mfd_id = 330
id_period_type = our_constants.PERIOD_TYPES["День"]
date_begin = "2018/12/10"
date_end = "2019/01/31"

dbase_connector.load_stock_prises_from_inet(mfd_id=mfd_id, id_period_type=id_period_type, date_begin=date_begin, date_end=date_end)


