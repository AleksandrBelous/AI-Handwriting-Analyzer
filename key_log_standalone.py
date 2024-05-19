#!/media/nemo/disk_2_hdd/Projects/Pycharm/AiKeyLogger/.venv/bin/python3.10
from time import time
from pynput.keyboard import Listener, Key, KeyCode


class KeyLogger:
    def __init__(self, training_data=None, word_limit: int = 2, is_verbose: bool = False):
        if training_data is None:
            training_data = []
        self.training_data: list = training_data
        self.word_limit = word_limit
        self.is_verbose = is_verbose

        self.word_count = -word_limit
        self.current_word: list = []
        self.start_time = None

        self.keyboard_listener = Listener(on_press=self.on_press)

    def on_press(self, key):
        pass

    def start(self):
        self.keyboard_listener.start()
        self.keyboard_listener.join()

    def finish(self):
        self.keyboard_listener.stop()


class DataTrainPrep(KeyLogger):
    def __init__(self, training_data=None, word_limit: int = 2, is_verbose: bool = False):
        super().__init__(training_data, word_limit, is_verbose)

        self.available = { Key.shift, Key.shift_l, Key.shift_r }
        self.on_caps_lock: bool = False
        self.key = None
        self.time_diff: float = 0.0
        self.time_diff_min_limit: float = 2.0
        self.time_diff_max_limit: float = 4.0
        self.threat_marker = 99999.0
        self.datasets_log = '/media/nemo/disk_2_hdd/Projects/Pycharm/AiKeyLogger/datasets.txt'

    def save_datasets(self):
        # if self.is_verbose: print('in save func')
        with open(self.datasets_log, 'a') as file:
            for data in self.training_data:
                # if self.is_verbose: print(data)
                file.write(' '.join(map(str, data)))
                file.write('\n')

    def add_word(self):
        # if self.is_verbose:
        #     print(f'curr word = {self.current_word}')
        #     print(f'dataset = {self.training_data}')
        if self.current_word:
            # if self.is_verbose: print(f'curr word is {self.current_word}')
            self.training_data.append(self.current_word)
            self.word_count += 1
            # if self.is_verbose: print(f'count = {self.word_count}')
            if not self.word_count:
                self.word_count = -self.word_limit
                self.save_datasets()
                self.training_data = []
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
                if time_diff > self.time_diff_min_limit:
                    time_diff = self.threat_marker
                self.current_word.append(time_diff)
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
                # if self.is_verbose: print(f'Клавиша Key {key}: код {key.value.vk}')
                self.key = key.value.vk
            if isinstance(key, KeyCode):
                # if self.is_verbose: print(f'Клавиша KeyCode {key}: код {key.vk}')
                self.key = ord(key.char.upper()) if self.on_caps_lock else key.vk if key.vk else ord(key.char)
                self.key *= 1000
                if self.key > 99999:
                    self.key //= 10
            # if self.is_verbose: print(f'finally key = {self.key}')
            self.add_char_time()


if __name__ == '__main__':
    datasets = []
    dtp = DataTrainPrep(datasets, 10)
    dtp.start()
