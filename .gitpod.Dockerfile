# Pythonの最新化とpipアップグレード
RUN pyenv global 3.12.9 \
    && pip install --upgrade pip

# デフォルトで入れておくPythonパッケージ（必要なら追加）
RUN pip install manim