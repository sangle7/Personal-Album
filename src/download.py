from dotenv import load_dotenv
load_dotenv()

import replicate
import subprocess
import pandas as pd
from openai.embeddings_utils import get_embedding

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

    # https://replicate.com/salesforce/blip/versions/2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746#input
    inputs = {
        # Input image
        'image': open(filePath, "rb"),
        'task': "image_captioning",
    }

    # https://replicate.com/salesforce/blip/versions/2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746#output-schema
    out = version.predict(**inputs)

    print(out)

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

    dataset = pd.read_csv(input_datapath)
    dataset = dataset.append(df, ignore_index=True)
    dataset.to_csv(input_datapath, index=False)

# download()