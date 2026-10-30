import streamlit as st
import os
import sys
from dotenv import load_dotenv

#Path config
BASE_DIR=os.path.abspath(
    os.path.join(os.path.dirname(__file__),"..")
)
sys.path.append(BASE_DIR)

ENV_PATH=os.path.join(BASE_DIR,".env")
loaded = load_dotenv(dotenv_path=ENV_PATH, override=True)
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

#imports
from db.database import init_db
from core.services import DocumentService
from core.analytics import AnalyticsService

#Session Storage
if "selected_doc" not in st.session_state:
    st.session_state.selected_doc = None

if "current_page" not in st.session_state:
    st.session_state.current_page = 0

if "search_results" not in st.session_state:
    st.session_state.search_results=[]

if "reader_mode" not in st.session_state:
    st.session_state.reader_mode=False

if "show_reset" not in st.session_state:
    st.session_state.show_reset = False


#initilazation
init_db()
service=DocumentService()
analytics=AnalyticsService()

#page headers and titles
st.set_page_config(page_title="Doc Manager",layout="wide")
st.title("📄 Smart Document Manager")
st.divider()

#Admin Panel
st.subheader("⚙️ Admin Controls")
if st.button("🧹 Clean Database"):
    st.session_state.show_reset=True

if st.session_state.show_reset:
    password_input=st.text_input("Enter your Password",type="password")

    if st.button("Confirm Reset"):
        if password_input=="abcdefghi":
            import shutil # os

            # Delete DB
            db_file_dir = os.path.join("data", "documents.db")
            if os.path.exists(db_file_dir):
                os.remove(db_file_dir)

            # Delete storage

            pdf_dir = os.path.join("storage", "pdfs")
            thumbnail_dir = os.path.join("storage", "thumbnails")

            shutil.rmtree(pdf_dir, ignore_errors=True)
            shutil.rmtree(thumbnail_dir, ignore_errors=True)

            os.makedirs(pdf_dir, exist_ok=True)
            os.makedirs(thumbnail_dir, exist_ok=True)

            st.success("✅ System reset successfully. Restart app.")
            st.session_state.show_reset = False
            st.rerun()
        else:
            st.error("❌ Incorrect password")
            print(ADMIN_PASSWORD)
            print("error in password")
            st.session_state.show_reset = False
            st.rerun()


#Tabs 
tabs=st.tabs(["Upload","Search & View","Analytics"])

with tabs[0]:
    st.header("PDF UPLOADER")
    uploaded_file=st.file_uploader("Upload PDF File",type=['PDF'])
    tags=st.text_input("Enter tags with comma seperation")
    description=st.text_area("Enter the file description")

    if st.button("Upload",type='primary'):
        analytics.record_app_visit("upload_button")
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
        analytics.record_app_visit("search_button")
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
                        analytics.record_app_visit("doc_open_button")
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
                    analytics.record_app_visit("prev_page")
                    st.session_state.current_page -= 1
                    st.rerun()

            with col2:
                if st.button("Next ➡") and current_page < (Total_Pages)- 1:
                    analytics.record_app_visit("next_page")
                    st.session_state.current_page += 1
                    st.rerun()

            image_path=os.path.join(image_dir,images[st.session_state.current_page])
            st.image(image_path,width="stretch")

            #Anayltics
            analytics.record_page_visit(doc.id,st.session_state.current_page)
            unique_pages=analytics.get_unique_pages_viewed(doc.id)

            progress= (unique_pages/doc.Total_Pages)*100 if doc.Total_Pages else 0

            st.progress(progress/100)
            st.write(f"Progress: {progress:.2f}% ({unique_pages}/{doc.Total_Pages})")
        if st.button("Close Document"):
            analytics.record_app_visit("close_doc_button")
            st.session_state.reader_mode=False
            st.rerun()
        

#Anaylatics
with tabs[2]:
    st.header("Analytics")
    if st.button("Reset Anaylatics"):
        analytics.reset_analytics()
        st.write("Anaytics are reset sucessfully")
    st.subheader("App Usage")
    app_data=analytics.get_app_visits()

    import pandas as pd
    df=pd.DataFrame(app_data,columns=['Events','Count'])

    if df.empty:
        st.info("There is no data to show the Anaylatics please record some data")
    else:
        st.bar_chart(df.set_index("Events"))

    docs=service.get_all_documents()
    data=[]

    for doc in docs:
        unique_pages=analytics.get_unique_pages_viewed(doc.id)
        Total_Pages=doc.Total_Pages
        progress=(unique_pages/Total_Pages)*100 if Total_Pages else 0

        data.append({
            "Document":doc.name,
            "Pages Read":unique_pages,
            "Total Pages":doc.Total_Pages,
            "progress %":round(progress,2)
        })
    df_docs=pd.DataFrame(data)
    st.dataframe(df_docs)
