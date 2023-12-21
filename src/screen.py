import machine
import config as cfg
import max7219_async as max7219

def config_screen(brightness=cfg.SCREEN_BRIGHTNESS):
    # Use hardware SPI id #1 on ESP32 -> Pins sck 14, mosi 13, miso 12
    # https://docs.micropython.org/en/latest/esp32/quickref.html#hardware-spi-bus
    spi = machine.SPI(
        1,
        baudrate=10000000,
        sck=machine.Pin(cfg.PIN_CLK),
        mosi=machine.Pin(cfg.PIN_DATA),
    )

    # Matrix of 4 8x8 modules: 32x8 pixels
    screen = max7219.Max7219(
        cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT, spi, machine.Pin(cfg.PIN_CS)
    )

    # Adjust brightness: 1 to 15
    screen.brightness(brightness)

    return screen