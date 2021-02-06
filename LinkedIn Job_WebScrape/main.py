import pandas as pd
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from time import time

start_time = time()

position = input("Position: ")
location = input("Location: ")

url = f'https://www.linkedin.com/jobs/search/?f_TPR=r604800&keywords={position}&location={location}&sortBy=DD'
no_of_jobs = 25

driver = webdriver.Chrome('chromedriver.exe')
driver.get(url)
sleep(3)
action = ActionChains(driver)

i = 2
while i <= (no_of_jobs / 25):
    driver.find_element_by_xpath('/html/body/main/div/section/button').click()
    i = i + 1
    sleep(5)

pageSource = driver.page_source
lxml_soup = BeautifulSoup(pageSource, 'lxml')

# searching for all job containers
job_container = lxml_soup.find('ul', class_='jobs-search__results-list')

# setting up list for job information
job_id = []
position = []
company_name = []
post_date = []
job_location = []
job_desc = []

# for loop for job title, company, id, location and date posted
for job in job_container:
    # job title
    job_titles = job.find("span").text
    position.append(job_titles)

    # linkedin job id
    job_ids = job.find('a')['href']
    job_ids = re.findall(r'(?!-)([0-9]*)(?=\?)', job_ids)[0]
    job_id.append(job_ids)

    # company name
    company_names = job.select_one('img')['alt']
    company_name.append(company_names)

    # job location
    job_locations = job.find("span").text
    job_location.append(job_locations)

    # Job posting date
    Job_post_date = job.select_one('time')['datetime']
    post_date.append(Job_post_date)

# for loop for job description and criterias
for i in range(1, len(job_id) + 1):
    # clicking on different job containers to view information about the job
    job_xpath = '/html/body/main/div/section/ul/li[{}]/img'.format(i)
    driver.find_element_by_xpath(job_xpath).click()
    sleep(3)

    # job description
    jobdesc_xpath = '/html/body/main/section/div[2]/section[2]/div'
    job_descs = driver.find_element_by_xpath(jobdesc_xpath).text
    job_desc.append(job_descs)

    # job criteria container below the description
    job_criteria_container = lxml_soup.find('ul', class_='job-criteria__list')
    all_job_criterias = job_criteria_container.find_all("span",
                                                        class_='job-criteria__text job-criteria__text--criteria')

    i = i + 1

# creating a dataframe
job_data = pd.DataFrame({'Job ID': job_id,
                         'Position': position,
                         'Company Name': company_name,
                         'Date': post_date,
                         'Location': job_location,
                         'Description': job_desc,
                         })

# cleaning description column
job_data['Description'] = job_data['Description'].str.replace('\n', ' ')

# print(job_data.info())
job_data.head()
job_data.to_csv('Your job Posting LinkedIn.csv')

print("Done scraping")
