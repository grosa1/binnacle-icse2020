FROM python:3.7.6-slim-stretch

RUN apt-get update \
  && apt-get install -y --no-install-recommends xz-utils \
  && rm -rf /var/apt/lists*

RUN pip install --no-cache dockerfile==2.2.0 tqdm

COPY . /app/

ENTRYPOINT [ "/app/entrypoint.sh" ]
