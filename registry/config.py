import os
import uuid

secret_key = os.environ.get('SECRET_KEY', uuid.uuid4().hex)
records_path = os.environ.get('RECORDS_PATH', './data/records/reviewed-publish')

oidc_server = os.environ.get('OIDC_SERVER')
oidc_client_id = os.environ.get('OIDC_CLIENT_ID')
oidc_client_secret = os.environ.get('OIDC_CLIENT_SECRET')
oidc_redirect_uri = os.environ.get('OIDC_REDIRECT_URI', 'http://localhost:5000/oidc_redirect')

es_host = os.environ.get("ES_HOST", "http://localhost:9200")
es_user = os.environ.get("ES_USER")
es_password = os.environ.get("ES_PASSWORD")
es_index = os.environ.get("ES_INDEX", "vocab")

email_smtp_host = os.environ.get('EMAIL_SMTP_HOST', 'localhost')
email_smtp_port = os.environ.get('EMAIL_SMTP_PORT', 8025)
email_sender = os.environ.get('EMAIL_SENDER', 'noreply@localhost')
email_recipient = os.environ.get('EMAIL_RECIPIENT', 'noreply@localhost')

