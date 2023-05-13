FROM python:3.11-slim AS builder
WORKDIR /app

# install build requirements
RUN apt-get update && apt-get install -y binutils patchelf upx build-essential scons
RUN pip install --no-warn-script-location --upgrade virtualenv pip pyinstaller staticx

# copy the app
COPY ./ /app

## build the app
# install requirements
RUN pip install --upgrade pip --constraint=package-requirements.txt && pip install .
# pyinstaller package the app
