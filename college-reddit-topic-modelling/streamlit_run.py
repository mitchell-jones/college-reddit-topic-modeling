# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 15:08:08 2022

@author: Mitchell Gaming PC
"""
import streamlit as st
import os
import pandas as pd

st.title('Using BERTopic for Topic Exporation of Student Discussion on Colleges in the State of North Carolina')

master_path = os.getcwd()

selected_college = st.selectbox('Select a college for analysis',
                                ['NCSU', 'UNCC', 'UNC', 'Duke'])

if selected_college == 'NCSU':
    path = master_path + r'\data\processed\NCSU Reddit Posts.csv'
    df = pd.read_csv(path)
    
if selected_college == 'UNCC':
    path = master_path + r'\data\processed\UNCC Reddit Posts.csv'
    df = pd.read_csv(path)
    

st.write(df)
