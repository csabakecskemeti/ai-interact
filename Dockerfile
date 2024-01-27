FROM python:3.11.7-slim-bookworm

RUN apt-get --yes update && \
    apt-get --yes --no-install-recommends install \
        linux-libc-dev \
        gcc \
        python3-dev \
        python3-evdev \
        python3-pip \
        tesseract-ocr \
        tk \
        x11-apps

# Set working directory.
ENV WORK_DIR="/aihub_app/"

WORKDIR $WORK_DIR

# Copy the application.
COPY aihub/ aihub/
COPY requirements.txt .

# Install the Python dependencies.
# RUN pip3 install -r requirements.txt
# TODO: Use cleaned up `requirements.txt`.
RUN pip3 install pillow pytesseract pyautogui pynput keyboard requests grpcio protobuf openai

# Redirect display.
ENV DISPLAY :0

# Start bootsrapping the application.
ENTRYPOINT cd aihub && python3 -m aihub_bootstrap
