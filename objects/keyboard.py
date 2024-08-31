class Keyboard:
    def __init__(self, address_size:int=4, data_size:int=8):
        self.address_size = address_size
        self.address = [0] * address_size
        self.last_address = [0] * address_size

        self.data_size = data_size
        self.data = [0] * data_size
        self.last_data = [0] * data_size


    def reset(self):
        self.address = [0] * self.address_size
        self.last_address = [0] * self.address_size
        self.data = [0] * self.data_size
        self.last_data = [0] * self.data_size


    def increment_address(self):
        for index in range(3, -1, -1):
            if self.address[index] == 1:
                self.address[index] = 0
            else:
                self.address[index] = 1
                break
    

    def send_address(self) -> str:
        chunk = ""

        for index, bit in enumerate(self.address):
            if self.last_address[index] != bit:
                key = self.address_size - index - 1
                func = "dn" if bit == 1 else "up"

                chunk += f"\t{func}(\"{key}\")\n"
                self.last_address[index] = bit
        
        return chunk
    

    def dec_to_binary(self, number:int, size:int=8) -> list[int]:
        bits = []
        factor = 2 ** (size - 1)

        while factor > 0:
            if number >= factor:
                bits.append(1)
                number -= factor
            else:
                bits.append(0)
            
            factor //= 2
        
        return bits
    

    def send_data(self, number:int) -> str:
        self.data = self.dec_to_binary(number, self.data_size)
        chunk = ""

        for index, bit in enumerate(self.data):
            if self.last_data[index] != bit:
                key = f"Numpad{self.data_size - index - 1}"
                func = "dn" if bit == 1 else "up"

                chunk += f"\t{func}(\"{key}\")\n"
                self.last_data[index] = bit
        
        return chunk
    
    
    def submit_data(self) -> str:
        chunk = "\tSleep, 25\n\tSend, {NumpadEnter Down}\n"
        chunk += "\tSleep, 25\n\tSend, {NumpadEnter Up}\n"
        return chunk


    def encode_data(self, data:list[int]):
        script = "dn(k)\n{\n\tSend, {%k% Down}\n}\nup(k)\n{\n\tSend, {%k% Up}\n}"
        script += "\n\nF8::\n"

        for byte in data:
            script += self.send_address()
            script += self.send_data(byte)
            script += self.submit_data()
            self.increment_address()
        
        self.address = [0] * self.address_size
        script += self.send_address()
        script += self.send_data(0)
        self.reset()
        
        with open("input.ahk", 'w') as fp:
            fp.write(script + "Return")
            fp.close()
