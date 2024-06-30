import streamlit as st

st.markdown('# Overviews')
seasons = st.sidebar.multiselect("Select Seasons", [1, 2, 3], [1, 2, 3])

pitch_data = st.session_state.pitch_data
deal_data = st.session_state.deal_data
shark_data = st.session_state.shark_data
industry_data = st.session_state.industry_data
location_data = st.session_state.location_data

filtered_pitch_data = pitch_data[pitch_data['season_id'].isin(seasons)]
filtered_deal_data = deal_data[deal_data['pitch_id'].isin(filtered_pitch_data['pitch_id'])]

num_pitches = len(filtered_pitch_data)

num_deals = len(filtered_deal_data.groupby('pitch_id'))

total_deal_amount = filtered_deal_data['amount_invested'].sum()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Number of Pitches", num_pitches)
with col2:
    st.metric("Number of Deals", num_deals)
with col3:
    st.metric("Total Deal Amount", f"₹{total_deal_amount/100:,.2f} Cr")

# Industry Distribution Chart
industry_counts = filtered_pitch_data.merge(industry_data, on='industry_id')['industry_name'].value_counts()
st.subheader("Industry Distribution")
st.bar_chart(industry_counts)

# Sharks Involved in Deals
sharks_in_deals = filtered_deal_data.merge(shark_data, on='shark_id')['shark_name'].value_counts()
st.subheader("Sharks Involved in Deals")
st.bar_chart(sharks_in_deals)