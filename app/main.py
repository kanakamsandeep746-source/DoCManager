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

#Session Storage
if "search_results" not in st.session_state:
    st.session_state.search_results=[]

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
    st.header("Search and View")

    col1,col2=st.columns(2)

    with col1:
        search_by_tag=st.text_input("Search by Tag")

    with col2:
        search_by_date=st.date_input("Search by Date",value=None)

    if st.button("Search"):
        st.session_state.search_results=service.search_documents(
            tag=search_by_tag if search_by_tag else None,
            date=search_by_date if search_by_date else None
        )
    results=st.session_state.search_results


with tabs[2]:
    pass