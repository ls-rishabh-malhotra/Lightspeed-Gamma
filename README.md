# Lightspeed-Gamma

1) To install, first activate the Python3.8 venv
2) Next, pip3 install -r requirements.txt
3) Next, go inside annoy/ and then pip3 install [Because this is a local fork that compiles and we want to install this copy of annoy]
4) Once this is done, all required dependencies should be installed

## TO RUN:

1) Do you want to link the server straight to the website or run it locally to test first? Set the RUN_MODE in Constants.RUN_MODE first
2) Do you want the server to check for and build the index automatically if it doesnt exist? This is the default behaviour but to change it, consider looking at Constants.BUILD_INDX_SEPARATELY
3) Now, simply run the server using `python3 server.py`
4) Once the server is running, it will await messages on the pubsub queue.
5) Upload the image you want to query to [this google cloud bucket](https://console.cloud.google.com/storage/browser/ls-inno-week-gamma-image-upload;tab=objects?forceOnBucketsSortingFiltering=false&project=ls-sandbox-dev&prefix=&forceOnObjectsSortingFiltering=false). You can also use the Go service for this, esp if you are trying to hook your app up with Gamma!
6) Keep in mind to have an item image in your local instance of LS RetailPOS which has the same item which you expect to be matched. Note that these do not have to be the same images. They can be 2 different images of the same item! (Try different angles, different lighting, etc)
7) As soon as you upload an image to the bucket above, the server will pick up the cue and start the pipeline!
8) After you are done running it, dont forget to purge any remaining messages from [here](https://console.cloud.google.com/cloudpubsub/subscription/detail/client_activity-sub?project=ls-sandbox-dev)
9) Have fun exploring the limits of how different 2 images can be before gamma stops recognizing them!!


### NOTE: 

1) This is a WIP so expect it to be a little rough around the edges for now. [If something breaks, feel free to reach out]<BR>
2) I will create a script for handling all of this once the code is in better shape.<BR>
3) <BR>
    a) Next step is to create a template and build a simple yet beautiful frontend component to be able to ingest an image...<BR>
    b) Simultaneously, use the response from the LS API to add secondary index to cross ref uids.<BR>
4) If you encounter issues while installing the local fork of annoy, try these steps:<BR>
    a) brew install python@3.8 <BR>
    b)brew link --overwrite python@3.8<BR>
    c)export ARCHFLAGS="-arch x86_64”<BR>
    d)pip3 install . --user<BR>
<BR>
Most importantly, have fun!


## Docs:
[Google Docs](https://docs.google.com/document/d/1w_aB0q9nkjY22v8v8daKB21QHwhlngmh7joU1tv3RME/edit#heading=h.2fmdi5b06xe0)

## Presentation:
[INNO WEEK 1](https://docs.google.com/presentation/d/1YYlzK2OFNEffFBwaMvu-qxeWprjIGW7QqIHrcxSGGic/edit#slide=id.g3754f1d088_0_4)
[INNO WEEK 2] (https://docs.google.com/presentation/d/1JKYsSvUIAk9Q2uOHEIL6uaKf4I-Qk8ekvsDxCzAvsSI/edit?ts=6078b2a4#slide=id.g3754f1d088_0_4)

## Acknowledgements:
1.[Spotify's Annoy](https://github.com/spotify/annoy) has been immensely useful for indexing and getting vector comparisons, currently using min euclidean distance.
Since it is currently undergoing some compile issues , a fork, modified locally has been used and consequentially included in this repo. (We are to use the installation from this fork)<BR>
2.[Approximate Nearest Neighbors](https://towardsdatascience.com/comprehensive-guide-to-approximate-nearest-neighbors-algorithms-8b94f057d6b6)<BR>
3.[annDB](https://anndb.com)<BR>
4.[Building image search from scratch](https://www.kdnuggets.com/2019/01/building-image-search-service-from-scratch.html)<BR>
5.[Common archs for CNNs](https://www.jeremyjordan.me/convnet-architectures/)<BR>
6.[Comapring performance for different DNN archs](https://forums.fast.ai/t/comparison-of-kerass-built-in-vgg16-resnet50-inception-v3-on-cats-vs-dogs-suspicions-about-preprocessing/1425)<BR>
