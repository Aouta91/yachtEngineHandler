#!/usr/bin/env bash
docker system prune -f
docker image build -t yacht:latest -f docker/Dockerfile .
