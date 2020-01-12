from flask import Flask, jsonify, request

from factchecker.lib.downloader import get_page, split_to_sentences


api = Flask(__name__)


@api.route('/healthcheck')
def health_check():
    return jsonify({'status': 'success'})


@api.route('/sentences', methods=['POST'])
def no_name():
    url = request.form.get('url')

    if not url:
        ret = {'status': 'fail', 'result': None,
               'message': "'url' is required."}
        return jsonify(ret), 400

    title, content = get_page(url)
    sentences = split_to_sentences(content)

    ret = {'status': 'success', 'result': sentences}
    return jsonify(ret)
