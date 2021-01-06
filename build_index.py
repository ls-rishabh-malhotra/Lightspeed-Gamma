import os
import json
import image_ingestion as ingest_img
import get_image_embedding as embed_img
from annoy import AnnoyIndex
from argparse import ArgumentParser
from Constants import ANNOY_VECTOR_DIMENSIONS, ANNOY_METRICS, ANNOY_METRIC_IN_USE, WRITE_PERMISSIONS, IMG_DIR_IDX, INDX_DIR, INDX_METADATA_FILE, INDX_FILE, NUM_IMAGES

def get_vectors_all_imgs(model, args, batch):
    ids, imgs, imgFnames = zip(*batch)
    imgFeatureVectors = embed_img.generate_image_feature_vectors(
        model,
        imgs
    ).numpy()
    return imgFeatureVectors, ids, imgFnames

def populateIndex(imgFeatureVectors, index, indexMetadata, ids, imgFnames):
    print("ids are " + str(ids))
    for ind, featureVector in enumerate(imgFeatureVectors):
        index.add_item(ids[ind], featureVector.tolist())
        indexMetadata[ids[ind]] = {
            'fname': imgFnames[ind]
        }

def main(args):
    index = AnnoyIndex(
        ANNOY_VECTOR_DIMENSIONS,
        ANNOY_METRICS[ANNOY_METRIC_IN_USE-1]
    )
    indexMetadata = {}

    curModel = embed_img.load_model()

    batch = []
    total_size = 0

    for i, fname in enumerate(os.listdir(args.images_dir)):
        if not (fname.endswith('.jpg') or fname.endswith('.png') or fname.endswith('.jpeg')):
            # This file is not a valid image to be passed so ignore
            print(str(fname) + " is not a valid image type. Please check this file again.")
            continue

        imgPath = os.path.join(args.images_dir, fname)

        try:
            img = ingest_img.ingest_image(imgPath)
            batch.append((i, img, fname))
        except Exception as e:
            print(e)
            continue
        
        if len(batch) == args.batch_size:
            total_size += len(batch)
            print("Processing batch: " + str(total_size) + " .......")
            # Get vectors with activation figures for images
            # with simple forward pass from our imagenet DNN
            imgFeatureVectors, ids, imgFnames = get_vectors_all_imgs(
                curModel,
                args,
                batch
            )

            populateIndex(
                imgFeatureVectors, 
                index, 
                indexMetadata, 
                ids, 
                imgFnames
            )
            
            # Existing batch is finished indexing
            print("Finished indexing batch: " + str(total_size) + " ......")
            batch = []

            if total_size >= args.max_items:
                break


    print("Building Index on given Images......")
    index.build(args.n_trees)
    print("Saving Index as mmap........")
    index.save(
        os.path.join(args.dst, INDX_FILE)
    )
    json.dump(
        indexMetadata,
        open(
            os.path.join(args.dst, INDX_METADATA_FILE), 
            WRITE_PERMISSIONS
        )
    )



# Execute
if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--images-dir', type=str, default=IMG_DIR_IDX)
    parser.add_argument('--dst', type=str, default=INDX_DIR)
    parser.add_argument('--batch-size', type=int, default=NUM_IMAGES)
    parser.add_argument('--n-trees', type=int, default=10)
    parser.add_argument('--max-items', type=int, default=10000)

    main(parser.parse_args())