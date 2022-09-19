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
time.sleep(3)
accept_cookies = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[1]/div[5]/button[1]')
accept_cookies.click()

# Getting information from the table of clubs and stadiums at the bottom of the website
stadiums = driver.find_elements(By.XPATH,'//*[@id="mainContent"]/div[2]/div/div/div[3]/div/table/tbody/tr')
# Making a list of stadiums to store all the sadium information to be put in CSV file
stadiumList = []
# Getting the profile links of all the stadiums and storing them to visit them for each website and get its data
for stadium in stadiums:
    attr = stadium.find_elements(By.TAG_NAME,'td')
    [clubName, clubStadium] = attr #Object Destruction
    stadiumProfile = clubStadium.find_element(By.TAG_NAME,'a').get_attribute("href")
    stadiumDict = {
		"StadiumName": clubStadium.text,
        "StadiumProfile": stadiumProfile
	}
    print(stadiumDict)
    stadiumList.append(stadiumDict)

#Up till now, we have the club profile in Website not the official website
#We need to fetch every club profile to get the official website
for stadium in stadiumList:
    driver.get(stadium["StadiumProfile"])
    time.sleep(1)
    try:
        # Clicking the stadium information button
        clicker = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div[3]/div[2]/div/ul/li[2]')
        clicker.click()
        
        # Begin scrapping

        # Capacity
        capacity = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div[3]/div[3]/div[2]/p[1]')
        capacity2 = capacity.text.split(":")
        capacity3 = capacity2[1][1:]
        stadium["Capacity"] = capacity3
        print(capacity3)
        
        recordPlAttendance = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div[3]/div[3]/div[2]/p[2]')
        recordPlAttendance2 = recordPlAttendance.text.split()
        if recordPlAttendance2[0] == "Record":
            # Record attendance in case exists
            recordPlAttendance3 = recordPlAttendance2[3]
            stadium["RecordPremierLeagueAttendace"] = recordPlAttendance3
            print(recordPlAttendance3)

            # Building date
            buildingDate = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div[3]/div[3]/div[2]/p[3]')
            buildingDate2 = buildingDate.text.split()
            buildingDate3 = buildingDate2[1]
            stadium["BuldingDate"] = buildingDate3
            print(buildingDate3)

            # Pitch length
            pitchSize = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div[3]/div[3]/div[2]/p[4]')
            pitchSize2 = pitchSize.text.split()
            if pitchSize2[0] == "Recent":   
                pitchLength = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div[3]/div[3]/div[2]/p[5]')
                pitchLength2 = pitchLength.text.split()
                pitchLength3 = pitchLength2[2][:-1]
                stadium["PitchLength"] = pitchLength3
                print(pitchLength3)

                # Pitch width 
                pitchWidth = pitchLength2[4][:-1]
                stadium["PitchWidth"] = pitchWidth
                print(pitchWidth)

                address = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div[3]/div[3]/div[2]/p[6]')
                address2 = address.text.split(",")
                
                if len(address2) == 4:
                    # Street 
                    street = address2[0].split(":")
                    street2 = street[1][1:]
                    street3 = address2[1][1:]
                    street4 = street2 + ", " + street3
                    stadium["Street"] = street4
                    print(street4)

                    # City
                    city = address2[2][1:]
                    stadium["City"] = city
                    print(city)
                    
                    # Zipcode
                    zipCode = address2[3][1:]
                    stadium["Zipcode"] = zipCode
                    print(zipCode)
                else:
                    # Street 
                    street = address2[0].split(":")
                    street2 = street[1][1:]
                    stadium["Street"] = street2
                    print(street2)

                    # City
                    city = address2[1][1:]
                    stadium["City"] = city
                    print(city)
                    
                    # Zipcode
                    zipCode = address2[2][1:]
                    stadium["Zipcode"] = zipCode
                    print(zipCode)
            else:
                pitchLength = pitchSize2[2][:-1]
                stadium["PitchLength"] = pitchLength
                print(pitchLength)

                # Pitch width 
                pitchWidth = pitchSize2[4][:-1]
                stadium["PitchWidth"] = pitchWidth
                print(pitchWidth)

                address = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div[3]/div[3]/div[2]/p[5]')
                address2 = address.text.split(",")
                
                if len(address2) == 4:
                    # Street 
                    street = address2[0].split(":")
                    street2 = street[1][1:]
                    street3 = address2[1][1:]
                    street4 = street2 + ", " + street3
                    stadium["Street"] = street4
                    print(street4)

                    # City
                    city = address2[2][1:]
                    stadium["City"] = city
                    print(city)
                    
                    # Zipcode
                    zipCode = address2[3][1:]
                    stadium["Zipcode"] = zipCode
                    print(zipCode)
                else:
                    # Street 
                    street = address2[0].split(":")
                    street2 = street[1][1:]
                    stadium["Street"] = street2
                    print(street2)

                    # City
                    city = address2[1][1:]
                    stadium["City"] = city
                    print(city)
                    
                    # Zipcode
                    zipCode = address2[2][1:]
                    stadium["Zipcode"] = zipCode
                    print(zipCode)

        else:
            # Record attendance in case does not exist
            recordPlAttendance3 = ""
            stadium["RecordPremierLeagueAttendace"] = recordPlAttendance3

            # Building date
            buildingDate = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div[3]/div[3]/div[2]/p[2]')
            buildingDate2 = buildingDate.text.split()
            buildingDate3 = buildingDate2[1]
            stadium["BuldingDate"] = buildingDate3
            print(buildingDate3)
            
            # Pitch length
            pitchSize = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div[3]/div[3]/div[2]/p[3]')
            pitchSize2 = pitchSize.text.split()
            if pitchSize2[0] == "Recent":   
                pitchLength = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div[3]/div[3]/div[2]/p[4]')
                pitchLength2 = pitchLength.text.split()
                pitchLength3 = pitchLength2[2][:-1]
                stadium["PitchLength"] = pitchLength3
                print(pitchLength3)

                # Pitch width 
                pitchWidth = pitchLength2[4][:-1]
                stadium["PitchWidth"] = pitchWidth
                print(pitchWidth)

                address = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div[3]/div[3]/div[2]/p[5]')
                address2 = address.text.split(",")
                
                if len(address2) == 4:
                    # Street 
                    street = address2[0].split(":")
                    street2 = street[1][1:]
                    street3 = address2[1][1:]
                    street4 = street2 + ", " + street3
                    stadium["Street"] = street4
                    print(street4)

                    # City
                    city = address2[2][1:]
                    stadium["City"] = city
                    print(city)
                    
                    # Zipcode
                    zipCode = address2[3][1:]
                    stadium["Zipcode"] = zipCode
                    print(zipCode)
                else:
                    # Street 
                    street = address2[0].split(":")
                    street2 = street[1][1:]
                    stadium["Street"] = street2
                    print(street2)

                    # City
                    city = address2[1][1:]
                    stadium["City"] = city
                    print(city)
                    
                    # Zipcode
                    zipCode = address2[2][1:]
                    stadium["Zipcode"] = zipCode
                    print(zipCode)
            else:
                pitchLength = pitchSize2[2][:-1]
                stadium["PitchLength"] = pitchLength
                print(pitchLength)

                # Pitch width 
                pitchWidth = pitchSize2[4][:-1]
                stadium["PitchWidth"] = pitchWidth
                print(pitchWidth)

                address = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div[3]/div[3]/div[2]/p[4]')
                address2 = address.text.split(",")
                
                if len(address2) == 4:
                    # Street 
                    street = address2[0].split(":")
                    street2 = street[1][1:]
                    street3 = address2[1][1:]
                    street4 = street2 + ", " + street3
                    stadium["Street"] = street4
                    print(street4)

                    # City
                    city = address2[2][1:]
                    stadium["City"] = city
                    print(city)
                    
                    # Zipcode
                    zipCode = address2[3][1:]
                    stadium["Zipcode"] = zipCode
                    print(zipCode)
                else:
                    # Street 
                    street = address2[0].split(":")
                    street2 = street[1][1:]
                    stadium["Street"] = street2
                    print(street2)

                    # City
                    city = address2[1][1:]
                    stadium["City"] = city
                    print(city)
                    
                    # Zipcode
                    zipCode = address2[2][1:]
                    stadium["Zipcode"] = zipCode
                    print(zipCode)
    except:
        print("No stadium information for club " + stadium["StadiumName"] + " The missing information will be NULL ")
        stadium["Capacity"] = ""
        stadium["RecordPremierLeagueAttendace"] = ""
        stadium["BuldingDate"] = ""
        stadium["PitchLength"] = ""
        stadium["PitchWidth"] = ""
        stadium["Street"] = ""
        stadium["City"] = ""
        stadium["Zipcode"] = ""


# Deleting the stadium profile from every stadium in the list because it is not needed anymore
for stadium in stadiumList:
    del stadium["StadiumProfile"]

# Create a DataFrame and Export CSV
df = pd.DataFrame(stadiumList)
df.to_csv(r'Stadiums.csv',index=True)
driver.close()