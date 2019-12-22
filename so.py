import requests
from bs4 import BeautifulSoup

URL = f'https://stackoverflow.com/jobs?q=python&sort=i'


def get_last_page():
  # last page is different with actual SO search results with word for 'python', don't know why.... T.T
  # but it's working..
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, 'html.parser')
    pages = soup.find('div', {'class': 's-pagination'}).find_all('a')
    last_page=pages[-2].get_text(strip=True)
    return int(last_page)


def extract_job(html):
    # fist version :
    # title = html.find('a', {'class': 'job-link'})['title']
    # now changed..
    title = html.find('h2', {'class': 'fs-body3'}).text
    # ok3
    # recursive 옵션은 바로 밑에 있는 children정보만 가져온다.
    company, location = html.find('h3',{'class' : 'fs-body1'}).find_all('span', recursive=False)

    # .string command also get text from the tag
    company = company.get_text(strip=True)
    location = location.get_text(strip=True).strip(',')
    # previous one...since it is made from mac? it should be strip by \r and \n element.
    # location = location.get_text(strip=True).strip('-').strip(' \r').strip('\n')

    job_id = html['data-jobid']
    return {
        'title': title,
        'company': company,
        'location': location,
        'apply_link': f'https://stackoverflow.com/jobs/{job_id}'
    }


def extract_jobs(last_page):
    jobs = []
    print(f'Scraping {last_page} pages of Job information from Stackoverflow')
    for page in range(last_page):
        print(f'Scrapping SO: page {page}')
        result = requests.get(f'{ URL }&pg={page + 1}')
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all('div', {'class': '-job'})
        for result in results:
          job = extract_job(result)
          jobs.append(job)
    return jobs


def get_jobs():
    last_page = get_last_page()
    # ok1
    jobs = extract_jobs(last_page)
    return jobs
