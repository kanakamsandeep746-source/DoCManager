import streamlit as st
import os
import sys

#Path config
BASE_DIR=os.path.abspath(
    os.path.join(os.path.dirname(__file__),"..")
)
sys.path.append(BASE_DIR)

#imports
from db.database import init_db
from core.services import DocumentService

#initilazation
init_db()
service=DocumentService()

#page headers and titles
st.set_page_config(page_title="Doc Manager",layout="wide")
st.title("📄 Smart Document Manager")
st.divider()

#Tabs 
tabs=st.tabs(["Upload","Search & View","Analytics"])

with tabs[0]:
    st.header("PDF UPLOADER")
    uploaded_file=st.file_uploader("Upload PDF File",type=['PDF'])
    tags=st.text_input("Enter tags with comma seperation")
    description=st.text_area("Enter the file description")

    if st.button("Upload",type='primary'):
        if uploaded_file:
            service.upload_document(uploaded_file,tags,description)
        else:
            st.error("Please upload the file")

with tabs[1]:
    st.write("This is search and view page")


with tabs[2]:
    pass