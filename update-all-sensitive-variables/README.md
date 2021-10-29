# Update All Sensitive Variables

Setup a virtual environment.

```bash
virtualenv venv
source venv/bin/activate
pip install -r pip-reqs.txt
```

Set the variables you need to communicate with TFE.

```bash
export TFC_URL=""
export TFC_TOKEN=""
export TFC_ORG=""
```

Set the new AWS sensitive variables in your environment.

```bash
export AWS_ACCESS_KEY_ID=""
export AWS_SECRET_ACCESS_KEY=""
```

Run the script and update all the workspaces with those new sensitive variables.

```bash
python main.py
```
