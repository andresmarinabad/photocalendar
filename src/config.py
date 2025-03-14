import os
from datetime import datetime


class Config:

    def __init__(self):
        self.ROOT = os.path.abspath(
            os.path.dirname(
                os.path.dirname(__file__)
            )
        )
        self.DB_PATH = os.path.join(self.ROOT, 'data', 'data.db')
        self.CSV_FOLDER = os.path.join(self.ROOT, 'input')
        self.YEAR = os.getenv("YEAR", datetime.now().year+1)


config = Config()