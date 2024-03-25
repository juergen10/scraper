import requests
import os
import json
from dotenv import load_dotenv
from models import job
from devjobs import Devjobs
import sys

load_dotenv()

URL_SCRAP = os.getenv('URL_SCRAP')
WP_BASE_URL = os.getenv("WP_BASE_URL")
TOKEN = os.getenv("TOKEN")
CATEGORY_ID = os.getenv("CATEGORY_ID")

if not URL_SCRAP:
    print('Error: Scrapping URL not specified in environment variables.')
    sys.exit(-1)

if not WP_BASE_URL:
    print('Error: WP BASE URL not specified in environment variables.')
    sys.exit(-1)
    
if not TOKEN:
    print('Error: Token not specified in environment variables.')
    sys.exit(-1)
    
if not CATEGORY_ID:
    print('Error: Category id not specified in environment variables.')
    sys.exit(-1)
    
WP_URL = WP_BASE_URL+"/wp-json/wp/v2/posts"

print('Scrapping start!')
scrap_jobs = Devjobs(URL_SCRAP)
obj = json.dumps(scrap_jobs.get_jobs(), indent=4)

with open("jobs.json", "w") as outfile:
    outfile.write(obj)
    
if os.path.exists("jobs.json"):
    job = job.Job()
    with open('jobs.json') as f:
        jobs = json.load(f)
        for value in jobs:
            is_slug_available = job.select_job(value['slug'])
            print(is_slug_available);
            if is_slug_available != None:
                continue
            
            insert_jobs = job.insert_job(title=value['title'], slug=value['slug'], start_date=value['start_date'], end_date=value['end_date'])
        
            data = {
                "content":str(value['content']),
                "title": value['title'],
                "status": "publish",
                "categories":[CATEGORY_ID],
                "comment_status": "closed"
            }

            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": "Bearer "+TOKEN
            }
            post = requests.post(WP_URL, data = data, headers = headers)    
            print(post.status_code)     
        print('Finish scrapping!')
else:
    print("jobs.json doesn't exists!")
os.remove("jobs.json")
