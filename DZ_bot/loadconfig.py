try:
    from config.config import __telegramtoken__, __admin_id__, __db_config__, __bot_id__
except ImportError:
    #Heorku stuff
    import os

    __telegramtoken__ = os.environ.get('TELEGRAM_TOKEN')
    __admin_id__ = os.environ.get('ADMIN_ID') #@Shorox
    __db_config__ = os.environ.get('DATABASE_CFG')




