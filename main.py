import requests
import json
from bs4 import BeautifulSoup

URL = "https://devjobsindo.org/ngo-jobs/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
job_elements = soup.find_all("div", class_="row is-flex")
child_job_elements = job_elements[0].contents
keys = len(child_job_elements)
jobs = {}

for i in range(keys):
    url = child_job_elements[i].find("a", class_="job-details-link")['href']
    jobs[i] = {
        "title": child_job_elements[i].find("a", class_="job-details-link")['href'],
        "url": url,
        "slug": url.strip().split("/")[-2],
        "end_date": child_job_elements[i].find("span", class_="job-date__closing").text.strip().lstrip("- ")
    }


print(json.dumps(jobs))