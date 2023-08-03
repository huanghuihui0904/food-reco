import streamlit as st
from recommender import get_recommendation

st.write('Hello Food!')

col1, col2, col3 = st.columns(3)
with col1:
    number = st.number_input('Number to show', min_value=1, value=5, step=1)

if st.button('Show where to eat')
    st.write(f"Showing {number} places to eat in :flag-sg:!")
    st.dataframe(get_recommendation(int(number)).reset_index(drop=True))