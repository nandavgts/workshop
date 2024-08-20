from datetime import datetime

from fastapi import FastAPI, HTTPException

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

global todos
global todo_increament_id

todo_increament_id = 1

todos = [
	{
		"id": 1,
		"todo": "Have my brushed my teeth?",

		"completed": False,
		"deleted": False,
		
		"createdAt": "2024-08-18 22:47:14.484846",
		"updatedAt": "2024-08-18 22:47:14.484846",
		"deletedAt": None
	}
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/todos")
def list_todos():
	return todos

@app.post("/create-todo")
def create_todo(data: dict):
	global todo_increament_id
	data = {
		"id": todo_increament_id + 1,
		"todo": data["todo"],
		"completed": False,
		"deleted": False,
		"createdAt": datetime.now(),
		"updatedAt": datetime.now(),
		"deletedAt": None
	}
	todos.append(data)
	todo_increament_id += 1
	return data

@app.get("/todo/{id}")
def get_todo(id: int):
	todo_data = None
	for data in todos:
		if data["id"] == id:
			todo_data = data
	if not todo_data:
		raise HTTPException(status_code=400, detail="Todo not found!")
	return todo_data

@app.put("/update-todo/{id}")
def update_todo(id: int, request_data: dict):
	todo_data = None
	todo_index = None
	for index, data in enumerate(todos):
		if data["id"] == id:
			todo_data = data
			todo_index = index
	if todo_data is None:
		raise HTTPException(status_code=400, detail="Todo not found!")
	
	todo_data["todo"] = request_data["todo"] if "todo" in request_data else todo_data["todo"]
	todo_data["completed"] = request_data["completed"] if "completed" in request_data else todo_data["completed"]
	todo_data["updatedAt"] = datetime.now()

	if "deleted" in request_data:
		todo_data["deleted"] = request_data["deleted"]
		if request_data["deleted"]:
			todo_data["deletedAt"] = datetime.now()

	todos[todo_index] = todo_data
	return todo_data


@app.delete("/delete-todo/{id}")
def delete_todo(id: int):
	todo_index = None
	for index, data in enumerate(todos):
		if data["id"] == id:
			todo_index = index
	if todo_index is None:
		raise HTTPException(status_code=400, detail="Todo not found!")
	
	todos.pop(todo_index)
	return {"message": "Todo deleted successfully"}
