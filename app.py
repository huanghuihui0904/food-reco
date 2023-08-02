import streamlit as st
from recommender import get_recommendation

st.write('Hello Food!')

number = st.number_input('Number to show')
if st.button('Show where to eat'):
    st.dataframe(get_recommendation(number))