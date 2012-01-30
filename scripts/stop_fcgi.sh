#!/bin/bash
kill $(pgrep -f `pwd`/fcgi_fooservice.py)
[ -e `pwd`/tmp/pid ] && rm `pwd`/tmp/pid

