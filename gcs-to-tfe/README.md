### Set env vars

```bash
export GOOGLE_APPLICATION_CREDENTIALS=""
export TFE_TOKEN=""
export TFE_ORG=""
```

### Run Script

First, update `migration.json`. Probably a good idea to use
a `venv` and you must use Python 3.

*TODO / NOTE: This has not been modified to run on anything after `terrasnek v0.0.2`*

```python
pip install -i pip-reqs.txt
python main.py
```
