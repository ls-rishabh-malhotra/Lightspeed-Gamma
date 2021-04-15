import requests
import time
import json
import urllib3
import urllib
import os
from collections import namedtuple
from requests.structures import CaseInsensitiveDict
from Constants import *


Token = namedtuple("Token", "value expiresAt scope")
curAccountToken = None
urllib3.disable_warnings()
# itemIDToImages: {ItemID: {ImgData}}
itemIDToImages = {}


def shouldRefreshToken(token):
    now = time.time()
    if token.expiresAt >= now:
        return False
    return True


def makeCall(url, type, params=None, headers=None):
    global curAccountToken
    if not(curAccountToken) or shouldRefreshToken(curAccountToken):
        curAccountToken = getToken()

    # Request headers
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer " + curAccountToken.value

    if type.strip().lower() == "post":
        return requests.post(url=url, params=params, headers=headers, verify=False)
    elif type.strip().lower() == "get":
        return requests.get(url=url, headers=headers, verify=False)
    else:
        raise Exception("Invalid request type specified.")
    return


def getToken():
    tokenRequestParams = {
        "userID": "1",
        "accountID": "1",
        "apiKey": "test_account",
        "scope": ["employee:all", "system"],
        "refresh": False
    }
    tokenResponse = requests.post(
        url= BEARER_TOKEN_URL,
        json= tokenRequestParams,
        verify= False
    )
    tokenData = tokenResponse.json()
    token = Token(
        value= tokenData["access_token"],
        expiresAt= time.time() + tokenData["expires_in"],
        scope= tokenData["scope"]
    )

    return token


def getAllItems():
    itemsURL = LOCALDEV_RAD_RETAIL_ACCT_1_URL + "Item.json?load_relations=[\"ItemShops\"]"
    itemsRes = makeCall(
        url=itemsURL,
        type="get"
    ).json()

    return itemsRes


def getAllImages():
    itemImagesURL = LOCALDEV_RAD_RETAIL_ACCT_1_URL + "Image.json"
    imagesRes = makeCall(
        url=itemImagesURL,
        type="get"
    ).json()

    return imagesRes


def buildItemsAndImagesMap():
    global itemIDToImages
    imagesResponse = getAllImages()
    if imagesResponse['@attributes']['count'] == 0: 
        itemIDToImages = {}
        return

    images = imagesResponse['Image']
    imagesByItemIDs = {}
    for image in images:
        itemID = image['itemID']
        if itemID not in imagesByItemIDs.keys():
            imgDataToPreserve = {}
            imgDataToPreserve['imageID'] = image['imageID']
            imgDataToPreserve['filename'] = image['filename']
            imgDataToPreserve['baseImageURL'] = image['baseImageURL']
            imgDataToPreserve['publicID'] = image['publicID']
            imgDataToPreserve['accessUrl'] = image['baseImageURL'] + image['publicID']
            imgDataToPreserve['size'] = image['size']
            imgDataToPreserve['createTime'] = image['createTime']
            imgDataToPreserve['timeStamp'] = image['timeStamp']
            imagesByItemIDs[itemID] = imgDataToPreserve

            itemIDToImages = imagesByItemIDs
    return


# Write this one later when tackling pertial re-indexing.
# This should also trigger the partial index re-build in
# case there are new values added to the map
def updateItemsAndImagesMap():
    pass


def fetchNewImagesFromItemImagesMap():
    global itemIDToImages

    #Iterate through map and fetch images to put into test download dir
    for itemID, imageData in itemIDToImages.items():
        imgID= imageData['imageID']
        imgName= imageData['filename']

        # Next, check if an image already exists before attempting download:
        checkFilename = str(imgID) + '_' + str(imgName) + '_' + str(itemID) + '.jpg'
        if checkFilename in os.listdir(IMG_UVSET_DIR):
            print("Image already exists in dir")
            continue
        
        try:
            print("fetching image..... " + str(checkFilename))
            fetchImage(
                imgUrl= imageData['accessUrl'],
                itemID= itemID,
                imgID= imgID,
                imgName= imgName
            )
        except:
            print("There was an error and image for itemID: " + str(itemID) + " could not be fetched\n")
    return


def fetchImage(imgUrl, itemID, imgID, imgName):
    imgSaveName = str(imgID) + '_' + str(imgName) + '_' + str(itemID) + '.jpg'
    imgSavePath = str(IMG_UVSET_DIR) + str(imgSaveName)
    return urllib.request.urlretrieve(imgUrl, imgSavePath)


def cleanupAllImgsInDir(path):
    for file in os.listdir(IMG_UVSET_DIR):
        if file.endswith('.jpg'):
            fullPath = str(IMG_UVSET_DIR) + str(file)
            os.remove(fullPath)
    return


def cleanupItemsAndImagesMap():
    global itemIDToImages
    itemIDToImages = {}
    return


# This will cleanup both the current in memory map and the images from the directory
def cleanup():
    cleanupItemsAndImagesMap()
    cleanupAllImgsInDir(IMG_UVSET_DIR)
    return


# Uncomment to run only this crawler as a standalone app
# cleanup()
# buildItemsAndImagesMap()
# fetchNewImagesFromItemImagesMap()