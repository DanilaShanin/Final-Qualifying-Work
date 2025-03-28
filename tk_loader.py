from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from time import sleep
import multiprocessing as mp
from multiprocessing import Process
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

    def _window_update_thread(self, shated_list, frame_amount, delay):
        sleep(1)  # Ждем загрузки нескольких кадров

        i = 0
        while self._working:
            image = ImageTk.PhotoImage(shated_list[
                                           i])  # Конвертируем изображения из формата библиотеки Pillow в формат, который может понять Tkinter
            # Не сохраняем изображения в данном формате изначально, потому, что его нельзя серилизовать библиотекой pickle
            # библиотека multiprocessing, общие данные под капотом серилизует библиотекой pickle
            self._canvas.create_image(0, 0, anchor='nw', image=image)
            i += 1

            if self._process_func:
                self._process_func(1 / frame_amount * 100)

            # print('GUI:',i)
            if i >= frame_amount:
                i = 0

                if self._go_next:
                    self._working = False
                    self._go_next()

            self._canvas.update()
            sleep(delay)

    def get_frame_amount(self):
        return self._image_data.n_frames

    def get_image_size(self):
        return (self._image_data.height, self._image_data.width)


def update_progress(value):
    bar.step(value)


def navigate_to_app():
    update_progress(100)


if __name__ == "__main__":
    root = Tk()
    load_screen = Screensaver(root, progress_func=update_progress, go_next=navigate_to_app)
    bar = ttk.Progressbar(orient='horizontal')
    bar.pack(fill='both')

    image_id = randint(1, 4)
    load_screen.play_gif(f'loading_gifs/{image_id}.gif', 0.03)

    root.title("FootScaut")
    root.mainloop()