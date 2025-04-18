"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['POST'])
def add_member():
    new_member = request.get_json()
    if not new_member.get("first_name") or not new_member.get("lucky_numbers"):
        return jsonify("Any field cant be empty"), 400

    member = jackson_family.add_member(new_member)
    return jsonify(member), 200


@app.route('/members', methods=['GET'])
def get_all_members():

    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    return jsonify(members), 200


@app.route('/members/<int:id>', methods=['GET'])
def get_single_member(id):

    member = jackson_family.get_member(id)
    return jsonify(member), 200


@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):

    member = jackson_family.delete_member(id)
    return jsonify(member)


# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
