import streamlit as st
from recommender import get_recommendation

st.write('Hello Food!')
st.dataframe(get_recommendation(3))