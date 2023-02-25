FROM python:3.11-slim AS builder
WORKDIR /app

# install build requirements
RUN apt-get update && apt-get install -y binutils patchelf upx build-essential scons
RUN pip install --no-warn-script-location --upgrade virtualenv pip pyinstaller staticx

# copy the app
COPY Docker/builder/rootfs/requirements.txt ./
COPY main.py ./

## build the app
# install requirements
RUN pip install -r requirements.txt
# pyinstaller package the app
RUN python -OO -m PyInstaller -F main.py --name clone-releases --hidden-import _cffi_backend
# static link the repo-manager binary
RUN cd ./dist && \
    staticx clone-releases clone-releases-static
# will be copied over to the scratch container, pyinstaller needs a /tmp to exist
RUN mkdir /app/tmp

FROM scratch

ENTRYPOINT ["/clone-releases"]

COPY --from=builder /app/dist/clone-releases-static /clone-releases
COPY --from=builder /app/tmp /tmp
