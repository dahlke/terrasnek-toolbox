from terrasnek.api import TFC
import os

modules_to_purge = [
    "terrasnek-unittest-aa2fc0e9d0c33168",
    "terrasnek-unittest-57a8d0769b709c38",
    "terrasnek-unittest-462bfb29abfe2fed",
    "terrasnek-unittest-5f3d643d50228247"
]

create_module_payload = {
  "data": {
    "type": "registry-modules",
    "attributes": {
      "name": None,
      "provider": "tfe"
    }
  }
}

create_module_version_payload = {
  "data": {
    "type": "registry-module-versions",
    "attributes": {
      "version": "0.0.1"
    }
  }
}

# TODO: build this into the purge logic.
TFC_TOKEN = os.getenv("TFC_TOKEN", None)
TFC_URL = os.getenv("TFC_URL", None)

if __name__ == "__main__":
    api = TFC(TFC_TOKEN, url=TFC_URL)
    api.set_org("terrasnek-unittest")

    modules = api.registry_modules.list()["modules"]

    for module in modules:
        module_name = module["name"]
        module_provider = module["provider"]

        create_payload = create_module_payload
        create_payload["data"]["attributes"]["name"] = module_name

        created_module = api.registry_modules.create(create_payload)["data"]
        created_version = \
            api.registry_modules.create_version(\
                module_name, module_provider, create_module_version_payload)["data"]
