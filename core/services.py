from datetime import datetime

from core.file_manager import FileManager
from db.repository import DocumentRepository
from core.thumbnail import ThumbNail_Generator
from core.reader import PDFReader
from core.models import Document
class DocumentService:

    def __init__(self):
        self.repo=DocumentRepository()
        self.file_manager=FileManager()
        self.thumNail_generator=ThumbNail_Generator()
        self.pdf_reader=PDFReader()

    def upload_document(self,uploaded_file,tags,description):
        doc=[]

        file_path=self.file_manager.save_file(uploaded_file)
        thumnail_path=self.thumNail_generator.thumbnail_generator(file_path)

        total_pages=self.thumNail_generator.get_total_pages(file_path)
        image_paths=self.pdf_reader.convert_pdf_to_images(file_path)

        upload_date=datetime.now().strftime("%Y-%m-%d")

        doc=Document(
            id=None,
            name=uploaded_file.name,
            Path=file_path,
            thumbnail_path=thumnail_path,
            tags=tags,
            description=description,
            upload_date=datetime.now().strftime("%Y-%m-%d"),
            Total_Pages=total_pages
        )
        self.repo.add_document(doc)
        # self.repo.add_document(doc)

# name,Path,thumbnail_path,tags,description,upload_date,Total_Pages
#Save file
#save thumbnail
#get total pages
#convert to images
#create req variables :upload date
#save to db
#