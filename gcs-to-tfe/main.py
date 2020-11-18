import json
import os
import hashlib
import base64
import time
from terrasnek.api import TFC
from google.cloud import storage

TFC_TOKEN = os.environ["TFC_TOKEN"]
TFC_ORG = os.environ["TFC_ORG"]
GCS_BUCKET = os.environ["GCS_BUCKET"]


if __name__ == "__main__":
    migration_targets = []

    with open("migration.json", "r") as f:
        migration_targets = json.loads(f.read())

    # Define the bucket to search
    bucket_name = GCS_BUCKET

    # Create the GCS client
    storage_client = storage.Client()

    # Retrieve the blob info from the GCS bucket
    blobs = storage_client.list_blobs(bucket_name)

    # Loop through all the blobs and download any statefiles that match
    # one of the migration targets
    for blob in blobs:
        full_blob_path = f"{bucket_name}/{blob.name}"

        # Check to see if we have found a TF statefile
        if '.tfstate' in full_blob_path:
            # If so, we want to carve up the path to get some of the
            # individual components for use
            split_path = full_blob_path.split("/")
            parent_bucket_path = "/".join(split_path[:-1])
            statefile_name = split_path[-1]

            # Loop through the migration_targets file we defined
            for mt in migration_targets:
                # If the bucket path for this statefile matches
                # the one we want to pull over to TFC
                if parent_bucket_path == mt["bucket"]:
                    # Download the statefile to a local copy
                    bucket = storage_client.bucket(bucket_name)
                    blob = bucket.blob(blob.name)
                    filename = f"statefiles/{statefile_name}"
                    blob.download_to_filename(filename)

                    # And update migration targets with the information we
                    # parsed above
                    mt["blob-path"] = full_blob_path
                    mt["statefile-name"] = statefile_name
                    mt["statefile-local-path"] = filename

    # Write the updated version of the migration targets so we can
    # reference what occurred later
    with open('migration-enriched.json', 'w') as f:
        json.dump(migration_targets, f, indent=4)

    api = TFC(TFC_TOKEN)
    api.set_org(TFC_ORG)

    workspaces = api.workspaces.list()
    oauth_clients = api.oauth_clients.list()["data"]
    oauth_token_id = None

    for oac in oauth_clients:
        org_name = oac["relationships"]["organization"]["data"]["id"]
        if org_name == TFC_ORG:
            oauth_token_id = oac["relationships"]["oauth-tokens"]["data"][0]["id"]

    for mt in migration_targets:
        # Configure our create payload with the data
        # from the migration targets JSON file
        create_ws_payload = {
            "data": {
                "attributes": {
                    "name": mt["workspace-name"],
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

        # Unlock the workspace so other people can use it
        api.workspaces.unlock(ws_id)
