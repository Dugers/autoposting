from os import getenv
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = getenv('BOT_TOKEN')
VK_TOKEN = getenv('VK_TOKEN')
ADMINS_IDS = list(map(int, getenv('ADMINS_IDS').split(",")))

DB_HOST = getenv('DB_HOST')
DB_PORT = getenv('DB_PORT')
DB_USER = getenv('DB_USER')
DB_PASSWORD = getenv('DB_PASSWORD')
DB_DATABASE = getenv('DB_DATABASE')

HEROKU_APP_NAME = getenv('HEROKU_APP_NAME')

WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{BOT_TOKEN}'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = int(getenv('PORT'))