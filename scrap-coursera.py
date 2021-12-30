
# # SCRAP COURSERA

# %%
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import traceback

#subjects
#subjects = ['Business', 'Computer Science', 'Data Science','Health', 'Social Sciences','Physical Science and Engineering','Information Technology', 'Arts and Humanities', 'Language Learning', 'Personal Development', 'Math and Logic']
subjects = ['Business' ,'Physical Science and Engineering']

#course tab on edx.org
base_website = 'https://www.coursera.org/search'

#query string as per subject
# eg for Business, https://www.coursera.org/search?index=prod_all_launched_products_term_optimization&entityTypeDescription=Courses&topic=Business
website = 'https://www.coursera.org/search?index=prod_all_launched_products_term_optimization&entityTypeDescription=Courses&topic={courseName}'

# maximum number of courses to parse per subject
MAX_COURSES_PER_SUBJECT = 12


# return url for the passed on subject
def subjectUrl(subName):
    subName = subName.replace(" ","%20").replace("&","%26")
    return website.format(courseName=subName)


## NOTE: Configure WebDriver and append webdriver's location into PATH system variable

# driver = webdriver.Chrome()
driver = webdriver.Edge()




lsubject = []
ltitle = []
ldesc = []
loutcome = []
lskills = []
lhours = []
linstit = []
llevel = []
llang = []
lurl = []
limgurl =  []




# return False if element is absent and else text within 
def isPresent(by, xpth, returnList = False):
    lst = driver.find_elements( by ,xpth)
    if ( len(lst) > 0):
        if(returnList):
            return list(map(lambda x: x.get_attribute('textContent'), lst))
        else:
            return lst[0].get_attribute('textContent')
    else:
        return False 

try:
    for subject in subjects:

        #load the subject page
        driver.get(subjectUrl(subject))
        time.sleep(3)

        #Counter cnt
        cnt = 0

        #list course links
        course_list = []

        #list of img urls mapped with above courses
        course_img_list = []

        #do ... while cnt <= MAX_COURSES_PER_SUBJECT and next is enabled
        while(cnt <= MAX_COURSES_PER_SUBJECT):

            iter_list = driver.find_elements(By.XPATH, "/html//main[@id='main']/div[@class='ais-InstantSearch__root']/div/div[@class='rc-SearchTabs']/div[@class='ais-MultiIndex__root']//ul[@class='ais-InfiniteHits-list']//a")

            iter_img_list = driver.find_elements(By.XPATH, "/html//img[@class='product-photo']")

            if ( MAX_COURSES_PER_SUBJECT > cnt + len(iter_list) ):
                #Filter out the urls from elements 
                course_list += list(map(lambda x: str(x.get_attribute('href')), iter_list))
                course_img_list += list(map(lambda x: str(x.get_attribute('src')), iter_img_list))
                cnt += len(iter_list)

            else:
                #Filter out the urls from elements 
                course_list += list(map(lambda x: str(x.get_attribute('href')), iter_list[:(MAX_COURSES_PER_SUBJECT-cnt)]))
                course_img_list += list(map(lambda x: str(x.get_attribute('src')), iter_img_list[:(MAX_COURSES_PER_SUBJECT-cnt)]))
                cnt += MAX_COURSES_PER_SUBJECT-cnt
            
            # NEXT button on course result page
            NEXT_BTN = driver.find_element(By.XPATH,"/html//main[@id='main']/div[@class='ais-InstantSearch__root']//div[@class='rc-SearchTabs']//div[@class='ais-InfiniteHits']/div[1]/div[@role='navigation']/button[7]")
            
            # if cnt<MAX_COURSES_PER_SUBJECT and NEXT_BTN is enabled
            if(cnt<MAX_COURSES_PER_SUBJECT and NEXT_BTN.is_enabled()):
                NEXT_BTN.click()
                time.sleep(2)
            else:
                break

        # Subject and count
        print("\nSubject: ", subject)
        print("Count: ",cnt)
        #print(course_list)
        #print(course_img_list)

        
        for course_count in range(cnt):

            driver.get(course_list[course_count])

            #tit = driver.find_element_by_xpath("/html//main[@id='main-content']/div[@class='course-about course-info-content']/div[@class='header']//h1").text
            tit = isPresent(By.XPATH, "/html//main[@id='main']/div//div[@id='main']/div[2]/h1[@class='banner-title banner-title-without--subtitle m-b-0']")
            
            des = isPresent(By.XPATH, "/html//div[@class='m-t-1 description']")

            out = isPresent(By.XPATH, "/html//main[@id='main']/div/div[2]//div[@class='m-y-2']/div[@class='CmlLearningObjectives border-a p-x-2 p-t-1']/ul/*", True)

            ski = isPresent(By.XPATH, "/html//main[@id='main']/div/div[2]//div[@class='Skills m-y-2 p-x-2 p-t-1 p-b-2 border-a css-1rj0z6b']/ul[@role='list']/*", True)

            tim = isPresent(By.XPATH, "/html//main[@id='main']/div/div[2]/div[@class='_1d3lkver p-b-2']//div[@class='ProductGlance']/div[last()-1]//span")
            
            ins = isPresent(By.XPATH, "/html//main[@id='main']/div/div[4]/div[@class='_1d3lkver']//div[@class='_wtdnuob']/a/h3")

            lvl = isPresent(By.XPATH, "/html//main[@id='main']/div/div[2]/div[@class='_1d3lkver p-b-2']//div[@class='ProductGlance']/div[last()-2]/div[2]")

            lan = isPresent(By.XPATH, "/html//main[@id='main']/div/div[2]/div[@class='_1d3lkver p-b-2']//div[@class='ProductGlance']/div[last()]/div[2]/*", True)

            img = course_img_list[course_count]

            #out, ski, lan are list
            #print(tit, des, out, ski, tim, ins, lvl, lan, img, sep='\n')
            
            
            # clean and append or omit if absent 
            tim = tim.replace('Approx. ','').replace(' hours to complete','')
            lvl = lvl.replace(' level', '')

            #separate medium language and subtitles by "-"
            lan = lan[0] + lan[1].replace('Subtitles: ', '-')

            if( out ):
                out = ". ".join(out)
            else:
                out = "NA"

            if( ski ):
                ski = ". ".join(ski)
            else:
                ski = "NA"
            
            #print(tit, des, out, ski, tim, ins, lvl, lan, img, sep='\n')
            # append values into list
            lsubject.append(subject)
            ltitle.append(tit)
            ldesc.append(des)
            loutcome.append(out)
            lskills.append(ski)
            lhours.append(tim)
            linstit.append(ins)
            llevel.append(lvl)
            llang.append(lan)
            lurl.append(course_list[course_count])
            limgurl.append(img)
            
except Exception:
    print('ERROR: Process interupted due to an error at url', driver.current_url)
    print(traceback.format_exc())
    


#closing the browser
driver.close()


df = pd.DataFrame({'subject': lsubject, 'title': ltitle, 'description': ldesc, 'outcomes': loutcome, 'skills': lskills, 'hours': lhours, 'institute': linstit, 'level':llevel, 'Languages': llang, 'url': lurl, 'img_url': limgurl})
df.to_csv('cousera.csv')
df


