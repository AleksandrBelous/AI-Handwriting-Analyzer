from tensorflow.keras.models import load_model
from numpy import array, float32
from time import time
from pynput.keyboard import Listener, Key, KeyCode


class NN:
    def __init__(self):
        self.model = load_model('smth_good.h5')
        self.bad_prediction = None
        self.request: list = []

    def get_prediction(self):
        return round(self.model.predict(array(self.request).reshape(1, 3), verbose=False)[0][0])


class KeyLogger(NN):
    def __init__(self, word_limit):
        super().__init__()
        self.keyboard_listener = Listener(on_press=self.on_press)
        self.available = { Key.shift, Key.shift_l, Key.shift_r }
        self.on_caps_lock: bool = False
        self.key = None
        self.time_diff: float = 0.0
        self.time_diff_max_limit: float = 4.0
        self.start_time = None
        self.current_word: list = []
        self.word_limit = word_limit
        self.word_count = -word_limit

    def start(self):
        self.keyboard_listener.start()
        self.keyboard_listener.join()

    def finish(self):
        self.keyboard_listener.stop()

    def check_handwriting(self):
        for i in range(0, len(self.current_word) - 2, 2):
            self.request = self.current_word[i:i + 2 + 1]
            self.bad_prediction = self.get_prediction()
            if self.bad_prediction:
                print(f'Alarm !!!')
            else:
                print('Ok')

    def add_word(self):
        # if self.is_verbose:
        #     print(f'curr word = {self.current_word}')
        #     print(f'dataset = {self.training_data}')
        if self.current_word:
            if len(self.current_word) == 1:
                print('Soft Alarm !!!')
            else:
                print(self.current_word)
            # if self.is_verbose: print(f'curr word is {self.current_word}')
            self.word_count += 1
            # if self.is_verbose: print(f'count = {self.word_count}')
            if not self.word_count:
                self.word_count = -self.word_limit
                self.check_handwriting()
            self.current_word = []
        self.start_time = None

    def add_char_time(self):
        if self.start_time is None:
            self.current_word.append(self.key)
            self.start_time = time()
        else:
            current_time = time()
            time_diff = round(current_time - self.start_time, 5)  # Время в микросекундах
            if time_diff > self.time_diff_max_limit:
                self.add_word()
                # оставшийся в памяти символ (и связанный с ним временной интервал) считаем началом нового слова
            else:
                self.current_word.append(time_diff)
                # print(self.time_diff)
            self.current_word.append(self.key)
            self.start_time = current_time

    def on_press(self, key):
        # if self.is_verbose: print(self.start_time)
        if isinstance(key, Key) and key not in self.available:
            if key == Key.caps_lock:
                self.on_caps_lock = not self.on_caps_lock
            else:
                # Завершение текущего слова, добавление его в обучающие данные и сброс текущего слова
                self.add_word()
        else:
            if key in self.available:
                # print(f'Клавиша Key {key}: код {key.value.vk}')
                self.key = key.value.vk
            if isinstance(key, KeyCode):
                # print(f'Клавиша KeyCode {key}: код {key.vk}')
                self.key = ord(key.char.upper()) if self.on_caps_lock else key.vk if key.vk else ord(key.char)
                self.key *= 1000
                if self.key > 99999:
                    self.key //= 10
            # print(f'finally key = {self.key}')
            self.add_char_time()


def main():
    kl = KeyLogger(1)
    kl.start()


if __name__ == '__main__':
    main()
