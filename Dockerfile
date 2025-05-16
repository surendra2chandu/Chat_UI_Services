FROM python:3.10.13-slim

# ILW Python package index
ARG ILW_PY_PKG_IDX_TOKEN_NAME
ARG ILW_PY_PKG_IDX_TOKEN_VALUE

ENV DOCKER_REGISTRY ilwcr.azurecr.us

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN python -m pip install --upgrade --no-cache-dir pip && \
    pip install --no-cache-dir -r requirements.txt

COPY ./src /code/src

CMD ["streamlit", "run", "src/frontend/UI.py","--server.address", "0.0.0.0", "--server.port","80"]
