# myshows-python3
This is a myshows.me Python API.

# Quick Start
```
pip install myshows
```
# Usage
```python
>>> import myshows
>>> api = myshows.session()
>>> api.shows(1)['title']
'House'
>>> api.shows(1)['ruTitle']
'Доктор Хаус'
```