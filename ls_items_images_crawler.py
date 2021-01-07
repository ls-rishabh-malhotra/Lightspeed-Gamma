from lightspeed_api_mocks.get_all_items_response import allItemsResponse
from lightspeed_api_mocks.get_all_images_response import allImagesResponse

def retrieve_image_url_for_item(itemData, getAllItemImagesResponse=allImagesResponse):
    itemId = itemData["itemID"]
    for imageData in getAllItemImagesResponse:
        if imageData["itemID"] == itemId:
            return imageData["baseImageURL"] + imageData["publicID"]
        continue
    return None

def build_item_ids_images_map(
    getAllItemsResponse=allItemsResponse, 
    getAllItemImagesResponse=allImagesResponse):

    itemsToItemImages = {}                   # {itemID: [imgURL, name]}
    allItems = getAllItemsResponse["Item"]
    allItemImages = getAllItemImagesResponse["Image"]
    for item in allItems:
        curItemId = item["itemID"]
        curItemName = item["description"]
        imageDataForCurItem = retrieve_image_url_for_item(item, allItemImages)
        if (imageDataForCurItem):
            itemsToItemImages[curItemId] = [imageDataForCurItem, curItemName]
        continue
    return itemsToItemImages

# To Test:
# m= build_item_ids_images_map()
# for k, v in m.items():
#     print(k, v)
#     print("\n")