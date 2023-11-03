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
