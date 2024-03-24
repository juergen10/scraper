import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil import parser

class Devjobs:
    def __init__(self, url) -> None:
        self.url = url
        
    def __set_parse_html(url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        
        return soup
    
    def __set_html(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "html.parser")
        return soup
    
    def __get_total_page(self):
        content_html = self.__set_html()
        pagination = content_html.find_all("div", class_="pagination list-center")[1]
        last_page = pagination.find_all('a', class_="page-numbers")[1].text
        
        return int(last_page)

    def get_jobs(self):
        jobs = []
        counter = 1;
        total_page = self.__get_total_page()
        
        while counter <= total_page:
            url = f'{self.url}/page/{counter}'
            page = requests.get(url)
            content_html = BeautifulSoup(page.content, "html.parser")
            
            job_elements = content_html.find_all("div", class_="row is-flex")
            child_job_elements = job_elements[0].contents
            keys = len(child_job_elements)
            
            for i in range(keys):
                job_url = child_job_elements[i].find("a", class_="job-details-link")['href']
                get_end_date = child_job_elements[i].find("span", class_="job-date__closing").text.strip().lstrip("- ")
                job_page = requests.get(job_url)
                soup = BeautifulSoup(job_page.content, "html.parser")
                job_description = soup.find("div", class_="job-desc")
                end_date = datetime.strptime(get_end_date, '%B %d, %Y').strftime('%Y-%m-%d %H:%M:%S')
                format_end_date = parser.parse(end_date)
                
                now = datetime.now()
                
                if now > format_end_date:
                    continue
                
                job = {
                    "title": child_job_elements[i].find("span", class_="noo-icon-tool noo-tool-email-job")["data-title"],
                    "url": job_url,
                    "slug": job_url.strip().split("/")[-2],
                    "content": str(job_description),
                    "start_date": child_job_elements[i].find("time", class_="entry-date")["datetime"],
                    "end_date": end_date
                }
                
                jobs.append(job);
            counter +=1
        return jobs
        
    
b = Devjobs('https://devjobsindo.org/ngo-jobs')
obj =json.dumps(b.get_jobs(), indent=4)
with open("jobs.json", "w") as outfile:
    outfile.write(obj)