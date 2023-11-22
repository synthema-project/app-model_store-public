import mlflow as mlf

# @@@@@@@ KC SETTINGS @@@@@@
# realm = os.getenv('KEYCLOAK_REALM')
# keycloack_url = os.getenv('KEYCLOAK_URL')
# client_id = os.getenv('KEYCLOAK_CLIENT_ID')
# authorization_url = keycloack_url + "realms/" + realm + "/protocol/openid-connect/auth"
# token_url = keycloack_url + "realms/" + realm + "/protocol/openid-connect/token"
# keycloack_admin = os.getenv('KEYCLOAK_ADMIN')
from hydra import initialize, compose

initialize(version_base=None, config_path="conf")
cfg = compose(config_name="config")
TRACKING_URI = cfg["mlflow"]["ip"]
HOST = cfg["app"]["host"]
PORT = cfg["app"]["port"]

# t_cfg = compose(config_name="test_upm")
# FTRACKING_URI=t_cfg["ip"]

mlf.set_tracking_uri(TRACKING_URI)
client = mlf.MlflowClient(tracking_uri=TRACKING_URI)
