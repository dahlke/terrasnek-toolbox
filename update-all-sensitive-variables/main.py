import json
import os
import hashlib
import base64
import time
from terrasnek.api import TFC

TFC_URL = os.environ["TFC_URL"]
TFC_TOKEN = os.environ["TFC_TOKEN"]
TFC_ORG = os.environ["TFC_ORG"]
AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]

if __name__ == "__main__":
	api = TFC(TFC_TOKEN, url=TFC_URL)
	api.set_org(TFC_ORG)

	# Get all the workspaces
	all_ws = api.workspaces.list_all()["data"]

	# Loop through each workspace
	for ws in all_ws:
		ws_id = ws["id"]
		# List all of the variables in the workspace
		all_vars = api.workspace_vars.list(ws["id"])["data"]

		# Loop through all the variables in the workspace
		for var in all_vars:
			key = var["attributes"]["key"]
			var_id = var["id"]

			# If the key matches one of the values we need to update, update the variable
			if key == "AWS_ACCESS_KEY_ID":
				update_payload = {
					"data": {
						"id": var_id,
						"attributes": {
							"key": "AWS_ACCESS_KEY_ID",
							"value": AWS_ACCESS_KEY_ID,
							"description": "",
							"category": "env",
							"hcl": False,
							"sensitive": False
						},
						"type":"vars"
					}
				}
				print("updating", update_payload)
				api.workspace_vars.update(ws_id, var_id, update_payload)
			elif key == "AWS_SECRET_ACCESS_KEY":
				update_payload = {
					"data": {
						"id": var_id,
						"attributes": {
							"key": "AWS_SECRET_ACCESS_KEY",
							"value": AWS_SECRET_ACCESS_KEY,
							"description": "",
							"category": "env",
							"hcl": False,
							"sensitive": True
						},
						"type":"vars"
					}
				}
				api.workspace_vars.update(ws_id, var_id, update_payload)
