from typing import Annotated

from fastapi import FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from DB.config import conn

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8000/",
    "http://127.0.0.1:8000/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


# Home Page
@app.route("/", methods=["GET", "POST", "PUT"])
async def Home(request: Request):
    try:
        dict_format = []
        query = 'SELECT * FROM todo'
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()

        for i in data:
            dict_format.append(
                {"id": i[0], "title": i[len(i) - 1]})
        cursor.close()
    except Exception as e:
        print(f'Error : {e}')
    finally:
        return templates.TemplateResponse("Home.html", {"request": request, "todos": dict_format})


# Create Todo API
@app.post("/create")
async def create_todo(title: Annotated[str, Form()], request: Request):
    try:
        query = 'INSERT INTO todo (id, title) VALUES (%s,%s)'
        cursor = conn.cursor()
        data = (None, title)
        cursor.execute(query, data)
        conn.commit()
        cursor.close()
        return RedirectResponse(url=request.url_for("Home"))
    except Exception as e:
        print(f'Error : {e}')


# Update Todo API
@app.post("/update/{id}")
async def update_one(id: int, new_title: Annotated[str, Form()], request: Request):
    try:
        # Perform the UPDATE query
        update_query = 'UPDATE todo SET title = %s WHERE id = %s'
        data = (new_title, id)
        cursor = conn.cursor()
        cursor.execute(update_query, data)
        conn.commit()
        # Check the number of affected rows
        return RedirectResponse(url=request.url_for("Home"))

    except Exception as e:
        print(f'Error: {e}')


# Delete Todo API
@app.post("/delete/{id}")
async def delete_one(id: int, request: Request):
    try:
        query = f'DELETE FROM todo WHERE id = {id}'
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        return RedirectResponse(url=request.url_for("Home"))

    except Exception as e:
        print(f'Error : {e}')

# # Get One Todo API
# @app.get("/todos/{id}")
# async def get_one(id: int):
#     try:
#         query = f'SELECT * FROM todo WHERE id = {id}'
#         cursor.execute(query)
#         data = cursor.fetchone()
#         if data:
#             todo_dict = {
#                 "id": data[0],
#                 "title": data[len(data) - 1]
#             }
#             return todo_dict
#         else:
#             raise HTTPException(status_code=404, detail=f"No data found for ID: {id}")
#     except Exception as e:
#         print(f'Error : {e}')
#
