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

# Define local time zone as UTC-3
UTC_OFFSET = cfg.UTC_OFFSET


def wifi_connect():
    # Disable access point mode
    ap = network.WLAN(network.AP_IF)
    ap.active(False)

    # Connect to wifi network
    station = network.WLAN(network.STA_IF)
    if not station.isconnected():
        print("Connecting to network...")
        station.active(True)
        station.connect(cfg.WIFI_SSID, cfg.WIFI_PASSWORD)
        while not station.isconnected():
            machine.idle()
    print("Network config:", station.ifconfig())


def wifi_disable():
    # Disable wifi station
    station = network.WLAN(network.STA_IF)
    station.active(False)


def screen_write(screen, msg):
    screen.fill(0)
    screen.text(msg, 0, 0, 1)
    screen.show()


def main():
    # Configure dot matrix LED screen
    screen = config_screen(cfg.SCREEN_BRIGHTNESS)

    # Connect to wifi network
    try:
        wifi_connect()
    except:
        screen_write(screen, "wifi ERR")
        return False
    else:
        screen_write(screen, "wifi OK")
        time.sleep(1)

    # Sync internal RTC with NTP servers. Only done once on startup. From then on, ESP32's internal
    # real time clock (RTC())
    try:
        ntptime.settime()
    except:
        screen_write(screen, "NTP ERR")
        return False
    else:
        screen_write(screen, "NTP OK")
        time.sleep(1)

    # Wifi no longer needed. Disable to save energy
    wifi_disable()

    # Characters to create a dynamic effect every X seconds
    blinker = [" ", ":"]
    index_blinker = 1

    time_iteration = time.ticks_ms()

    while True:
        # Every 500 ms, refresh screen
        if time.ticks_diff(time.ticks_ms(), time_iteration) >= 500:
            time_iteration = time.ticks_ms()

            # Cycle between ":" and " " to show a 1-second blink
            index_blinker = int(not index_blinker)

            # Get corrected time applying local UTC offset
            # Result format is (year, month, day, hour, minutes, seconds, weekday, yearday)
            # See https://docs.python.org/3/library/time.html#time.struct_time
            actual_time = time.localtime(time.time() + UTC_OFFSET)

            # Construct the 8-characters string to show on the dot matrix screen
            new_time = f"{actual_time[3]:02d}{blinker[index_blinker]}{actual_time[4]:02d}{blinker[index_blinker]}{actual_time[5]:02d}"

            # Show time on screen
            screen_write(screen, new_time)
        else:
            machine.idle()


main()
