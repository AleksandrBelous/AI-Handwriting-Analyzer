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

        self.on_caps_lock: bool = False
        self.datasets_log = '/media/nemo/disk_2_hdd/Projects/Pycharm/AiKeyLogger/datasets.txt'

    def save_datasets(self):
        # if self.is_verbose: print('in save func')
        with open(self.datasets_log, 'a') as file:
            for data in self.training_data:
                if self.is_verbose: print(data)
                file.write(' '.join(map(str, data)))
                file.write('\n')

    def on_press(self, key):
        if key in (Key.space, Key.enter):
            # Завершение текущего слова, добавление его в обучающие данные и сброс текущего слова
            # if self.is_verbose:
            #     print(f'curr word = {self.current_word}')
            #     print(f'dataset = {self.training_data}')
            if self.current_word:
                # if self.is_verbose: print(f'curr word is OK')
                self.training_data.append(self.current_word)
                self.word_count += 1
                # if self.is_verbose: print(f'count = {self.word_count}')
                if not self.word_count:
                    self.word_count = -self.word_limit
                    self.save_datasets()
                    self.training_data = []
                self.current_word = []
            self.start_time = None
        else:
            if key == Key.caps_lock:
                self.on_caps_lock = not self.on_caps_lock
            if isinstance(key, Key):
                # if self.is_verbose: print(f'Клавиша Key {key}: код {key.value.vk}')
                key = key.value.vk
            elif isinstance(key, KeyCode):
                # if self.is_verbose: print(f'Клавиша KeyCode {key}: код {key.vk}')
                key = ord(key.char.upper()) if self.on_caps_lock else key.vk if key.vk else ord(key.char)
                key *= 1000
                if key > 99999:
                    key //= 10
            # if self.is_verbose: print(f'finally key = {key}')
            if self.start_time is None:
                self.current_word.append(key)
                self.start_time = time()
            else:
                current_time = time()
                time_diff = round(current_time - self.start_time, 5)  # Время в микросекундах
                self.current_word.append(time_diff)
                self.current_word.append(key)
                self.start_time = current_time


class DataPredictPrep(KeyLogger):
    def __init__(self, training_data=None, word_limit: int = 2, is_verbose: bool = False):
        super().__init__(training_data, word_limit, is_verbose)

        self.on_caps_lock: bool = False

    def on_press(self, key):
        if key in (Key.space, Key.enter):
            # Завершение текущего слова, добавление его в обучающие данные и сброс текущего слова
            if self.is_verbose:
                print(f'curr word = {self.current_word}')
                print(f'dataset = {self.training_data}')
            if self.current_word:
                if self.is_verbose: print(f'curr word is OK')
                self.training_data.append(self.current_word)
                self.word_count += 1
                if self.is_verbose: print(f'count = {self.word_count}')
                if not self.word_count:
                    self.word_count = -self.word_limit
                    self.training_data = []
                self.current_word = []
            self.start_time = time()
        else:
            if key == Key.caps_lock:
                self.on_caps_lock = not self.on_caps_lock
            if isinstance(key, Key):
                if self.is_verbose: print(f'Клавиша Key {key}: код {key.value.vk}')
                key = key.value.vk
            elif isinstance(key, KeyCode):
                if self.is_verbose: print(f'Клавиша KeyCode {key}: код {key.vk}')
                key = ord(key.char.upper()) if self.on_caps_lock else key.vk if key.vk else ord(key.char)
                key *= 1000
                if key > 99999:
                    key //= 10
            if self.is_verbose: print(f'finally key = {key}')
            #
            current_time = time()
            time_diff = round(current_time - self.start_time, 5)  # Время в микросекундах
            self.current_word.append(key)
            self.current_word.append(time_diff)
            self.start_time = current_time


if __name__ == '__main__':
    datasets = []
    dtp = DataTrainPrep(datasets, 2, True)
    dtp.start()
