from database import DB

class Job:
    def __init__(self) -> None:
        self.database = DB()
        self.connection = self.database.connect()
        
    def insert_job(self, )