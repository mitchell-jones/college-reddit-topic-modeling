# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 15:08:08 2022

@author: Mitchell Gaming PC
"""
import streamlit as st
import pandas as pd
from src.data.bert_tests import remove_punc_stopwords, lemma_sentence, get_topic_model

selected_college = st.sidebar.selectbox('Select a college for analysis',
                                ['NCSU', 'UNCC', 'UNC', 'Duke'])
#selected_college = 'UNCC'

if selected_college == 'NCSU':
    df = pd.read_csv(r'https://raw.githubusercontent.com/mitchell-jones/college-reddit-topic-modeling/main/data/processed/NCSU%20Reddit%20Posts.csv')
if selected_college == 'UNCC':
    df = pd.read_csv(r'https://raw.githubusercontent.com/mitchell-jones/college-reddit-topic-modeling/main/data/processed/UNCC%20Reddit%20Posts.csv')
    

df_1 = remove_punc_stopwords(df, 'title', 'title_cleaned')
df_1['title_cleaned_lemmatized'] = df_1['title_cleaned'].apply(lemma_sentence)
title_list = list(df_1['title_cleaned_lemmatized'])

topic_model, topics = get_topic_model(title_list)

plot = topic_model.visualize_barchart(n_words = 10)
plot.update_layout(
    title={
        'text': 'Extracted topics for {}'.format(selected_college), 
        'font':dict(family="Arial",size=18, color ='white')})

timestamps = list(df_1['created_time_converted'])

@st.cache(allow_output_mutation=True)
def plot_topics_overtime(selected_college):
    topics_over_time = topic_model.topics_over_time(title_list, topics[0], timestamps, nr_bins=15)
    plot2 = topic_model.visualize_topics_over_time(topics_over_time, top_n_topics=8)
    return plot2

plot2 = plot_topics_overtime(selected_college)
plot2.update_layout(
    title={
        'text': 'Topics over time for {}'.format(selected_college), 
        'font':dict(family="Arial",size=18, color ='white')})

df_1['topic'] = topics[0]
    
def main_page():
    st.markdown("# Main page: Analysis of Discussion on NC-College Subreddits")
    st.markdown('## Selected College: {}'.format(selected_college))
    st.markdown("""
             This website was created by @mitchell-jones on GitHub. \n
             While looking around for a good package for dynamic topic modeling, 
             I stumbled onto BERTopic - a new topic modeling package that incorporates 
             BERT into it's pipeline and allows for easy visualization of topic prevalence.
             So, I decided to apply it to college subreddits in NC, to allow students to visualize
             the most popular points of discussion in their communities. \n
             
             Overall, this codebase includes scripts to 
             """)

    st.plotly_chart(plot, use_container_width=True)
    st.plotly_chart(plot2, use_container_width = True)
    
    st.write('The posts used, and their assigned topics. Head to the "Exploratory Visuals" page for more analysis on this.')
    topic_selected = st.selectbox("Select a topic to filter to posts. Select -1 to see posts which the algorithm couldn't determine a topic for.", ['All']+list((range(-1,8))))
    if topic_selected != 'All':
        st.write(df_1[['author', 'topic', 'title', 'selftext']][df_1['topic'] == topic_selected], use_container_width = True)
    else:
        st.write(df_1[['author', 'topic', 'title', 'selftext']], use_container_width = True)

def page2():
    st.markdown("# Exploring other aspects of the Subreddits through visualization.")
    st.markdown('## Selected College: {}'.format(selected_college))

def page3():
    st.markdown("# Page 3")

page_names_to_funcs = {
    "Topic Analysis": main_page,
    "Exploratory Visuals": page2,
    "Page 3": page3,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
