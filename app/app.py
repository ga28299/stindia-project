import streamlit as st
from utils.db import *
import os


if 'pitch_data' not in st.session_state:
    pitch_data, deal_data, shark_data, industry_data,location_data = load_from_db()
    st.session_state.pitch_data = pitch_data
    st.session_state.deal_data = deal_data
    st.session_state.shark_data = shark_data
    st.session_state.industry_data = industry_data
    st.session_state.location_data = location_data
else:
    pitch_data = st.session_state.pitch_data
    deal_data = st.session_state.deal_data
    shark_data = st.session_state.shark_data
    industry_data = st.session_state.industry_data
    location_data = st.session_state.location_data

current_dir = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(page_title="Streamlit India", 
                   page_icon="🦈", layout="wide")

st.image(os.path.join(current_dir,'assets','sti-image.jpg'), use_column_width=True)
st.title("Welcome to Shark Tank India Insights")


st.sidebar.success("Select a demo above.")

st.write("""
Welcome to the Shark Tank India Insights dashboard! Here you can explore various aspects of the pitches and deals made on the show. 
Navigate through the different sections to find detailed analyses on pitches, deals, sharks, industries, and locations.

## What You Will Find:
- **Overview Dashboard**: High-level summary of key metrics and trends.
- **Detailed Data View**: Access to the entire dataset with filters and export options.
- **Pitches Analysis**: Insights into the pitches, including financial metrics and success factors.
- **Deals Analysis**: Breakdown of the deals made, including investment amounts and conditions.
- **Sharks Analysis**: Analysis of the sharks' investment patterns and preferences.
         
    We hope you find these insights helpful and informative. Dive in and discover the fascinating world of Shark Tank India!
""")