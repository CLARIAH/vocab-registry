from flask import Flask, request, jsonify, abort, redirect, session
from flask_cors import CORS
from flask_pyoidc import OIDCAuthentication
from flask_pyoidc.provider_configuration import ProviderConfiguration, ClientMetadata
from flask_pyoidc.user_session import UserSession
from werkzeug.http import parse_date
from functools import wraps
from registry.elastic_index import Index
from registry.cmdi import get_record, create_basic_cmdi, add_review_to_cmdi, \
    persist_review_like_to_cmdi, get_reviews_user_interaction
from registry.config import secret_key, oidc_server, oidc_client_id, oidc_client_secret, oidc_redirect_uri

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
    auth_request_params={'scope': ['openid', 'email', 'profile'],
                         'claims': {'userinfo': {'nickname': None, 'email': None, 'eppn': None}}}
)}, app) if oidc_server is not None else None

index = Index()


def get_user_id():
    user_session = UserSession(session, 'default')
    if 'eppn' in user_session.userinfo:
        eppn = user_session.userinfo['eppn']
        return eppn[0] if type(eppn) == list else eppn

    return user_session.userinfo['sub']


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
@authenticated
def post_vocab():
    if 'title' in request.values and 'homepage' in request.values and 'description' in request.values:
        if create_basic_cmdi(request.values['title'], request.values['homepage'], request.values['description']):
            # TODO: send email
            return jsonify(success=True), 201

    return jsonify(success=False), 400


@app.post('/review/<id>')
@authenticated
def post_review(id):
    if 'body' in request.values and 'rating' in request.values:
        user_id = get_user_id()
        add_review_to_cmdi(id, user_id, request.values['body'], int(request.values['rating']))
        return jsonify(success=True), 201

    return jsonify(success=False), 400


@app.get('/reviews_user_interaction/<id>')
@authenticated
def reviews_user_interaction(id):
    user_id = get_user_id()
    return jsonify(get_reviews_user_interaction(id, user_id).model_dump())


@app.post('/review/<id>/report')
def report_abuse(id):
    if 'name' in request.values and 'email' in request.values and 'description' in request.values:
        # TODO: send email
        return jsonify(success=True), 200

    return jsonify(success=False), 400


@app.post('/like/<id>/<int:review_no>')
@authenticated
def post_like(id, review_no):
    user_id = get_user_id()
    persist_review_like_to_cmdi(id, review_no, user_id, True)
    return jsonify(success=True)


@app.post('/dislike/<id>/<int:review_no>')
@authenticated
def post_dislike(id, review_no):
    user_id = get_user_id()
    persist_review_like_to_cmdi(id, review_no, user_id, False)
    return jsonify(success=True)


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


if __name__ == '__main__':
    app.run()
