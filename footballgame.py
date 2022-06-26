import random
import pandas as pd
import numpy as np

# create a high school football player generator.  Each player has a unique id, a random skill rating between 1 and 100, and a year in school between 1 and 4.
# the skill rating is a number between 1 and 100.  the higher the skill rating, the better the player.

def generate_player():
    player_id = random.randint(1, 1000000)

    #create a skill rating between 1 and 100 where the average skill rating is 20 and the standard deviation is 30.  The minimum is 0.
    skill_rating = np.random.normal(10, 20, 1)
    skill_rating = int(skill_rating[0])

    #the max skill rating is 100 and the minimum skill rating is 0
    if skill_rating > 100:
        skill_rating = 100
    elif skill_rating < 0:
        skill_rating = 0
        
    year_in_school = 1
    return (player_id, skill_rating, year_in_school)


#each high school player can play until the year they are in school is 5. Once the year = 5 then they are removed from the high school roster.
# only the top 10000 players are kept.
# 50000 players are generated each year
# simulate 100 years of high school football
# store the players in a dataframe

high_school_players = pd.DataFrame(columns=['player_id', 'skill_rating', 'year_in_school'])
college_players = pd.DataFrame(columns=['player_id', 'skill_rating', 'year_in_school'])
nfl_players = pd.DataFrame(columns=['player_id', 'skill_rating', 'year_in_school'])

for year in range(0,1000):
    
    #generate new players into a list
    new_players = []
    for i in range(0,50000):
        new_players.append(generate_player())
    
    #add the new players to a dataframe then concatenate the old dataframe with the new dataframe
    new_high_school_players = pd.DataFrame(new_players, columns=['player_id', 'skill_rating', 'year_in_school'])
    high_school_players = pd.concat([high_school_players, new_high_school_players])
    
    #sort the dataframe by skill rating
    high_school_players = high_school_players.sort_values(by=['skill_rating'], ascending=False)
    high_school_players = high_school_players.head(10000)
    #print the mean of the skill rating for the top 10000 players
    print(high_school_players['skill_rating'].mean())

    #print how many players have a sklll rating of 100
    print('There are ' + str(high_school_players[high_school_players['skill_rating'] == 100].shape[0]) + ' players with a skill rating of 100')
    
    #increment the year in school for each player in the dataframe
    high_school_players['year_in_school'] = high_school_players['year_in_school'] + 1

    #make all 5th year players college players
    college_players = pd.concat([college_players, high_school_players[high_school_players['year_in_school'] == 5]])

    #remove all players from the dataframe who have been in school for 5 years
    high_school_players = high_school_players[high_school_players['year_in_school'] < 5]

    #if there are no players in the college football roster then do nothing
    # otherwise increment all the years in school for the players in the college football roster
    if len(college_players) > 0:
        college_players['year_in_school'] = college_players['year_in_school'] + 1
    
    
    #combine the college eligible players and the college football roster
    # sort the dataframe by skill rating to only keep the top 5000 players
    # if there are no players in the college football roster then do nothing

    college_players = college_players.sort_values(by=['skill_rating'], ascending=False)
    college_players = college_players.head(5000) 

    
    #print the mean of the skill rating for the top 5000 players
    print('college_players', college_players['skill_rating'].mean())


    #print how many college players are in the college football roster
    print('There are ' + str(college_players.shape[0]) + ' players in the college football roster')
    

    #there are 500 nfl player spots
    # get how many open spots are left in the nfl roster
    nfl_player_spots = 500 - college_players.shape[0]

    # if there are no open spots then do nothing
    # otherwise generate new players into a list
    
    #get the top nfl_player_spots players from the college football roster
    #if there are no nfl players then 
    if len(nfl_players) > 0:
        nfl_players = college_players.head(nfl_player_spots)
    else:
        #combine the nfl_players and the top nfl_player_spots players from the college football roster
        nfl_players = pd.concat([nfl_players, college_players.head(nfl_player_spots)])

        #until the highest skill remaining college player is = to the lowest skill remaining nfl player
        #put the highest skill remaining college player in the nfl roster and remove them from the college roster
        while college_players['skill_rating'].max() > nfl_players['skill_rating'].min():
            #get the highest skill remaining college player
            highest_skill_remaining_college_player = college_players[college_players['skill_rating'] == college_players['skill_rating'].max()]
            #get the lowest skill remaining nfl player
            lowest_skill_remaining_nfl_player = nfl_players[nfl_players['skill_rating'] == nfl_players['skill_rating'].min()]
            #put the highest skill remaining college player in the nfl roster and remove them from the college roster
            nfl_players = pd.concat([nfl_players, highest_skill_remaining_college_player])
            college_players = college_players[college_players['skill_rating'] != college_players['skill_rating'].max()]
      

    #remove all the players who have been in school for 8 years
    college_players = college_players[college_players['year_in_school'] < 8]

    #an nfl player can play until they are 18 years
    nfl_players = nfl_players[nfl_players['year_in_school'] < 18]

    #print the mean nfl skill rating
    print('nfl_players', nfl_players['skill_rating'].mean())

    #print how many nfl players have a skill rating of 100
    print('There are ' + str(nfl_players[nfl_players['skill_rating'] == 100].shape[0]) + ' players with a skill rating of 100')

