import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://devjobsindo.org/ngo-jobs/"
page = requests.get(URL)
wp_url = "/wp-json/wp/v2/posts"


soup = BeautifulSoup(page.content, "html.parser")
job_elements = soup.find_all("div", class_="row is-flex")
child_job_elements = job_elements[0].contents
keys = len(child_job_elements)
jobs = {}

for i in range(keys):
    job_url = child_job_elements[i].find("a", class_="job-details-link")['href']
    end_date = child_job_elements[i].find("span", class_="job-date__closing").text.strip().lstrip("- ")
    job_page = requests.get(job_url)
    soup = BeautifulSoup(job_page.content, "html.parser")
    job_description = soup.find("div", class_="job-desc")
    
    jobs[i] = {
        "title": child_job_elements[i].find("span", class_="noo-icon-tool noo-tool-email-job")["data-title"],
        "url": job_url,
        "slug": job_url.strip().split("/")[-2],
        "content": job_description,
        "start_date": child_job_elements[i].find("time", class_="entry-date")["datetime"],
        "end_date": datetime.strptime(end_date, '%B %d, %Y').strftime('%Y-%m-%d %H:%M:%S')
    }
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEsIm5hbWUiOiJiaW5hIiwiaWF0IjoxNzEwNDEzODc5LCJleHAiOjE4NjgwOTM4Nzl9._c_c3RHB65M6tuUE-rq_AIcV-gos6C3KyoOGqg48KW8"
}

for key, value in jobs.items():
    data = {
           "content":str(value['content']),
           "title": value["title"],
           "status": "publish",
           "categories":[21],
           "comment_status": "closed"
    }
    post = requests.post(wp_url, data = data, headers = headers)
    print(post.text)
    # print(value["content"])

# print(jobs)
