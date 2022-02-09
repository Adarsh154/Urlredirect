# using flask_restful
import string
import random

import redis
from flask import Flask, request, redirect
from flask_restful import Resource, Api

# creating the flask app
app = Flask(__name__)
# creating an API object
api = Api(app)
BaseUrl = "http://127.0.0.1:5000/shortly/"


class ShortUrl(Resource):

    @staticmethod
    def make_short_url():
        random_short_url = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        while True:
            is_present = get_key_from_values(random_short_url)
            if is_present:
                random_short_url = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            else:
                break
        return random_short_url

    # corresponds to the GET request.
    def get(self):
        url = request.args.get("url")
        if not url:
            return {'message': 'Url parameter not passed'}, 400
        key = read_from_redis(url)
        if key:
            return {"Success": "Your short url is " + BaseUrl + key}, 200
        else:
            return {"Error_msg": "Url not found"}, 400

    # Corresponds to POST request
    def post(self):
        url = request.get_json()['url']
        key = read_from_redis(url)
        if key:
            return {"Error_msg": "Url already shortened as " + BaseUrl + key}, 400
        random_id = ShortUrl.make_short_url()
        write_to_redis(url, random_id)
        return {"Success": "Your short url is " + BaseUrl + random_id}, 201

    # Corresponds to put request
    def put(self):
        url = request.get_json()['url']
        key = read_from_redis(url)
        if key:
            random_id = ShortUrl.make_short_url()
            write_to_redis(url, random_id)
            return {"Success": "Your short url is changed to " + BaseUrl + random_id}, 201
        else:
            return {"Error_msg": "Url not found, make a post request"}, 400


class ServeUrl(Resource):

    def get(self, ids):
        key = get_key_from_values(ids)
        if key:
            return redirect(key, code=302)
        else:
            return {'message': 'Page Not Found'}, 400


api.add_resource(ShortUrl, '/genUrl')
api.add_resource(ServeUrl, '/shortly/<string:ids>')


def write_to_redis(url, value):
    client.set(url, value)


def read_from_redis(url):
    return client.get(url)


def get_key_from_values(value):
    for key in client.keys():
        if value == client.get(key):
            return key
    return None


# driver function
if __name__ == '__main__':
    client = redis.StrictRedis('localhost', 6379, charset="utf-8", decode_responses=True)
    app.run(debug=True)
