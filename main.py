import requests
import os
import json
from dotenv import load_dotenv
from models import job
from devjobs import Devjobs

load_dotenv()

URL_JOB = os.getenv('URL_JOB')
WP_URL = os.getenv("WP_URL") + "/wp-json/wp/v2/posts"

print('Scrapping start!')
scrap_jobs = Devjobs(URL_JOB)
obj = json.dumps(scrap_jobs.get_jobs(), indent=4)
queries = [];

with open("jobs.json", "w") as outfile:
    outfile.write(obj)
    
if os.path.exists("jobs.json"):
    job = job.Job()
    with open('jobs.json') as f:
        jobs = json.load(f)
        for value in jobs:
            is_slug_available = job.select_job(value['slug'])
            
            if is_slug_available != None:
                continue
            
            insert_jobs = job.insert_job(title=value['title'], slug=value['slug'], start_date=value['start_date'], end_date=value['end_date'])
        
            data = {
                "content":str(value['content']),
                "title": value['title'],
                "status": "publish",
                "categories":[21],
                "comment_status": "closed"
            }

            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEsIm5hbWUiOiJiaW5hIiwiaWF0IjoxNzEwNDEzODc5LCJleHAiOjE4NjgwOTM4Nzl9._c_c3RHB65M6tuUE-rq_AIcV-gos6C3KyoOGqg48KW8"
            }
            post = requests.post(WP_URL, data = data, headers = headers)            
    print('Finish scrapping!')
    os.remove("jobs.json")
