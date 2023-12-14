from fastapi import FastAPI, HTTPException
from typing import List
from src.models import Event
from src.operations import *
import uvicorn

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to the Event Management API!"}


# list events under a group
@app.get("/api/{group_id}/events")
def list_events(group_id: str):
    return list_events_by_group_id(group_id)

# create an event (under a group?)
@app.post("/api/{group_id}/events")
def create_event(user_id: str, group_id: str, event: Event):
    return add_event(user_id, group_id, event)

# get an event info
@app.get("/api/events/{event_id}")
def read_event(event_id: str):
    event = get_event(event_id)
    if event:
        return event
    raise HTTPException(status_code=404, detail="Event not found")

# update event location, time, capacity, description
@app.put("/api/events/{event_id}/update_location")
def update_event_location(event_id: str, location: str):
	return update_event_location(event_id, location)

@app.put("/api/events/{event_id}/update_time")
def update_event_time(event_id: str, time: str):
	return update_event_time(event_id, time)

@app.put("/api/events/{event_id}/update_capacity")
def update_event_capacity(event_id: str, capacity: int):
	return update_event_capacity(event_id, capacity)

@app.put("/api/events/{event_id}/update_description")
def update_event_description(event_id: str, description: str):
	return update_event_description(event_id, description)

@app.put("/api/events/{event_id}/update_tag2")
def update_event_tag2(event_id: str, tag_2: str):
	return update_event_tag2(event_id, tag_2)

# @app.put("/api/events/{event_id}")
# def update_event_route(event_id: str, event: Event):
#     return update_event(event_id, event)

@app.delete("/api/events/{event_id}")
def delete_event_route(event_id: str):
    return delete_event(event_id)

# Route for getting a group associated with an event (not for eventservice)
# @app.get("/api/events/{event_id}/group")
# def read_event_group(event_id: str):
#     group = get_group(event_id)
#     if group:
#         return group
#     raise HTTPException(status_code=404, detail="Group not found")

# list attendees of an event
@app.get("/api/events/{event_id}/members")
def read_event_members(event_id: str):
    members = list_attendees(event_id)
    if members:
        return members
    raise HTTPException(status_code=404, detail="Members not found")

# add an attendee to an event
@app.post("/api/events/{event_id}/members")
def add_an_event_member(event_id: str, user_id: str):
	return add_event_member(event_id, user_id)

# delete an attendee of an event
@app.delete("/api/events/{event_id}/members")
def delete_an_event_member(event_id: str, user_id: str):
	return delete_event_member(event_id, user_id)

# list all comments of an event
@app.get("/api/events/{event_id}/comments")
def read_event_comments(event_id: str):
    comments = get_comments(event_id)
    if comments:
        return comments
    raise HTTPException(status_code=404, detail="Comments not found")

# add a comment to an event
@app.post("/api/events/{event_id}/comments")
def add_event_comment(event_id: str, user_id: str, comment: str):
    return add_comment(event_id, user_id, comment)
