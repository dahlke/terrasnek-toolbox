# Update All Sensitive Variables

```bash
virtualenv venv
source venv/bin/activate
pip install -r pip-reqs.txt


export TFC_URL=""
export TFC_TOKEN=""
export TFC_ORG=""

export AWS_ACCESS_KEY_ID=""
export AWS_SECRET_ACCESS_KEY=""

python main.py
```
