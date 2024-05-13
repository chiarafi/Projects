"""
"""
"""
Group A1

Our Objectives:
    Scrape the Premier League Football Table and capture the following data:
        Teams; for each team, capture:
        Rank
        Matches Played
        Matches Won
        Matches Lost
        Top Scorer  ------------------------------------------------------------------ in PART 2 of the document
        Total Goals Scored in Previous 5 Matches
        Total Opposing Goals in Previous 5 Matches
        Number of Matches that ended in a Draw
        Current Points
        Information regarding the most previous match played: Opponent, Result, Date
        Next Opponent of the current gameweek ----------------------------------------- in Part 3 of the document


Introduction

As a betting and odds making company, our aim is to use the following code to scrape and process
data from the Premier League and use it for more precise odds calculation. By doing so, we can
obtain deeper insights into team performances, player trends, and historical match outcomes. 
This approach will not only enable us to offer a broader range of betting options, including
player-specific and match-specific bets, but also enhance our in-play betting. In addition to this,
with predictive analytics we will be able to offer more informed predictions for future matches, 
enriching our pre-match betting offerings. Additionally, this will also help us establish an appropriate
risk management strategy, helping us identify potential high-risk bets and patterns, thereby 
safeguarding our financial interests.

"""


# import needed libraries and modules
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# URL of the webpage to be scraped
url = "https://www.bbc.com/sport/football/tables"
url2 = "https://www.bbc.com/sport/football/premier-league/top-scorers"
url3 = "https://www.bbc.com/sport/football/premier-league/scores-fixtures"

# Sending a request to the website
response = requests.get(url)

# Using BeautifulSoup to parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Attempt to find the table
table = soup.find('table')

# Check if the table was found
if table:
    # Extracting the rows
    rows = table.find_all('tr')

    # Parsing each row for data
    teams_data = [] # Prepare list for storing the data which will be used to create a dataframe later
    for row in rows:
        cols = row.find_all('td') # Finding all the table data (<td>) tags
        if cols and len(cols) >= 10:  # Ensure there are enough columns
            try:
                # Extracting team name, rank, wins, draws, losses, points, total goals scored in previous 5 matches, total opposing goals from previous 5 matches, and infos regarding the last match played by this team
                team_info = {
                    'Rank': cols[0].text.strip(),
                    'Team': cols[2].text,
                    'Played': cols[3].text.strip(),
                    'Wins': cols[4].text.strip(),
                    'Draws': cols[5].text.strip(),
                    'Losses': cols[6].text.strip(),
                    'Points': cols[10].text.strip(),
                    'Top Scorer(s)': np.nan, # temporary filler NaN values
                    'Last match': cols[11].text.strip(), # this column captures opponent, result, and date of the previous 5 games of each team all in one string; We will split this string later to handle its information more easily
                    'Total Goals Scored in Previous 5 Matches': np.nan, # temporary filler NaN values
                    'Total Opposing Goals in Previous 5 Matches': np.nan, # temporary filler NaN values
                    'Most Previous Result': np.nan, # temporary filler NaN values
                    'Most Previous Opponent': np.nan, # temporary filler NaN values
                    'Date of Most Previous Match': np.nan # temporary filler NaN values
                }
                
                # Append the scraped data to the list teams_data
                teams_data.append(team_info)
            # In case the row could not be processed, let the user know
            except IndexError:
                print("Error processing a row, skipping...")
                continue 

    # Creating a pandas dataframe
    df = pd.DataFrame(teams_data)

    # Iterate through the rows of the dataframe df in order to execute the following operations for each team
    for i in df.index: 
        count = -6 # Counter variable for the upcoming while loop to flexibly capture the name of the latest opponent for each team, regardless of the number of words their names include; reading the column 'Last match' from the back, the name of the latest opponent always start at position 5, so we use the value of this counter variable to read additional parts of the teamname in case it consists of more than one word
        numbers = [] # Prepared array for all the parts of 'Last match' that are part of the results of the matches
        no_numbers = [] # Prepared array for all the parts of 'Last match' that are not part of the results of the matches
        team_info_split = (df.iloc[i]['Last match']).split() # Splits the info regarding opponent, result, and date of the previous 5 games of each team into an array of strings; this helps to extract specific information seperately
        for s in team_info_split: # Iterate through the array
            # Seperate the strings into strings containing digits (match results) and non-digits (no match results); this helps to extract specific information seperately
            if s.isdigit():
                numbers.append(int(s))
            else:
                no_numbers.append(s)
        
        # Append total goals scored in previous 5 matches, total opposing goals from previous 5 matches, the most previous result and match date for each team to the dataframe df
        df.at[i, 'Most Previous Result'] = str(numbers[-2]) + ' - ' + str(numbers[-1]) # The results of the latest match are located in the last two positions of the numbers-array
        df.at[i, 'Date of Most Previous Match'] = no_numbers[-3] + ' ' + no_numbers[-2] + ' ' + no_numbers[-1] # The date of the latest match are located in the last three positions of the no_numbers-array
        df.at[i, 'Total Goals Scored in Previous 5 Matches'] =  numbers[0] + numbers[2] + numbers[4] + numbers[6] + numbers[8] # Total goals scored in the previous 5 matches is the sum of every second value in numbers-array, starting from the first element
        df.at[i, 'Total Opposing Goals in Previous 5 Matches'] =  numbers[1] + numbers[3] + numbers[5] + numbers[7] + numbers[9]  # Total opposing goals in the previous 5 matches is the sum of every second value in numbers-array, starting from the second element
        
        # Using a while-loop, capture the full name of the most previous opponent for each team and append this information to the dataframe df
        opponent = no_numbers[-5] # Capture the name of the latest opponent as it is located at the 5th last position of the no_numbers-array
        while(no_numbers[count] != 'against'): # Reading no_numbers from the back, if the word before no_numbers[-5] is not 'against', it means that the opponent's team name consists of more than one word, so we need to capture them
            opponent = no_numbers[count] + ' ' + opponent # Because we read the array from the behind, append the newly captured part of the opponent's team name in the front of the parts of the opponent's team name we captured to far
            count -= 1 # Decrease count variable in order to capture the word located before the word we just read in no_numbers-array (because we read the no_numbers-array from behind)
        df.at[i, 'Most Previous Opponent'] = opponent # Append the latest opponent's team name to the dataframe df
        
    # as total goals and total opposing goals are represented as floats, we convert them to integers
    df['Total Goals Scored in Previous 5 Matches'] = df['Total Goals Scored in Previous 5 Matches'].astype(int)
    df['Total Opposing Goals in Previous 5 Matches'] = df['Total Opposing Goals in Previous 5 Matches'].astype(int)
    
    # Because we subtracted the information we were interested in from the column 'Last match' and added it to the dataframe seperately, we can delete this column
    df = df.drop(columns = ['Last match'])
        
    
