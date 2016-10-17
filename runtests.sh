#!/bin/bash

function quit {
    killall python
    exit $1
}

coverage run manage.py test || quit 1
coverage report
quit 0
