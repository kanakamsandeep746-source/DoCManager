import os
import pymupdf

class PDFReader:

    def __init__(self):
        pass

    def convert_pdf_to_images(self,file_path):
        doc=pymupdf.open(file_path)
        folder_name=os.path.basename(file_path).replace(".pdf","")
        output_dir=os.path.join("storage","pdfs",folder_name)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        image_paths=[]

        for i in range(len(doc)):
            page=doc.load_page(i)
            matrix=pymupdf.Matrix(2,2)
            pix=page.get_pixmap(matrix=matrix)
            image_path=os.path.join(output_dir,f"page{i}.png")
            print(output_dir)
            print(image_path)
            pix.save(image_path)
            image_paths.append(image_path)
        doc.close()

        return image_paths