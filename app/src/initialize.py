import boto3
from .models import Event, Group, Member, Comment, EventMemberRelation 
import pandas as pd

# Initialize DynamoDB Client
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')

# Function to Load Data into DynamoDB
def load_data_to_dynamodb(table_name, data):
    table = dynamodb.Table(table_name)
    for item in data:
        table.put_item(Item=item.dict())
        
def load_event_to_dynamodb(csv_file):
    table = dynamodb.Table("Event")
    event_data = pd.read_csv(csv_file)
    for _, row in event_data.iterrows():
        event = Event(
            event_id=row['event_id'],
            status=row['status'],
            capacity=row['capacity'],
            event_name=row['event_name'],
            description=row['description'],
            location=row['location'],
            time=row['time'],
            group_id=row.get('group_id', ''),
            organizer_id=row.get('organizer_id', ''),
            tag_1=row['tag_1'],
            tag_2=row.get('tag_2', '')
        )
        table.put_item(Item=event.model_dump())

        
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

relations = [EventMemberRelation(event_id="", user_ids="1")]

if __name__ == "__main__":
    load_event_to_dynamodb("./mock_data.csv")
    # load_data_to_dynamodb('Events', events)
    load_data_to_dynamodb('Groups', groups)
    load_data_to_dynamodb('Members', members)
    load_data_to_dynamodb('Comments', comments)
    load_data_to_dynamodb('EventMemberRelation', relations)
