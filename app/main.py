import streamlit as st
import os
import sys

BASE_DIR=os.path.abspath(
    os.path.join(os.path.dirname(__file__),"..")
)
sys.path.append(BASE_DIR)

from db.database import init_db
init_db()


st.set_page_config(page_title="Doc Manager",layout="wide")

st.title("📄 Smart Document Manager")
st.divider()

tabs=st.tabs(["Upload","Search & View","Analytics"])

with tabs[0]:
    st.write("This is upload page")
with tabs[1]:
    st.write("This is search and view page")
with tabs[2]:
    pass