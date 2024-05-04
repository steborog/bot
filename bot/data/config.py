import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

DB_FILE = str(os.getenv("DB_FILE"))

USERS_TABLE_NAME = str(os.getenv("USERS_TABLE_NAME"))
USERS_SEARCH_RECORDS_TABLE_NAME = str(os.getenv("USERS_SEARCH_RECORDS_TABLE_NAME"))
PHONES_TABLE_NAME = str(os.getenv("PHONES_TABLE_NAME"))