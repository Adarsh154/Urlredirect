# using flask_restful
from flask import Flask, jsonify, request
from flask_restful import Resource, Api

# creating the flask app
app = Flask(__name__)
# creating an API object
api = Api(app)


class ShortUrl(Resource):

    # corresponds to the GET request.
    def get(self):
        return jsonify({'message': 'hello world'})

    # Corresponds to POST request
    def post(self):
        data = request.get_json()  # status code
        return jsonify({'data': data}), 201


api.add_resource(ShortUrl, '/shorty')

# driver function
if __name__ == '__main__':
    app.run(debug=True)
