# Import necessary libraries and models
import boto3
from .models import Event, Group, Member, Comment  # Replace with the actual path to your models

# Initialize DynamoDB Client
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')

# Function to Load Data into DynamoDB
def load_data_to_dynamodb(table_name, data):
    table = dynamodb.Table(table_name)
    for item in data:
        table.put_item(Item=item.dict())
        
events = [
    Event(event_id=1, group_id=101, attended_person=[1, 2], not_attended_person=[3], no_response_person=[4, 5]),
    Event(event_id=2, group_id=102, attended_person=[6, 7], not_attended_person=[8], no_response_person=[9, 10]),
    Event(event_id=3, group_id=103, attended_person=[11, 12], not_attended_person=[13], no_response_person=[14, 15]),
    # Add more events as needed
]

groups = [
    Group(group_id=101, name="Group 1", description="Description for Group 1"),
    Group(group_id=102, name="Group 2", description="Description for Group 2"),
    Group(group_id=103, name="Group 3", description="Description for Group 3"),
    # Add more groups as needed
]

members = [
    Member(user_id=1, username="User1", event_id=1),
    Member(user_id=2, username="User2", event_id=1),
    Member(user_id=3, username="User3", event_id=2),
    Member(user_id=4, username="User4", event_id=2),
    Member(user_id=5, username="User5", event_id=3),
    # Add more members as needed
]

comments = [
    Comment(comment_id=1, event_id=1, text="Great event!", user_id=1),
    Comment(comment_id=2, event_id=1, text="Really enjoyed it.", user_id=2),
    Comment(comment_id=3, event_id=2, text="Looking forward to the next one.", user_id=3),
    Comment(comment_id=4, event_id=2, text="Had a great time.", user_id=4),
    Comment(comment_id=5, event_id=3, text="Wonderful experience.", user_id=5),
    # Add more comments as needed
]

# Load Data into DynamoDB
if __name__ == "__main__":
    load_data_to_dynamodb('EventsTable', events)
    load_data_to_dynamodb('GroupsTable', groups)
    load_data_to_dynamodb('MembersTable', members)
    load_data_to_dynamodb('CommentsTable', comments)
