#!/bin/bash
export FETCH_SITE_WAIT=0
function quit {
    killall python
    exit $1
}

coverage run manage.py test || quit 1
coverage report
quit 0
