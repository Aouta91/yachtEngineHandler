#!/usr/bin/env bash
docker run --rm -it --privileged -p 8000:8000 -v `pwd`:/workspace yacht-dev:latest /bin/bash -c "uvicorn server:app --reload --host=0.0.0.0"
