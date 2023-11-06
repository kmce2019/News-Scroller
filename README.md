# News-Scroller
Use rpi-rgb-led-matrix to scroll current news on rpi and led matrix

This project is inspired and assited by many, to include

https://github.com/hzeller/rpi-rgb-led-matrix

https://www.youtube.com/watch?v=xSwoM3M24W8

https://www.youtube.com/watch?v=omMVAtGGr_0&t=906s

https://gist.github.com/akeaswaran/b48b02f1c94f873c6655e7129910fc3b

### Hardware used
Raspberry Pi 4B

Adafruit RGB Matrix + RTC HAT (Soldering required!) (After the fact, I discovered Adafruit RGB Matrix Bonnet, no soldering required)

64x32 LED Matrix (HUB75 )

USB power supply for RPI

5VDC  power supply for HAT

Overview
--------
The RGB LED matrix panels can be scored at [Sparkfun][sparkfun],
[AdaFruit][ada] or eBay and Aliexpress. If you are in China, I'd try to get
them directly from some manufacturer, Taobao or Alibaba.

The `RGBMatrix` class provided in `include/led-matrix.h` does what is needed
to control these. You can use this as a library in your own projects or just
use the demo binary provided here which provides some useful examples.

Check out [utils/ directory for some ready-made tools](./utils) to get started
using the library, or the [examples-api-use/](./examples-api-use) directory if
you want to get started programming your own utils.

All Raspberry Pi versions supported
-----------------------------------

This supports the old Raspberry Pi's Version 1 with 26 pin header and also the
B+ models, the Pi Zero, Raspberry Pi 2 and 3 with 40 pins, as well as the
Compute Modules which have 44 GPIOs.
The 26 pin models can drive one chain of RGB panels, the 40 pin models
**up to three** chains in parallel (each chain 12 or more panels long).
The Compute Module can drive **up to 6 chains in parallel**.
The Raspberry Pi 2 and 3 are faster and generally perferred to the older
models (and the Pi Zero). With the faster models, the panels sometimes
can't keep up with the speed; check out
this [troubleshooting section](#troubleshooting) what to do.

A lightweight, non-GUI, distribution such as [DietPi] is recommended.
[Raspbian Lite][raspbian-lite] is a bit easier to get started with and
is a good second choice.


### Hardware Setup
Follow your favorite guide for connecting the hardware.

Install Raspberry Pi OS (Legacy) LITE

They have a new image downloader and SD Card creation tool at https://www.raspberrypi.com/software/operating-systems/

After creating the SD Card, and connecting all of the hardware, insert SD Card and power on the devices.

This can take some time so be patient

Log into your Pi

###  Software Setup

I took bits and pieces from all sources and smashed them together to make this work!

From https://www.youtube.com/watch?v=xSwoM3M24W8 at 8:15
```
git clone https://github.com/hzeller/rpi-rgb-led-matrix.git
```

Follow the guide on Github for Authentication Processes!

```
cd rpi-rgb-led-matrix
make build-python PYTHON=$(Which python 3)
sudo make install-python
```
Any dependencies not installed above can be installed using pip
```
sudo apt-get install python3-pil
sudo apt-get install python3-feedparser

```

Create newsrss.py
```
cd bindings/python/samples
sudo nano newsrss.py
```

```
#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
from rgbmatrix import RGBMatrixOptions
import feedparser
import time

class RunRSSFeed(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunRSSFeed, self).__init__(*args, **kwargs)
        self.parser.add_argument("-u", "--url", help="RSS feed URL to display", default="https://moxie.foxnews.com/google-publisher/world.xml")

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("../../../fonts/7x13.bdf")
        textColor = graphics.Color(255, 0, 0)
        rss_url = self.args.url

        while True:
            offscreen_canvas.Clear()
            feed = feedparser.parse(rss_url)
            items = feed.entries
            display_text = ""

            for item in items:
                display_text += item.title + " | "

            len = graphics.DrawText(offscreen_canvas, font, offscreen_canvas.width, 10, textColor, display_text)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

            for i in range(offscreen_canvas.width, -len, -1):
                offscreen_canvas.Clear()
                x = i
                graphics.DrawText(offscreen_canvas, font, x, 10, textColor, display_text)
                offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
                time.sleep(0.05)

if __name__ == "__main__":
    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 64
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = "adafruit-hat"

    run_rss_feed = RunRSSFeed(options=options)
    if (not run_rss_feed.process()):
        run_rss_feed.print_help()
```

```
CTRL-X
Y
ENTER
```

### Usage
```
sudo python3 news.py --led-cols=64 --led-rows=32 --led-slowdown-gpio=4 --led-no-hardware-pulse=1 --led-gpio-mapping=adafruit-hat
```

See https://github.com/hzeller/rpi-rgb-led-matrix#controlling-rgb-led-display-with-raspberry-pi-gpio for flag descriptions


### Things to update:
Add as a service

Add to startup

Could use guidance on how to repackage all of this and install it in home/ instead of buried in directories

Want to add a second matrix for larger display, easier to read all the text
