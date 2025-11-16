from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Students(BaseModel):
    id: int
    name: str
    age: int


def save_data_to_file(data):
    with open("student.txt", "a") as f:
        f.write(f"{data.id}, {data.name},{data.age}\n")


@app.post("/students")
def create_student(stud: Students):
    data = stud.dict()
    save_data_to_file(data)
    return {"message": "Student data saved"}
