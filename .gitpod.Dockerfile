FROM gitpod/workspace-full

USER root

# 必要なLinuxパッケージをインストール（texliveはminimal構成）
RUN apt-get update && apt-get install -y \
    ffmpeg \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-latex-recommended \
    pkg-config \
    libcairo2-dev \
    libpango1.0-dev \
    python3-dev \
    libgl1 \
    libegl1 \
    libxcb-xinerama0 \
    libxcb-cursor0 \
    libxkbcommon-x11-0 \
    libxcb-xinerama0 \
    libxcb1 \
    libx11-xcb1 \
    libxcb-render0 \
    libxcb-shape0 \
    libxcb-shm0 \ 
    && apt-get clean

# Pythonパッケージをインストール（Manim + manim-slides + GUIサポート）
RUN pip install manim PySide6 manim-slides
