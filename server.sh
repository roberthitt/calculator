#!/usr/bin/env bash

python -m sanic calculator.server.app --host=0.0.0.0 --port=8080 --workers=4