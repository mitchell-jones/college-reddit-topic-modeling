# -*- coding: utf-8 -*-
"""
Created on Mon May 23 16:23:42 2022

@author: Mitchell Gaming PC
"""
#%%
from bertopic import BERTopic
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# --Hidden Dependencies--
# import nltk
# nltk.download('omw-1.4')
# nltk.download('wordnet')

#%% Loading Data
df = pd.read_csv(r'C:\Users\Mitchell Gaming PC\OneDrive - Visual Risk IQ, LLC\School Files\Personal Projects\college-reddit-topic-modelling\data\processed\NCSU Reddit Posts.csv')

#%% Removing Punctuation and Stopwords

df['fulltext'] = df['title'] + ' ' + df['selftext']

stop = stopwords.words('english')
removal_pattern = r'\b(?:{})\b'.format('|'.join(stop))

def remove_punc_stopwords(data, column, final_name):
    temp_data = data.copy()
    
    temp_data[final_name] = temp_data[column].str.replace('/', ' ')
    temp_data[final_name] = temp_data[final_name].str.replace('-', ' ')
    
    temp_data = temp_data.assign(temp=temp_data[final_name].str.replace(r'[^\w\s]+', ''))

    temp_data[final_name] = temp_data['temp'].str.replace(removal_pattern, '')
    temp_data[final_name] = temp_data[final_name].str.replace(r'\s+', ' ').str.lower()
    
    temp_data.drop('temp', inplace = True, axis = 1)
    
    return temp_data

df_1 = remove_punc_stopwords(df, 'title', 'title_cleaned')

#%% Lemmatizing Sentences
lemmy = WordNetLemmatizer()

def lemma_sentence(sentence):
    return " ".join([lemmy.lemmatize(word) for word in word_tokenize(sentence)])

df_1['title_cleaned_lemmatized'] = df_1['title_cleaned'].apply(lemma_sentence)

title_list = list(df_1['title_cleaned_lemmatized'])

#%% Fitting Topic Model (Takes a long time)
topic_model = BERTopic(calculate_probabilities=False)
topics =topic_model.fit_transform(title_list)

#%% Plotting Topic Model Results
import plotly.io as pio
pio.renderers.default='browser'
plot = topic_model.visualize_barchart(n_words = 10)
plot.show()

#%%
import pickle
filename = 'nscu topics'
outfile = open(filename,'wb')
pickle.dump(topic_model,outfile)
outfile.close()


