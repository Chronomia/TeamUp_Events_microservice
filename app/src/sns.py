import boto3

# Initialize the SNS client
sns_client = boto3.client('sns')

# Your SNS topic ARN (replace with your actual ARN)
topic_arn = 'arn:aws:sns:us-east-2:856186703608:event'


def publish_to_sns(message, subject):
    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=message,
        Subject=subject
    )
    return response


def sns_add_event(event_data):
    # Publish a message to the SNS topic
    sns_message = f"Event Created: {event_data['name']} with ID {event_data['id']}"
    sns_subject = "Event Creation Notification"
    publish_to_sns(sns_message, sns_subject)

    return event_data