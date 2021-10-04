# main.py

from mysqlCnx import MysqlCnx
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
import json

##### NEW STUFF #####################################
# open the config file and read it
with open('.config.json') as f:
    config = json.loads(f.read())

cnx = MysqlCnx(**config)

#####################################################
# LOCAL DB

# Basics
basics = {
    1 : {"sql":"SELECT population FROM world WHERE name = 'Germany'","question":"The example uses a WHERE clause to show the population of 'France'. Note that strings (pieces of text that are data) should be in 'single quotes'; Modify it to show the population of Germany."},
    2 : {"sql":"SELECT name, population FROM world WHERE name IN ('Sweden', 'Norway', 'Denmark');","question":"Checking a list The word IN allows us to check if an item is in a list. The example shows the name and population for the countries 'Brazil', 'Russia', 'India' and 'China'. Show the name and the population for 'Sweden', 'Norway' and 'Denmark'."},
    3 : {"sql":"SELECT name, area FROM world WHERE area BETWEEN 200000 AND 250000","question":"Which countries are not too small and not too big? BETWEEN allows range checking (range specified is inclusive of boundary values). The example below shows countries with an area of 250,000-300,000 sq. km. Modify it to show the country and the area for countries with an area between 200,000 and 250,000."}
    }

# World Tutorial
world = {
    1 : {"sql":"SELECT name, continent, population FROM world","question":"Observe the result of running this SQL command to show the name, continent and population of all countries."},
    2 : {"sql":"SELECT name FROM world WHERE population > 200000000","question":"Show the name for the countries that have a population of at least 200 million. 200 million is 200000000, there are eight zeros."},
    3 : {"sql":"SELECT name, gdp/population FROM world WHERE population > 200000000","question":"Give the name and the per capita GDP for those countries with a population of at least 200 million."},
    4 : {"sql":"SELECT name, population/1000000 FROM world WHERE continent = 'South America'","question":"Show the name and population in millions for the countries of the continent 'South America'. Divide the population by 1000000 to get population in millions."},
    5 : {"sql":"SELECT name, population FROM world WHERE name IN ('France', 'Germany', 'Italy')","question":"Show the name and population for France, Germany, Italy"},
    6 : {"sql":"SELECT name FROM world WHERE name LIKE 'United%'","question":"Show the countries which have a name that includes the word 'United'"},
    7 : {"sql":"SELECT name, population, area FROM world WHERE area > 3000000 OR population > 250000000","question":"Two ways to be big: A country is big if it has an area of more than 3 million sq km or it has a population of more than 250 million. Show the countries that are big by area or big by population. Show name, population and area."},
    8 : {"sql":"SELECT name, population, area FROM world WHERE area > 3000000 XOR population > 250000000","question":"Exclusive OR (XOR). Show the countries that are big by area (more than 3 million) or big by population (more than 250 million) but not both. Show name, population and area. Australia has a big area but a small population, it should be included. Indonesia has a big population but a small area, it should be included. China has a big population and big area, it should be excluded. United Kingdom has a small population and a small area, it should be excluded."},
    9 : {"sql":"SELECT name, ROUND(population/1000000, 2), ROUND(gdp/1000000000, 2) FROM world WHERE continent = 'South America'","question":"Show the name and population in millions and the GDP in billions for the countries of the continent 'South America'. Use the ROUND function to show the values to two decimal places. For South America show population in millions and GDP in billions both to 2 decimal places."},
    10 : {"sql":"SELECT name, ROUND(gdp/population, -3) FROM world WHERE gdp > 1000000000000","question":"Show the name and per-capita GDP for those countries with a GDP of at least one trillion (1000000000000; that is 12 zeros). Round this value to the nearest 1000. Show per-capita GDP for the trillion dollar countries to the nearest $1000."},
    11 : {"sql":"SELECT name, capital FROM world WHERE LENGTH(name) = LENGTH(capital)","question":"Greece has capital Athens. Each of the strings 'Greece', and 'Athens' has 6 characters. Show the name and capital where the name and the capital have the same number of characters."},
    12 : {"sql":"SELECT name, capital FROM world WHERE LEFT(name, 1) = LEFT(capital, 1) AND name <> capital","question":"The capital of Sweden is Stockholm. Both words start with the letter ’S'. Show the name and the capital where the first letters of each match. Don't include countries where the name and the capital are the same word."},
    13 : {"sql":"SELECT name FROM world WHERE name LIKE '%a%' AND name LIKE '%e%' AND name LIKE '%i%' AND name LIKE '%o%' AND name LIKE ‘%u%' AND name NOT LIKE '% %'","question":"quatorial Guinea and Dominican Republic have all of the vowels (a e i o u) in the name. They don't count because they have more than one word in the name. Find the country that has all the vowels and no spaces in its name"}      
    }

