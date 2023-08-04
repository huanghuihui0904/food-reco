import streamlit as st
from recommender import get_recommendation

st.write('Hello Food!')

col1, col2, col3 = st.columns(3)
with col1:
    number = st.number_input('Number to show', min_value=1, value=5, step=1)
    new_place = st.checkbox('New places only')

if st.button('Show places to eat!'):
    st.write(f"Showing {number} places to eat in :flag-sg:!")
    st.dataframe(get_recommendation(int(number), new_place=new_place).reset_index(drop=True))