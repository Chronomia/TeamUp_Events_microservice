import boto3
from boto3.dynamodb.conditions import Key, Attr
from .models import Event, Group, Member, Comment

# Initialize a DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')


def load_data_to_dynamodb(table_name, data):
    table = dynamodb.Table(table_name)
    for item in data:
        table.put_item(Item=item.dict())  # Convert Pydantic model to dict


# Replace with your table names
events_table = dynamodb.Table('EventsTable')
groups_table = dynamodb.Table('GroupsTable')
members_table = dynamodb.Table('MembersTable')
comments_table = dynamodb.Table('CommentsTable')

# CRUD operations for events
def add_event(event_data: Event) -> dict:
    event_dict = event_data.dict()
    events_table.put_item(Item=event_dict)
    return event_dict

def get_event(event_id: int) -> dict:
    response = events_table.get_item(Key={'event_id': event_id})
    return response.get('Item')

def update_event(event_id: int, event_data: Event) -> dict:
    # Assuming 'event_id' is the primary key and cannot be updated
    event_dict = event_data.dict()
    response = events_table.update_item(
        Key={'event_id': event_id},
        UpdateExpression="set group_id=:g, attended_person=:a, not_attended_person=:n, no_response_person=:nr",
        ExpressionAttributeValues={
            ':g': event_dict['group_id'],
            ':a': event_dict['attended_person'],
            ':n': event_dict['not_attended_person'],
            ':nr': event_dict['no_response_person']
        },
        ReturnValues="UPDATED_NEW"
    )
    return response.get('Attributes', {})

def delete_event(event_id: int) -> dict:
    events_table.delete_item(Key={'event_id': event_id})
    return {"message": "Event deleted"}

def get_events(limit: int = 10, skip: int = 0) -> list:
    # This is a simple scan operation. For large datasets, consider using query and indexes.
    response = events_table.scan()
    items = response.get('Items', [])
    return items[skip: skip + limit]

# Operations for groups, members, comments
# Implement similar functions for groups, members, and comments
# For example:

def get_group(event_id: int) -> dict:
    response = groups_table.get_item(Key={'event_id': event_id})
    return response.get('Item')

def get_members(event_id: int) -> list:
    response = members_table.query(
        KeyConditionExpression=Key('event_id').eq(event_id)
    )
    return response.get('Items', [])

def get_comments(event_id: int) -> list:
    response = comments_table.query(
        KeyConditionExpression=Key('event_id').eq(event_id)
    )
    return response.get('Items', [])

def add_comment(event_id: int, comment_data: Comment) -> dict:
    comment_dict = comment_data.dict()
    comment_dict['event_id'] = event_id
    comments_table.put_item(Item=comment_dict)
    return comment_dict
