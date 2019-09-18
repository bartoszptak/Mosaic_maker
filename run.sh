#!/bin/bash
docker build -t app .
docker run --rm --name mosaicMaker -p 5000:5000 app