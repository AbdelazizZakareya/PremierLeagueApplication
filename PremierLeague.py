from http.client import CannotSendRequest
import mysql.connector
mydb = mysql.connector.connect(
 host="sql4.freemysqlhosting.net",
 user="sql4494409",
 password="AUh4YVvDlf",
 database="sql4494409"
)
mycursor = mydb.cursor()

def review(emailAddress):
    print('You are now logged in. Please choose the match you want to review: ')
    season = input("Match season (Eaxmple Format: 2021/22 ): ")
    homeTeam = input("Match Home Team: ")
    awayTeam = input("Match Away Team: ")
    sql = "SELECT * FROM matches WHERE HomeTeamName = %s AND AwayTeamName = %s AND Season = %s"
    mycursor.execute(sql,(homeTeam,awayTeam,season))
    result = mycursor.fetchall()
    while len(result) == 0:
        print("Please enter a valid match information")
        season = input("Match season (Eaxmple Format: 2021/22 ): ")
        homeTeam = input("Match Home Team: ")
        awayTeam = input("Match Away Team: ")
        sql = "SELECT * FROM matches WHERE HomeTeamName = %s AND AwayTeamName = %s AND Season = %s"
        mycursor.execute(sql,(homeTeam,awayTeam,season))
        result = mycursor.fetchall()
    rating = int(input("Please enter your rating as a number from 1 to 10: "))
    sql2 = "INSERT INTO review VALUES (%s,%s,%s,%s,%s,%s)"
    option = input("Do you want to add a textual review? Type Y if yes or N otherwise: ")
    if option == 'Y':
        textReview = input("Type a textual review for the match: ")
    else:
        textReview = ""
    mycursor.execute(sql2,(emailAddress,homeTeam,awayTeam,season,rating,textReview))
    mydb.commit()
    response = input("Review Added. Type M to go back to mainmenu or any other key to quit ")
    if response == "M":
        applicationMainMenu()
    else:
        quit()
def logIN():
    emailAddress = input("Please log in with your email address to add a review: ")
    sql = "SELECT EmailAddress FROM premierleagueuser"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    found = 0
    for r in result:
        if emailAddress == r[0]:
            found = 1
            break
    if found:
        review(emailAddress)
    else:
        print("Email is incorrect or not found. Would you like to: ")
        print("1. Log in again ")
        print("2. Creat a new premierleague user account: ")
        option = input("Enter your response: ")
        if option == '1':
            logIN()
        else:
            createUserAccount()

def emailChecker(email,result):
    found = 0
    for r in result:
        if email == r[0]:
            found = 1
            break
    if found:
        return 1
    else:
        return 0

def userNameChecker(userName,result):
    found = 0
    for r in result:
        if userName == r[0]:
            found = 1
            break
    if found:
        return 1
    else:
        return 0
def createUserAccount():
    email = input("Please enter your email address: ")
    while '@' not in email:
        email = input("Please enter a valid email address: ")
    sql = "SELECT EmailAddress FROM premierleagueuser"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    if emailChecker(email,result):
        response = input("Email address has already been registered. Type Y for loging in instead or N for creating account with another email address: ")
        if response == 'Y':
            logIN()
        else:
            createUserAccount()
    userName = input("Please enter your user name: ")
    sql = "SELECT UserName FROM premierleagueuser"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    while userNameChecker(userName,result):
        userName = input("User Name has already been taken. Please choose another one: ")
    favTeam = input("Please enter you favourite team name: ")
    sql = "SELECT ClubName FROM club"
    mycursor.execute(sql)
    list = []
    result = mycursor.fetchall()
    for r in result:
        list.append(r[0])
    while favTeam not in list:
        favTeam = input("Please enter a valid favourite team name: ")
    birthdate = input("Please enter your birthdate in the following format YYYY-MM-DD: ")
    gender = input("Please enter your gender. Type M for male or F for female. Type N if you prefer not to say ")
    if gender == 'N':
        gender = ""
    sql = "INSERT INTO premierleagueuser (EmailAddress,FavouriteTeamName,UserName,Gender,Birthdate) VALUES (%s,%s,%s,%s,%s)"
    mycursor.execute(sql,(email,favTeam,userName,gender,birthdate))
    mydb.commit()
    option = input("Account created successfully. User has been registered into the system. Type M to go to main menu or any other letter to exit  ")
    if option == "M":
        applicationMainMenu()
    else:
        quit()
