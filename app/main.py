from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.get("/api/events")
def list_events():
    return {"events": [{"id": 1, "name": "Event1"}, {"id": 2, "name": "Event2"}]}


@app.get("/api/events/{event_id}")
def get_event(event_id: int):
    return {"event": {"id": event_id, "name": f"Event{event_id}"}}


@app.get("/api/events/{event_id}/group")
def get_event_group(event_id: int):
    return {"group": {"id": 1, "name": f"Group for Event{event_id}"}}


@app.get("/api/events/{event_id}/members")
def get_event_members(event_id: int):
    return {"members": [{"user_id": 1, "username": "User1"}, {"user_id": 2, "username": "User2"}]}


@app.get("/api/events/{event_id}/comments")
def get_event_comments(event_id: int):
    return {"comments": [{"comment_id": 1, "text": "Comment1"}, {"comment_id": 2, "text": "Comment2"}]}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8002)
