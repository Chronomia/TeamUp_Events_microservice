# Import necessary libraries and models
import boto3
from models import Event, Group, Member, Comment 

# Initialize DynamoDB Client
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

tables_to_delete = ["Event", "Group", "Member", "Comment"]

# Function to delete a table
def delete_table(table_name):
    table = dynamodb.Table(table_name)
    try:
        # Delete the table
        table.delete()
        table.wait_until_not_exists()
        print(f"Table {table_name} deleted successfully.")
    except Exception as e:
        # Handle exceptions
        print(f"Error deleting table {table_name}: {e}")

# Delete each table in the list
for table_name in tables_to_delete:
    delete_table(table_name)

# Function to create a DynamoDB table
def create_table(name, key_schema, attribute_definitions, read_capacity_units=1, write_capacity_units=1):
    try:
        table = dynamodb.create_table(
            TableName=name,
            KeySchema=key_schema,
            AttributeDefinitions=attribute_definitions,
            ProvisionedThroughput={
                'ReadCapacityUnits': read_capacity_units,
                'WriteCapacityUnits': write_capacity_units
            }
        )
        table.meta.client.get_waiter('table_exists').wait(TableName=name)
        print(f"Table {name} created successfully.")
    except Exception as e:
        print(f"Error creating table {name}: {e}")

# Event Table
create_table(
    name="Event",
    key_schema=[{'AttributeName': 'event_id', 'KeyType': 'HASH'}],  # Partition key
    attribute_definitions=[{'AttributeName': 'event_id', 'AttributeType': 'N'}]
)

# Group Table
create_table(
    name="Group",
    key_schema=[{'AttributeName': 'group_id', 'KeyType': 'HASH'}],  # Partition key
    attribute_definitions=[{'AttributeName': 'group_id', 'AttributeType': 'N'}]
)

# Member Table
create_table(
    name="Member",
    key_schema=[{'AttributeName': 'user_id', 'KeyType': 'HASH'}], 
    attribute_definitions=[{'AttributeName': 'user_id', 'AttributeType': 'N'}]
)

# Comment Table
create_table(
    name="Comment",
    key_schema=[{'AttributeName': 'event_id', 'KeyType': 'HASH'}, {'AttributeName': 'comment_id', 'KeyType': 'RANGE'}],  # Partition key
    attribute_definitions=[{'AttributeName': 'comment_id', 'AttributeType': 'N'},  {'AttributeName': 'event_id', 'AttributeType': 'N'}]
)


# Function to Load Data into DynamoDB
def load_data_to_dynamodb(table_name, data):
    table = dynamodb.Table(table_name)
    for item in data:
        table.put_item(Item=item.model_dump())
        
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
    Group(group_id=104, name="Group 4", description="Description for Group 4"),
    Group(group_id=105, name="Group 5", description="Description for Group 5"),
    Group(group_id=106, name="Group 6", description="Description for Group 6"),
    Group(group_id=107, name="Group 7", description="Description for Group 7"),
    Group(group_id=108, name="Group 8", description="Description for Group 8"),
    Group(group_id=109, name="Group 9", description="Description for Group 9"),
    Group(group_id=110, name="Group 10", description="Description for Group 10")
    # Add more groups as needed
]

members = [
    Member(user_id=1, username="User1", attended_events=[1], attended_groups=[101, 102]),
    Member(user_id=2, username="User2", attended_events=[1], attended_groups=[102]),
    Member(user_id=3, username="User3", attended_events=[2], attended_groups=[103]),
    Member(user_id=4, username="User4", attended_events=[2], attended_groups=[101, 103]),
    Member(user_id=5, username="User5", attended_events=[3], attended_groups=[104]),
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

def scan_all_events():
    table = dynamodb.Table('Event')

    try:
        response = table.scan()
        items = response.get('Items', [])
        if items:
            return items
        else:
            return "No events found in the table."
    except Exception as e:
        return f"Error scanning table: {e}"


# Load Data into DynamoDB
if __name__ == "__main__":
    load_data_to_dynamodb('Event', events)
    load_data_to_dynamodb('Group', groups)
    load_data_to_dynamodb('Member', members)
    load_data_to_dynamodb('Comment', comments)
    all_events = scan_all_events()
    for event in all_events:
        print(event)
