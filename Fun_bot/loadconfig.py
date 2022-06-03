try:
    from config.config import __telegramtoken__, __tg_group_id__, __my_id__, __discordtoken__, __prefix__, __discord_channels__, __botserverid__, __greetmsg__, __selfassignrole__, __cookieJar__, __discourseAPIKey__
except ImportError:
    #Heorku stuff
    import os
    __discordtoken__ = os.environ.get('DISCORD_TOKEN')
    __prefix__ = os.environ.get('DISCORD_PREFIX')

    __botserverid__ = int(os.environ.get('DISCORD_BOTSERVERID'))
    __discord_channels__ = int(os.environ.get('DISCORD_KAWAIICHANNEL'))
    __greetmsg__ = 778710639899181067
    __selfassignrole__ = os.environ.get('DISCORD_SELFASSIGNROLE')

    __cookieJar__ = os.environ.get('DISCORD_COOKIEJAR')
    __discourseAPIKey__ = os.environ.get('DISCORD_DISCOURSEAPIKEY')

    __telegramtoken__ = os.environ.get('TELEGRAM_TOKEN')
    __tg_group_id__ = os.environ.get('TG_GROUP_ID')
    __my_id__ = os.environ.get('AUTHOR_TG_ID') #@Shorox