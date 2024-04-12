from flask import Flask, render_template, request, session, redirect, url_for, abort
from google.cloud import storage, pubsub_v1
from threading import Thread
import os
import json
import uuid
import time

app = Flask(__name__)
app.secret_key = 'your secret key'  # Replace with your secret key

# Google Cloud credentials setup
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/jeril/disproj/spheric-rhythm-414505-7469436e6688.json"

# Create a global dictionary
object_urls = {}

# Google Cloud Storage setup
storage_client = storage.Client()
bucket_name1 = "source_bucket_transcoder"



@app.route('/')
def upload_form():
    return render_template('upload.html')



@app.route('/process', methods=['POST'])
def process_upload():
    file = request.files['file']
    session_id = str(uuid.uuid4())  # Generate a new session ID
    session['session_id'] = session_id  # Store session ID in the session object
    
    # Upload file to GCS
    bucket = storage_client.bucket(bucket_name1)
    blob = bucket.blob(session_id+'-'+file.filename)
    blob.content_type = file.content_type
    # print(blob.content_type)
    blob.upload_from_file(file)

    # Check if the upload was successful
    if bucket.get_blob(blob.name) is not None:
        print('Upload was successful')
        # Start a background task to listen for a message from Pub/Sub
        Thread(target=listen_for_pubsub_message, args=(session_id,)).start()

        return redirect(url_for('processing'))
    else:
        print('Upload failed')

    

@app.route('/processing')
def processing():
    return render_template('processing.html')

def listen_for_pubsub_message(session_id):
    global object_urls
    callback_done = False
    i=0
    # Listen for a message from Pub/Sub with condition that the content contains message with object_url = f"https://storage.googleapis.com/{bucket}/{name} in which name starts with session_id
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path("spheric-rhythm-414505", "download-video-creation-notifier-sub")
    def callback(message: pubsub_v1.subscriber.message.Message) -> None:
        nonlocal i
        # print(f"Received message: {message}")
        if session_id in message.data.decode("utf-8"):
            if(i==1):
                object_url = json.loads(message.data.decode("utf-8"))['object_url']
                # Associate the object_url with the session_id
                if session_id not in object_urls:
                    object_urls[session_id]= object_url
                    print(object_urls)
                    message.ack()
                else:
                    print("URL already exists")
                    print(object_url)
                    message.ack()
                    nonlocal callback_done
                    callback_done = True
            else:
                i=1
                print("First message received")
                message.ack()
            
    subscriber.subscribe(subscription_path, callback=callback)
    while not callback_done:
        time.sleep(1)
    subscriber.close()

@app.route('/get_object_url')
def get_object_url():
    global object_urls
    session_id = session.get('session_id')
    print(session_id)
    # Get the object_url associated with the session_id
    object_url = object_urls.get(session_id)
    print(object_url)
    if object_url is not None:
        return object_url
    else:
        abort(404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)