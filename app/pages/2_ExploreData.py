import streamlit as st


pitch_data = st.session_state.pitch_data
deal_data = st.session_state.deal_data
shark_data = st.session_state.shark_data
industry_data = st.session_state.industry_data
location_data = st.session_state.location_data


st.title("Detailed Data View")

st.subheader("Pitch Data")
pitch_data_filtered = st.dataframe(pitch_data)

st.subheader("Deal Data")
deal_data_filtered = st.dataframe(deal_data)

st.subheader("Shark Data")
shark_data_filtered = st.dataframe(shark_data)

st.subheader("Industry Data")
industry_data_filtered = st.dataframe(industry_data)

st.subheader("Location Data")
location_data_filtered = st.dataframe(location_data)

st.download_button("Download Pitch Data as CSV", pitch_data.to_csv().encode('utf-8'), "pitch_data.csv")
st.download_button("Download Deal Data as CSV", deal_data.to_csv().encode('utf-8'), "deal_data.csv")
st.download_button("Download Shark Data as CSV", shark_data.to_csv().encode('utf-8'), "shark_data.csv")
st.download_button("Download Industry Data as CSV", industry_data.to_csv().encode('utf-8'), "industry_data.csv")
st.download_button("Download Location Data as CSV", location_data.to_csv().encode('utf-8'), "location_data.csv")