# Nobel Tutorial
nobel = {
    1 : {"sql":"SELECT yr, subject, winner FROM nobel WHERE yr = 1950","question":"Change the query shown so that it displays Nobel prizes for 1950."},
    2 : {"sql":"SELECT winner FROM nobel WHERE yr = 1962 AND subject = 'Literature'","question":"Show who won the 1962 prize for Literature."},
    3 : {"sql":"SELECT yr, subject FROM nobel WHERE winner = 'Albert Einstein'","question":"Show the year and subject that won 'Albert Einstein' his prize."},
    4 : {"sql":"SELECT winner FROM nobel WHERE subject = 'Peace' AND yr >= 2000","question":"Give the name of the 'Peace' winners since the year 2000, including 2000."},
    5 : {"sql":"SELECT yr, subject, winner FROM nobel WHERE subject = 'Literature' AND yr BETWEEN 1980 AND 1989","question":"Show all details (yr, subject, winner) of the Literature prize winners for 1980 to 1989 inclusive."},
    6 : {"sql":"SELECT * FROM nobel WHERE winner IN ('Theodore Roosevelt','Woodrow Wilson','Jimmy Carter', 'Barack Obama')","question":"Show all details of the presidential winners: Theodore Roosevelt, Woodrow Wilson, Jimmy Carter, Barack Obama"},
    7 : {"sql":"SELECT winner FROM nobel WHERE winner LIKE 'John%'","question":"Show the winners with first name John"},
    8 : {"sql":"SELECT yr, subject, winner FROM nobel WHERE subject = 'Physics' AND yr = 1980 OR subject = 'Chemistry' AND yr = 1984","question":"Show the year, subject, and name of Physics winners for 1980 together with the Chemistry winners for 1984."},
    9 : {"sql":"SELECT yr, subject, winner FROM nobel WHERE yr = 1980 AND subject NOT LIKE 'Chemistry' AND yr = 1980 AND subject NOT LIKE 'Medicine'","question":"Show the year, subject, and name of winners for 1980 excluding Chemistry and Medicine"},
    10 : {"sql":"SELECT yr, subject, winner FROM nobel WHERE yr < 1910 AND subject = 'Medicine' OR yr >= 2004 AND subject = 'Literature'","question":"Show year, subject, and name of people who won a 'Medicine' prize in an early year (before 1910, not including 1910) together with winners of a 'Literature' prize in a later year (after 2004, including 2004)"},
    11 : {"sql":"SELECT * FROM nobel WHERE winner = 'Peter Grünberg'","question":"Find all details of the prize won by PETER GRÜNBERG"},
    12 : {"sql":"SELECT * FROM nobel WHERE winner = 'Eugene O''neill'","question":"Find all details of the prize won by EUGENE O'NEILL"},
    13 : {"sql":"SELECT winner, yr, subject FROM nobel WHERE winner LIKE 'Sir%'","question":"Knights in order. List the winners, year and subject where the winner starts with Sir. Show the the most recent first, then by name order."},
    14 : {"sql":"SELECT SUM(population) FROM world","question":"The expression subject IN ('Chemistry','Physics') can be used as a value - it will be 0 or 1. Show the 1984 winners and subject ordered by subject and winner name; but list Chemistry and Physics last."}    
    }

