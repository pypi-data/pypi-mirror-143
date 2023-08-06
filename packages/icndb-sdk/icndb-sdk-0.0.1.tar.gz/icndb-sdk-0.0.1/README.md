# icndb-sdk

Unofficial SDK for some Chuck Norris jokes.

## Getting Started

```shell
python3 -m venv venv
source venv/bin/activate
pip install icndb-sdk
```

## Examples

```python
In [1]: from icndb_sdk import API

In [2]: chuck = API()

In [3]: chuck.get_jokes_random()
Out[3]:
{'type': 'success',
 'value': [{'id': 203,
   'joke': 'Chuck Norris can lead a horse to water AND make it drink.',
   'categories': []}]}

In [4]: chuck.get_jokes_specific(id_number=503)
Out[4]:
{'type': 'success',
 'value': {'id': 503,
  'joke': 'Chuck Norris protocol design method has no status, requests or responses, only commands.',
  'categories': ['nerdy']}}

In [5]: PARAMS = {"firstName": "Julio", "lastName": "PDX"}

In [6]: chuck.get_jokes_specific(params=PARAMS, id_number=503)
Out[6]:
{'type': 'success',
 'value': {'id': 503,
  'joke': 'Julio PDX protocol design method has no status, requests or responses, only commands.',
  'categories': ['nerdy']}}

In [7]:
```