# In case the table was not found, let the user know
else:
    print("Table not found on the page.")
    
    
    
    
    
    
    
   

"""
PART 2

  Now, we want to scrape the only missing information: Top Scorers (different url), and integrate them into our dataframe df.
  When scraping the data from this table, we realized that the table seems to be implemented in an unorganized way.
  There are many inconsistencies compared to the first table we scraped as well as inconsistencies within the table itself. For example, when the first table was saying
  'Man City', the new table we now want to scrape from is saying 'Manchester City', which makes integarting the Top Scorers
  from the new table into our dataframe df difficult. We still wanted to try, but consequently we needed to do some small manual changes 
  to enable a solid representation and organization of the data.
  
  Therefore, this part can be seen as a part in which we got creative in solving this problem.
  Our code also works without this part. 

"""  
    


# Now, we will use the second url in order to grasp the top scorers for each team (if one of the Top 24 Table of the webiste belongs to that team)
# Sending a request to the website
response_new = requests.get(url2)

# Using BeautifulSoup to parse the HTML content
soup_new = BeautifulSoup(response_new.content, 'html.parser')

# Attempt to find the table
table_new = soup_new.find('table')

# Check if the table was found
if table_new:
    # Extracting the rows
    rows_new = table_new.find_all('tr')

    # Parsing each row for data
    players_data = [] # Prepare list for storing the data which will be used to create a dataframe later
    for row in rows_new:
        cols = row.find_all('td') # Finding all the table data (<td>) tags
        if cols:  
            try:
                # Extracting Name of the Player and Team of that Player
                players_info = {
                    'Best Player': cols[1].text.strip()
                }
                
                # Append the scraped data to the list players_data
                players_data.append(players_info)
                
                # Create df2, our second dataframe. This dataframe will hold the information regarding the top scorers and their team, before we will integrate that data into our original dataframe df in the end
                df2 = pd.DataFrame(players_data)
                
                # First, we need to further edit our data stored in df2, as it looks very messy now
                # Iterate through the rows of df2
                for i in df2.index:
                    # We will put a blankspace between each word. We identify the beginning of a new word checking whether the letter is in uppercase (indicates new word) or lowercase
                    cell_value = df2.iloc[i]['Best Player']
                    cell_length = len(cell_value)
                    positions = [] # Positions will hold the indexes, where new words begin
                    # Identify indexes, where a new word starts
                    for j in range(0,cell_length):
                        if cell_value[j].isupper():
                            positions.append(j)
                    # Put a blankspace between them
                    for j in positions:
                        cell_value = cell_value[:j] + ' ' + cell_value[j:]
                        for x in range(len(positions)):
                            positions[x] += 1 # In case we insert a blankspace, we increase the values of positions-array by 1 so that we adapt the positions of where new words begin to the increased length of the overall string
                    # Replace the string with the more organized string we just created
                    df2.iloc[i]['Best Player'] = cell_value
                    
                # Now, we will separate the strings, each containing Top Scorer and his team, into a list of arrays to separate the words from each other; This helps to further organize the information
                for i in df2.index:        
                    players_info_split = (df2.iloc[i]['Best Player']).split()
                    df2.iloc[i]['Best Player'] = players_info_split
                    
                # Now, let's answer the question: What is the index the team in dataframe df for each top scorer in dataframe df2?
                indexes = [] # for each Top Scorer, this array will hold the index of his team in dataframe df; this prepares the integration of the Top Scorers into dataframe df
                for i in df2.index:
                    counter = 0 # This is our counter which we use as an index to iterate through the teams of dataframe df
                    stop = False 
                    cell_value = df2.iloc[i]['Best Player'] # String in row i, containing top scorer of row i and his team 
                    while stop == False: # While-Loop that stops once the correct index of the team in dataframe df is found for top scorer in row i of dataframe df2
                        intersection = set(cell_value) & set(df.iloc[counter]['Team'].split()) # 
                        if intersection: # Check, if the string stored in cell_value contains the team name stored at index 'counter' in dataframe df
                            if ('Man' in intersection) or ('Utd' in intersection): # Exception: Because more than one team names contain the word 'Man' and 'Utd', in the cases that one of these words are included in the intersection, we check whether the intersection contains more than one word (Yes means that top scorer belongs to the team of dataframe df, No means we have to go to the next row of dataframe df to search for the correct team)
                                if len(intersection) > 1:
                                    indexes.append(counter)
                                    stop = True
                                else:
                                    counter += 1
                            else:
                                indexes.append(counter)
                                stop = True
                        else:
                            counter += 1
                
                # Next, since we now know to which team and row in dataframe df every top scorer belongs to, we want to capture the names of the top scorer. Although they are included in dataframe df2, they are still mixed with the team names. Therefore, we now want to delete all the strings / characters, that don't belong to a player's name
                remove = [] # we want to store all strings / characters, that don't belong to player's names, in this array
                for i in df.index:
                    # Here, the inconsistencies of the tables from the website make it more complicated (eg sometimes it's Man City, sometimes Manchester City, ...). To cover all strings / characters that should be removed, we include the team names of the 'Team' column in dataframe df and the team names of the 'Most Previous Opponent' column in the dataframe df to cover all different spellings of the team names
                    remove.append(df.iloc[i]['Team'])
                    remove.append(df.iloc[i]['Most Previous Opponent'])
                    
                separated_remove = [] # We once again split the strings stores in array 'remove' into a list of strings because it's easier to work with in this context
                for phrase in remove:
                    separated_remove.extend(phrase.split())
                    
                separated_remove = separated_remove + ['A'] + ['F'] + ['C'] + ['Chelsea,'] # these are the expressions that were not captured in the remove-array before, but need to be removed from the 'Best Players' column in dataframe df2 in order to solely capture the names of the top scorers
               
                # Let's remove everything that is not a name from the column in dataframe df2
                for i in df2.index:
                    for j in remove:
                        df2.iloc[i]['Best Player'] = set(df2.iloc[i]['Best Player']) - set(separated_remove)
                    df2.iloc[i]['Best Player'] = list(df2.iloc[i]['Best Player']) # change set back to list so that we can transform the list of strings now to one string, containing the -Name,Surname- of the top scorer
                    df2.iloc[i]['Best Player'] = " ".join(df2.iloc[i]['Best Player']) 
                    
                # Another inconsistency of the scraped information regarding the top players: some of the names are -Surname, Name- while other are -Name, Surname-, we will correct this so that all player's names are organized like -Name, Surname-
                wrong_order = [0, 4, 6, 8, 10, 12, 16, 17, 18] # these are the indexes of the players's names we need to chang
                for i in df2.index:
                    if i in wrong_order:
                        s = df2.iloc[i]['Best Player'].split()[::-1]
                        l = [] # this array contains the string in correct order
                        for x in s:
                            l.append(x)
                        df2.iloc[i]['Best Player'] = " ".join(l) # transform the array of strings back to a string again and use it to overwrite the name of wrong order in the dataframe df2
                
                        
            # In case the row could not be processed, let the user know
            except IndexError:
                print("Error processing a row, skipping...")
                continue
