from tkinter import *
from random import randint
import tkinter as ttk

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


    def _open(self):
        self._image_data = Image.open(self._image)

    def _set_canvas_size(self, size):
        self._canvas.configure(height=size[0],
                               width=size[1])

    def create_thread_shared_array(self):
        manager = mp.Manager()
        frames = manager.list()
        return frames

    def create_and_start_separated_thread(self, shared_list, amount):
        self._process = Process(target=self._frame_loader, args=(shared_list, amount), daemon=True)
        self._process.start()

    def _frame_loader(self, shared_list, amount):
        for i in range(amount):
            self._image_data.seek(i)  # Устанавливаем, кадр, который будем считывать
            shared_list.append(self._image_data)
            # print('Thread:', i)




if __name__ == "__main__":
    root = Tk()
    bar = ttk.Progressbar(orient='horizontal')
    bar.pack(fill='both')

    image_id = randint(1, 4)

    root.title("FootScaut")
    root.mainloop()