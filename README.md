<p align="center">
    <img src="https://raw.githubusercontent.com/meteosangue/meteosangue.github.io/master/tile-wide.png"/>
    <br>
    <a href="https://codecov.io/gh/meteosangue/meteosangue">
      <img src="https://codecov.io/gh/meteosangue/meteosangue/branch/master/graph/badge.svg" />
    </a>
    <a href="https://travis-ci.org/meteosangue/meteosangue">
      <img src="https://travis-ci.org/meteosangue/meteosangue.svg?branch=master" />
    </a>
</p>

## Quickstart

    pip install -r requirements.txt

## Test

Enter your virtual env and install requirements

    $ pip install -r requirements-test.txt

Launch

    $ python manage.py test


## Docker

Build image

    $ docker-compose build

and run

    $ docker-compose up

## Our API

`/api/bloodgroups` : gives you all bloodgroups in database


```json
[

    {
        "status": "S",
        "status_expanded": "Stabile",
        "groupid": "A+",
        "id": 1
    },
    {
        "status": "S",
        "status_expanded": "Stabile",
        "groupid": "AB+",
        "id": 2
    },

]
```


If you want retrieve a specific blood group (example *AB+*) you can use `/api/bloodgroups/AB+`

`/api/bloodgroups/:Groupid`
- **Groupid** : Group id (AB+, AB-, A+ ...)

### Deal with Facebook tokens

To generate a page access token follow this guide: https://developers.facebook.com/docs/pages/access-tokens/

You need a user access token to proceed.

## License

Released under MIT License by @astagi