def viewReviews():
    print("Viewing all the reviews on all matches ")
    sql = "SELECT * FROM review"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    for r in result:
        print(r)
    response = input("Type Y if you want to view the reviews on a given match, otherwise type N to go back to main menu ")
    if response == 'Y':
        print("Please enter the match information: ")
        season = input("Match season (Eaxmple Format: 2021/22 ): ")
        homeTeam = input("Match Home Team: ")
        awayTeam = input("Match Away Team: ")
        sql = "SELECT * FROM matches WHERE HomeTeamName = %s AND AwayTeamName = %s AND Season = %s"
        mycursor.execute(sql,(homeTeam,awayTeam,season))
        result = mycursor.fetchall()
        while len(result) == 0:
            print("Please enter a valid match information")
            season = input("Match season (Eaxmple Format: 2021/22 ): ")
            homeTeam = input("Match Home Team: ")
            awayTeam = input("Match Away Team: ")
            sql = "SELECT * FROM matches WHERE HomeTeamName = %s AND AwayTeamName = %s AND Season = %s"
            mycursor.execute(sql,(homeTeam,awayTeam,season))
            result = mycursor.fetchall()
        print("Here is the review for the selected match: ")
        sql = "SELECT * FROM review WHERE MatchHomeTeamName = %s AND MatchAwayTeamName = %s AND MatchSeason = %s"
        mycursor.execute(sql,(homeTeam,awayTeam,season))
        result = mycursor.fetchall()
        for r in result:
            print(r)
        option = input("Type M to go to main menu or any other letter to exit  ")
        if option == "M":
            applicationMainMenu()
        else:
            quit()
    else:
        applicationMainMenu()

# This function shows the teams who won the most games in the 4 seasons we have
def showTeamsWonMostGamesBySeason():
    sql = "SELECT Season, AwayTeamName AS Team, MAX(NumberOfWins) AS Wins \
            FROM (SELECT m.AwayTeamName, m.Season,COUNT(m.AwayTeamName)+h.NumberOfHomeTeamWins AS NumberOfWins \
            FROM matches m inner join (SELECT HomeTeamName, Season, COUNT(HomeTeamName) AS NumberOfHomeTeamWins \
            FROM matches \
            WHERE HomeTeamGoals >AwayTeamGoals \
            GROUP BY Season,HomeTeamName) AS h ON m.AwayTeamName = h.HomeTeamName AND m.Season = h.Season \
            WHERE m.AwayTeamGoals > m.HomeTeamGoals \
            GROUP BY m.Season, m.AwayTeamName \
            ORDER BY NumberOfWins DESC) AS T \
            GROUP BY Season"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    for r in result:
        print(r)
    option = input("Type M to go to main menu or any other letter to exit  ")
    if option == "M":
        applicationMainMenu()
    else:
        quit()
# Assuming that the location of the team is the location of its homeStadium which I think is the case
def showTeamsInAGivenCity():
    city = input("Enter the city that you want to find all its teams: ")
    sql = "SELECT City FROM stadium"
    mycursor.execute(sql)
    list = []
    result = mycursor.fetchall()
    for r in result:
        list.append(r[0])
    while city not in list:
        city = input("Enter a valid city that you want to filter players with: ")
    sql = "SELECT c.ClubName FROM club c, stadium s WHERE c.HomeStadiumName = s.StadiumName AND s.City =%s"
    mycursor.execute(sql,(city,))
    result = mycursor.fetchall()
    print("All the team in "+city+": ")
    for r in result:
        print(r[0])
    option = input("Type M to go to main menu or any other letter to exit  ")
    if option == "M":
        applicationMainMenu()
    else:
        quit()
def showPlayersByPosition():
    position = input("Enter the position of the player (Possible positions: Forward, Midfieleder, Defender, Goalkeeper): ")
    while position not in ("Forward", "Midfieleder", "Defender", "Goalkeeper"):
        position = input("Enter a valid position of the player (Possible positions: Forward, Midfieleder, Defender, Goalkeeper): ")
    sql = "SELECT * FROM player WHERE Position = %s"
    mycursor.execute(sql,(position,))
    result = mycursor.fetchall()
    for r in result:
        print(r)
    option = input("Type M to go to main menu or any other letter to exit  ")
    if option == "M":
        applicationMainMenu()
    else:
        quit()
