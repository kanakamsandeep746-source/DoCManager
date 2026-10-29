from datetime import datetime
import os
class FileManager:

    def __init__(self):
        pass

    def save_file(self,uploaded_file):
            upload_date = datetime.now().strftime("%Y-%m-%d")
            file_name=f"{upload_date}_{uploaded_file.name}"
            file_path=os.path.join("storage","pdfs")
            file_path=os.path.join(file_path,file_name)
        
            with open(file_path,"wb") as f:
                f.write(uploaded_file.read())
            return  file_path