import boto3
from boto3.dynamodb.conditions import Key, Attr
from .models import Event, Group, Comment, EventMemberRelation, EventsLog
from .sns import sns_add_event
import uuid
from datetime import datetime


# Initialize a DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name="us-east-2")


def load_data_to_dynamodb(table_name, data):
	table = dynamodb.Table(table_name)
	for item in data:
		table.put_item(Item=item.dict())  # Convert Pydantic model to dict


# Replace with your table names
events_table = dynamodb.Table('Event')
groups_table = dynamodb.Table('Group')
comments_table = dynamodb.Table('Comment')
relations_table = dynamodb.Table('EventMemberRelation')
log_table = dynamodb.Table('EventsLog')

def add_event(user_id : str, group_id : str, event_data: Event) -> dict:
	event_dict = event_data.model_dump()
	event_dict['group_id'] = group_id
	event_dict['organizer_id'] = user_id
	event_dict['event_id'] = str(uuid.uuid4())
	events_table.put_item(Item=event_dict)
	sns_add_event(event_dict)

	return event_dict

def get_event(event_id: str) -> dict:
	response = events_table.get_item(Key={'event_id': event_id})
	return response.get('Item')


def list_attendees(event_id: str) -> list:
	response = relations_table.query(
		KeyConditionExpression=Key('event_id').eq(event_id)
	)
	items = response.get('Items', [])
	user_ids = [item['user_id'] for item in items]
	return user_ids

def event_exists(event_id: str) -> bool:
	try:
		response = events_table.get_item(
			Key={'event_id': event_id}
		)
		return 'Item' in response
	except Exception as e:
		print(f"An error occurred: {e}")
		return False

def list_logs(limit: int = 10, skip: int = 0) -> list:
	response = log_table.scan()
	items = response.get('Items', [])
	return items[skip: skip + limit]

def get_event_log_by_event_id(event_id: str, limit: int = 10, skip: int = 10) -> list:
	response = log_table.scan(
		FilterExpression=boto3.dynamodb.conditions.Attr('event_id').eq(event_id)
	)
	items = response.get('Items', [])
	return items[skip: skip + limit]

def update_event_name(event_id: str, event_name: str) -> dict:
	current_event = get_event(event_id)
	if not current_event:
		return {'message': 'Event not found'}
	current_name = current_event.get('event_name', 'Unknown')
	if current_name == event_name:
		return {'message': 'Event name is the same, no need to update'}

	response = events_table.update_item(
		Key={'event_id': event_id},
		UpdateExpression="set #en = :en",
		ExpressionAttributeNames={'#en': 'event_name'},
		ExpressionAttributeValues={':en': event_name},
		ReturnValues="UPDATED_NEW"
	)

	return {
		'event_id': event_id,
		'previous_event_name': current_name,
		'updated_event_name': event_name
	}


def update_event_location(event_id: str, location: str) -> dict:
	current_event = get_event(event_id)
	if not current_event:
		return {'message': 'Event not found'}
	current_location = current_event.get('location', 'Unknown')
	if current_location == location:
		return {'message': 'Event location is the same, no need to update'}

	response = events_table.update_item(
		Key={'event_id': event_id},
		UpdateExpression="set #loc = :l",
		ExpressionAttributeNames={'#loc': 'location'},
		ExpressionAttributeValues={':l': location},
		ReturnValues="UPDATED_NEW"
	)

	return {
		'event_id': event_id,
		'previous_location': current_location,
		'updated_location': location
	}


def update_event_time(event_id: str, time: str) -> dict:
	current_event = get_event(event_id)
	if not current_event:
		return {'message': 'Event not found'}
	current_time = current_event.get('time', 'Unknown')
	if current_time == time:
		return {'message': 'Event start time is the same, no need to update'}

	try:
		datetime.fromisoformat(time)
	except ValueError:
		return {'error': 'Invalid time format'}

	response = events_table.update_item(
		Key={'event_id': event_id},
		UpdateExpression="set #t = :t",
		ExpressionAttributeNames={'#t': 'time'},
		ExpressionAttributeValues={':t': time},
		ReturnValues="UPDATED_NEW"
	)

	return {
		'event_id': event_id,
		'previous_time': current_time,
		'updated_time': time
	}


def update_event_capacity(event_id: str, capacity: int) -> dict:
	current_event = get_event(event_id)
	if not current_event:
		return {'message': 'Event not found'}
	current_capacity = current_event.get('capacity', 'Unknown')
	if current_capacity == capacity:
		return {'message': 'Event capacity is the same, no need to update'}

	response = events_table.update_item(
		Key={'event_id': event_id},
		UpdateExpression="set #c = :c",
		ExpressionAttributeNames={'#c': 'capacity'},
		ExpressionAttributeValues={':c': capacity},
		ReturnValues="UPDATED_NEW"
	)

	return {
		'event_id': event_id,
		'previous_capacity': current_capacity,
		'updated_capacity': capacity
	}


