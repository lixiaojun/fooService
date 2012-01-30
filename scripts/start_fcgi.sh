#!/bin/bash
spawn-fcgi -f `pwd`/fcgi_fooservice.py -a 127.0.0.1 -p 9002
