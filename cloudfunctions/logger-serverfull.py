import json
import google.cloud.logging
from google.cloud import storage
from datetime import datetime

# Initialize Cloud Logging client
client = google.cloud.logging.Client()
# Connects the logger to the root logging handler; by default
# this captures all logs at INFO level and higher
client.setup_logging()

def process_object_created(data, context):
    """Triggered by a change to a Cloud Storage bucket."""
    print(data)
    if data['size'] != '0':
        print(data)
        session_id = data['name'].split('-SID-')[0]
        print(session_id)
        storage_client = storage.Client()
        # Get list of objects in the first bucket with the specified session_id
        first_bucket_name = 'source_bucket_transcoder'
        first_bucket = storage_client.get_bucket(first_bucket_name)
        first_bucket_objects = list(first_bucket.list_blobs(prefix=session_id))
        print(first_bucket_objects)

        # Get list of objects in the second bucket with the specified session_id


        if len(first_bucket_objects)>0 and len(first_bucket_objects)<2:
          source_object_time=first_bucket_objects[0].time_created
          destination_object_time=datetime.fromisoformat(data['timeCreated'])
          print(source_object_time, destination_object_time)
          time_difference=abs(source_object_time-destination_object_time).total_seconds()
          print(time_difference)
          text=f"Response time for session_id {session_id} (serverfull): {time_difference} seconds"
          log_type="serverfull"
          logger = client.logger('response-times-serverfull')  
          logger.log_struct(
              {   
                  'text' : text,
                  'type' : log_type,
                  'session_id': session_id,
                  'response_time_seconds': time_difference
              },
              severity='INFO'
          )

#requirements:
# google-cloud-storage==2.14.0
# google-cloud-logging>=2.0.2