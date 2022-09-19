import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse

#Open browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
season22 = "https://www.premierleague.com/players"
season21 = "https://www.premierleague.com/players?se=363&cl=-1"
season20 = "https://www.premierleague.com/players?se=274&cl=-1"
season19 = "https://www.premierleague.com/players?se=210&cl=-1"
seasons =[season22,season21,season20,season19]
playerListAll = []
playerListNew = []
for seasonURL in seasons: 
    driver.get(seasonURL)
    try:
        time.sleep(3)
        accept_cookies = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[1]/div[5]/button[1]')
        accept_cookies.click()
    except:
        time.sleep(3)
    # Scroll down
    current_height = driver.execute_script("return document.body.scrollHeight")
    time.sleep(3)
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

    players = driver.find_elements(By.XPATH,'//*[@id="mainContent"]/div[2]/div[1]/div/div/table/tbody/tr')
    print("Number of players found",len(players))
    # Loop in players for each player: name, position, nationality
    playerList = []
    for player in players:
        attr = player.find_elements(By.TAG_NAME,'td')
        [name, position, nationality] = attr #Object Destruction
        websitePlayer = name.find_element(By.TAG_NAME,('a')).get_attribute("href")
        playerDict = {
            "Name": name.text,
            "Position": position.text,
            "Nationality": nationality.text,
            "Website": websitePlayer,
        }
        print(playerDict)
        playerList.append(playerDict)
        playerListAll.append(playerDict)

    for player in playerList:
        url = player["Website"]
        driver.get(url)
        time.sleep(1)
        parts = urlparse(url)
        parts2 = parts.path.strip('/').split('/')
        id = parts2[1]
        print("ID Found "+ id)

        seasonsPlayer = driver.find_elements(By.XPATH,'//*[@id="mainContent"]/div[3]/div/div/div[3]/table/tbody/tr')
        seasonList = []

        for season in seasonsPlayer:
            attr = season.find_elements(By.TAG_NAME,'td')
            if len(attr) == 5:
                [season, club, app_sub, goals, more] = attr #Object Destruction
                if season.text != "" and season.text in ["2021/2022","2019/2020","2020/2021","2018/2019"]:
                    seasonDict = {
                        "Season": season.text,
                        "Club": club.text,
                        "App": app_sub.text, 
                        "Goals": goals.text,
                        "More": more.text
                    }
                    seasonList.append(seasonDict)
                    player["Season"] = season.text
                    player["Club"] = club.text
        for season in seasonList:
            playerDictNew = {
                "PlayerID": id,
                "Club": season["Club"],
                "Season": season["Season"]
            }
            playerListNew.append(playerDictNew)
print("Number of players before ", len(playerListAll))

print("Number of Players before in the updated squad list ",len(playerListNew))
print(playerListNew)
playerListNoDuplicates = [i for n, i in enumerate(playerListNew) if i not in playerListNew[n + 1:]]
print("Number of Players after in the updated squad list ",len(playerListNoDuplicates))
print(playerListNoDuplicates)

# Create a DataFrame and Export CSV
df = pd.DataFrame(playerListNoDuplicates)
df.to_csv(r'Squads3.csv',index=False)
driver.close()