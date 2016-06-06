# myshows-python3
This is a myshows.me Python API.

# Quick Start
```
pip install myshows
```
# Usage APIv1 (incomplete support, but with auth)
```python
>>> import myshows
>>> api = myshows.session()
>>> api.shows(1)['title']
'House'
>>> api.shows(1)['ruTitle']
'Доктор Хаус'
>>> api.user_profile('farestz')['stats']
{'remainingEpisodes': 83, 'watchedDays': 60.4, 'remainingHours': 60.8, 'totalHours': 1509.3, 'watchedEpisodes': 2199, 'remainingDays': 2.5, 'totalEpisodes': 2282, 'watchedHours': 1448.5, 'totalDays': 62.9}
```

See https://api.myshows.me for detailed API guide.

# Usage APIv2 (complete support, but without auth (oauth later))
```python
>>> import myshows
>>> api = myshows.apiv2_beta()
>>> response = api.shows.GetById(showId=1).json()
>>> response['result']['originalTitle']
'House'
```

See https://api.myshows.me/shared/doc/ for detailed API guide.
