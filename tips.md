Some of this should go without saying, but, I had to google a lot to find some of this, so maybe you don't have to!!

To change the color of the scroller look at 

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("../../../fonts/7x13.bdf")
        textColor = graphics.Color(255, 0, 0)

Remember this is an RGB display. So color is displayed via RGB commands (x, x, x)

Red = (255, 0, 0)

Green = (0, 255, 0)

Blue = (0, 0, 255)

------------------

To move where the text scrolls on the screen look at 

            for i in range(offscreen_canvas.width, -len, -1):
                offscreen_canvas.Clear()
                x = i
                graphics.DrawText(offscreen_canvas, font, x, 20, textColor, nfl_scores_text)
                offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
                time.sleep(0.05)

In this example, the "20" is what we are after

20 displays the scores in the middle of my 64x32 matrix

10 would display it at the bottom 

and 30 would display it at the top

----------------------------------

To change the font of the scroller look at 

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("../../../fonts/7x13.bdf")
        textColor = graphics.Color(255, 0, 0)

Change the path to the font you want to use.

I've seen some interesting discussion on fonts at https://github.com/hzeller/rpi-rgb-led-matrix/issues/176 but haven't tried this yet.
