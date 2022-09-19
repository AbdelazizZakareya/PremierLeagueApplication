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
i = True
playerListAll = []
playerListNewAll = []
for seasonURL in seasons: 
    driver.get(seasonURL)
    # Accept on Cookies
    time.sleep(3) # Wait to load page
    try:
        accept_cookies = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[1]/div[5]/button[1]')
        accept_cookies.click()
    except:
        time.sleep(1)
    time.sleep(3)
    # Scroll down
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

    players = driver.find_elements(By.XPATH,'//*[@id="mainContent"]/div[2]/div[1]/div/div/table/tbody/tr')
    print("Number of Players",len(players))
    playerList = []
    # Loop in players for each player: name, position, nationality
    for player in players:
        attr = player.find_elements(By.TAG_NAME,'td')
        [name, position, nationality] = attr #Object Destruction
        websitePlayer = name.find_element(By.TAG_NAME,('a')).get_attribute("href")
        player_dict = {
            "Name": name.text,
            "Position": position.text,
            "Nationality": nationality.text,
            "Website": websitePlayer,
        }
        print(player_dict)
        playerList.append(player_dict)
        playerListAll.append(player_dict)
        
    for player in playerList:
        url = player["Website"]
        driver.get(url)
        time.sleep(1)
        parts = urlparse(url)
        parts2 = parts.path.strip('/').split('/')
        id = parts2[1]
        print("ID Found "+ id)
        try:
            height = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div[3]/div/div/div[1]/section/div/ul[3]/li[1]/div[2]')
            height2 = height.text[0:3]
            print(height2)   
        except:
            print("No height for player " + player["Name"] + ". We will keep it NULL")
            height2 = ""
        try:
            birth = driver.find_element(By.XPATH, '//*[@id="mainContent"]/div[3]/div/div/div[1]/section/div/ul[2]/li/div[2]')
            birth2 = birth.text[0:10]
            print(birth2)
        except:
            print("No birthdate for player " + player["Name"] + ". We will keep it NULL")
            birth2 = ""
        playerDictNew = {
            "PlayerID": id,
            "PlayerName":   player["Name"],
            "Position": player["Position"],
            "Nationality":player["Nationality"],
            "Height": height2,
            "DateOfBirth": birth2
        }
        playerListNewAll.append(playerDictNew)
print("Before")
print("Number of Players before",len(playerListNewAll))
print(playerListNewAll)
print("After")
playerListNoDuplicates = [i for n, i in enumerate(playerListNewAll) if i not in playerListNewAll[n + 1:]]
print("Number of Players after",len(playerListNoDuplicates))
print(playerListNoDuplicates)

# Create a DataFrame and Export CSV
df = pd.DataFrame(playerListNoDuplicates)
df.to_csv(r'Players3.csv',index=False)
driver.close()