from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str('BOT_TOKEN')
ADMINS = env.list('ADMINS')
IP = env.str('IP')
URL = env.str('URL')
REDIS = env.bool('REDIS')
REDIS_URL = env.str('REDIS_URL')