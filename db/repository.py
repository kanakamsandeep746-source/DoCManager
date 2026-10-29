from db.database import get_connection
from core.models import Document 
class DocumentRepository:
    def __init__(self):
        pass

    def add_document(self,doc:Document):

        conn=get_connection()
        cursor=conn.cursor()

        cursor.execute("""
        INSERT INTO documents(
            name,Path,thumbnail_path,tags,description,upload_date,Total_Pages
        )
        VALUES(?,?,?,?,?,?,?)
        """,(doc.name,
            doc.Path,
            doc.thumbnail_path,
            doc.tags,
            doc.description,
            doc.upload_date,
            doc.Total_Pages ))

        conn.commit()
        conn.close()
    def search_documents(self,tag=None,date=None):
        conn=get_connection()
        cursor=conn.cursor()
        query="Select * from documents"
        conditons=[]
        params=[]

        if tag:
            conditons.append("tags like ?")
            params.append(f"%{tag}%")

        if date:
            conditons.append("upload_date ?")
            params.append(date)

        if conditons:
            final_query=query+" Where " + "or".join(conditons)
        

        cursor.execute(final_query,params)

        rows=cursor.fetchall()

        conn.close()

        return [Document(*row) for row in rows]
    