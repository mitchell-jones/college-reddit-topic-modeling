# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 15:08:08 2022

@author: Mitchell Gaming PC
"""
import streamlit as st
import os
import pandas as pd

st.title('Using BERTopic for Topic Exporation of Student Discussion on Colleges in the State of North Carolina')
df = pd.read_csv('https://raw.githubusercontent.com/mitchell-jones/college-reddit-topic-modeling/main/college-reddit-topic-modelling/data/processed/NCSU%20Reddit%20Posts.csv')

st.write(df)