def homeTeamForAStadium():
    stadium = input("Enter the name of the stadium: ")
    sql = "SELECT ClubName FROM club WHERE HomeStadiumName = %s"
    mycursor.execute(sql,(stadium,))
    result = mycursor.fetchall()
    for r in result:
        print(r[0])
    option = input("Type M to go to main menu or any other letter to exit  ")
    if option == "M":
        applicationMainMenu()
    else:
        quit()
# This function queries and view any player information
def queryAndViewAPlayerInformation():
    name = input("Enter the full name of the player you want to get his information: ")
    sql = "SELECT * FROM player WHERE PlayerName =%s"
    mycursor.execute(sql,(name,))
    result = mycursor.fetchall()
    for r in result:
        print(r)
    option = input("Type M to go to main menu or any other letter to exit  ")
    if option == "M":
        applicationMainMenu()
    else:
        quit()
def queryAndViewAClubInformation():
    name = input("Enter the name of the team you want to get its information: ")
    sql = "SELECT * FROM club WHERE ClubName =%s"
    mycursor.execute(sql,(name,))
    result = mycursor.fetchall()
    for r in result:
        print(r)
    option = input("Type M to go to main menu or any other letter to exit  ")
    if option == "M":
        applicationMainMenu()
    else:
        quit()
def showTopTeams():
    print("Would you like to show the top teams (for the 4 seasons) in: ")
    print("1. Home matches won ")
    print("2. Matches won ")
    print("3. Yellow cards ")
    print("4. Fouls ")
    print("5. Shots ")
    option = int(input("Choose the filter: "))
    while option <1 or option >5:
        option = int(input("Please choose a valid option: "))
    number = int(input("Enter the number of teams you want to get: "))
    match option:
        case 1:
            sql = "SELECT HomeTeamName, COUNT(HomeTeamName) AS NumberOfHomeTeamWins\
                FROM matches\
                WHERE HomeTeamGoals >AwayTeamGoals\
                GROUP BY HomeTeamName\
                ORDER BY NumberOfHomeTeamWins DESC\
                LIMIT %s;"
            mycursor.execute(sql,(number,))
            result = mycursor.fetchall()
            print("TeamName, NumberOfHomeWins")
            for r in result:
                print(r[0] + ", " + str(r[1]))
            response = input("Enter M if you want to browse the main menu and press any other key to quit: ")
            if response == 'M':
                applicationMainMenu()
            else:
                quit()
        case 2:
            sql = "SELECT m.AwayTeamName AS Team,COUNT(m.AwayTeamName)+h.NumberOfHomeTeamWins AS NumberOfWins\
                FROM matches m inner join (SELECT HomeTeamName, COUNT(HomeTeamName) AS NumberOfHomeTeamWins\
                FROM matches\
                WHERE HomeTeamGoals >AwayTeamGoals\
                GROUP BY HomeTeamName) AS h ON m.AwayTeamName = h.HomeTeamName\
                WHERE m.AwayTeamGoals > m.HomeTeamGoals\
                GROUP BY m.AwayTeamName\
                ORDER BY NumberOfWins DESC\
                LIMIT %s"
            mycursor.execute(sql,(number,))
            result = mycursor.fetchall()
            print("TeamName, NumberOfWins")
            for r in result:
                print(r[0] + ", " + str(r[1]))
            response = input("Enter M if you want to browse the main menu and press any other key to quit: ")
            if response == 'M':
                applicationMainMenu()
            else:
                quit()
        case 3:
            sql = "SELECT m.AwayTeamName AS Team,SUM(m.AwayTeamNumberOFYellowCards)+ h.NumberOfHomeTeamYellowCards AS NumberOfYellowCards\
                FROM matches m inner join (SELECT HomeTeamName, Sum(HomeTeamNumberOFYellowCards) AS NumberOfHomeTeamYellowCards\
                FROM matches\
                GROUP BY HomeTeamName) AS h ON m.AwayTeamName = h.HomeTeamName\
                GROUP BY m.AwayTeamName\
                ORDER BY NumberOfYellowCards DESC\
                LIMIT %s"
            mycursor.execute(sql,(number,))
            result = mycursor.fetchall()
            print("Team, NumberOfYellowCards")
            for r in result:
                print(r[0] + ", " + str(r[1]))
            response = input("Enter M if you want to browse the main menu and press any other key to quit: ")
            if response == 'M':
                applicationMainMenu()
            else:
                quit()
        case 4:
            sql = "SELECT m.AwayTeamName AS Team,SUM(m.AwayTeamFouls)+ h.HomeTeamFouls AS Fouls\
                FROM matches m inner join (SELECT HomeTeamName, Sum(HomeTeamFouls) AS HomeTeamFouls\
                FROM matches\
                GROUP BY HomeTeamName) AS h ON m.AwayTeamName = h.HomeTeamName\
                GROUP BY m.AwayTeamName\
                ORDER BY Fouls DESC\
                LIMIT %s"
            mycursor.execute(sql,(number,))
            result = mycursor.fetchall()
            print("Team, Fouls")
            for r in result:
                print(r[0] + ", " + str(r[1]))
            response = input("Enter M if you want to browse the main menu and press any other key to quit: ")
            if response == 'M':
                applicationMainMenu()
            else:
                quit()
        case 5:
            sql = "SELECT m.AwayTeamName AS Team,SUM(m.AwayTeamShots)+ h.HomeTeamShots AS Shots\
                FROM matches m inner join (SELECT HomeTeamName, Sum(HomeTeamShots) AS HomeTeamShots\
                FROM matches\
                GROUP BY HomeTeamName) AS h ON m.AwayTeamName = h.HomeTeamName\
                GROUP BY m.AwayTeamName\
                ORDER BY Shots DESC\
                LIMIT %s"
            mycursor.execute(sql,(number,))
            result = mycursor.fetchall()
            print("Team, Fouls")
            for r in result:
                print(r[0] + ", " + str(r[1]))
            response = input("Enter M if you want to browse the main menu and press any other key to quit: ")
            if response == 'M':
                applicationMainMenu()
            else:
                quit()
