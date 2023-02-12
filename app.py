import os
import openai

from src.search import search_with_keywords
from flask_cors import CORS
from flask import Flask, send_file, request, jsonify, send_from_directory

app = Flask(__name__)
CORS(app)
openai.api_key = os.getenv("OPENAI_API_KEY")


def is_empty_or_none(string):
    if string is None:
        return True
    elif len(string) == 0:
        return True
    else:
        return False


@app.route("/")
def upload():
    return send_file('client/index.html')

@app.route('/dist/<path:filename>')
def serve_client_static(filename):
    print(filename)
    return send_from_directory('client/dist', filename)

@app.route("/search")
def search():
    if request.method == "GET":
        query = request.args.get('query')
        if (is_empty_or_none(query)):
            return jsonify({"error_message": "Please enter a query"}), 400
        else:
            # return query
            return search_with_keywords(query)


@app.route('/images/<path:filename>')
def serve_static_images(filename):
    print(filename)
    return send_from_directory('images', filename)
