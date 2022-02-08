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
stored_urls = dict()
BaseUrl = "http://127.0.0.1:5000/shortly/"


class ShortUrl(Resource):

    @staticmethod
    def make_short_url():
        random_short_url = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        while True:
            if random_short_url in stored_urls.values():
                random_short_url = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            else:
                break
        return random_short_url

    # corresponds to the GET request.
    def get(self):
        url = request.args.get("url")
        if not url:
            return {'message': 'Url parameter not passed'}, 400
        if url in stored_urls.keys():
            return {"Success": "Your short url is " + BaseUrl + stored_urls[request.get_json()['url']]}, 200
        else:
            return {"Error_msg": "Url not found"}, 400

    # Corresponds to POST request
    def post(self):
        if request.get_json()['url'] in stored_urls.keys():
            return {"Error_msg": "Url already shortened as " + BaseUrl + stored_urls[request.get_json()['url']]}, 400

        stored_urls[request.get_json()['url']] = ShortUrl.make_short_url()
        write_to_redis()
        return {"Success": "Your short url is " + BaseUrl + stored_urls[request.get_json()['url']]}, 201

    # Corresponds to put request
    def put(self):
        if request.get_json()['url'] in stored_urls.keys():
            stored_urls[request.get_json()['url']] = ShortUrl.make_short_url()
            write_to_redis()
            return {"Success": "Your short url is changed to " + BaseUrl + stored_urls[request.get_json()['url']]}, 201
        else:
            return {"Error_msg": "Url not found, make a post request"}, 400


class ServeUrl(Resource):

    def get(self, ids):
        for k, v in stored_urls.items():
            if v == ids:
                return redirect(k, code=302)
        else:
            return {'message': 'Page Not Found'}, 400


api.add_resource(ShortUrl, '/genUrl')
api.add_resource(ServeUrl, '/shortly/<string:ids>')


def write_to_redis():
    client.hmset("urls", stored_urls)


def read_from_redis():
    return client.hgetall("urls")


# driver function
if __name__ == '__main__':
    client = redis.StrictRedis('redis', 6379, charset="utf-8", decode_responses=True)
    stored_urls = read_from_redis()
    app.run(debug=True, host="0.0.0.0")
