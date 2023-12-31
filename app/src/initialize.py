# Import necessary libraries and models
import boto3
from models import Event, Group, Comment, EventMemberRelation, EventsLog
import pandas as pd

# Initialize DynamoDB Client
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')

tables_to_delete = ["Event", "Group", "Comment", "EventMemberRelation", "EventsLog"]

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
	key_schema=[{'AttributeName': 'event_id', 'KeyType': 'HASH'}],  
	attribute_definitions=[{'AttributeName': 'event_id', 'AttributeType': 'S'}]
)

# Group Table
create_table(
	name="Group",
	key_schema=[{'AttributeName': 'group_id', 'KeyType': 'HASH'}], 
	attribute_definitions=[{'AttributeName': 'group_id', 'AttributeType': 'S'}]
)

# Comment Table
create_table(
	name="Comment",
	key_schema=[{'AttributeName': 'comment_id', 'KeyType': 'HASH'}],  
	attribute_definitions=[{'AttributeName': 'comment_id', 'AttributeType': 'S'}]
)

# EventMemberRelation Table 
create_table(
	name="EventMemberRelation",
	key_schema=[{'AttributeName': 'event_id', 'KeyType': 'HASH'}, {'AttributeName': 'user_id', 'KeyType': 'RANGE'}], 
	attribute_definitions=[{'AttributeName': 'event_id', 'AttributeType': 'S'},  {'AttributeName': 'user_id', 'AttributeType': 'S'}]
)

# EventsLog Table
create_table(
	name="EventsLog",
	key_schema=[{'AttributeName': 'log_id', 'KeyType': 'HASH'}],
	attribute_definitions=[{'AttributeName': 'log_id', 'AttributeType': 'S'}]
)


# Function to Load Data into DynamoDB
def load_data_to_dynamodb(table_name, data):
	table = dynamodb.Table(table_name)
	for item in data:
		table.put_item(Item=item.model_dump())

def load_event_to_dynamodb(csv_file):
    table = dynamodb.Table("Event")
    event_data = pd.read_csv(csv_file)
    event_data = event_data.fillna('')
    for _, row in event_data.iterrows():
        event = Event(
            event_id=row['event_id'],
            status=row['status'],
            capacity=row['capacity'],
            event_name=row['event_name'],
            description=row['description'],
            location=row['location'],
            time=row['time'],
            # group_id=row.get('group_id', ''),
            group_id='101',
            organizer_id=row.get('organizer_id', ''),
            tag_1=row['tag_1'],
            tag_2=row.get('tag_2', ''),
            duration=row['duration']
        )
        table.put_item(Item=event.model_dump())
		

groups = [
	Group(group_id="101", name="Group 1", description="Description for Group 1"),
	Group(group_id="102", name="Group 2", description="Description for Group 2"),
	Group(group_id="103", name="Group 3", description="Description for Group 3"),
	Group(group_id="104", name="Group 4", description="Description for Group 4"),
	Group(group_id="105", name="Group 5", description="Description for Group 5"),
]


comments = [
	Comment(comment_id="1", event_id="fcf5e56d-ebe5-4e5d-8cfb-7c9d271bcfa3", text="Great event!", user_id="1"),
	Comment(comment_id="2", event_id="fcf5e56d-ebe5-4e5d-8cfb-7c9d271bcfa3", text="Really enjoyed it.", user_id="2"),
	Comment(comment_id="3", event_id="6abcc4ed-96e2-4aa3-9dca-92e0e0844b42", text="Looking forward to the next one.", user_id="3"),
	Comment(comment_id="4", event_id="6abcc4ed-96e2-4aa3-9dca-92e0e0844b42", text="Had a great time.", user_id="4"),
	Comment(comment_id="5", event_id="6527fac9-46e9-4abd-bcc3-2bdef0e8cea4", text="Wonderful experience.", user_id="5"),
]

event_member_relations = [
	EventMemberRelation(event_id="fcf5e56d-ebe5-4e5d-8cfb-7c9d271bcfa3", user_id="1"),
	EventMemberRelation(event_id="fcf5e56d-ebe5-4e5d-8cfb-7c9d271bcfa3", user_id="2"),
	EventMemberRelation(event_id="6abcc4ed-96e2-4aa3-9dca-92e0e0844b42", user_id="3"),
	EventMemberRelation(event_id="6527fac9-46e9-4abd-bcc3-2bdef0e8cea4", user_id="3"),
	EventMemberRelation(event_id="0f852b74-c4ba-4bbb-a09b-2f9dcbbf9faa", user_id="4"),
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
	# load_data_to_dynamodb('Event', events)
	load_event_to_dynamodb("./src/mock_data.csv")
	load_data_to_dynamodb('EventMemberRelation', event_member_relations)
	load_data_to_dynamodb('Group', groups)
	load_data_to_dynamodb('Comment', comments)
	all_events = scan_all_events()
	print(len(all_events))
	if len(all_events) > 0:
		print("Initialization loaded successfully.")
	else:
		print("Initialization Failed.")
