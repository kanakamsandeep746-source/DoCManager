import os
import pymupdf
THUMBNAIL_DIR=os.path.join("storage","thumbnails")

class ThumbNail_Generator:
    def __init__(self):
        pass

    def thumbnail_generator(self,file_path):
        doc=pymupdf.open(file_path)
        page=doc.load_page(0)
        pix=page.get_pixmap()

        base_name=os.path.basename(file_path).replace(".pdf",'.png')
        thumbNail_path=os.path.join(THUMBNAIL_DIR,base_name)
        pix.save(thumbNail_path)
        doc.close()

        return thumbNail_path
    def get_total_pages(self,file_path):
        doc=pymupdf.open(file_path)
        count=len(doc)
        doc.close()
        return count
