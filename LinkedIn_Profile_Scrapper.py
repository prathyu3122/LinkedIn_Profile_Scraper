from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys 
import time
import pandas as pd


driver = webdriver.Chrome()
driver.get('https://www.linkedin.com')
username = driver.find_element_by_id('session_key')

# Enter your username 
username.send_keys("prathyusharejeti@gmail.com")

password = driver.find_element_by_id('session_password')

# Enter your Password
password.send_keys("Upendra@2006")

log_in_button = driver.find_element_by_class_name('sign-in-form__submit-button')

log_in_button.click()

# Enter the search word that is to be searched

text_to_be_searched = input('Enter the Field : ')
 
profile_link=set()
search_area=driver.find_elements_by_xpath('//*[@class="search-global-typeahead__input always-show-placeholder"]')
        
      
search_area[0].send_keys(text_to_be_searched)
search_area[0].send_keys(Keys.RETURN)



for i in range(1,2):
    if i==1:
        link='https://www.linkedin.com/search/results/people/?keywords={}&origin=CLUSTER_EXPANSION'.format(text_to_be_searched)
        driver.get(link)
    else:
        link='https://www.linkedin.com/search/results/people/?keywords={}&origin=CLUSTER_EXPANSION&page={}'.format(text_to_be_searched,i)
        driver.get(link)
    elems = driver.find_elements_by_xpath("//a[@href]")
    for elem in elems:  
        profile_name=elem.get_attribute("href")
        if 'miniProfileUrn' in profile_name:
            profile_link.add(profile_name)

            
total_information = [['Name','Working at','Location','Bio','LinkedIn Profile','Job Title','Company','Working Date','Years of Experience', 'College Name','Degree','Field of study','Graduation year']]


for Profile_link in profile_link:
    driver.get(Profile_link)

    source = driver.page_source

    soup = BeautifulSoup(source, 'lxml')

    name_tag = soup.find('div', {'class' : 'pv-text-details__left-panel mr5'})

    info = []

    name = name_tag.find('h1',{'class' : 'text-heading-xlarge inline t-24 v-align-middle break-words'}).get_text().strip()
    print(name)

    working_at = name_tag.find('div',{'class' : 'text-body-medium break-words'}).get_text().strip()
    print(working_at)

    location = soup.find('span',{'class' : 'text-body-small inline t-black--light break-words'}).get_text().strip()
    print(location)

    try:
        bio = soup.find('div', {'class' : 'inline-show-more-text inline-show-more-text--is-collapsed mt4 t-14'}).get_text().strip()
        print(bio)
    except:
        bio = "No bio exists"

    # EXPERIENCE SECTION

    try:
        exp_sec = soup.find('section', {'id' : 'experience-section'})
        exp_sec = exp_sec.find('ul')
        li_tags = exp_sec.find('div')
        a_tags = li_tags.find('a')

        job_position = a_tags.find('h3').get_text().strip()
        print(job_position)

        company = a_tags.find_all('p')[1].get_text().strip()
        print(company)

        working_date = a_tags.find_all('h4')[0].find_all('span')[1].get_text().strip()
        print(working_date)

        experience = a_tags.find_all('h4')[1].find_all('span')[1].get_text().strip()
        print(experience)
    except:
        job_position = "Job position is not updated"
        company = "Working Company is not updated"
        working_date = "Working date is not updated"
        experience = "Experience is not updated"


    # EDUCATION SECTION

    try:
        edu_sec = soup.find('section',{'id':'education-section'}).find('ul')

        college_name = edu_sec.find('h3').get_text().strip()
        print(college_name)

        degree = edu_sec.find('p',{'class' : 'pv-entity__secondary-title pv-entity__degree-name t-14 t-black t-normal'}).find_all('span')[1].get_text().strip()
        print(degree)

        study_field = edu_sec.find('p',{'class' : 'pv-entity__secondary-title pv-entity__fos t-14 t-black t-normal'}).find_all('span')[1].get_text().strip()
        print(study_field)

        grad_year = edu_sec.find('p', {'class' : 'pv-entity__dates t-14 t-black--light t-normal'}).find_all('span')[1].get_text().strip()
        print(grad_year)
    except:
        college_name = "College name not updated"
        degree = "Degree is not updated"
        study_field = "Field of study is not updated"
        grad_year = "Graduation year is not updated"

    # Appending into a list

    info.append(name)
    info.append(working_at)
    info.append(location)
    info.append(bio)
    info.append(link)

    info.append(job_position)
    info.append(company)
    info.append(working_date)
    info.append(experience)

    info.append(college_name)
    info.append(degree)
    info.append(study_field)
    info.append(grad_year)
    # print(info)

    total_information.append(info)

    df=pd.DataFrame(total_information)
    df.to_csv('profile_data.csv',index=False,header=False)
    print(total_information)