def update_event_duration(event_id: str, duration: int) -> dict:
	current_event = get_event(event_id)
	if not current_event:
		return {'message': 'Event not found'}
	current_duration = current_event.get('duration', 'Unknown')
	if current_duration == duration:
		return {'message': 'Event duration is the same, no need to update'}

	response = events_table.update_item(
		Key={'event_id': event_id},
		UpdateExpression="set #d = :d",
		ExpressionAttributeNames={'#d': 'duration'},
		ExpressionAttributeValues={':d': duration},
		ReturnValues="UPDATED_NEW"
	)

	return {
		'event_id': event_id,
		'previous_duration': current_duration,
		'updated_duration': duration
	}


def update_event_status(event_id: str, status: str) -> dict:
	current_event = get_event(event_id)
	if not current_event:
		return {'message': 'Event not found'}
	current_status = current_event.get('status', 'Unknown')
	if current_status == status:
		return {'message': 'Event status is the same, no need to update'}

	response = events_table.update_item(
		Key={'event_id': event_id},
		UpdateExpression="set #s = :s",
		ExpressionAttributeNames={'#s': 'status'},
		ExpressionAttributeValues={':s': status},
		ReturnValues="UPDATED_NEW"
	)

	return {
		'event_id': event_id,
		'previous_status': current_status,
		'updated_status': status
	}

def update_event_description(event_id: str, description: str) -> dict:
	current_event = get_event(event_id)
	if not current_event:
		return {'message': 'Event not found'}
	current_description = current_event.get('description', 'Unknown')
	if current_description == description:
		return {'message': 'Event description is the same, no need to update'}

	response = events_table.update_item(
		Key={'event_id': event_id},
		UpdateExpression="set #desc = :d",
		ExpressionAttributeNames={'#desc': 'description'},
		ExpressionAttributeValues={':d': description},
		ReturnValues="UPDATED_NEW"
	)

	return {
		'event_id': event_id,
		'previous_description': current_description,
		'updated_description': description
	}


def update_event_tag2(event_id: str, tag2: str) -> dict:
	current_event = get_event(event_id)
	if not current_event:
		return {'message': 'Event not found'}
	current_tag2 = current_event.get('tag_2', 'Unknown')
	if current_tag2 == tag2:
		return {'message': 'Event tag2 is the same, no need to update'}

	response = events_table.update_item(
		Key={'event_id': event_id},
		UpdateExpression="set tag_2=:t2",
		ExpressionAttributeValues={':t2': tag2},
		ReturnValues="UPDATED_NEW"
	)

	return {
		'event_id': event_id,
		'previous_tag2': current_tag2,
		'updated_tag2': tag2
	}



def update_event(event_id: str, event_data: Event) -> dict:
	# Assuming 'event_id' is the primary key and cannot be updated
	event_dict = event_data.model_dump()
	response = events_table.update_item(
		Key={'event_id': event_id},
		UpdateExpression="set status=:s, capacity=:c, event_name=:en, description=:d, location=:l, time=:t, group_id=:g, organizer_id=:o, tag_1=:t1, tag_2=:t2",
		ExpressionAttributeValues={
			':s': event_dict['status'],
			':c': event_dict['capacity'],
			':en': event_dict['event_name'],
			':d': event_dict['description'],
			':l': event_dict['location'],
			':t': event_dict['time'],
			':g': event_dict['group_id'],
			':o': event_dict['organizer_id'],
			':t1': event_dict['tag_1'],
			':t2': event_dict['tag_2']
		},
		ReturnValues="UPDATED_NEW"
	)
	return response.get('Attributes', {})

def delete_event(event_id: str) -> dict:
	# Check if the event exists
	if not event_exists(event_id):
		return {'message': 'Event not found'}

	try:
		events_table.delete_item(Key={'event_id': event_id})
		return {"message": "Event deleted"}
	except Exception as e:
		return {'error': str(e)}


def list_events_by_group_id(group_id: str) -> list:
	# Query the events table for items with the specified group_id
	try:
		response = events_table.scan(
			FilterExpression=boto3.dynamodb.conditions.Attr('group_id').eq(group_id)
		)
		return response.get('Items', [])
	except Exception as e:
		print(f"Error querying table: {str(e)}")
		return []


def get_events(limit: int = 10, skip: int = 0) -> list:
	response = events_table.scan()
	items = response.get('Items', [])
	return items[skip: skip + limit]

def get_events_by_ids(event_ids: list) -> list:
	events = []
	try:
		for event_id in event_ids:
			response = events_table.get_item(
				Key={'event_id': event_id}
			)
			event = response.get('Item')
			if event:
				events.append(event)
	except Exception as e:
		print(f"An error occurred: {e}")
	return events

def list_events_by_user_id(user_id: str) -> list:
	# Query the relations table for items with the specified user_id
	try:
		response = relations_table.scan(
			FilterExpression=boto3.dynamodb.conditions.Attr('user_id').eq(user_id)
		)
		items = response.get('Items', [])
		event_ids = [item['event_id'] for item in items]

		return get_events_by_ids(event_ids)
	except Exception as e:
		print(f"error: {str(e)}")
		return []


