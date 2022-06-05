# -*- coding: utf-8 -*-
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
import os

# Packages from me
import datetime as dt
import psaw
import praw
import pandas as pd


def obtain_psaw_data(subreddit):
    api = psaw.PushshiftAPI()
    
    start_epoch=int(dt.datetime(2010, 1, 1).timestamp())

    # Call to PSAW - will take a loooong time.
    post_list = list(api.search_submissions(after=start_epoch,
                                            subreddit=subreddit,
                                            filter=['id', 'url','author', 'title', 'subreddit', 'selftext'],
                                            limit=50000))
    
    # Generate DataFrame Columns from those obtained from PRAW
    keys = post_list[0].d_.keys()
    
    parent_df = pd.DataFrame(columns = keys)
    
    for post in post_list:
        parent_df = parent_df.append(post.d_, ignore_index = True)
    
    return parent_df


def obtain_praw_data(psaw):
     client_id = os.environ.get("client_id")
     client_secret = os.environ.get("client_secret")
     user_agent = os.environ.get("user_agent")
     
     # initialize reddit object
     reddit = praw.Reddit(client_id=client_id,
                          client_secret=client_secret,
                          user_agent=user_agent)
     
    # initialize empty record of scores and comments for each post.
     score_comments = []

     ids = psaw['id'].values
    
    # ids need formatting.
     ids2 = [i if i.startswith('t3_') else f't3_{i}' for i in ids]
    
    # reddit.info pulls submission list.
    # then we store info on each submission and convert to a dataframe
     for submission in reddit.info(ids2):
         score_comments.append([submission.id, submission.score, 
                                submission.num_comments])
     score_comments_df = pd.DataFrame(score_comments, columns = ['Submission ID', 'Score', 'Number of Comments'])
     
     return score_comments_df
 
    
def merge_prepare(psaw, praw):
    final_data = psaw.merge(praw, how = 'left', left_on = 'id',
                            right_on = 'Submission ID')
    
    dt_list = []
    for i in final_data['created_utc'].values:
        dt_list.append(dt.datetime.fromtimestamp(i).strftime("%m/%d/%Y, %H:%M:%S"))
    final_data['created_time_converted'] = dt_list
    final_data.drop(['created_utc', 'id', 'created'], inplace = True, axis = 1)
    
    return final_data


def main():
    """ Generates record of Reddit posts for given subreddit.
    Obtains id, url, author, title, subreddit, selftext, upvotes, and comments.
    """
    logger = logging.getLogger(__name__)
    logger.info('Connecting to PSAW.')
    
    selected_subreddit = 'NCSU'
    psaw = obtain_psaw_data(selected_subreddit)
    
    logger.info('Connecting to PRAW.')
    praw = obtain_praw_data(psaw)
    
    logger.info('Merging and preparing final data.')
    final_data = merge_prepare(psaw, praw)
    
    logger.info('Outputting Final Data to csv.')
    final_data.to_csv(r'C:\Users\Mitchell Gaming PC\OneDrive - Visual Risk IQ, LLC\School Files\Personal Projects\college-reddit-topic-modelling\data\processed\NCSU Reddit Posts.csv', index = False)

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())
    


    main()
