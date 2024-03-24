from db.db import DB

class Job:
    def __init__(self) -> None:
        self.database = DB()
        self.connection = self.database.connect()
        
    def insert_job(self, **kwargs):
        if self.connection:
            try:
                insert_job = "INSERT INTO jobs (title, slug, start_date, end_date) VALUES(?,?,?,?)"
                
                params = (kwargs['title'], kwargs['slug'], kwargs['start_date'], kwargs['end_date'])
                self.database.execute_insert_query(insert_job, params)
            except Exception as e:
                print("Error occurred:", e)
    
    def select_job(self, slug):
        if self.connection:
            query = f"select jobs.slug from jobs where slug='{slug}' limit 1"
            job = self.database.execute_query(query)
            
            if job:
                return job[0][0]
            
            return None
        
    def insert_transaction(self, queries):
        if self.connection:
            self.database.execute_transaction(queries)
            
            return True
            
            