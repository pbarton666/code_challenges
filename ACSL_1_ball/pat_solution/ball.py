"""
Solution to ACSL_1_ball_game using pandas, primarily.
"""

import sys
import os
import pandas as pd
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

PLAYERS_PER_TEAM = 4

os.chdir(os.path.dirname(__file__))
def main(fn='sample_input.txt'):
    #Ingest the data into a pandas DataFrame for easy processing
    df = pd.read_csv(fn, names=('player', 'ones', 'twos', 'threes'))

    #Most three-pointers
    three_ptrs = df['threes'].sum()

    #Highest total goals, both teams
    df['total_goals'] = df.loc[:,['ones', 'twos', 'threes' ]].sum(axis=1)
    player_most_goals = df.iloc[df['total_goals'].argmax(), 0]

    #Highest total score, both teams
    df['total_points'] = df['ones'] + df['twos'] * 2 + df['threes'] * 3
    player_high_score =  df.iloc[df['total_points'].argmax(), 0]

    #Highest score, winning team
    jets = slice(0, PLAYERS_PER_TEAM - 1)
    sharks = slice(PLAYERS_PER_TEAM , 2 * PLAYERS_PER_TEAM + 1)
    jets_score = df.loc[jets, 'total_points'].sum()
    sharks_score = df.loc[sharks, 'total_points'].sum()
    if jets_score >= sharks_score:
        losers = df.loc[sharks,:]
        winning_score = jets_score
    else:
        losers = df.loc[jets, :]
        winning_score = sharks_score
    
    #Second highest scoring player, losing team
    loser_2hi = losers.sort_values(by='total_points', ascending=False).iloc[1,:]['player']

    #Report results
    logger.debug(f"\n{df.to_string()}")

    for val in (three_ptrs, player_most_goals, player_high_score,
                winning_score, loser_2hi):
        logger.debug(val)

if __name__=='__main__':
    logger.debug("Sample")
    main('sample_input.txt')
    logger.debug("\nTest")
    main('test_input.txt')