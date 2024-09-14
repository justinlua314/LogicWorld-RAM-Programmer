from objects.keyboard import Keyboard
from random import randint


def generate_draws():
    pages:dict[int,list[int]] = {
        0 : [],
        1 : [],
        2 : [],
        3 : [],
        4 : [],
        5 : [],
        6 : [],
        7 : []
    }
    
    for number in range(256):
        digits = str(number).split()
        count = len(digits)


def main():
    address_size = 8
    byte_count = 2 ** address_size
    board = Keyboard(address_size=address_size, data_size=8, input_delay=100)
    # data = [170, 85, 0, 170, 0, 0, 0, 85, 85, 0, 0, 0, 170, 0, 85, 170]
    # data = [0] * byte_count
    # data = [randint(1, 255) for _ in range(byte_count)]
    data = [i for i in range(byte_count)]
    board.write_encoded_data(board.encode_page_data([data, data]))
    # encode = board.encode_memory_scan()
    
    # board.write_encoded_data(encode)


if __name__ == "__main__": main()
