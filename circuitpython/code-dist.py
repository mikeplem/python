import time
import board
import terminalio
import displayio
from adafruit_display_text import label
from adafruit_st7789 import ST7789

# This code is a variant of the example code from the Adafruit guides. 
# See the root README for links to those.

print("Starting TRS-80 Demo")

font_color = 0x55AA55
font_scale = 2
line_height = 30 
background_color = 0x111111
left_margin = 15
sleep_between_text = 1.25

# Release any resources currently in use for the displays
displayio.release_displays()

spi = board.SPI()
tft_cs = board.D5
tft_dc = board.D16

display_bus = displayio.FourWire(
    spi, command=tft_dc, chip_select=tft_cs, reset=board.D9
)

display = ST7789(display_bus, width=280, height=240, rowstart=20, rotation=270)

# Make the display context
splash = displayio.Group()
display.show(splash)

# Set up a color palette
color_bitmap = displayio.Bitmap(280, 240, 1)
color_palette = displayio.Palette(1)
color_palette[0] = background_color

# Set up a TileGrid into which we'll put the text
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)


def draw_label(txt, scale, color, x, y):
    '''Create a text Group, add a Label, and append it to splash'''
    text_group = displayio.Group(scale=scale, x=x, y=y)
    text_area = label.Label(terminalio.FONT, text=txt, color=color)
    text_group.append(text_area)  # Subgroup for text scaling
    splash.append(text_group)

def draw_text_array(txt=[]):
    '''Write a series of lines of text to the display'''
    for i in range(1, len(txt) + 1):
        draw_label(txt[i - 1], font_scale, font_color, left_margin, (i + 1) * line_height)
        time.sleep(sleep_between_text)

# Set up an array of text (you can change it to whatever you want!)
text_lines = [
    "TINY TRS-80 MODEL III",
    "BY TREVOR FLOWERS",
    "TRANSMUTABLE.COM",
]

draw_text_array(text_lines)

print("Setup complete")

# This loop is where you'd respond to input or change what is displayed
while True:
    pass


