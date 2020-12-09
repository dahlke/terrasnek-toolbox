import json
import os
import hashlib
import base64
import time
from terrasnek.api import TFC

TFC_URL = os.environ["TFC_URL"]
TFC_TOKEN = os.environ["TFC_TOKEN"]
TFC_ORG = os.environ["TFC_ORG"]
NUM_WORKSPACES = int(os.environ["NUM_WORKSPACES"])


if __name__ == "__main__":
    mapping = []

    # Write the updated version of the migration targets so we can
    # reference what occurred later
    with open("mapping.json", "r") as f:
        mapping = json.loads(f.read())

    api = TFC(TFC_TOKEN, url=TFC_URL)
    api.set_org(TFC_ORG)

    existing_workspaces = api.workspaces.list()["data"]
    existing_workspace_names = [ws["attributes"]["name"] for ws in existing_workspaces]
    oauth_clients = api.oauth_clients.list()["data"]
    oauth_token_id = None

    for oac in oauth_clients:
        org_name = oac["relationships"]["organization"]["data"]["id"]
        if org_name == TFC_ORG:
            oauth_token_id = oac["relationships"]["oauth-tokens"]["data"][0]["id"]

    for mt in mapping:
        for i in range(NUM_WORKSPACES):
            workspace_name = f"%s-%d" % (mt["workspace-name"], i)
            if workspace_name in existing_workspace_names:
                continue

            # Configure our create payload with the data
            # from the migration targets JSON file
            create_ws_payload = {
                "data": {
                    "attributes": {
                        "name": workspace_name,
                        "terraform_version": mt["tf-version"],
                        "working-directory": mt["working-dir"],
                        "vcs-repo": {
                            "identifier": mt["repo"],
                            "oauth-token-id": oauth_token_id,
                            "branch": mt["branch"],
                            "default-branch": True
                        }
                    },
                    "type": "workspaces"
                }
            }

            # Create a workspace with the VCS repo attached
            ws = api.workspaces.create(create_ws_payload)
            ws_id = ws["data"]["id"]

            # Read in the statefile contents we just pulled from GCS
            raw_state_bytes = None
            with open(mt["statefile-local-path"], "rb") as infile:
                raw_state_bytes = infile.read()

            # Perform a couple operations on the data required for the
            # create payload. See more detail here:
            # https://www.terraform.io/docs/cloud/api/state-versions.html
            state_hash = hashlib.md5()
            state_hash.update(raw_state_bytes)
            state_md5 = state_hash.hexdigest()
            state_b64 = base64.b64encode(raw_state_bytes).decode("utf-8")

            # Build the payload
            create_state_version_payload = {
                "data": {
                    "type": "state-versions",
                    "attributes": {
                        "serial": 1,
                        "md5": state_md5,
                        "state": state_b64
                    }
                }
            }

            # State versions cannot be modified if the workspace isn't locked
            api.workspaces.lock(ws_id, {"reason": "migration script"})

            # Create the state version
            api.state_versions.create(ws_id, create_state_version_payload)
            print(workspace_name, "created")

            # Unlock the workspace so other people can use it
            api.workspaces.unlock(ws_id)
    """
    workspaces = api.workspaces.list()["data"]
    for ws in workspaces:
        run_create_payload = {
            "data": {
                "attributes": {
                    "is-destroy": False,
                    "message": "test"
                },
                "type": "runs",
                "relationships": {
                    "workspace": {
                        "data": {
                            "type": "workspaces",
                            "id": ws["id"]
                        }
                    }
                }
            }
        }
        api.runs.create(run_create_payload)
    """