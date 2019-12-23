import requests
from bs4 import BeautifulSoup

URL = f"https://stackoverflow.com/jobs?q=python&sort=i"

def get_last_pages():
   result = requests.get(URL)
   # Float soup
   soup = BeautifulSoup(result.text, "html.parser")  
   pages = soup.find("div",{"class":"s-pagination"}).find_all("a")
   last_page = pages[-2].get_text(strip=True)
   return int(last_page)

def extract_job(html):
   title = html.find("div", {"class","grid--cell fl1 mr12"}).find("h2")
   # TODO:Sometimes you don't have h2 so you should check it.
   if title is not None:
     title = title.get_text()
   else:
     title = None

   compact = html.find("h3", {"class","fc-black-700 fs-body1 mb4"})
   # TODO:Sometimes you don't have h3 so you should check it.
   if compact is not None:
     company = compact.find("span").get_text(strip=True)
     location = compact.find("span", {"class","fc-black-500"}).get_text(strip=True)
     job_id = html['data-jobid']
   else :
     compact = None

   return {
     "title": title,
     "company": company,
     "location": location,
     "link": f"https://stackoverflow.com/jobs/{job_id}/"
   }


def extract_jobs(last_page):
  jobs = []
  for page in range(last_page):
     print(f"Scrapping SO: Page {page}")
     result = requests.get(f"{URL}&pg={page + 1}")
     soup = BeautifulSoup(result.text, "html.parser")
     results = soup.find_all("div",{"class":"-job"})
     for result in results:
        job = extract_job(result)
        jobs.append(job)
  
  return jobs
     
      
def get_jobs():
   last_page = get_last_pages()
   jobs = extract_jobs(last_page)
   return jobs