FROM debian:buster-slim

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    jq \
    python3 \
    python3-pip \
    haskell-stack \
    cabal-install \
    ghc \
    git \
  && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/koalaman/shellcheck.git shellcheck \
  && cd /shellcheck \
  && git checkout 37e78141bd57f56b2a8d7ec0c91e76edec6a9dc5 \
  && cabal update \
  && cabal install \
  && cabal build \
  && rm -rf /shellcheck

ENV PATH="${HOME}/.cabal/bin:${PATH}"

RUN pip3 install --no-cache-dir tqdm==4.27.0

WORKDIR /app

COPY app.hs /build/
RUN ghc /build/app.hs

COPY filter-*.jq /filters/
COPY app.py /app.py

ENTRYPOINT [ "python3", "/app.py" ]
