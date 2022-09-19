import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://www.premierleague.com/')
time.sleep(3)
accept_cookies = driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[1]/div[5]/button[1]')
accept_cookies.click()



seasons = {
    "2021/22": "https://www.premierleague.com/results?co=1&se=418&cl=-1",
    "2020/21": "https://www.premierleague.com/results?co=1&se=363&cl=-1",
    "2019/20": "https://www.premierleague.com/results?co=1&se=274&cl=-1",
    "2018/19": "https://www.premierleague.com/results?co=1&se=210&cl=-1"
}
matchesListAll = []
seasonMatches = {}
for seasonName, seasonURL in seasons.items(): 
    # while True:
        try:
            driver.get(seasonURL)
            time.sleep(5)
            # #Scroll down
            current_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 	# Scroll step
                time.sleep(3) 	# Wait to load page
                try:
                    new_height = driver.execute_script("return document.body.scrollHeight") # Calculate new scroll height
                except:
                    print("Failed: ", new_height)
                if new_height == current_height: # Compare with last scroll height
                    break
                current_height = new_height
            print("scorlled till",current_height) 
        except:
            print("Unable to open season "+ seasonURL)
        matchListLinks = []
        matches = driver.find_elements(By.CLASS_NAME,"matchFixtureContainer")
        time.sleep(5)
        for match in matches:
            matchLink = match.find_element(By.TAG_NAME,"div").get_attribute("data-href")
            matchLink2 = "https:" + matchLink
            matchListLinks.append(matchLink2)
        print("Number of matches found in season " + seasonName + " ", len(matchListLinks))
        for match in matchListLinks:
           while True:
                try:
                    driver.get(match)
                    time.sleep(5)
                    clickStats = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div/section[2]/div[2]/div[2]/div[1]/div/div/ul/li[3]')
                    clickStats.click()
                    time.sleep(3)
                    homeTeamName = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div/section[2]/div[2]/section/div[3]/div/div/div[1]/div[1]/a[2]/span[1]')
                    print(homeTeamName.text)
                    awayTeamName = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div/section[2]/div[2]/section/div[3]/div/div/div[1]/div[3]/a[2]/span[1]')
                    print(awayTeamName.text)
                    matchDate = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div/section[2]/div[2]/section/div[1]/div/div[1]/div[1]')
                    matchDate2 = matchDate.text.split()
                    matchDate3 = matchDate2[1] + " " + matchDate2[2] + " " + matchDate2[3]
                    print(matchDate3)
                    matchStadium = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div/section[2]/div[2]/section/div[1]/div/div[1]/div[3]')
                    matchStadium2 = matchStadium.text.split(",")
                    matchStadium3 = matchStadium2[0]
                    print(matchStadium3)
                    homeTeamGoals = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div/section[2]/div[2]/section/div[3]/div/div/div[1]/div[2]/div/div')
                    homeTeamGoals2 = homeTeamGoals.text.split("-")
                    homeTeamGoals3 = homeTeamGoals2[0]
                    print(homeTeamGoals3)
                    awayTeamGoals = homeTeamGoals2[1]
                    print(awayTeamGoals)
                    # We noticed that the table is not consistent. Sometimes we have yellow cards and/or red cards, other time not
                    # So, we will focus on the table by making it in a dictionary as follows
                    # The statsRows is the list that contains all the rows in the table
                    statsRows = driver.find_elements(By.XPATH, '/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr')
                    statsHome = {}
                    statsAway = {}
                    
                    for stat in statsRows:
                        attr = stat.find_elements(By.TAG_NAME,'td')
                        [homeStat, statName, awaystat] = attr
                        statsHome[statName.text] = homeStat.text
                        statsAway[statName.text] = awaystat.text

                    matchDict = {
                        "MatchDate": matchDate3,
                        "HomeTeamName": homeTeamName.text,
                        "AwayTeamName": awayTeamName.text,
                        "MatchStadium": matchStadium3,
                        "MatchSeason": seasonName,
                        "HomeTeamGoals": homeTeamGoals3,
                        "AwayTeamGoals": awayTeamGoals,
                        "HomeTeamshots": statsHome.get("Shots",0),
                        "AwayTeamShots": statsAway.get("Shots",0),
                        "HomeTeamPossession": statsHome.get("Possession %",0),
                        "AwayTeamPossession": statsAway.get("Possession %",0),
                        "HomeTeamFoulsConceded": statsHome.get("Fouls conceded",0),
                        "AwayTeamFoulsConceded": statsAway.get("Fouls conceded",0),
                        "HomeTeamYellowCards": statsHome.get("Yellow cards",0),
                        "AwayTeamYellowCards": statsAway.get("Yellow cards",0),
                        "HomeTeamRedCards": statsHome.get("Red cards",0),
                        "AwayTeamRedCards": statsAway.get("Red cards",0)
                    }
                    print(matchDict)
                    matchesListAll.append(matchDict)
                    time.sleep(3)
                    break
                except:
                    print("Unable to get match information ")
        
            

# Create a DataFrame and Export CSV
df = pd.DataFrame(matchesListAll)
df.to_csv(r'Matches.csv',index=True)
driver.close()