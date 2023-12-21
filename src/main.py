###
# ESP32-based dot LED matrix clock with auto sync to NTP servers
###

# TODO ideas
# - Disconnect from wifi after time sync
# - Resync once per day, reporting offset
# - Add webserver for wifi and timezone config
# - Add button support for access point/reset/webserver mode, show date
# - Add error handling ;)

# Micropython/NTP concepts taken from
# https://bhave.sh/micropython-ntp/

import time
import ntptime
import machine
import config as cfg
import network
from screen import config_screen


def wifi_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print("Connecting to network...")
        sta_if.active(True)
        sta_if.connect(cfg.WIFI_SSID, cfg.WIFI_PASSWORD)
        while not sta_if.isconnected():
            machine.idle()
    print("Network config:", sta_if.ifconfig())


def main():
    wifi_connect()
    screen = config_screen(cfg.SCREEN_BRIGHTNESS)

    # rtc = machine.RTC()
    ntptime.settime()

    UTC_OFFSET = -3 * 60 * 60
    actual_time = time.localtime(time.time() + UTC_OFFSET)
    # actual_time
    # (2023, 12, 20, 23, 12, 23, 2, 354)

    blinker = " "
    while True:
        if blinker == ":":
            blinker = " "
        else:
            blinker = ":"
        actual_time = time.localtime(time.time() + UTC_OFFSET)
        new_time = f"{actual_time[3]:02d}{blinker}{actual_time[4]:02d}{blinker}{actual_time[5]:02d}"

        screen.fill(0)
        screen.text(new_time, 0, 0, 1)
        screen.show()
        time.sleep(1)


main()
