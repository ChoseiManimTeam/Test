FROM gitpod/workspace-full

USER root

# 必要なLinuxパッケージだけをインストール（texliveはminimal構成）
RUN apt-get update && apt-get install -y \
    ffmpeg \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-latex-recommended \
    pkg-config \
    libcairo2-dev \
    libpango1.0-dev \
    python3-dev && \
    apt-get clean

# Pythonパッケージもインストール（Manim）
RUN pip install manim
