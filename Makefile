DEV_ESP32=/dev/ttyACM0

all: upload

clean:
	rm -rf venv && rm -rf *.egg-info && rm -rf dist && rm -rf build #&& rm -rf *.log*

upload:
	ampy --port ${DEV_ESP32} put ./src/main.py
	ampy --port ${DEV_ESP32} put ./src/config.py
	ampy --port ${DEV_ESP32} put ./src/screen.py

upload_main:
	ampy --port ${DEV_ESP32} put ./src/main.py
