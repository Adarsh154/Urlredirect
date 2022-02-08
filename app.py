# using flask_restful
import json
import string
from os import path
import random

from flask import Flask, jsonify, request, redirect
from flask_restful import Resource, Api

# creating the flask app
app = Flask(__name__)
# creating an API object
api = Api(app)
urls1 = dict()
BaseUrl = "http://127.0.0.1:5000/shortly/"


def make_short_url():
    random_short_url = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    while True:
        if random_short_url in urls1.values():
            random_short_url = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        else:
            break
    return random_short_url


class ShortUrl(Resource):

    # corresponds to the GET request.
    def get(self):
        global urls1
        urls1 = read_from_file()
        url = request.args.get("url")
        if url in urls1.keys():
            return {"Success": "Your short url is " + BaseUrl + urls1[request.get_json()['url']]}
        else:
            return {"Error_msg": "Url not found"}, 400

    # Corresponds to POST request
    def post(self):
        if request.get_json()['url'] in urls1.keys():
            return {"Error_msg": "Url already shortened as " + BaseUrl + urls1[request.get_json()['url']]}, 400

        urls1[request.get_json()['url']] = make_short_url()
        write_to_file(urls1)
        return {"Success": "Your short url is " + BaseUrl + urls1[request.get_json()['url']]}, 201


class ServeUrl(Resource):

    def get(self, id):
        for k, v in urls1.items():
            if v == id:
                return redirect(k, code=302)
        else:
            return jsonify({'message': 'Page Not Found'})


api.add_resource(ShortUrl, '/genUrl')
api.add_resource(ServeUrl, '/shortly/<string:id>')


def write_to_file(data):
    with open("urls.json", "w") as f:
        json.dump(data, f, indent=2)


def read_from_file():
    with open("urls.json") as f:
        return json.load(f)


# driver function
if __name__ == '__main__':
    if not path.exists("urls.json"):
        write_to_file(dict())
    urls1 = read_from_file()
    app.run(debug=True)
