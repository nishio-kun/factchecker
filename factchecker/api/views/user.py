import json

from flask import Blueprint, request, make_response, jsonify

from api.models import User, UserSchema


# routing
user_router = Blueprint('user_router', __name__)


@user_router.route('/users', methods=['GET'])
def get_user_list():
    users = User.get_user_list()
    user_schema = UserSchema(many=True)

    return make_response(jsonify({
        'code': 200,
        'users': user_schema.dump(users).data
    }))


@user_router.route('/users', methods=['POST'])
def regist_user():
    # jsonデータを取得する
    json_data = json.dumps(request.json)
    user_data = json.loads(json_data)

    user = User.regist_user(user_data)
    user_schema = UserSchema(many=True)

    return make_response(jsonify({
        'code': 200,
        'user': user
    }))
