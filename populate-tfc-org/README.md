### Set env vars

```bash
source secrets.op.sh
```

### Run Script

First, update `migration.json`. Probably a good idea to use a `venv` and you must use Python 3.

```python
pip install -i pip-reqs.txt
python main.py
```