# In case the table was not found, let the user know
else:
    print("Table not found on the page.")
 
# In case both tables were found on the webpage, integrate the top scorers from dataframe df2 into the main dataframe df         
if table and table_new:
    # Integrate the top scorers into dataframe df
    for i in df2.index:
        index = indexes[i] # Holds the index of where top scorer in row i of column 'Best Player' in dataframe df2 belongs in dataframe df
        # Some teams have multiple top scorers. For this, check if a top scorer already got integrated, and if yes, add the other top scorer after adding a space
        if pd.isna(df.at[index, 'Top Scorer(s)']): 
            df.at[index, 'Top Scorer(s)'] = df2.at[i,'Best Player']
        else:
            df.at[index, 'Top Scorer(s)'] = df.at[index, 'Top Scorer(s)'] + ", " + df2.at[i,'Best Player']












"""
PART 3

 Adding the next opponents for each team

"""  


if table:
    # Function to get the next opponents for each team
    def get_next_opponents(url):
        # Send a GET request to the URL
        response = requests.get(url)
        if response.status_code != 200:
            return "Failed to retrieve data"
    
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
    
        # Find the section containing the fixtures
        fixtures_section = soup.find_all('div', class_='qa-match-block')
        next_opponents = {}
    
        # Parse the fixtures to extract team names and match details
        for fixture in fixtures_section:
            matches = fixture.find_all('div', class_='sp-c-fixture__wrapper')
            for match in matches:
                teams = match.find_all('span', class_='sp-c-fixture__team-name-trunc')
                if teams:
                    home_team = teams[0].get_text(strip=True)
                    away_team = teams[1].get_text(strip=True)
                    # Update the next opponents dictionary
                    next_opponents[home_team] = away_team
                    next_opponents[away_team] = home_team
        return next_opponents
    team_name_map = {
        'Manchester United': ['Man United', 'Man Utd', 'MUFC'],
        'Manchester City': ['Man City', 'MCFC'],
        'Sheffield United': ['Sheff Utd', 'sheff utd'],
        'Nottingham Forest': ['Nottm Forest']
    }
    
    def modify_string(s):
        if s == 'Man Utd':
            return 'Manchester United'
        elif s == 'Man City':
            return 'Manchester City'
        elif s == 'Sheff Utd':
            return 'Sheffield United'
        elif s == 'Wolves':
            return 'Wolverhampton Wanderers'
        elif s == 'Nottm Forest':
            return 'Nottingham Forest'
        else:
            return s
    
    # Apply the function to the 'Team' column
    df['Team'] = df['Team'].apply(modify_string)
    # URL for the Premier League fixtures
    url = "https://www.bbc.com/sport/football/premier-league/scores-fixtures"
    
    # Get the next opponents
    next_opponents = get_next_opponents(url)
    
    # Convert the dictionary to a list of tuples
    opponents_list = [(team, opponent) for team, opponent in next_opponents.items()]
    
    # Create a DataFrame from the list
    dataframe3 = pd.DataFrame(opponents_list, columns=['Team', 'Next Opponent'])
    
    # 4 Display the DataFrame
    # Step 1: Create a flexible matching function
    def get_next_opponent(team, opponents_dict):
        for key in opponents_dict.keys():
            if team in key or key in team:
                return opponents_dict[key]
        return 'No Match'  # Return this if no match is found
    
    # Create a dictionary from dataframe3 for easy lookup
    next_opponents_dict = dict(zip(dataframe3['Team'], dataframe3['Next Opponent']))
    
    # Step 2: Apply the matching function
    df['Next Opponent'] = df['Team'].apply(lambda x: get_next_opponent(x, next_opponents_dict))

    
    # Printing and saving as CSV file

    if table_new: 
        print("Information regarding the Top 20 Football Teams of Premier League:")
        print()
        print(df)
        print()
    
        # Save the DataFrame to a CSV file and inform the user about the success of the execution 
        df.to_csv('football_table.csv', index=False)
        print("Data saved to 'football_table.csv'")

    elif table:
    
        print("Information regarding the Top 20 Football Teams of Premier League (without Top Scorers):")
        print()
        print(df)
        print()

        # Save the DataFrame to a CSV file and inform the user about the success of the execution 
        df.to_csv('football_table.csv', index=False)
        print("Data (without top scorers) saved to 'football_table.csv'")
 
else: print("Table was not found")


"""

Conclusion

We successfully implemented the code and scraped the Premier League data. It has significantly 
enhanced the company’s odds calculation capabilities, allowing them to offer more precise and 
varied betting options to its customers. The results allowed the company the possibility to use 
predictive analytics not only to improve its pre-match betting strategies but also provided valuable 
content for customer engagement and marketing efforts. It would also make it possible to share 
insightful analysis and predictions with customers, which can increase customer interaction and 
satisfaction. Overall, the incorporation of this data scraping and processing tool can significantly 
make the company’s betting and odds making services more accurate, engaging, and secure.

"""



