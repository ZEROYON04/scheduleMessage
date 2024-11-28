# ベースイメージを指定
FROM python:latest



# 必要な依存パッケージをインストール
RUN apt-get update && apt-get install -y \
    wget \
    xvfb \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Miniconda をインストール
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/miniconda3 && \
    rm Miniconda3-latest-Linux-x86_64.sh

ENV PATH="/opt/miniconda3/bin:$PATH"


# Conda をアップデート
RUN conda update -n base -c defaults conda && \
    pip install --upgrade pip

# 作業ディレクトリを設定
WORKDIR /workspace

# 他の環境からエクスポートされた environment.yml をコピー
COPY environment.yml environment.yml

# Conda 環境を作成
RUN conda env create -f environment.yml

RUN pip install playwright==1.49.0
RUN playwright install --with-deps

# 必要なソースコードをコピー
COPY . /workspace/

# conda init を実行して bashrc を設定
RUN /opt/miniconda3/bin/conda init bash

# 環境を有効化するために .bashrc を適切に設定
RUN echo "conda activate lineMessage" >> ~/.bashrc