def add_event_member(event_id: str, user_id: str) -> dict:
	# Check if the member already exists
	existing_member = relations_table.get_item(
		Key={'event_id': event_id, 'user_id': user_id}
	).get('Item')

	if existing_member:
		return {'message': 'Member already exists in the event'}

	try:
		response = relations_table.put_item(
			Item={'event_id': event_id, 'user_id': user_id}
		)
		return {'message': 'Member added to event successfully', 'response': response}
	except Exception as e:
		return {'error': str(e)}


def delete_event_member(event_id: str, user_id: str) -> dict:
	# Check if the member exists
	existing_member = relations_table.get_item(
		Key={'event_id': event_id, 'user_id': user_id}
	).get('Item')

	if not existing_member:
		return {'message': 'No such member exists in the event'}

	try:
		response = relations_table.delete_item(
			Key={'event_id': event_id, 'user_id': user_id}
		)
		return {'message': 'Member removed from event successfully', 'response': response}
	except Exception as e:
		return {'error': str(e)}


# def get_group(event_id: int) -> dict:
#     # First, get the event to find the associated group_id
#     event_response = events_table.get_item(Key={'event_id': event_id})
#     event = event_response.get('Item')

#     # If the event exists, use its group_id to find the group
#     if event:
#         group_id = event['group_id']
#         group_response = groups_table.get_item(Key={'group_id': group_id})
#         return group_response.get('Item')
#     else:
#         return None  # or raise an exception, or handle as appropriate

# def get_members(event_id: int) -> list:
#     response = events_table.get_item(Key={'event_id': event_id})
#     event = response.get('Item')
#     if event and 'attended_person' in event:
#         return event['attended_person']
#     else:
#         return []


def list_comments_by_event_id(event_id: str) -> list:
	try:
		response = comments_table.scan(
			FilterExpression=boto3.dynamodb.conditions.Attr('event_id').eq(event_id)
		)
		return response.get('Items', [])
	except Exception as e:
		print(f"Error querying table: {str(e)}")
		return []


def add_comment(event_id: str, user_id: str, comment_text: str) -> dict:
	# Check if the user has already commented on the event
	response = comments_table.scan(
		FilterExpression=Attr('event_id').eq(event_id) & Attr('user_id').eq(user_id)
	)

	if response.get('Items'):
		return {'message': 'User has already commented on this event'}

	# If the user hasn't commented, add the new comment
	try:
		comment_id = str(uuid.uuid4())
		comment_dict = {
			'comment_id': comment_id,
			'event_id': event_id,
			'user_id': user_id,
			'text': comment_text
		}
		comments_table.put_item(Item=comment_dict)
		return {'message': 'Comment added successfully', 'comment_id': comment_id}
	except Exception as e:
		return {'error': str(e)}

def update_comment(comment_id: str, new_comment: str) -> dict:
	# Check if the comment exists
	existing_comment = comments_table.get_item(
		Key={'comment_id': comment_id}
	).get('Item')

	if not existing_comment:
		return {'message': 'No such comment exists'}

	try:
		response = comments_table.update_item(
			Key={'comment_id': comment_id},
			UpdateExpression="set #t = :t",
			ExpressionAttributeNames={
				'#t': 'text'
			},
			ExpressionAttributeValues={
				':t': new_comment
			},
			ReturnValues="UPDATED_NEW"
		)
		return {'message': 'Comment updated successfully', 'response': response}
	except Exception as e:
		return {'error': str(e)}

def delete_comment(comment_id: str) -> dict:
	# Check if the comment exists
	existing_comment = comments_table.get_item(
		Key={'comment_id': comment_id}
	).get('Item')

	if not existing_comment:
		return {'message': 'No such comment exists'}

	try:
		response = comments_table.delete_item(
			Key={'comment_id': comment_id}
		)
		return {'message': 'Comment deleted successfully', 'response': response}
	except Exception as e:
		return {'error': str(e)}


# def update_comment(event_id: str, user_id: str, new_comment: str) -> dict:
#     # Check if the comment exists
# 	existing_comment = comments_table.get_item(
# 		Key={'event_id': event_id, 'user_id': user_id}
# 	).get('Item')

# 	if not existing_comment:
# 		return {'message': 'No such comment exists'}

# 	try:
# 		response = comments_table.update_item(
# 			Key={'event_id': event_id, 'user_id': user_id},
# 			UpdateExpression="set #t = :t",
# 			ExpressionAttributeNames={
# 				'#t': 'text'
# 			},
# 			ExpressionAttributeValues={
# 				':t': new_comment
# 			},
# 			ReturnValues="UPDATED_NEW"
# 		)
# 		return {'message': 'Comment updated successfully', 'response': response}
# 	except Exception as e:
# 		return {'error': str(e)}

# def delete_comment(event_id: str, user_id: str) -> dict:
# 	# Check if the comment exists
# 	existing_comment = comments_table.get_item(
# 		Key={'event_id': event_id, 'user_id': user_id}
# 	).get('Item')

# 	if not existing_comment:
# 		return {'message': 'No such comment exists'}

# 	try:
# 		response = comments_table.delete_item(
# 			Key={'event_id': event_id, 'user_id': user_id}
# 		)
# 		return {'message': 'Comment deleted successfully', 'response': response}
# 	except Exception as e:
# 		return {'error': str(e)}