def ShowPlayersNationality():
    nationality = input("Enter the nationality that you want to filter players with: ")
    sql = "SELECT Nationality FROM player"
    mycursor.execute(sql)
    list = []
    result = mycursor.fetchall()
    for r in result:
        list.append(r[0])
    while nationality not in list:
        nationality = input("Enter a valid nationality that you want to filter players with: ")
    sql = "SELECT p.PlayerID, p.PlayerName, p.Position, p.Nationality, p.Height, p.DateOfBirth, s.clubNameSquad, s.Season\
            FROM player p, squad s\
            WHERE Nationality = %s AND p.PlayerID = s.PlayerID; "
    mycursor.execute(sql,(nationality,))
    result = mycursor.fetchall()
    print("PlayerID, PlayerName, PlayerPosition, PlayerNationality, PlayerHeight, PlayerBirthDate, PlayerHomeTeam, PlayerSeason")
    for r in result:
        print(r)
    response = input("Enter M if you want to browse the main menu and press any other key to quit: ")
    if response == 'M':
        applicationMainMenu()
    else:
        quit()
def switchCase(x):
    match x:
        case 1:
            logIN()
        case 2:
            viewReviews()
        case 3:
            createUserAccount()
        case 4:
            ShowPlayersNationality()
        case 5:
            showTopTeams()
        case 6:
            showTeamsWonMostGamesBySeason()
        case 7:
            queryAndViewAClubInformation()
        case 8:
            queryAndViewAPlayerInformation()
        case 9:
            homeTeamForAStadium()
        case 10:
            showPlayersByPosition()
        case 11:
            showTeamsInAGivenCity()
        case 12:
            quit()
def applicationMainMenu():
    print("Welcome to the Premier League Website!\nWould you like to: ")
    print("1. Add a new user review on a match")
    print("2. View reviews on a match")
    print("3. Register a user")
    print("4. Show all the players from a certain nationality and their home team history ")
    print("5. Show top teams by filters such as matches won, home matches won, yellow cards, fouls,and shots")
    print("6. Show all the teams who won the most games by season")
    print("7. Query and view a given team information")
    print("8. Query and view a given player information (by their first and last name)")
    print("9. Identify the home team for a given stadium name")
    print("10. Show all the players who played a certain position")
    print("11. Identify all the teams in a given city in the UK")
    print("12. Exit")
    option = int(input("Type in your choice: "))
    while option<1 or option>12:
        option = input("Please enter a valid response: ")
    switchCase(option)
applicationMainMenu()
