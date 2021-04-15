import os
import json
import time
from Constants import *
from google.cloud import pubsub_v1
from lookup_engine import get_image_match
from flask import Flask, jsonify, request, render_template, send_file, make_response
from crawler import cleanup, buildItemsAndImagesMap, fetchNewImagesFromItemImagesMap, fetchImage


################  Utilities  ################

def print_in_flask(s):
    import sys
    print(str(s), file=sys.stdout)
    return

def poll_notifications(project= PROJECT_ID, subscription_name= SUBSCRIPTION_NAME):
    """Polls a Cloud Pub/Sub subscription for new GCS events for display."""
    # [START poll_notifications]
    # subscriber = pubsub_v1.SubscriberClient()
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = 'projects/{project}/subscriptions/{subscription}'.format(
        project= project, 
        subscription= subscription_name
    )

    # subscriber.subscribe(subscription_path, callback=callback)

    # The subscriber is non-blocking, so we must keep the main thread from
    # exiting to allow it to process messages in the background.
    print("Listening for messages on {}".format(subscription_path))
    while True:

        pull_response= subscriber.pull(subscription=subscription_path, max_messages=10)
        for msg in pull_response.received_messages:
            message = msg.message.data.decode('utf-8')
            print(message)
            
            # # do your thing
            # # 1) Crawler: Get reqd images(if any) from Lightspeed
            # #    Retail into idx_images + build in memory map
            # cleanup()
            # buildItemsAndImagesMap()
            # fetchNewImagesFromItemImagesMap()

            # # 2) Fetch query img from bucket into the relevant dir
            

            # # 3) Lookup engine: Build the index + match against an index img
            # queryImgHeldAtPath = ''
            # jsonResponse = get_image_match(queryImgHeldAtPath)
            # print(jsonResponse)

            subscriber.acknowledge(
                request= {
                    "subscription": subscription_path,
                    "ackIds": [msg.ack_id]
                }
            )

        time.sleep(30)


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