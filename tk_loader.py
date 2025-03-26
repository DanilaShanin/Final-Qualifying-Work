from tkinter import *
from random import randint


class Screensaver:
    _image = None
    _image_data = None
    _working = True

    def __init__(self, root, progress_func=None, go_next=None):
        self._root = root
        self._process_func = progress_func
        self._go_next = go_next
        self._canvas = Canvas()
        self._canvas.pack()

    def play_gif(self, image, delay):
        self._image = image

        self._open()
        size = self.get_image_size()
        self._set_canvas_size(size)

        frame_amount = self.get_frame_amount()
        frames = self.create_thread_shared_array()
        self.create_and_start_separated_thread(frames, frame_amount)

        self._root.after(0, lambda: self._window_update_thread(frames, frame_amount, delay))



if __name__ == "__main__":
    root = Tk()

    image_id = randint(1, 4)
    root.mainloop()