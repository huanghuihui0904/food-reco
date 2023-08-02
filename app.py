import streamlit as st
from recommender import get_recommendation

st.write('Hello Food!')

number = st.number_input('Number to show', min_value=1, value=5, step=1)
if st.button('Show where to eat'):
    st.write(f"Showing {number} place to eat!")
    st.dataframe(get_recommendation(int(number)))