import requests
import json
from bs4 import BeautifulSoup

job_url = "https://devjobsindo.org/ngo-jobs/disability-inclusion-disaster-risk-management-di-drm-coordinator/"
job_page = requests.get(job_url)

soup = BeautifulSoup(job_page.content, "html.parser")

job_description = soup.find("div", class_="job-desc")
print(job_description)