import os
import json
from PIL import Image
from annoy import AnnoyIndex
from io import BytesIO
from flask import Flask, jsonify, request, render_template, send_file, make_response
from build_index import build_index
from Constants import *
from google.cloud import pubsub_v1
import time

################  Utilities  ################

def print_in_flask(s):
    import sys
    print(str(s), file=sys.stdout)
    return

def poll_notifications(project= PROJECT_ID, subscription_name= SUBSCRIPTION_NAME):
    """Polls a Cloud Pub/Sub subscription for new GCS events for display."""
    # [START poll_notifications]
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = 'projects/{project}/subscriptions/{subscription}'.format(
        project= project, 
        subscription= subscription_name
    )
    pull_response= subscriber.pull(subscription=subscription_path, max_messages=1)

    # subscriber.subscribe(subscription_path, callback=callback)

    # The subscriber is non-blocking, so we must keep the main thread from
    # exiting to allow it to process messages in the background.
    print("Listening for messages on {}".format(subscription_path))
    while True:

        for msg in pull_response.received_messages:
            message = msg.message.data.decode('utf-8')
            print(message)
            # do your thing
            subscriber.acknowledge(
                subscription_path, 
                [msg.ack_id]
            )

        time.sleep(1)


    # [END poll_notifications]

    return


################  Server Code  ################

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    print("Server is up :)")
    return render_template("index_image_upload.html")

if __name__ == "__main__":
    if (MODE == RUN_MODE.LOCAL_TERMINAL_TEST):
        with app.app_context():
            poll_notifications() #get_image_match()
    elif (MODE == RUN_MODE.LINK_TO_WEBSITE):
        app.run(debug=True)
    else:
        raise Exception("Invalid RUN_MODE specified, please specify the correct one at the top pf the server file.")