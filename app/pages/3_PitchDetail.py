import streamlit as st
import folium
from streamlit_folium import st_folium
from unidecode import unidecode
import json
import os 


curr_path=os.path.dirname(os.path.abspath(__file__))

def normalize_name(name):
    name = unidecode(name) 
    name = name.replace(' and ', ' & ')  
    return name

def season_industry_filters(df):
    seasons = st.sidebar.multiselect("Select Seasons", [1, 2, 3], [1, 2, 3])
    
    industry_filter = st.sidebar.multiselect("Select Industry", df['industry_name'].unique(), df['industry_name'].unique())
    
    return seasons, industry_filter

def state_map(df,year,industry_filter):

    df = df[df['season_id'].isin(year)]
    df = df[df['industry_name'].isin(industry_filter)]

    m = folium.Map(location=[22,84], zoom_start=4,tiles='CartoDB positron')

    geojson=os.path.join(curr_path,'../data/india_geo.geojson')
    with open(geojson, encoding='utf-8') as f:
        india_states = json.load(f)

    for feature in india_states['features']:
        feature['properties']['shapeName'] = normalize_name(feature['properties']['shapeName'])

    state_pitches = df.groupby('state')['pitch_id'].count().reset_index()


    choropleth=folium.Choropleth(
        geo_data=india_states,
        data=state_pitches,
        columns=('state','pitch_id'),
        key_on='feature.properties.shapeName',
        fill_opacity=0.3,
        line_weight=2,
    )
    choropleth.geojson.add_to(m)

    for feature in choropleth.geojson.data['features']:
        state_name=feature['properties']['shapeName']
        #state pitches will taken from pitch id for corren=sponding state in the daataframe else ''
        feature['properties']['state_pitch']='Number of Pitches: '+str(state_pitches[state_pitches['state']==state_name]['pitch_id'].values[0]) if state_name in state_pitches['state'].values else ''


    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['shapeName','state_pitch'], labels=False)
    )

    st_map = st_folium(m, width=700, height=500)

    state_name = ""
    if st_map['last_active_drawing']:
        state_name = st_map['last_active_drawing']['properties']['shapeName']

    return state_name

def state_filter(df,state_name):
    state_list = [''] + list(df['state'].unique())
    state_list.sort()
    state_index = state_list.index(state_name) if state_name and state_name in state_list else 0
    return st.sidebar.selectbox('State', state_list, state_index)

def total_filter(df,seasons,industry_filter,state):
    if state:
        filtered_data=df[(df['state']==state) & (df['season_id'].isin(seasons)) & (df['industry_name'].isin(industry_filter))]
    else:
        filtered_data=df[(df['season_id'].isin(seasons)) & (df['industry_name'].isin(industry_filter))]
    return filtered_data
    

pitch_data = st.session_state.pitch_data
industry_data = st.session_state.industry_data
location_data = st.session_state.location_data

pitch_data = pitch_data.merge(industry_data, on='industry_id')
pitch_data = pitch_data.merge(location_data, on='location_id')

pitch_data.drop(columns=['industry_id', 'location_id'], inplace=True)

seasons, industry_filter = season_industry_filters(pitch_data)
state_name=state_map(pitch_data,seasons,industry_filter)
state=state_filter(pitch_data,state_name)
filtered_data=total_filter(pitch_data,seasons,industry_filter,state)

st.subheader("Ask Amount Distribution")
st.bar_chart(filtered_data['ask_amount'])

st.subheader("Equity asked in")
st.bar_chart(filtered_data['equity_asked'])

st.subheader("Yearly Revenue Distribution")
st.bar_chart(filtered_data['yearly_revenue'])

st.subheader("Monthly Revenue Distribution")
st.bar_chart(filtered_data['monthly_revenue'])

# st.subheader("Scatter Plot of Yearly Revenue vs. Equity Asked")
# st.scatter(pitch_data['yearly_revenue'], pitch_data['equity_asked'])

# st.subheader("Pie Chart of Bootstrap Status")
# st.pie_chart(filtered_pitches['bootstrapped'].value_counts())