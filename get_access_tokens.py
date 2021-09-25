import globus_sdk
from globus_sdk import GroupsClient
import toml

CLIENT_ID = toml.load("globus_config.toml")["CLIENT_ID"]

client = globus_sdk.NativeAppAuthClient(CLIENT_ID)
client.oauth2_start_flow(refresh_tokens=True, requested_scopes=["openid", "profile", "email", "urn:globus:auth:scope:transfer.api.globus.org:all", GroupsClient.scopes.all])

authorize_url = client.oauth2_get_authorize_url()
print("Please go to this URL and login: {0}".format(authorize_url))

auth_code = input("Please enter the code you get after login here: ").strip()
token_response = client.oauth2_exchange_code_for_tokens(auth_code)

globus_auth_data = token_response.by_resource_server["auth.globus.org"]
globus_transfer_data = token_response.by_resource_server["transfer.api.globus.org"]
globus_groups_data = token_response.by_resource_server["groups.api.globus.org"]

import toml
with open("globus_auth_data.toml", "w") as f:
    toml.dump(globus_auth_data, f)
with open("globus_transfer_data.toml", "w") as f:
    toml.dump(globus_transfer_data, f)
with open("globus_groups_data.toml", "w") as f:
    toml.dump(globus_groups_data, f)
