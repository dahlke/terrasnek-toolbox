from terrasnek.api import TFC
import os
import logging

UNITTEST_PREFIX = "terrasnek-unittest"

modules_to_purge = [
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
TFC_ORG = os.getenv("TFC_ORG", None)
SSL_VERIFY = os.getenv("SSL_VERIFY", None)

if __name__ == "__main__":
    api = TFC(TFC_TOKEN, url=TFC_URL, log_level=logging.DEBUG, verify=False)
    # logging.basicConfig(level=logging.DEBUG)
    api.set_org(TFC_ORG)

    listed_modules = api.registry_modules.list()["modules"]
    print(listed_modules)
    data = api.registry_modules.list()
    print(data)

    for module in listed_modules:
        module_name = module["name"]
        module_provider = module["provider"]

        if module_name in modules_to_purge:
          create_payload = create_module_payload
          create_payload["data"]["attributes"]["name"] = module_name

          print("creating module", module_name)
          created_module = api.registry_modules.create(create_payload)["data"]
          print("uploading module version for module", module_name)
          created_version = \
              api.registry_modules.create_version(\
                  module_name, module_provider, create_module_version_payload)["data"]
          print("purging module", module_name)
          api.registry_modules.destroy(module_name)

    """
    for module_name in modules_to_purge:
        module_name = module_name
        module_provider = "tfe"

        print("purging module", module_name)
        api.registry_modules.destroy(module_name)
    """