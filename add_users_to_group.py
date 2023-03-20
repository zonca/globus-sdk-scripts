import globus_sdk
from globus_sdk import GroupsClient, AuthClient
import toml
from utils import create_authorizer
import sys

globus_config = toml.load("globus_config.toml")
CLIENT_ID = globus_config["CLIENT_ID"]

client = globus_sdk.NativeAppAuthClient(CLIENT_ID)

auth_authorizer = create_authorizer("globus_auth_data.toml", client)

ac = AuthClient(authorizer=auth_authorizer)

groups_authorizer = create_authorizer("globus_groups_data.toml", client)

gc = GroupsClient(authorizer=groups_authorizer)

groups = gc.get_my_groups()
group = [g for g in groups if g["name"] == globus_config["GROUP_NAME"]][0]


import pandas as pd

users = pd.read_csv(sys.argv[1])

chunk_size = 50
for i in range(0, len(users), chunk_size):
    emails = list(users["Email Address"][i:i+chunk_size])
    identities = ac.get_identities(usernames=emails)
    ids = [{"identity_id":each["id"]} for each in identities["identities"]]
    gc.batch_membership_action(group["id"], actions={"add": ids})
