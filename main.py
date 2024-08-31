from objects.keyboard import Keyboard
from random import randint

def main():
    board = Keyboard()
    # data = [170, 85, 0, 170, 0, 0, 0, 85, 85, 0, 0, 0, 170, 0, 85, 170]
    data = [0] * 16
    # data = [randint(1, 255) for _ in range(16)]
    board.encode_data(data)


if __name__ == "__main__": main()
