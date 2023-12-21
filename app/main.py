from fastapi import FastAPI, HTTPException, Request, Response
from typing import List
from time import time
from src.models import Event
import json
from src.operations import *
import uvicorn
import re
from datetime import datetime
from starlette.concurrency import iterate_in_threadpool

app = FastAPI()
log_table = dynamodb.Table('EventsLog')



from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"], # Allows all origins
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

@app.middleware("http")
async def log_updates_middleware(request: Request, call_next):
	response = await call_next(request)
 
	create_path_pattern = re.compile(r"^/api/\w+/events$")
	update_operations_paths = [
		"/update_name",
		"/update_duration",
		"/update_location",
		"/update_time",
		"/update_capacity",
		"/update_status",
		"/update_description",
		"/update_tag2"
	]
 
	if request.method == "POST" and create_path_pattern.match(request.url.path):
		response_body = [chunk async for chunk in response.body_iterator]
		response.body_iterator = iterate_in_threadpool(iter(response_body))
		body_data = json.loads(response_body[0].decode())
		event_id = body_data.get('event_id')

		# try:
		details = generate_create_log_details(body_data)
		# except json.JSONDecodeError:
		# 	details = body_data.get('message')

		# Log data to DynamoDB
		log_item = {
			'log_id': str(uuid.uuid4()),
			'timestamp': datetime.now().isoformat(),
			'event_id': event_id,
			'action': f"{request.method} {request.url}",
			'details': details,
			'user_id': 'test_user_id'
		}
		log_table.put_item(Item=log_item)
  
	
	elif request.method in ["PUT", "POST"] and any(path in request.url.path for path in update_operations_paths):
		response_body = [chunk async for chunk in response.body_iterator]
		response.body_iterator = iterate_in_threadpool(iter(response_body))
		body_data = json.loads(response_body[0].decode())
		event_id = body_data.get('event_id')

		# try:
		details = generate_log_details(body_data)
		# except json.JSONDecodeError:
		# 	details = body_data.get('message')

		# Log data to DynamoDB
		log_item = {
			'log_id': str(uuid.uuid4()),
			'timestamp': datetime.now().isoformat(),
			'event_id': event_id,
			'action': f"{request.method} {request.url}",
			'details': details,
			'user_id': 'test_user_id'
		}
		log_table.put_item(Item=log_item)

	# print(dict(response.headers))
		
	return response

@app.get("/")
async def root():
	return {'event_service_status': 'ONLINE'}

# ===== For Logs =====

# show all logs
@app.get("/api/events/logs")
async def list_all_logs(limit: int = 10, skip: int = 0):
	return list_logs(limit, skip)

# show logs of a specific event
@app.get("/api/events/{event_id}/logs")
async def list_event_logs(event_id: str, limit: int = 10, skip: int = 0):
	return get_event_log_by_event_id(event_id, limit, skip)

# list events under a group
@app.get("/api/{group_id}/events")
async def list_events(group_id: str):
	return list_events_by_group_id(group_id)

# create an event (under a group?)
@app.post("/api/{group_id}/events")
async def create_event(user_id: str, group_id: str, event: Event):
	return add_event(user_id, group_id, event)

# list some events
@app.get("/api/events")
async def read_events(limit: int = 10, skip: int = 0):
	return get_events(limit, skip)

# get an event info
@app.get("/api/events/{event_id}")
async def read_event(event_id: str):
	event = get_event(event_id)
	if event:
		return event
	raise HTTPException(status_code=404, detail="Event not found")


# middleware application
def generate_log_details(body_data: dict):
	details = ''
	if 'message' in body_data.keys():
		return body_data['message']
	for key in body_data.keys():
		if key.startswith('previous_'):
			details += f"Event is updated from {key}: {body_data[key]}"

		elif key.startswith('updated_'):
			details += f" to {key}: {body_data[key]}."
	return details

def generate_create_log_details(body_data: dict):
	details = 'Event created with details: '
	for key in body_data.keys():
		details += f"{key}: {body_data[key]}, "
	details = details[:-2]
	details += '.'
	return details


# update event attributes
@app.put("/api/events/{event_id}/update_name")
async def event_name_update(event_id: str, event_name: str):
	return update_event_name(event_id, event_name)

@app.put("/api/events/{event_id}/update_duration")
async def event_duration_update(event_id: str, duration: int):
	return update_event_duration(event_id, duration)

# update event location, time, capacity, description
@app.put("/api/events/{event_id}/update_location")
async def event_location_update(event_id: str, location: str):
	return update_event_location(event_id, location)

@app.put("/api/events/{event_id}/update_time")
async def event_time_update(event_id: str, time: str):
	return update_event_time(event_id, time)

@app.put("/api/events/{event_id}/update_capacity")
async def event_capacity_update(event_id: str, capacity: int):
	return update_event_capacity(event_id, capacity)


@app.put("/api/events/{event_id}/update_status")
async def event_status_update(event_id: str, status: str):
	return update_event_status(event_id, status)

@app.put("/api/events/{event_id}/update_description")
async def event_description_update(event_id: str, description: str):
	return update_event_description(event_id, description)

@app.put("/api/events/{event_id}/update_tag2")
async def event_tag2_update(event_id: str, tag_2: str):
	return update_event_tag2(event_id, tag_2)

# @app.put("/api/events/{event_id}")
# def event_update(event_id: str, event: Event):
#     return update_event(event_id, event)

# delete an event
@app.delete("/api/events/{event_id}")
async def delete_event_route(event_id: str):
	return delete_event(event_id)

# Route for getting a group associated with an event (not for eventservice)
# @app.get("/api/events/{event_id}/group")
# def read_event_group(event_id: str):
#     group = get_group(event_id)
#     if group:
#         return group
#     raise HTTPException(status_code=404, detail="Group not found")

# ===== For Attendee =====

# list events that a user is attending
@app.get("/api/users/{user_id}/events")
async def list_events(user_id: str):
	return list_events_by_user_id(user_id)

# list attendees of an event
@app.get("/api/events/{event_id}/members")
async def read_event_members(event_id: str):
	members = list_attendees(event_id)
	if members:
		return members
	raise HTTPException(status_code=404, detail="Members not found")

# add an attendee to an event
@app.post("/api/events/{event_id}/members")
async def add_an_event_member(event_id: str, user_id: str):
	return add_event_member(event_id, user_id)

# delete an attendee of an event
@app.delete("/api/events/{event_id}/members")
async def delete_an_event_member(event_id: str, user_id: str):
	return delete_event_member(event_id, user_id)

# ===== For Comment =====

# list all comments of an event
@app.get("/api/events/{event_id}/comments")
async def read_event_comments(event_id: str):
	comments = list_comments_by_event_id(event_id)
	if comments:
		return comments
	raise HTTPException(status_code=404, detail="Comments not found")

# add a comment to an event
@app.post("/api/events/{event_id}/comments")
async def add_event_comment(event_id: str, user_id: str, comment: str):
	return add_comment(event_id, user_id, comment)

# update a comment to an event
@app.put("/api/events/{event_id}/comments")
async def update_event_comment(comment_id: str, comment: str):
	return update_comment(comment_id, comment)

# delete a comment to an event
@app.delete("/api/events/{event_id}/comments")
async def delete_event_comment(comment_id: str):
	return delete_comment(comment_id)


if __name__ == "__main__":
	uvicorn.run(app, host="0.0.0.0", port=8011)
