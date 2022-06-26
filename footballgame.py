import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# create a high school football player generator.  Each player has a unique id, a random skill rating between 1 and 100, and a year in school between 1 and 4.
# the skill rating is a number between 1 and 100.  the higher the skill rating, the better the player.

def generate_player():
    player_id = random.randint(1, 1000000)

    # create a skill rating between 1 and 100 where the average skill rating is 20 and the standard deviation is 30.  The minimum is 0.
    skill_rating = np.random.normal(10, 20, 1)
    skill_rating = int(skill_rating[0])

    # the max skill rating is 100 and the minimum skill rating is 0
    if skill_rating > 100:
        skill_rating = 100
    elif skill_rating < 0:
        skill_rating = 0

    year_in_school = 1
    return (player_id, skill_rating, year_in_school)


# create constants for 100 years, 5000 high school players, 700 college players, and 60 nfl players
NUM_YEARS = 100
NUM_HIGH_SCHOOL_PLAYERS = 5000
NUM_COLLEGE_PLAYERS = 700
NUM_NFL_PLAYERS = 60


# each high school player can play until the year they are in school is 5. Once the year = 5 then they are removed from the high school roster.
# only the top 10000 players are kept.
# 50000 players are generated each year
# simulate 100 years of high school football
# store the players in a dataframe

high_school_players = pd.DataFrame(
    columns=['player_id', 'skill_rating', 'year_in_school'])
college_players = pd.DataFrame(
    columns=['player_id', 'skill_rating', 'year_in_school'])
nfl_players = pd.DataFrame(
    columns=['player_id', 'skill_rating', 'year_in_school'])

# store the average skill rating of high school, college, and nfl players in a dataframe for each year.  the year is the index
average_skill_rating = pd.DataFrame(
    columns=['high_school', 'college', 'nfl'], index=range(0, 100))

# store the minimum skill rating of high school, college, and nfl players in a dataframe for each year.  the year is the index
minimum_skill_rating = pd.DataFrame(
    columns=['high_school', 'college', 'nfl'], index=range(0, 100))

for year in range(0, NUM_YEARS):

    # generate new players into a list
    new_players = []
    for i in range(0, NUM_HIGH_SCHOOL_PLAYERS):
        new_players.append(generate_player())

    # add the new players to a dataframe then concatenate the old dataframe with the new dataframe
    new_high_school_players = pd.DataFrame(
        new_players, columns=['player_id', 'skill_rating', 'year_in_school'])
    high_school_players = pd.concat(
        [high_school_players, new_high_school_players])

    # sort the dataframe by skill rating
    high_school_players = high_school_players.sort_values(
        by=['skill_rating'], ascending=False)
    high_school_players = high_school_players.head(NUM_HIGH_SCHOOL_PLAYERS)

    # make all 4th year players college players
    college_players = pd.concat(
        [college_players, high_school_players[high_school_players['year_in_school'] == 4]])

    # combine the college eligible players and the college football roster
    # sort the dataframe by skill rating to only keep the top 5000 players
    # if there are no players in the college football roster then do nothing

    college_players = college_players.sort_values(
        by=['skill_rating'], ascending=False)
    college_players = college_players.head(5000)

    # there are 500 nfl player spots
    # get how many open spots are left in the nfl roster
    nfl_player_spots = NUM_NFL_PLAYERS - college_players.shape[0]

    # get the top nfl_player_spots players from the college football roster
    # if there are no nfl players then
    if len(nfl_players) > 0:
        nfl_players = college_players.head(nfl_player_spots)
    else:
        # combine the nfl_players and the top nfl_player_spots players from the college football roster
        nfl_players = pd.concat(
            [nfl_players, college_players.head(nfl_player_spots)])

        # until the highest skill remaining college player is = to the lowest skill remaining nfl player
        # put the highest skill remaining college player in the nfl roster and remove them from the college roster
        while college_players['skill_rating'].max() > nfl_players['skill_rating'].min():
            # get the highest skill remaining college player
            highest_skill_remaining_college_player = college_players[
                college_players['skill_rating'] == college_players['skill_rating'].max()]
            # get the lowest skill remaining nfl player
            lowest_skill_remaining_nfl_player = nfl_players[nfl_players['skill_rating'] == nfl_players['skill_rating'].min(
            )]
            # put the highest skill remaining college player in the nfl roster and remove them from the college roster
            nfl_players = pd.concat(
                [nfl_players, highest_skill_remaining_college_player])
            college_players = college_players[college_players['skill_rating']
                                              != college_players['skill_rating'].max()]

    # increment years for high school, college, and nfl players
    high_school_players['year_in_school'] = high_school_players['year_in_school'] + 1
    college_players['year_in_school'] = college_players['year_in_school'] + 1
    nfl_players['year_in_school'] = nfl_players['year_in_school'] + 1

    # remove all the high school players who have been in school for 5 years
    # remove all the college players who have been in school for 9 years
    # remove all the nfl players who have been in school for 18 years
    high_school_players = high_school_players[high_school_players['year_in_school'] < 5]
    college_players = college_players[college_players['year_in_school'] < 9]
    nfl_players = nfl_players[nfl_players['year_in_school'] < 18]

    # add the year to the average skill rating dataframe
    average_skill_rating.loc[year] = [high_school_players['skill_rating'].mean(
    ), college_players['skill_rating'].mean(), nfl_players['skill_rating'].mean()]
    minimum_skill_rating.loc[year] = [high_school_players['skill_rating'].min(
    ), college_players['skill_rating'].min(), nfl_players['skill_rating'].min()]

# show a plot with the average skill rating for each year
# label the x axis with the year and y axis with the average skill rating
plt.plot(average_skill_rating.index,
         average_skill_rating['high_school'], label='high school')
plt.plot(average_skill_rating.index,
         average_skill_rating['college'], label='college')
plt.plot(average_skill_rating.index, average_skill_rating['nfl'], label='nfl')

# plot the min skill ratings for each year
plt.plot(minimum_skill_rating.index,
         minimum_skill_rating['high_school'], label='min high school')
plt.plot(minimum_skill_rating.index,
         minimum_skill_rating['college'], label='min college')
plt.plot(minimum_skill_rating.index,
         minimum_skill_rating['nfl'], label='min nfl')


# label the x axis with the year and y axis with the average skill rating
plt.xlabel('year')
plt.ylabel('average skill rating')
# title the plot "Difference in skill level through high school, college, and nfl"
plt.title('Difference in skill level through high school, college, and nfl')

plt.legend()
plt.show()
