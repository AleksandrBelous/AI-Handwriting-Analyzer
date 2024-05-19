from pynput.keyboard import Listener, Key, KeyCode

print('Для выхода нажмите `ESC`\n\n')


def on_press(key):
    if type(key) is Key:
        print(f'Клавиша Key {key}: код {key.value.vk}')
    elif type(key) is KeyCode:
        print(f'Клавиша KeyCode {key}: код {key.vk}')


with Listener(on_press=on_press) as listener:
    listener.join()
