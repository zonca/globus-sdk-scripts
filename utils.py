import globus_sdk
import toml

def create_authorizer(auth_tokens_file, client):
    globus_data = toml.load(auth_tokens_file)

    auth_rt = globus_data["refresh_token"]
    auth_at = globus_data["access_token"]
    expires_at_s = globus_data["expires_at_seconds"]

    authorizer = globus_sdk.RefreshTokenAuthorizer(
                auth_rt, client, access_token=auth_at, expires_at=expires_at_s
                )
    return authorizer
