import os
from datetime import datetime
from pathlib import Path


class Config:
    def __init__(self):
        self.ROOT = str(Path(__file__).parent.parent)
        self.CALENDARS_PATH = os.path.join(self.ROOT, "data", "calendars")
        self.CSV_FOLDER = os.path.join(self.ROOT, "input")
        self.OUTPUT_PATH = os.path.join(self.ROOT, "output")
        self.DEFAULT_YEAR = int(os.getenv("YEAR", str(datetime.now().year + 1)))

        os.makedirs(self.CALENDARS_PATH, exist_ok=True)
        os.makedirs(self.OUTPUT_PATH, exist_ok=True)


config = Config()
