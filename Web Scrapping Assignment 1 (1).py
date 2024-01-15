#!/usr/bin/env python
# coding: utf-8

# Assignment 1 Web Scrapping

# In[8]:


get_ipython().system(' pip install bs4')
get_ipython().system(' pip install requests')


# 1) Write a python program to display all the header tags from wikipedia.org and make data frame.

# In[9]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
url = 'https://en.wikipedia.org/wiki/Main_Page'
response = requests.get(url)
html_content = response.text
soup = BeautifulSoup(html_content, 'html.parser')
header_tags = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
header_texts = [tag.get_text() for tag in header_tags]
df = pd.DataFrame({'Headers': header_texts})
print(df)


# 2)Write s python program to display list of respected former presidents of India(i.e. Name , Term ofoffice)
# from https://presidentofindia.nic.in/former-presidents.htm and make data frame

# In[10]:


import requests
from bs4 import BeautifulSoup
import pandas as pd


url = "https://presidentofindia.nic.in/former-presidents.htm" 


response = requests.get(url)


if response.status_code == 200:
  
    soup = BeautifulSoup(response.text, 'html.parser')

    
    table = soup.find('table')

  
    presidents_data = []
    for row in table.find_all('tr')[1:]:  
        columns = row.find_all('td')
        name = columns[0].text.strip()
        term_of_office = columns[1].text.strip()
        presidents_data.append([name, term_of_office])

   
    df = pd.DataFrame(presidents_data, columns=['Name', 'Term of Office'])

   
    print(df)

else:
    print("Failed to retrieve data from the website. Please check the URL.")


# 3)Write a python program to scrape cricket rankings from icc-cricket.com. You have to scrape and make data framea) Top 10 ODI teams in men’s cricket along with the records for matches, points and rating.
# b) Top 10 ODI Batsmen along with the records of their team andrating.
# c) Top 10 ODI bowlers along with the records of their team andrating.

# In[11]:


