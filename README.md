# TeamUp Events Microservice

Welcome to the TeamUp Events Microservice! This FastAPI application is designed to manage events, including creating, updating, and logging event details.

## Features

- List events under a specific group
- Create new events
- Read event details
- Update event attributes (name, duration, location, time, capacity, status, description, tags)
- Delete events
- Attendee management (list, add, delete attendees for an event)
- Comment management (list, add, update, delete comments for an event)
- Event logs (list all logs, list logs for a specific event)

## Endpoints

### Root Endpoint
- `GET /`: Welcome message

### Event Management
- `GET /api/{group_id}/events`: List events under a specific group
- `POST /api/{group_id}/events`: Create a new event
- `GET /api/events`: List a number of events
- `GET /api/events/{event_id}`: Get details of a specific event
- `PUT /api/events/{event_id}/update_name`: Update the name of an event
- `PUT /api/events/{event_id}/update_duration`: Update the duration of an event
- `PUT /api/events/{event_id}/update_location`: Update the location of an event
- `PUT /api/events/{event_id}/update_time`: Update the time of an event
- `PUT /api/events/{event_id}/update_capacity`: Update the capacity of an event
- `PUT /api/events/{event_id}/update_status`: Update the status of an event
- `PUT /api/events/{event_id}/update_description`: Update the description of an event
- `PUT /api/events/{event_id}/update_tag2`: Update the second tag of an event
- `DELETE /api/events/{event_id}`: Delete an event

### Attendee Management
- `GET /api/users/{user_id}/events`: List events that a user is attending
- `GET /api/events/{event_id}/members`: List attendees of an event
- `POST /api/events/{event_id}/members`: Add an attendee to an event
- `DELETE /api/events/{event_id}/members`: Delete an attendee from an event

### Comment Management
- `GET /api/events/{event_id}/comments`: List all comments of an event
- `POST /api/events/{event_id}/comments`: Add a comment to an event
- `PUT /api/events/{event_id}/comments`: Update a comment on an event
- `DELETE /api/events/{event_id}/comments`: Delete a comment from an event

### Logs
- `GET /api/events/logs`: Show all logs
- `GET /api/events/{event_id}/logs`: Show logs of a specific event

## Middleware Logging
The service includes middleware for logging updates and event creation. Logs are stored in a DynamoDB table named `EventsLog`.

## Running the Application
To start the server, run the following command:

```uvicorn main:app --host 0.0.0.0 --port 8011```