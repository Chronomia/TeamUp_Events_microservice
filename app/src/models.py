from pydantic import BaseModel
from typing import List, Optional

class EventMemberRelation(BaseModel):
	event_id: str 
	user_id: str


class Event(BaseModel):
	event_id: str
	status: str
	capacity: int
	event_name: str
	description: str
	location: str
	time: str
	group_id: str
	organizer_id: str
	tag_1: str
	tag_2: Optional[str]
	duration: int
	
class EventsLog(BaseModel):
	log_id: str
	event_id: str
	action: str
	details: str
	time: str 
	user_id: Optional[str]

# class Event(BaseModel):
#     event_id: int
#     group_id: int
#     attended_person: List[int]
#     not_attended_person: List[int]
#     no_response_person: List[int]

class Group(BaseModel):
	group_id: str
	name: str
	description: Optional[str] = None

class Comment(BaseModel):
	comment_id: str
	event_id: str
	text: str
	user_id: str
