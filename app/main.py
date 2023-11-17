from fastapi import FastAPI, HTTPException
from typing import List
from src.models import Event, Group, Member, Comment
from src.operations import (add_event, update_event, delete_event, get_events, get_event,
                            get_group, get_members, get_comments, add_comment)
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Route for listing or creating events
@app.get("/api/events")
async def list_events(limit: int = 10, skip: int = 0):
    return await get_events(limit, skip)

@app.post("/api/events")
async def create_event(event: Event):
    return await add_event(event)

# Route for getting, updating, or deleting a specific event
@app.get("/api/events/{event_id}")
async def read_event(event_id: int):
    event = await get_event(event_id)
    if event:
        return event
    raise HTTPException(status_code=404, detail="Event not found")

@app.put("/api/events/{event_id}")
async def update_event_route(event_id: int, event: Event):
    return await update_event(event_id, event)

@app.delete("/api/events/{event_id}")
async def delete_event_route(event_id: int):
    return await delete_event(event_id)

# Route for getting a group associated with an event
@app.get("/api/events/{event_id}/group")
async def read_event_group(event_id: int):
    group = await get_group(event_id)
    if group:
        return group
    raise HTTPException(status_code=404, detail="Group not found")

# Route for getting members associated with an event
@app.get("/api/events/{event_id}/members")
async def read_event_members(event_id: int):
    members = await get_members(event_id)
    if members:
        return members
    raise HTTPException(status_code=404, detail="Members not found")

# Route for getting or adding comments for an event
@app.get("/api/events/{event_id}/comments")
async def read_event_comments(event_id: int):
    comments = await get_comments(event_id)
    if comments:
        return comments
    raise HTTPException(status_code=404, detail="Comments not found")

@app.post("/api/events/{event_id}/comments")
async def add_event_comment(event_id: int, comment: Comment):
    return await add_comment(event_id, comment)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8011)
