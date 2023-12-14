import boto3
from boto3.dynamodb.conditions import Key, Attr
from .models import Event, Group, Comment, EventMemberRelation
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
events_table = dynamodb.Table('Events')
groups_table = dynamodb.Table('Groups')
# members_table = dynamodb.Table('Members')
comments_table = dynamodb.Table('Comments')
relations_table = dynamodb.Table('EventMemberRelation')

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
	return response.get('Items', [])

def update_event_location(event_id: str, location: str) -> dict:
	response = events_table.update_item(
		Key={'event_id': event_id},
		UpdateExpression="set location=:l",
		ExpressionAttributeValues={
			':l': location
		},
		ReturnValues="UPDATED_NEW"
	)
	
	return response.get('Attributes', {})

def update_event_time(event_id: str, time: str) -> dict:
	try:
		datetime.fromisoformat(time)
	except ValueError:
		return {'error': 'Invalid time format'}

	# Update the event time
	response = events_table.update_item(
		Key={'event_id': event_id},
		UpdateExpression="set time=:t",
		ExpressionAttributeValues={
			':t': time
		},
		ReturnValues="UPDATED_NEW"
	)

	return response.get('Attributes', {})


def update_event_capacity(event_id: str, capacity: int) -> dict:
	response = events_table.update_item(
		Key={'event_id': event_id},
		UpdateExpression="set capacity=:c",
		ExpressionAttributeValues={
			':c': capacity
		},
		ReturnValues="UPDATED_NEW"
	)
 
	return response.get('Attributes', {})

def update_event_status():
	pass

def update_event_description(event_id: str, description: str) -> dict:
	response = events_table.update_item(
		Key={'event_id': event_id},	
		UpdateExpression="set description=:d",
		ExpressionAttributeValues={
			':d': description
		},
		ReturnValues="UPDATED_NEW"
	)
	
	return response.get('Attributes', {})

def update_event_tag2(event_id: str, tag2: str) -> dict:
	response = events_table.update_item(
		Key={'event_id': event_id},	
		UpdateExpression="set tag_2=:t2",
		ExpressionAttributeValues={
			':t2': tag2
		},
		ReturnValues="UPDATED_NEW"
	)
	
	return response.get('Attributes', {})



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
	events_table.delete_item(Key={'event_id': event_id})
	return {"message": "Event deleted"}

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


# def get_events(limit: int = 10, skip: int = 0) -> list:
# 	response = events_table.scan()
# 	items = response.get('Items', [])
# 	return items[skip: skip + limit]

def add_event_member(event_id: str, user_id: str) -> dict:
	try:
		response = relations_table.put_item(
			Item={
				'event_id': event_id,
				'user_id': user_id
			}
		)
		return {'message': 'Member added to event successfully', 'response': response}
	except Exception as e:
		return {'error': str(e)}
	
def delete_event_member(event_id: str, user_id: str) -> dict:
	try:
		response = relations_table.delete_item(
			Key={
				'event_id': event_id,
				'user_id': user_id
			}
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

def get_comments(event_id: str) -> list:
	response = comments_table.query(
		KeyConditionExpression=Key('event_id').eq(event_id)
	)
	return response.get('Items', [])

def add_comment(event_id: str, user_id: str, comment: str) -> dict:
	comment_dict = {
		'comment_id': str(uuid.uuid4()),
		'event_id': event_id,
		'user_id': user_id,
		'text': comment
	}
	comments_table.put_item(Item=comment_dict)
	comments_table.put_item(Item=comment_dict)
	return comment_dict
