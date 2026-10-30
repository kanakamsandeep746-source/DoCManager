from db.database import get_connection
from datetime import datetime



class AnalyticsService:
    def __init__(self):
        pass

    def record_page_visit(self,document_id,page_number):
        conn=get_connection()
        cursor=conn.cursor()

        cursor.execute("""
        Insert into page_vists(document_id,page_number,time_stamp)
        values(?,?,?)
        """,(document_id,page_number,datetime.now().isoformat()))

        conn.commit()
        conn.close()

    def get_unique_pages_viewed(self,document_id):
        conn=get_connection()
        cursor=conn.cursor()

        cursor.execute("""
        SELECT COUNT(DISTINCT page_number)
        FROM page_vists
        WHERE document_id = ?
        """, (document_id,))

        result=cursor.fetchone()[0]

        return result if result else 0

    def record_app_visit(self, event_type):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO app_visits (event_type, timestamp)
        VALUES (?, ?)
        """, (event_type, datetime.now().isoformat()))

        conn.commit()
        conn.close()

    def get_app_visits(self):
        conn=get_connection()
        cursor=conn.cursor()

        cursor.execute("""
        Select event_type,count(*)
        from app_visits
        group by event_type
        """)

        data=cursor.fetchall()
        conn.close()

        return data
    def reset_analytics(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM page_vists")
        cursor.execute("DELETE FROM app_visits")

        conn.commit()
        conn.close()
