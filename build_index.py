import os
import image_ingestion as ingest_img
import get_image_embedding as embed_img
from annoy import AnnoyIndex

ANNOY_VECTOR_DIMENSIONS = 2048
ANNOY_METRICS = ['angular', 'euclidean', 'manhattan', 'hamming', 'dot']

def get_vectors_all_imgs(model, args, batch):
    ids, imgs, img_fnames = zip(*batch)
    return embed_img.generate_image_feature_vectors(
        model,
        imgs
    ).numpy()
    return img_feature_vectors


def main(args):
    index = AnnoyIndex(
        ANNOY_VECTOR_DIMENSIONS,
        ANNOY_METRICS[1]
    )
    index_metadata = {}

    cur_model = embed_img.load_model()

    batch = []
    total_size = 0

    for i, f_name in enumerate(os.listdir(args.images_dir)):
        if not (f_name.endsWith('.jpg') or f_name.endsWith('.png') or f_name.endsWith('.jpeg')):
            # This file is not a valid image to be passed
            # TODO Handle this case but for now, pass everything on
            continue

        img_path = os.path.join(args.images_dir, f_name)

        try:
            img = ingest_img.ingest_image(img_path)
            batch.append((i, img, f_name))
        except Exception as e:
            print(e)
            continue
        
        if len(batch) == args.batch_size:
            total_size += len(batch)
            print("Process batch: " + str(total_size))
            # Get vectors with activation figures for images
            # with simple forward pass from our imagenet DNN
            img_feature_vectors = get_vectors_all_imgs(
                cur_model,
                args,
                batch
            )
    pass