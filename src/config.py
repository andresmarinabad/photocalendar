import dotenv
import os
from datetime import datetime

dotenv.load_dotenv()


class Config:

    def __init__(self):
        self.DB_PATH = os.getenv("DB_PATH")
        self.CSV_FOLDER = os.getenv("CSV_FOLDER")
        self.TABLE_NAME = os.getenv("CSV_FOLDER")
        self.YEAR = os.getenv("YEAR", datetime.now().year+1)


config = Config()