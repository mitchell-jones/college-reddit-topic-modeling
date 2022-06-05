# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 15:08:08 2022

@author: Mitchell Gaming PC
"""
import streamlit as st
import pandas as pd
from src.data.bert_tests import remove_punc_stopwords, lemma_sentence, get_topic_model
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

st.title('Using BERTopic for Topic Exporation of Student Discussion on Colleges in the State of North Carolina')

selected_college = st.selectbox('Select a college for analysis',
                                ['NCSU', 'UNCC', 'UNC', 'Duke'])

if selected_college == 'NCSU':
    df = pd.read_csv(r'https://raw.githubusercontent.com/mitchell-jones/college-reddit-topic-modeling/main/data/processed/NCSU%20Reddit%20Posts.csv')
if selected_college == 'UNCC':
    df = pd.read_csv(r'https://raw.githubusercontent.com/mitchell-jones/college-reddit-topic-modeling/main/data/processed/UNCC%20Reddit%20Posts.csv')

df_1 = remove_punc_stopwords(df, 'title', 'title_cleaned')
df_1['title_cleaned_lemmatized'] = df_1['title_cleaned'].apply(lemma_sentence)
title_list = list(df_1['title_cleaned_lemmatized'])

topic_model, topics = get_topic_model(title_list)

plot = topic_model.visualize_barchart(n_words = 10)

st.plotly_chart(plot)