# Select Within Tutorial
within = {
    1 : {"sql":"SELECT name FROM world WHERE population > (SELECT population FROM world WHERE name='Russia')","question":"List each country name where the population is larger than that of 'Russia'."},
    2 : {"sql":"SELECT name FROM world WHERE continent='Europe' AND gdp/population > (SELECT gdp/population FROM world WHERE name='United Kingdom')","question":"Show the countries in Europe with a per capita GDP greater than 'United Kingdom'."},
    3 : {"sql":"SELECT name,continent FROM world WHERE continent IN (SELECT continent FROM world WHERE name IN ('Australia','Argentina')) ORDER BY name","question":"List the name and continent of countries in the continents containing either Argentina or Australia. Order by name of the country."},
    4 : {"sql":"SELECT name,population FROM world WHERE population BETWEEN (SELECT population+1 FROM world WHERE name='Canada') AND (SELECT population-1 FROM world WHERE name='Poland')","question":"Which country has a population that is more than Canada but less than Poland? Show the name and the population."},
    5 : {"sql":"SELECT name, CONCAT(CAST(ROUND(100*population/(SELECT population FROM world WHERE name = 'Germany'),0) as int), '%') FROM world WHERE continent = 'Europe'","question":"Germany (population 80 million) has the largest population of the countries in Europe. Austria (population 8.5 million) has 11 of the population of Germany. Show the name and the population of each country in Europe. Show the population as a percentage of the population of Germany"},
    6 : {"sql":"SELECT name FROM world WHERE gdp > ALL (SELECT gdp FROM world WHERE continent = 'Europe' AND gdp IS NOT NULL)","question":"Which countries have a GDP greater than every country in Europe? [Give the name only.] (Some countries may have NULL gdp values)"},
    7 : {"sql":"SELECT continent, name, area FROM world x WHERE area >= ALL (SELECT area FROM world y WHERE y.continent=x.continent and area > 0 )","question":"Find the largest country (by area) in each continent, show the continent, the name and the area:"},
    8 : {"sql":"SELECT continent,name FROM world x WHERE x.name <= ALL (SELECT name FROM world y WHERE x.continent=y.continent)","question":"List each continent and the name of the country that comes first alphabetically."},
    9 : {"sql":"SELECT name,continent,population FROM world x WHERE 25000000 >= ALL (SELECT population FROM world y WHERE x.continent=y.continent AND y.population>0)","question":"Find the continents where all countries have a population <= 25000000. Then find the names of the countries associated with these continents. Show name, continent and population."},
    10 : {"sql":"SELECT name, continent FROM world x WHERE population > ALL (SELECT population*3 FROM world y WHERE y.continent = x.continent AND y.name != x.name)","question":"Some countries have populations more than three times that of any of their neighbours (in the same continent). Give the countries and continents."}
    }

# Sum and Count
aggregate = {
    1 : {"sql":"SELECT SUM(population) FROM world","question":"Show the total population of the world."},
    2 : {"sql":"SELECT DISTINCT(continent) FROM world","question":"List all the continents - just once each."},
    3 : {"sql":"SELECT SUM(gdp) FROM world WHERE continent = 'Africa'","question":"Give the total GDP of Africa"},
    4 : {"sql":"SELECT COUNT(name) FROM world WHERE area >= 1000000","question":"How many countries have an area of at least 1000000"},
    5 : {"sql":"SELECT SUM(population) FROM world WHERE name IN ('Estonia', 'Latvia', 'Lithuania')","question":"What is the total population of ('Estonia', 'Latvia', 'Lithuania')"},
    6 : {"sql":"SELECT continent, COUNT(name) FROM world GROUP BY(continent)","question":"For each continent show the continent and number of countries."},
    7 : {"sql":"SELECT continent, COUNT(name) FROM world WHERE population >= 10000000 GROUP BY(continent)","question":"For each continent show the continent and number of countries with populations of at least 10 million."},
    8 : {"sql":"SELECT continent FROM world GROUP BY continent HAVING SUM(population)>= 100000000","question":"List the continents that have a total population of at least 100 million."}
    }

