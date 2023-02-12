from dotenv import load_dotenv
load_dotenv()

import replicate
import subprocess
import os
import pandas as pd
from openai.embeddings_utils import get_embedding
from PIL import Image

image_thumbnailPath = "image.thumbnail"

def download():
    url = input("Please enter the url of the image you want to download: ")
    fileName = input("Please enter the name of the file you want to save the image as: ")

    filePath = "images/"+fileName

    subprocess.run(["wget", url, "-O", filePath])
    embed_by_file(filePath)

def embed_by_file(filePath):
    model = replicate.models.get("salesforce/blip")
    version = model.versions.get(
        "2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746")

    print(filePath)

    original_image = Image.open(filePath)

    print(original_image)

    # Set the target height
    target_height = 200

    # Calculate the target width based on the aspect ratio of the original image
    aspect_ratio = original_image.width / original_image.height
    target_width = int(target_height * aspect_ratio)

    # Resize the image to the target size
    resized_image = original_image.resize((target_width, target_height), Image.ANTIALIAS)

    # Save the resized image
    resized_image.save(image_thumbnailPath, original_image.format)

    # https://replicate.com/salesforce/blip/versions/2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746#input
    inputs = {
        # Input image
        'image': open(image_thumbnailPath, "rb"),
        'task': "image_captioning",
    }

    # https://replicate.com/salesforce/blip/versions/2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746#output-schema
    out = version.predict(**inputs)

    print(out)

    if os.path.exists(image_thumbnailPath):
        os.remove(image_thumbnailPath)

    data = [["FileName", "Caption"],
            [str(filePath), str(out)]]

    print(data)

    # embedding model parameters
    embedding_model = "text-embedding-ada-002"
    df = pd.DataFrame(data[1:], columns=data[0])

    print(df)

    # # This may take a few minutes
    df["Embedding"] = df["Caption"].apply(lambda x: get_embedding(x, engine=embedding_model))

    print(df)

    input_datapath = "dataset/image-to-text.csv"

    if os.path.exists(input_datapath):
        dataset = pd.read_csv(input_datapath)
        dataset = dataset.append(df, ignore_index=True)
    else:
        dataset = df

    dataset.to_csv(input_datapath, index=False)

# download()