import json
import base64
from google.cloud import pubsub_v1

def publish_message(project_id, topic_name, message):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)
    message_data = json.dumps(message).encode("utf-8")
    future = publisher.publish(topic_path, data=message_data)
    future.result()  # Block until the message is published

def process_object_created(data, context):
    """Triggered by a change to a Cloud Storage bucket."""
    print(data)
    if data is not None:
        print(data)
        object_url = data['mediaLink']
        
        # Publish message to Pub/Sub topic
        project_id = 'spheric-rhythm-414505'
        topic_name = 'download-video-creation-notifier'
        message = {"object_url": object_url}
        publish_message(project_id, topic_name, message)

        print(f"Published message to Pub/Sub topic with URL: {object_url}")

# Note: The function name 'process_object_created' must match the 'entry_point' specified in Cloud Function configuration

# requirements.txt=google-cloud-pubsub==2.8.0