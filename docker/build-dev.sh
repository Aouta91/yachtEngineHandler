#!/usr/bin/env bash
docker system prune -f
docker image build --no-cache -t yacht-dev:latest -f docker/Dockerfile-dev .
