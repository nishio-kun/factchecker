import os

from flask import Blueprint, request, make_response, jsonify

from api.models import User, UserSchema
from api.src.downloader import get_page, split_to_sentences
from api.src.predict import predict, labeling


# routing
distinction = Blueprint('distinction', __name__)

MODEL = os.getenv('MODEL')


@distinction.route('/distinction', methods=['POST'])
def distinct():
    url = request.form.get('url')

    if not url:
        ret = {'status': 'fail', 'result': None,
               'message': "'url' is required."}
        return make_response(jsonify(ret), 400)

    # get sentences
    title, content = get_page(url)
    sentences = split_to_sentences(content)

    # TODO: save

    # distinct
    label = ['事実', '意見', '伝聞']

    try:
        predicts = predict(sentences, MODEL)
    except ValueError as e:
        # TODO: log
        ret = {'status': 'error', 'result': None,
               'message': "Can't get a text."}
        return make_response(jsonify(ret), 400)

    result = labeling(label, sentences, predicts)

    ret = {'status': 'success', 'result': result}
    return make_response(jsonify(ret))
