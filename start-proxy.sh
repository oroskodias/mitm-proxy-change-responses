#!/bin/bash

mitmproxy --set block_global=false -s ./mitm-script.py -p 888
