# NeverNoneDict
Python Dictionary that does not have None values.

### Installing

You can start using nn dict by installing it using pip.
```bash
pip install nndict
```


### Using nndict
```python
>nndict_ = nndict({"a": 2, "b": None, "c": {"d": None}})
>print(nndict_)
{'a': 2, 'c': {}}

>nndict_ = nndict({"a": 2})
>print(nndict_)
{'a': 2}

>nndict_["a"] = None
>print(nndict_)
{}
```

## Running the tests
Make sure you have the python versions listed in tox.ini installed. Then run tox:
```bash
tox
```

## Authors

* **Tiago Santos** - *Initial work* - tiago.santos@vizidox.com

