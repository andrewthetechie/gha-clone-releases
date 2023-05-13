FROM python:3.11-slim AS builder
WORKDIR /app

# install build requirements
RUN apt-get update && apt-get install -y binutils patchelf upx build-essential scons

# copy the app
COPY ./ /app

# install python build requirements
RUN pip install --no-warn-script-location --upgrade virtualenv pip poetry pyinstaller staticx --constraint=package-requirements.txt

# build the app
RUN poetry build
# Install the app
RUN pip install dist/gha_clone_releases*.whl

# pyinstaller package the app
RUN python -OO -m PyInstaller -F gha_clone_releases/main.py --name clone-releases --hidden-import _cffi_backend
# static link the repo-manager binary
RUN cd ./dist && \
    staticx -l $(ldconfig -p| grep libgcc_s.so.1 | awk -F "=>" '{print $2}' | tr -d " ") --strip clone-releases clone-releases-static && \
    strip -s -R .comment -R .gnu.version --strip-unneeded clone-releases-static
# will be copied over to the scratch container, pyinstaller needs a /tmp to exist
RUN mkdir /app/tmp

FROM scratch

ENTRYPOINT ["/clone-releases"]

COPY --from=builder /app/dist/clone-releases-static /clone-releases
COPY --from=builder /app/tmp /tmp
