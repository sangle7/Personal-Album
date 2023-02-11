import pandas as pd
import numpy as np
import openai

from openai.embeddings_utils import get_embedding, cosine_similarity
from pandas import DataFrame


def search_with_keywords(query) -> str:
    datafile_path = "dataset/image-to-text.csv"

    df = pd.read_csv(datafile_path)
    df["Embedding"] = df.Embedding.apply(eval).apply(np.array)

    # Load your API key from an environment variable or secret management service
    # openai.api_key = 

    # search through the reviews for a specific product
    def search_reviews(df, product_description, n=3) -> DataFrame:
        product_embedding = get_embedding(
            product_description,
            engine="text-embedding-ada-002"
        )
        df["similarity"] = df.Embedding.apply(lambda x: cosine_similarity(x, product_embedding))

        results = (
            df.sort_values("similarity", ascending=False)
            .head(n)
        )
        return results


    results = search_reviews(df, query, n=3)

    return results[['FileName','similarity']].to_json(orient='records')
