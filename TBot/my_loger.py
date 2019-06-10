import logging

def my_loger(log_text):
    print(log_text)
    logging.info(log_text)

def config_loggin():
    logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO,
                        filename='bot.log'
                        )
