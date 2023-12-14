from pydantic import BaseModel
from typing import List, Optional

class EventMemberRelation(BaseModel):
    event_id: str 
    user_ids: str


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

class Member(BaseModel):
    user_id: str
    username: str
    event_id: int  # a member is associated with an event

class Comment(BaseModel):
    comment_id: str
    event_id: str
    text: str
    user_id: str
