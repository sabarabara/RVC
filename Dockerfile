# 第一段階: アセット取得
FROM alpine:3.19.1 as assets

RUN apk add \
      --update \
      --no-cache \
        bash \
        git \
        git-lfs \
        dos2unix

COPY --chmod=755 ./assets-download.sh /assets-download.sh

RUN dos2unix /assets-download.sh

RUN /assets-download.sh 88e42f0cb3662ddc0dd263a4814206ce96d53214 assets

# 第二段階: アプリ本体
FROM python:3.10.14-bullseye as app

SHELL [ "/bin/bash", "-c" ]

# ffmpeg など必要なツールをインストール
RUN apt update && \
    apt install -y \
      libsndfile1 \
      libsndfile1-dev \
      ffmpeg && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

# assets 取得
COPY --from=assets /assets /assets

WORKDIR /app

# poetry セットアップと依存追加
COPY ./pyproject.toml .

RUN pip install \
      --no-cache-dir \
      "poetry==1.7.1" && \
    poetry config virtualenvs.create false && \
    poetry install \
      --no-interaction \
      --no-root && \
    poetry add flask pydub gtts && \
    poetry cache clear pypi --all

# ✅ 以下を追加して手動docker cpを不要にする
COPY ./assets ./assets
COPY ./rvc ./rvc
COPY ./run_infer.py ./run_infer.py
COPY ./.env ./.env
COPY ./server.py ./server.py 

# 起動コマンド
CMD [ "poetry", "run", "poe", "rvc-api" ]