# Join operations
joint = {
    1 : {"sql":"SELECT matchid, player FROM goal WHERE teamid LIKE 'GER'","question":"The first example shows the goal scored by a player with the last name 'Bender'. The * says to list all the columns in the table - a shorter way of saying matchid, teamid, player, gtime Modify it to show the matchid and player name for all goals scored by Germany. To identify German players, check for: teamid = 'GER'"},
    2 : {"sql":"SELECT id,stadium,team1,team2 FROM game WHERE id=1012","question":"From the previous query you can see that Lars Bender's scored a goal in game 1012. Now we want to know what teams were playing in that match. Notice in the that the column matchid in the goal table corresponds to the id column in the game table. We can look up information about game 1012 by finding that row in the game table. Show id, stadium, team1, team2 for just game 1012"},
    3 : {"sql":"SELECT player,teamid,stadium,mdate FROM game JOIN goal ON (id=matchid) WHERE teamid='GER'","question":"The FROM clause says to merge data from the goal table with that from the game table. The ON says how to figure out which rows in game go with which rows in goal - the matchid from goal must match id from game. (If we wanted to be more clear/specific we could say ON (game.id=goal.matchid) The code below shows the player (from the goal) and stadium name (from the game table) for every goal scored. Modify it to show the player, teamid, stadium and mdate for every German goal."},
    4 : {"sql":"SELECT team1, team2, player FROM game JOIN goal ON (id=matchid) WHERE player LIKE 'Mario%'","question":"Use the same JOIN as in the previous question. Show the team1, team2 and player for every goal scored by a player called Mario player LIKE 'Mario%'"},
    5 : {"sql":"SELECT player, teamid, coach, gtime FROM goal JOIN eteam ON (teamid=id) WHERE gtime<=10","question":"The table eteam gives details of every national team including the coach. You can JOIN goal to eteam using the phrase goal JOIN eteam on teamid=id Show player, teamid, coach, gtime for all goals scored in the first 10 minutes gtime<=10"},
    6 : {"sql":"SELECT mdate,teamname FROM game JOIN eteam ON (team1=eteam.id) WHERE coach='Fernando Santos'","question":"To JOIN game with eteam you could use either game JOIN eteam ON (team1=eteam.id) or game JOIN eteam ON (team2=eteam.id) Notice that because id is a column name in both game and eteam you must specify eteam.id instead of just id List the dates of the matches and the name of the team in which 'Fernando Santos' was the team1 coach."},
    7 : {"sql":"SELECT player FROM goal JOIN game ON (id=matchid) WHERE stadium = 'National Stadium, Warsaw'","question":"List the player for every goal scored in a game where the stadium was 'National Stadium, Warsaw'"},
    8 : {"sql":"SELECT DISTINCT player FROM game JOIN goal ON matchid = id WHERE (team1 = 'GER' OR team2 = 'GER') AND teamid!='GER'","question":"The example query shows all goals scored in the Germany-Greece quarterfinal. Instead show the name of all players who scored a goal against Germany."},
    9 : {"sql":"SELECT teamname,COUNT(teamid) FROM eteam JOIN goal ON id=teamid GROUP BY teamname","question":"Show teamname and the total number of goals scored."},
    10 : {"sql":"SELECT stadium,COUNT(1) FROM goal JOIN game ON id=matchid GROUP BY stadium","question":"Show the stadium and the number of goals scored in each stadium."},
    11 : {"sql":"SELECT matchid,mdate,COUNT(teamid) FROM game JOIN goal ON matchid = id WHERE (team1 = 'POL' OR team2 = 'POL') GROUP BY matchid,mdate","question":"For every match involving 'POL', show the matchid, date and the number of goals scored."},
    12 : {"sql":"SELECT matchid,mdate,COUNT(teamid) FROM game JOIN goal ON matchid = id WHERE (teamid='GER') GROUP BY matchid,mdate","question":"For every match where 'GER' scored, show matchid, match date and the number of goals scored by 'GER'"},
    13 : {"sql":"SELECT mdate, team1, SUM(CASE WHEN teamid=team1 THEN 1 ELSE 0 END) score1,team2, SUM(CASE WHEN teamid=team2 THEN 1 ELSE 0 END) score2 FROM game LEFT JOIN goal ON matchid = id GROUP BY mdate,matchid,team1,team2","question":"List every match with the goals scored by each team as shown. This will use CASE WHEN which has not been explained in any previous exercises. Notice in the query given every goal is listed. If it was a team1 goal then a 1 appears in score1, otherwise there is a 0. You could SUM this column to get a count of the goals scored by team1. Sort your result by mdate, matchid, team1 and team2."}
    }

# All


##### END NEW STUFF #######

class Stops(BaseModel):
    id: int
    name: str

