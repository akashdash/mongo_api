from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv()
SQL_URL = os.getenv("SQL_URL")

app = FastAPI()


class Students(BaseModel):
    id: int
    name: str
    age: int


@app.post("/students1")
def create_student1(stud: Students):
    return stud


def save_student_to_file(data):
    with open("students.json", "a") as f:
        f.write(f"{data['id']}: {data['name']}, {data['age']}\n")


@app.post("/students")
def create_students(stud: Students):
    data = stud.dict()
    save_student_to_file(data)
    return {"message": "Student data saved successfully"}


def get_connection_url(SQL_URL):
    conn = psycopg2.connect(SQL_URL, cursor_factory=RealDictCursor)
    return conn


@app.post("/students/db/insert")
def store_student_in_db(student: Students):
    conn = get_connection_url(SQL_URL)
    cursor = conn.cursor()
    insert_query = "INSERT INTO STUDENT (ID, NAME, AGE) VALUES (%s,%s,%s)"
    cursor.execute(insert_query, (student.id, student.name, student.age))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Student data inserted to DB successfully"}


@app.post("/students/db/update")
def update_in_db(stu_id: int, student: Students):
    conn = get_connection_url(SQL_URL)
    cursor = conn.cursor()
    update_query = """
    	UPDATE STUDENT
    	SET name = %s, age=%s
    	WHERE id = %s
    """
    cursor.execute(update_query, (student.name, student.age, stu_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Student updated successfully"}


@app.post("/students/db/delete/{stu_id}")
def delete_in_db(stu_id: int):
    conn = get_connection_url(SQL_URL)
    cursor = conn.cursor()
    delete_query = "DELETE FROM STUDENT WHERE ID = %s"
    cursor.execute(delete_query, (stu_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Student deleted successfully"}