import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_icc_rankings(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
  
    teams_data = []
    for team in soup.find_all('tr', class_='table-body'):
        rank = team.find('td', class_='rankings-block__position').text.strip()
        name = team.find('td', class_='rankings-block__team').text.strip()
        matches = team.find('td', class_='rankings-block__banner--matches').text.strip()
        points = team.find('td', class_='rankings-block__banner--points').text.strip()
        rating = team.find('td', class_='rankings-block__banner--rating').text.strip()
        teams_data.append([rank, name, matches, points, rating])

   
    players_data = []
    for player in soup.find_all('tr', class_='table-body'):
        name = player.find('td', class_='table-body__cell name').a.text.strip()
        team = player.find('td', class_='table-body__cell nationality-logo').text.strip()
        rating = player.find('td', class_='table-body__cell u-text-right rating').text.strip()
        players_data.append([name, team, rating])

    return teams_data, players_data


men_teams_url = 'https://www.icc-cricket.com/rankings/mens/team-rankings/odi'


men_batsmen_url = 'https://www.icc-cricket.com/rankings/mens/player-rankings/odi/batting'


men_bowlers_url = 'https://www.icc-cricket.com/rankings/mens/player-rankings/odi/bowling'


men_teams_data, men_batsmen_data = scrape_icc_rankings(men_teams_url)
_, men_bowlers_data = scrape_icc_rankings(men_bowlers_url)


men_teams_df = pd.DataFrame(men_teams_data, columns=['Rank', 'Team', 'Matches', 'Points', 'Rating'])
men_batsmen_df = pd.DataFrame(men_batsmen_data, columns=['Player', 'Team', 'Rating'])
men_bowlers_df = pd.DataFrame(men_bowlers_data, columns=['Player', 'Team', 'Rating'])


print("Top 10 ODI Teams:")
print(men_teams_df.head(10))

print("\nTop 10 ODI Batsmen:")
print(men_batsmen_df.head(10))

print("\nTop 10 ODI Bowlers:")
print(men_bowlers_df.head(10))


# 4) Write a python program to scrape cricket rankings from icc-cricket.com. You have to scrape and make data framea) Top 10 ODI teams in women’s cricket along with the records for matches, points and rating.
# b) Top 10 women’s ODI Batting players along with the records of their team and rating.
# c) Top 10 women’s ODI all-rounder along with the records of their team and rating.

# In[5]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape and create data frame for team rankings
def scrape_team_rankings(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    teams_data = []
    for team in soup.select('.table rankings-table tbody tr'):
        name = team.select_one('.team-names a').text.strip()
        matches = team.select_one('.matches').text.strip()
        points = team.select_one('.points').text.strip()
        rating = team.select_one('.rating').text.strip()

        teams_data.append({'Team': name, 'Matches': matches, 'Points': points, 'Rating': rating})

    return pd.DataFrame(teams_data)

# Function to scrape and create data frame for batting and all-rounder rankings
def scrape_player_rankings(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    players_data = []
    for player in soup.select('.table rankings-table tbody tr'):
        name = player.select_one('.player-name').text.strip()
        team = player.select_one('.table-body__logo-text').text.strip()
        rating = player.select_one('.rating').text.strip()

        players_data.append({'Player': name, 'Team': team, 'Rating': rating})

    return pd.DataFrame(players_data)

# URLs for team rankings, batting rankings, and all-rounder rankings
team_rankings_url = 'https://www.icc-cricket.com/rankings/team-rankings/women/odi'
batting_rankings_url = 'https://www.icc-cricket.com/rankings/womens/player-rankings/odi/batting'
all_rounder_rankings_url = 'https://www.icc-cricket.com/rankings/womens/player-rankings/odi/all-rounder'

# Scrape and display the data frames
team_df = scrape_team_rankings(team_rankings_url)
batting_df = scrape_player_rankings(batting_rankings_url)
all_rounder_df = scrape_player_rankings(all_rounder_rankings_url)

# Displaying the results
print("Top 10 ODI teams in women’s cricket:")
print(team_df.head(10))

print("\nTop 10 women’s ODI Batting players:")
print(batting_df.head(10))

print("\nTop 10 women’s ODI all-rounder:")
print(all_rounder_df.head(10))


# 5)Write a python program to scrape mentioned news details from https://www.cnbc.com/world/?region=world and
# make data frame
#  i) Headline
# ii) Time
# iii) News Link

# In[1]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.cnbc.com/world/?region=world"


response = requests.get(url)


if response.status_code == 200:
   
    soup = BeautifulSoup(response.text, 'html.parser')

   
    headlines = [headline.text.strip() for headline in soup.find_all('h3', class_='Card-title')]
    times = [time.text.strip() for time in soup.find_all('time', class_='Card-time')]
    news_links = [link['href'] for link in soup.find_all('a', class_='Card-title-link')]

    
    df = pd.DataFrame({
        'Headline': headlines,
        'Time': times,
        'News Link': news_links
    })

    
    print(df)

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")


# 6) Write a python program to scrape the details of most downloaded articles from AI in last 90
# days.https://www.journals.elsevier.com/artificial-intelligence/most-downloaded-articles
# Scrape below mentioned details and make data frame
# i) Paper Title
# ii) Authors
# iii) Published Date
# iv) Paper URL
# 

# In[2]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.journals.elsevier.com/artificial-intelligence/most-downloaded-articles"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    paper_titles = []
    authors_list = []
    published_dates = []
    paper_urls = []

    for article in soup.find_all('li', class_='js-article-item'):
        title = article.find('a', class_='highwire-cite-linked-title').text.strip()
        authors = article.find('span', class_='highwire-citation-authors').text.strip()
        date = article.find('span', class_='highwire-cite-metadata-date').text.strip()
        url = article.find('a', class_='highwire-cite-linked-title')['href']

        paper_titles.append(title)
        authors_list.append(authors)
        published_dates.append(date)
        paper_urls.append(url)

    data = {
        'Paper Title': paper_titles,
        'Authors': authors_list,
        'Published Date': published_dates,
        'Paper URL': paper_urls
    }

    df = pd.DataFrame(data)
    print(df)
else:
    print("Failed to retrieve the webpage.")


# 7) Write a python program to scrape mentioned details from dineout.co.inand make data framei) Restaurant name
# ii) Cuisine
# iii) Location
# iv) Ratings
# v) Image URL

# In[4]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.dineout.co.in/"


response = requests.get(url)


if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    
    restaurant_names = [name.text for name in soup.select('.restaurant-name')]
    cuisines = [cuisine.text for cuisine in soup.select('.cuisines')]
    locations = [location.text for location in soup.select('.location')]
    ratings = [rating.text for rating in soup.select('.rating')]
    image_urls = [img['src'] for img in soup.select('.restaurant-thumbnail img')]

   
    data = {
        'Restaurant Name': restaurant_names,
        'Cuisine': cuisines,
        'Location': locations,
        'Ratings': ratings,
        'Image URL': image_urls
    }

    df = pd.DataFrame(data)


    print(df)

else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

