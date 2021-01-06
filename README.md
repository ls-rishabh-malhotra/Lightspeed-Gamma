# Lightspeed-Gamma

1) To install, first activate the Python3.8 venv
2) Next, pip3 install -r requirements.txt
3) Next, go inside annoy/ and then pip3 install [Because this is a local fork that compiles and we want to install this copy of annoy]
4) Once this is done, all required dependencies should be installed

5) Now, to run, first build the index by running build_index.py
6) Once the index is built, you can test it by running server.py


### NOTE: 
1) This is a WIP so expect it to be a little rough around the edges for now. [If something breaks, feel free to reach out]
2) I will create a script for handling all of this once the code is in better shape. 
3) We shouldn't need to maunally build an index, the server automatically looks into it, however due to a current bug, it only works if we manually build the index first.
4) Next step is to create a template and build a simple yet beautoful frontend component to be able to ingest an image...

Most importantly, have fun!
