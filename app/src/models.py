from pydantic import BaseModel
from typing import List, Optional

class Event(BaseModel):
    event_id: int
    group_id: int
    attended_person: List[int]
    not_attended_person: List[int]
    no_response_person: List[int]

class Group(BaseModel):
    group_id: int
    name: str
    description: Optional[str] = None

class Member(BaseModel):
    user_id: int
    username: str
    event_id: int  # a member is associated with an event

class Comment(BaseModel):
    comment_id: int
    event_id: int
    text: str
    user_id: int
