import adafruit_ntp
import socketpool
import displayio
import terminalio
import board
import os
import rtc
import time
import wifi

from adafruit_st7789 import ST7789
from adafruit_display_text import label
from adafruit_datetime import datetime
from tzdb import timezone

font_color = 0x55AA55
font_scale = 9
background_color = 0x111111
last_hour = -1
last_minute = -1
has_fetched_time = False
TIME_ZONE = "America/New_York"
#NTP_SERVER = "0.north-america.pool.ntp.org"
#NTP_SERVER = "1.north-america.pool.ntp.org"
#NTP_SERVER = "2.north-america.pool.ntp.org"
NTP_SERVER = "3.north-america.pool.ntp.org"

# Try to set up the network
pool = None
try:
    # Depends on settings.toml for Wifi config
    wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))
    pool = socketpool.SocketPool(wifi.radio)
    print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])
    print("My IP address is", wifi.radio.ipv4_address)
except Exception as error:
    print("Error setting up the network", error)

# Create a clock
real_time_clock = rtc.RTC()
# get the NTP time
ntp = adafruit_ntp.NTP(pool, server=NTP_SERVER, tz_offset=0)
# update the real time clock to current time
real_time_clock.datetime = ntp.datetime

utc_now = time.time()
utc_now_dt = datetime.fromtimestamp(utc_now)
localtime = utc_now_dt + timezone(TIME_ZONE).utcoffset(utc_now_dt)
timezone_offset = timezone(TIME_ZONE).utcoffset(utc_now_dt)

# Set up the display
displayio.release_displays()
spi = board.SPI()
display_bus = displayio.FourWire(
    spi,
    command=board.D16,
    chip_select=board.D5,
    reset=board.D9
)
display = ST7789(display_bus, width=280, height=240, rowstart=20, rotation=270)

# setup colors
color_bitmap = displayio.Bitmap(280, 240, 1)
color_palette = displayio.Palette(1)
color_palette[0] = background_color

# Set up drawing utils
splash = displayio.Group()
display.show(splash)
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

txt_splash = displayio.Group()
txt_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
txt_splash.append(txt_sprite)

def fetch_time():
    print("Fetching time")
    if not pool:
        return False
    try:
        print("Getting NTP time")
        real_time_clock.datetime = ntp.datetime
        print("Fetched time")
        return True
    except Exception as error:
        print("Exception fetching time", error)
        return False

def draw_label(group, txt, scale, color, x, y):
    text_group = displayio.Group(scale=scale, x=x, y=y)
    text_area = label.Label(terminalio.FONT, text=txt, color=color)
    text_group.append(text_area)  # Subgroup for text scaling
    group.append(text_group)

while True:
    should_fetch = has_fetched_time is False
    should_draw = False
    if real_time_clock.datetime.tm_hour != last_hour:
        should_fetch = True # Check the network time once an hour
        should_draw = True
        last_hour = real_time_clock.datetime.tm_hour
    if real_time_clock.datetime.tm_min != last_minute:
        should_draw = True
        last_minute = real_time_clock.datetime.tm_min
    if should_fetch:
        has_fetched_time = has_fetched_time or fetch_time()
    if should_draw:
        splash.pop()
        utc_now = time.time()
        utc_now_dt = datetime.fromtimestamp(utc_now)
        localtime = utc_now_dt + timezone(TIME_ZONE).utcoffset(utc_now_dt)
        display_time = f'{localtime.hour:02}:{localtime.minute:02}'
        draw_label(splash, f'{display_time}', font_scale, font_color, 10, 80)
    time.sleep(1)
