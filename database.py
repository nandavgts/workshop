from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient

from bson import ObjectId

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["demo"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/todos")
async def list_todos():
	data = await db.demo.find().to_list(100)
	for todo in data:
		todo["id"] = str(todo["_id"])
		del todo["_id"]
	return data

@app.post("/create-todo")
async def create_todo(data: dict):
	inserted_data = await db.demo.insert_one({
		"todo": data["todo"],
		"completed": False,
		"deleted": False,
		"createdAt": datetime.now(),
		"updatedAt": datetime.now(),
		"deletedAt": None
	})
	data = await db.demo.find_one({"_id": inserted_data.inserted_id})
	data["id"] = str(data["_id"])
	del data["_id"]
	return data

@app.get("/todo/{id}")
async def get_todo(id: str):
	if data := await db.demo.find_one({"_id": ObjectId(id)}):
		data["id"] = str(data["_id"])
		del data["_id"]
		return data
	raise HTTPException(status_code=400, detail="Todo not found!")

@app.put("/update-todo/{id}")
async def update_todo(id: str, request_data: dict):
	if await db.demo.find_one({"_id": ObjectId(id)}):
		request_data["updatedAt"] = datetime.now()

		if "deleted" in request_data and request_data["deleted"]:
			request_data["deletedAt"] = datetime.now()

		await db.demo.update_one({"_id": ObjectId(id)}, {"$set": request_data})
		data = await db.demo.find_one({"_id": ObjectId(id)})
		data["id"] = str(data["_id"])
		del data["_id"]
		return data

	raise HTTPException(status_code=400, detail="Todo not found!")


@app.delete("/delete-todo/{id}")
async def delete_todo(id: str):
	if data := await db.demo.delete_one({"_id": ObjectId(id)}):
		if data.deleted_count > 0:
			return {"message": "Todo deleted successfully"}
	raise HTTPException(status_code=400, detail="Todo not found!")
