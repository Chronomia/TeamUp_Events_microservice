# TeamUp Events Microservice

## Overview
TeamUp Events Microservice is an API for managing events, attendees, and comments. This service allows users to create, update, list, and delete events, as well as manage event attendees and comments.

## API Endpoints

### General

- `GET /`
  - Welcome message for the API.

### Events

- `GET /api/{group_id}/events`
  - List all events under a specified group.

- `POST /api/{group_id}/events`
  - Create a new event under a specified group.

- `GET /api/events`
  - List some events with pagination.

- `GET /api/events/{event_id}`
  - Get detailed information about a specific event.

- `PUT /api/events/{event_id}/update_name`
  - Update the name of a specific event.

- `PUT /api/events/{event_id}/update_duration`
  - Update the duration of a specific event.

- `PUT /api/events/{event_id}/update_location`
  - Update the location of a specific event.

- `PUT /api/events/{event_id}/update_time`
  - Update the time of a specific event.

- `PUT /api/events/{event_id}/update_capacity`
  - Update the capacity of a specific event.

- `PUT /api/events/{event_id}/update_status`
  - Update the status of a specific event.

- `PUT /api/events/{event_id}/update_description`
  - Update the description of a specific event.

- `PUT /api/events/{event_id}/update_tag2`
  - Update the secondary tag of a specific event.

- `DELETE /api/events/{event_id}`
  - Delete a specific event.

### Attendees

- `GET /api/users/{user_id}/events`
  - List all events that a user attends.

- `GET /api/events/{event_id}/members`
  - List all attendees of a specific event.

- `POST /api/events/{event_id}/members`
  - Add an attendee to a specific event.

- `DELETE /api/events/{event_id}/members`
  - Remove an attendee from a specific event.

### Comments

- `GET /api/events/{event_id}/comments`
  - List all comments for a specific event.

- `POST /api/events/{event_id}/comments`
  - Add a comment to a specific event.

- `PUT /api/events/{event_id}/comments`
  - Update a comment on a specific event.

- `DELETE /api/events/{event_id}/comments`
  - Delete a comment from a specific event.

## Running the Application

To run the application, use the following command:

```bash
uvicorn main:app --host 0.0.0.0 --port 8011
