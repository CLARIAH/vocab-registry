import os
import json

from flask import Flask, request, jsonify, abort, redirect, session
from flask_cors import CORS
from flask_pyoidc import OIDCAuthentication
from flask_pyoidc.provider_configuration import ProviderConfiguration, ClientMetadata
from flask_pyoidc.user_session import UserSession
from saxonche import PySaxonProcessor, PyXdmValue
from werkzeug.http import parse_date
from functools import wraps
from elastic_index import Index
from cmdi import get_record, create_basic_cmdi, Review
from config import secret_key, oidc_server, oidc_client_id, oidc_client_secret, oidc_redirect_uri
from registry.rating import ReviewModel, RatingModel

app = Flask(__name__, static_folder='frontend/dist', static_url_path='')
app.config.update(
    OIDC_REDIRECT_URI=oidc_redirect_uri,
    SECRET_KEY=secret_key,
)

CORS(app)

auth = OIDCAuthentication({'default': ProviderConfiguration(
    issuer=oidc_server,
    client_metadata=ClientMetadata(
        client_id=oidc_client_id,
        client_secret=oidc_client_secret),
    auth_request_params={'scope': ['openid', 'email', 'profile']},
)}, app) if oidc_server is not None else None

index = Index()


def authenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if auth:
            user_session = UserSession(session, 'default')
            if user_session.last_authenticated is None:
                return jsonify(result='not_authenticated', error='Please login!'), 401

        return func(*args, **kwargs)

    return wrapper


@app.route('/', defaults={'path': ''})
@app.route('/<path>')
@app.route('/<path>/description')
@app.route('/<path>/summary')
@app.route('/<path>/reviews')
def catch_all(path):
    return app.send_static_file("index.html")


if auth:
    @app.get('/login')
    @auth.oidc_auth('default')
    def login():
        destination = request.values.get('redirect-uri', default='/')
        return redirect(destination)


    @app.get('/user-info')
    @authenticated
    def user_info():
        user_session = UserSession(session, 'default')
        return jsonify(user_session.userinfo)


@app.post('/facet')
def get_facet():
    struc = request.get_json()
    ret_struc = index.get_facet(struc["name"], struc["amount"], struc["filter"], struc["searchvalues"])
    return jsonify(ret_struc)


@app.post('/browse')
def browse():
    struc = request.get_json()
    ret_struc = index.browse(struc["page"], struc["page_length"], struc["searchvalues"])
    return jsonify(ret_struc)


@app.get('/vocab/<id>')
def get_vocab(id):
    return jsonify(get_record(id).model_dump())


@app.post('/vocab/new')
def post_vocab():
    if 'title' in request.values and 'homepage' in request.values and 'description' in request.values:
        if create_basic_cmdi(request.values['title'], request.values['homepage'], request.values['description']):
            # TODO: send email
            return jsonify(success=True), 201

    return jsonify(success=False), 400


@app.get('/proxy/<recipe>/<id>')
def proxy(recipe, id):
    # Proxy for cache: /{regex:[a-z0-9-_]+[^@](\\.[a-z]+)?}
    # Proxy to: /proxy/cache/$1 for regex: /([a-z0-9-_]+)(\\.[a-z]+)?

    # Proxy for skosmos: /{regex:[a-z0-9-]+[^_]*}
    # Proxy to: /proxy/skosmos/$1 for regex: /([a-z0-9-_]+)(/.*)?

    record = get_record(id)
    if not record:
        abort(404)

    request_date = parse_date(request.headers['accept-datetime']).replace(tzinfo=None) \
        if 'accept-datetime' in request.headers else None

    locations = None
    if request_date:
        for version in record.versions:
            if not locations and version.validFrom and version.validFrom <= request_date:
                locations = version.locations
    else:
        locations = record.versions[0].locations

    redirect_uri = next(loc.location for loc in locations if loc.recipe == recipe) if locations else None
    if not redirect_uri:
        abort(404)

    return redirect(redirect_uri, code=302)


@app.post('/review/<id>')
@authenticated
def review_form(id):
    review = ReviewModel(**request.get_json())
    rating_data = {
        "reviews": [review]}
    rating_model = RatingModel(**rating_data)
    rating_model_json = rating_model.model_dump_json(by_alias=True)
    # TODO: execute_xslt(os.environ.get('RECORDS_PATH', '../data/records/') + id + '.cmdi', rating_model_json, xsl="review.xsl")

    data = {"status": "OK", "id": id}
    return jsonify(data)


@app.post('/thumb/<id>')
@authenticated
def thumb_form(id):
    thumb_data = ReviewModel(**request.get_json())
    rating_data = {
        "reviews": [thumb_data]}
    rating_model = RatingModel(**rating_data)
    rating_model_json = rating_model.model_dump_json(by_alias=True)

    # TODO: execute_xslt(os.environ.get('RECORDS_PATH', '../data/records/') + id + '.cmdi', rating_model_json, xsl="thumbs.xsl")

    data = {"status": "OK", "id": id}
    return jsonify(data)


def execute_xslt(f_record_path, rating_model_json, xsl):
    with PySaxonProcessor(license=False) as proc:
        xsltproc = proc.new_xslt30_processor()
        xsltproc.set_cwd(os.getcwd())
        executable = xsltproc.compile_stylesheet(stylesheet_file=xsl)
        value = PyXdmValue()
        value.add_xdm_item(proc.make_string_value(rating_model_json))
        executable.set_parameter("json", value)
        result = executable.apply_templates_returning_string(source_file=f_record_path)

        with open(f_record_path, "r+") as f:
            f.seek(0)
            f.write(result)


if __name__ == '__main__':
    app.run()
