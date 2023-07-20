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

TODO


## API

API is generated under `/api` folder

```json
{
    "date": "2023-07-20T11:05:00+02:00",
    "status": {
        "A+": "E",
        "A-": "U",
        "B+": "E",
        "B-": "S",
        "O+": "E",
        "O-": "Z",
        "AB+": "S",
        "AB-": "S"
    }
}
```


## Docker

Build image

    $ docker-compose build

and run

    $ docker-compose up

### Deal with Facebook tokens

To generate a page access token follow this guide: https://developers.facebook.com/docs/pages/access-tokens/

You need a user access token to proceed.

## License

Released under MIT License by @astagi