class Item(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    brand: str
    price: float

class WorldItem(BaseModel):
    id: Optional[int] = None
    area: Optional[int] = None
    population: Optional[int] = None
    gdp: Optional[int] = None
    name: Optional[str] = None
    continent: Optional[str] = None
    capital: Optional[str] = None
    tld: Optional[str] = None
    flag: Optional[str] = None

class Teach(BaseModel):
    id: Optional[int] = None
    phone: int
    mobile: int
    dept: str
    name: str

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to Totally Kyle"}

## BASICS ##

# Return ID
@app.get("/basics/{item_id}")
async def read_item(item_id:int):
    sql = basics[item_id]['sql']

    response = {
        'question':basics[item_id]['question'],
        'sql':basics[item_id]['sql']
    }
    
    res = cnx.query(basics[item_id]['sql'])
    
    if res['success']:
        response['results']=res['data']

    return response

## WORLD TUT ##

# Return ID
@app.get("/world/{item_id}")
async def read_item(item_id:int):
    sql = world[item_id]['sql']

    response = {
        'question':world[item_id]['question'],
        'sql':world[item_id]['sql']
    }
    
    res = cnx.query(world[item_id]['sql'])
    
    if res['success']:
        response['results']=res['data']

    return response

## NOBEL ##

# Return ID
@app.get("/nobel/{item_id}")
async def read_item(item_id:int):
    sql = nobel[item_id]['sql']

    response = {
        'question':nobel[item_id]['question'],
        'sql':nobel[item_id]['sql']
    }
    
    res = cnx.query(nobel[item_id]['sql'])
    
    if res['success']:
        response['results']=res['data']

    return response

## WITHIN ##

# Return ID
@app.get("/within/{item_id}")
async def read_item(item_id:int):
    sql = within[item_id]['sql']

    response = {
        'question':within[item_id]['question'],
        'sql':within[item_id]['sql']
    }
    
    res = cnx.query(within[item_id]['sql'])
    
    if res['success']:
        response['results']=res['data']

    return response

## SUM AND COUNT ##
# Return all

# Return ID
@app.get("/aggregate/{item_id}")
async def read_item(item_id:int):
    sql = aggregate[item_id]['sql']

    response = {
        'question':aggregate[item_id]['question'],
        'sql':aggregate[item_id]['sql']
    }
    
    res = cnx.query(aggregate[item_id]['sql'])
    
    if res['success']:
        response['results']=res['data']

    return response


## ALL ##
@app.get("/all/")
async def read_item_all(request:Request):
    response = {
        "BASICS": "-----------------------------------",
        basics[1]['question']: request.url_for("read_item_basics", **{"item_id":1}),
        basics[2]['question']:  request.url_for("read_item_basics", **{"item_id":2}),
        basics[3]['question']:  request.url_for("read_item_basics", **{"item_id":3}),
        "WORLD": "-----------------------------------",
        world[1]['question']:  request.url_for("read_item_world", **{"item_id":1}),
        world[2]['question']:  request.url_for("read_item_world", **{"item_id":2}),
        world[3]['question']:  request.url_for("read_item_world", **{"item_id":3}),
        world[4]['question']:  request.url_for("read_item_world", **{"item_id":4}),
        world[5]['question']:  request.url_for("read_item_world", **{"item_id":5}),
        world[6]['question']:  request.url_for("read_item_world", **{"item_id":6}),
        world[7]['question']:  request.url_for("read_item_world", **{"item_id":7}),
        world[8]['question']:  request.url_for("read_item_world", **{"item_id":8}),
        world[9]['question']:  request.url_for("read_item_world", **{"item_id":9}),
        world[10]['question']:  request.url_for("read_item_world", **{"item_id":10}),
        world[11]['question']:  request.url_for("read_item_world", **{"item_id":11}),
        world[12]['question']:  request.url_for("read_item_world", **{"item_id":12}),
        world[13]['question']:  request.url_for("read_item_world", **{"item_id":13}),
        "NOBEL": "-----------------------------------",
        nobel[1]['question']:  request.url_for("read_item_nobel", **{"item_id":1}),
        nobel[2]['question']:  request.url_for("read_item_nobel", **{"item_id":2}),
        nobel[3]['question']:  request.url_for("read_item_nobel", **{"item_id":3}),
        nobel[4]['question']:  request.url_for("read_item_nobel", **{"item_id":4}),
        nobel[5]['question']:  request.url_for("read_item_nobel", **{"item_id":5}),
        nobel[6]['question']:  request.url_for("read_item_nobel", **{"item_id":6}),
        nobel[7]['question']:  request.url_for("read_item_nobel", **{"item_id":7}),
        nobel[8]['question']:  request.url_for("read_item_nobel", **{"item_id":8}),
        nobel[9]['question']:  request.url_for("read_item_nobel", **{"item_id":9}),
        nobel[10]['question']:  request.url_for("read_item_nobel", **{"item_id":10}),
        nobel[11]['question']:  request.url_for("read_item_nobel", **{"item_id":11}),
        nobel[12]['question']:  request.url_for("read_item_nobel", **{"item_id":12}),
        nobel[13]['question']:  request.url_for("read_item_nobel", **{"item_id":13}),
        nobel[14]['question']:  request.url_for("read_item_nobel", **{"item_id":14}),
        "SELECT WITHIN": "-----------------------------------",
        within[1]['question']:  request.url_for("read_item_select_Oper", **{"item_id":1}),
        within[2]['question']:  request.url_for("read_item_select_Oper", **{"item_id":2}),
        within[3]['question']:  request.url_for("read_item_select_Oper", **{"item_id":3}),
        within[4]['question']:  request.url_for("read_item_select_Oper", **{"item_id":4}),
        within[5]['question']:  request.url_for("read_item_select_Oper", **{"item_id":5}),
        within[6]['question']:  request.url_for("read_item_select_Oper", **{"item_id":6}),
        within[7]['question']:  request.url_for("read_item_select_Oper", **{"item_id":7}),
        within[8]['question']:  request.url_for("read_item_select_Oper", **{"item_id":8}),
        within[9]['question']:  request.url_for("read_item_select_Oper", **{"item_id":9}),
        within[10]['question']:  request.url_for("read_item_select_Oper", **{"item_id":10}),
        "SUM AND COUNT": "-----------------------------------",
        aggregate[1]['question']:  request.url_for("read_item_Sum_And_Count", **{"item_id":1}),
        aggregate[2]['question']:  request.url_for("read_item_Sum_And_Count", **{"item_id":2}),
        aggregate[3]['question']:  request.url_for("read_item_Sum_And_Count", **{"item_id":3}),
        aggregate[4]['question']:  request.url_for("read_item_Sum_And_Count", **{"item_id":4}),
        aggregate[5]['question']:  request.url_for("read_item_Sum_And_Count", **{"item_id":5}),
        aggregate[6]['question']:  request.url_for("read_item_Sum_And_Count", **{"item_id":6}),
        aggregate[7]['question']:  request.url_for("read_item_Sum_And_Count", **{"item_id":7}),
        aggregate[8]['question']:  request.url_for("read_item_Sum_And_Count", **{"item_id":8}),
        "JOINT": "-----------------------------------",
        joint[1]['question']:  request.url_for("read_item_join_Oper", **{"item_id":1}),
        joint[2]['question']:  request.url_for("read_item_join_Oper", **{"item_id":2}),
        joint[3]['question']:  request.url_for("read_item_join_Oper", **{"item_id":3}),
        joint[4]['question']:  request.url_for("read_item_join_Oper", **{"item_id":4}),
        joint[5]['question']:  request.url_for("read_item_join_Oper", **{"item_id":5}),
        joint[6]['question']:  request.url_for("read_item_join_Oper", **{"item_id":6}),
        joint[7]['question']:  request.url_for("read_item_join_Oper", **{"item_id":7}),
        joint[8]['question']:  request.url_for("read_item_join_Oper", **{"item_id":8}),
        joint[9]['question']:  request.url_for("read_item_join_Oper", **{"item_id":9}),
        joint[10]['question']:  request.url_for("read_item_join_Oper", **{"item_id":10}),
        joint[11]['question']:  request.url_for("read_item_join_Oper", **{"item_id":11}),
        joint[12]['question']:  request.url_for("read_item_join_Oper", **{"item_id":12}),
        joint[13]['question']:  request.url_for("read_item_join_Oper", **{"item_id":13})}

    return (response)

    
@app.post("/world/")
async def create_item(World:World):
    sql = f"""
    INSERT INTO `world` (`id`, `name`, `continent`, `area`, `population`, `gdp`, `capital`, `tld`, `flag`)
    VALUES ('{World.id}', '{World.name}', '{World.continent}', '{World.area}', '{World.population}', '{World.gdp}', '{World.capital}','{World.tld}', '{World.flag}')
    """
    res = cnx.query(sql)
    return res

@app.post("/teach/")
async def create_item(Teach:Teach):
    
    # prints go to console for debugging
    print(Teach.id)
    
    # build query using "item" concatenating both lines using += 
    sql =  f"INSERT INTO `teacher` (`id`,`dept`, `phone`,`mobile`) "
    sql += f"VALUES ('{Teach.id}','{Teach.dept}','{Teach.phone}','{Teach.mobile}');"

    # run the query
    res = cnx.query(sql)

    # result has a few entries when it comes back, success is true if everything worked
    # otherwise oops

    # if statement just as example
    # if res['success']:
    #     return res
    # else:
    #     return {'message':'oops'}

    # result has info for a successful query or failed query
    return res