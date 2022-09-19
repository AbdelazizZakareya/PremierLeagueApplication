import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

#Open browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
url='https://www.premierleague.com/clubs'
driver.get(url)

# Accept on Cookies
time.sleep(3) # Wait to load page
accept_cookies = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[1]/div[5]/button[1]')
accept_cookies.click()

clubs = driver.find_elements(By.XPATH,'//*[@id="mainContent"]/div[2]/div/div/div[3]/div/table/tbody/tr')

club_list = []

for club in clubs:
    attr = club.find_elements(By.TAG_NAME,'td')
    [clubName, clubStadium] = attr #Object Destruction
    clubProfile = clubName.find_element(By.TAG_NAME,'a').get_attribute("href")
    club_dict = {
		"Club": clubName.text,
		"Stadium": clubStadium.text,
        "Website": clubProfile
	}
    print(club_dict)
    club_list.append(club_dict)

#Up till now, we have the club profile in Website not the official website
#We need to fetch every club profile to get the official website
for club in club_list:
    driver.get(club["Website"])
    time.sleep(3)
    #try except to check if a club has no official website so that the crawling does not crash
    try:
        website1 = driver.find_element(By.CLASS_NAME,"website")
        website2 = website1.find_element(By.TAG_NAME,'a').get_attribute("href")
        print(website2)
        club["Website"] = website2
    except:
        print("No official website found for club " + club["Club"] + " We will use the club profile link instead " )
        
# Create a DataFrame and Export CSV
df = pd.DataFrame(club_list)
df.to_csv(r'Clubs.csv',index=False)
driver.close()


    