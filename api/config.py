import os

# GLOBAL VARS
global_vars = {
    "running": False,
    "task": None
}

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL_MLFLOW")
# WORKER_API = os.getenv("WORKER_API")

# @@@@@@@ KC SETTINGS @@@@@@
# realm = os.getenv('KEYCLOAK_REALM')
# keycloack_url = os.getenv('KEYCLOAK_URL')
# client_id = os.getenv('KEYCLOAK_CLIENT_ID')
# authorization_url = keycloack_url + "realms/" + realm + "/protocol/openid-connect/auth"
# token_url = keycloack_url + "realms/" + realm + "/protocol/openid-connect/token"
# keycloack_admin = os.getenv('KEYCLOAK_ADMIN')
