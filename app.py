from flask import (
    Flask, request, jsonify, render_template, abort, Response, make_response
)
from flask_accept import accept
from flask_restful import Resource, Api
import requests

app = Flask(__name__)
api = Api(app)

class UrlVerify(Resource):
    def get(self):
        response = make_response(render_template('test.html'))
        response.headers['Content-Type'] = 'text/html'
        return response

    def post(self):
        body = request.get_json()
        bad_urls = check_urls(body['urls'])
        return jsonify({'bad_urls': bad_urls})

api.add_resource(UrlVerify, '/')

# def test():
#     return render_template('test.html')

# @app.route('/', methods=['POST'])
# @accept('application/w-xxx-form-urlencoded')
# def check_url_endpoint():
    # body = request.form
    # bad_urls = check_urls(body['urls'])
    # return jsonify({'bad_urls': bad_urls})

def check_urls(urls):
    return filter(lambda x: x is not None, [check_url(url) for url in urls])

def check_url(url):
    response = requests.get(url)
    status_code = response.status_code
    failure_reasons = {
        401: 'Access to the url requires authentication',
        403: 'You are not authorized to access the url',
        404: 'url points to a page that does not exist',
        500: 'url points to a server that is broken'
    }

    if 200 <= status_code < 300:
        valid_url = True
    else:
        valid_url = False
        reason = failure_reasons.get(status_code, 'Unknown status code failure reason.')
        return {
            'url': url,
            'reason': reason
        }

if __name__ == '__main__':
    app.run(debug=True)
