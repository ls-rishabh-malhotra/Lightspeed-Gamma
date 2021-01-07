# Lightspeed-Gamma

1) To install, first activate the Python3.8 venv
2) Next, pip3 install -r requirements.txt
3) Next, go inside annoy/ and then pip3 install [Because this is a local fork that compiles and we want to install this copy of annoy]
4) Once this is done, all required dependencies should be installed

5) Now, to run, first build the index by running build_index.py
6) Once the index is built, you can test it by running server.py

## TO RUN:

1) Do you want to link the server straight to the website or run it locally to test first? Set the RUN_MODE in Constants.RUN_MODE first
2) Do you want the server to check for and build the index automatically if it doesnt exist? This is the default behaviour but to change it, consider looking at Constants.BUILD_INDX_SEPARATELY
3) Now, simply run the server using `python3 server.py`
4) Once the server is running, visit http://127.0.0.1:5000 to see the website. 
(Note: pls close and reopen the website tab if you make changes to the frontend code, else the browser cache will still show the old version of the site)


### NOTE: 

1) This is a WIP so expect it to be a little rough around the edges for now. [If something breaks, feel free to reach out]
2) I will create a script for handling all of this once the code is in better shape. 
3a) Next step is to create a template and build a simple yet beautiful frontend component to be able to ingest an image...
3b) Simultaneously, use the response from the LS API to add secondary index to cross ref uids.

Most importantly, have fun!
