import json

from flask import Blueprint, request, make_response, jsonify

from api.models import User, UserSchema
from api.src.downloader import get_page, split_to_sentences


# routing
misc = Blueprint('misc', __name__)


@misc.route('/healthcheck', methods=['GET'])
def health_check():
    return make_response(jsonify({
        'status': 'success'
    }))
