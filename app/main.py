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
if "selected_doc" not in st.session_state:
    st.session_state.selected_doc = None

if "current_page" not in st.session_state:
    st.session_state.current_page = 0

if "search_results" not in st.session_state:
    st.session_state.search_results=[]

if "reader_mode" not in st.session_state:
    st.session_state.reader_mode=False


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
            date=str(search_by_date) if search_by_date else None
        )
    results=st.session_state.search_results

    if results and not st.session_state.reader_mode:
        st.subheader(f"Results :{len(results)} documents")
        container=st.container(height=500)

        with container:
            for doc in results:
                col1,col2=st.columns([1,3])

                with col1:
                    if doc.thumbnail_path:
                        st.image(doc.thumbnail_path,width=120)
                with col2:
                    st.write(f"**{doc.name}**")
                    st.write(f"Tags: {doc.tags}")
                    st.write(f"Description: {doc.description}")
                    #st.write(f"Lecture Date: {doc.lecture_date}")

                    if st.button("open",key=f"open_{doc.id}"):
                        st.session_state.selected_doc=doc
                        st.session_state.selected_doc = doc
                        st.session_state.current_page = 0
                        st.session_state.reader_mode = True
                        st.rerun()
    if st.session_state.reader_mode and st.session_state.selected_doc:
        st.write("Reader Mode Activated")

        doc=st.session_state.selected_doc

        st.subheader(f"📖 Reading: {doc.name}")

        folder_name=os.path.basename(doc.Path).replace(".pdf","")
        image_dir=f"storage/pdfs/{folder_name}"

        st.write("Image dir:", image_dir)
        st.write("Files:", os.listdir(image_dir) if os.path.exists(image_dir) else "NOT FOUND")

        if not os.path.exists(image_dir):
            st.error("Images not found Pdf conversion error")
        else:
            images = sorted(os.listdir(image_dir))
            Total_Pages=doc.Total_Pages
            current_page=st.session_state.current_page
            col1,col2,col3=st.columns([1,2,1])

            with col1:
                if st.button("⬅ Previous") and current_page > 0:
                    #analytics.record_app_visit("prev_page")
                    st.session_state.current_page -= 1
                    st.rerun()

            with col2:
                if st.button("Next ➡") and current_page < (Total_Pages)- 1:
                    #analytics.record_app_visit("next_page")
                    st.session_state.current_page += 1
                    st.rerun()

            image_path=os.path.join(image_dir,images[st.session_state.current_page])
            st.image(image_path,width="stretch")
        




with tabs[2]:
    pass