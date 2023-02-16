import os
import openai
import json
import requests

from src.search import search_with_keywords
from flask_cors import CORS
from flask import Flask, send_file, request, jsonify, send_from_directory

app = Flask(__name__)
CORS(app)
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_drive_items(item_ids, auth) -> str:
    # for local, hardcode auth here    auth = ""    # TODO: according to input params filter items    
    values = []
    results = {}
    for item_id in item_ids:
        response = requests.get('https://api.onedrive.com/v1.0/drives/731ab8ceccfd3695/items/{}'.format(item_id),
            params={'$expand': 'thumbnails'},
            headers={'Authorization': auth})
        if response.status_code == 200:
            print('Success {}'.format(item_id))
            values.append(response.json())
        else:
            print('err {} {}'.format(item_id, response.status_code))
    results["@search.approximateCount"] = len(values)
    results["value"] = values    
    return json.dumps(results)

def is_empty_or_none(string):
    if string is None:
        return True
    elif len(string) == 0:
        return True
    else:
        return False

def list_images(path):
    image_files = []
    for filename in os.listdir(path):
        if filename.lower().endswith(".jpg") or filename.lower().endswith(".jpeg") or filename.lower().endswith(".png") or filename.lower().endswith(".gif"):
            image_files.append({"FileName": path + "/" + filename, "similarity": 1})
    return json.dumps(image_files)

@app.route("/")
def upload():
    return send_file('client/index.html')

@app.route('/dist/<path:filename>')
def serve_client_static(filename):
    return send_from_directory('client/dist', filename)

@app.route("/search")
def search():
    if request.method == "GET":
        query = request.args.get('@s')
        if (is_empty_or_none(query)):
            return list_images('images')
        else:
            # return query
            listIds = search_with_keywords(query)
            return get_drive_items(listIds, request.headers.get('authorization'))


@app.route('/images/<path:filename>')
def serve_static_images(filename):
    print(filename)
    return send_from_directory('images', filename)

