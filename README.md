# NTP synchronized LED matrix clock

This simple project implements a more than fairly accurate clock based on an ESP32-S2 microcontroller, and a 8\*8\*8 LED matrix screen.
Upon boot the microcontroller synchronizes its internal real time clock (RTC) with the nearest Network Time Protocol (NTP) server, providing an accuracy in the order of tens of milliseconds. From then on, the microcontroller disconnects from the internet and continues ticking on its own.   

Empirically, the [ESP32-S2 RTC](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/system_time.html) drifts reasonably slowly from the original setup. More testing is needed to present better data, but after running for several days clock time remains accurate within less than 1 second. A reboot will resync time, if needed.

![schematic diagram](img/demo.gif)

# TODO list
- Resync once per day, reporting offset.
- Add webserver for wifi and timezone configuration.
- Add button support to show date.
- Improve error handling ;)