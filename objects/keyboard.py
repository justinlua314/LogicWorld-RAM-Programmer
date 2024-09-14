class Keyboard:
    def __init__(self, address_size:int=4, data_size:int=8, input_delay:int=25):
        self.address_size = address_size
        self.address = [0] * address_size
        self.last_address = [0] * address_size

        self.data_size = data_size
        self.data = [0] * data_size
        self.last_data = [0] * data_size
        
        self.input_delay = input_delay


    def reset(self):
        self.address = [0] * self.address_size
        self.last_address = [0] * self.address_size
        self.data = [0] * self.data_size
        self.last_data = [0] * self.data_size


    def increment_binary(self, binary:list[int]) -> list[int]:
        for index in range(len(binary) -1, -1, -1):
            if binary[index] == 1:
                binary[index] = 0
            else:
                binary[index] = 1
                break
        
        return binary


    def increment_address(self):
        self.address = self.increment_binary(self.address)
    

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
        dn = "{NumpadEnter Down}"
        up = "{NumpadEnter Up}"
        chunk = f"\tSleep, {self.input_delay}\n\tSend, {dn}\n"
        chunk += f"\tSleep, {self.input_delay + 5}\n\tSend, {up}\n"
        return chunk


    def encode_data(self, data:list[int], header=True, reset=True):
        script = ""
        
        if header:
            script += "dn(k)\n{\n\tSend, {%k% Down}\n}\nup(k)\n{\n\tSend, {%k% Up}\n}"
            script += "\n\nF8::\n"

        for byte in data:
            script += self.send_address()
            script += self.send_data(byte)
            script += self.submit_data()
            self.increment_address()
        
        self.address = [0] * self.address_size
        script += self.send_address()
        script += self.send_data(0)
        
        if reset: self.reset()
        
        return script
            
            
    def encode_page_data(self, data:list[list[int]]) -> str:
        script = "dn(k)\n{\n\tSend, {%k% Down}\n}\nup(k)\n{\n\tSend, {%k% Up}\n}"
        script += "\n\nF8::\n"
        page_keys = ['i', 'o', 'p']
        page = [0, 0, 0]
        last_page = [0, 0, 0]
        
        for pg_index, pg in enumerate(data):
            for p_index, bit in enumerate(page):
                if bit != last_page[p_index]:
                    key = page_keys[p_index]
                    func = "dn" if bit == 1 else "up"

                    script += f"\t{func}(\"{key}\")\n"
                    last_page[p_index] = bit
                
            script += self.encode_data(pg, header=False, reset=False)
            if pg_index != len(data) - 1: page = self.increment_binary(page)
        
        for p_index, bit in enumerate(page):
            if bit == 1:
                key = page_keys[p_index]
                script += f"\tup(\"{key}\")\n"
        
        return script
    
    
    def encode_memory_scan(self, input_delay:int=40) -> str:
        script = "dn(k)\n{\n\tSend, {%k% Down}\n}\nup(k)\n{\n\tSend, {%k% Up}\n}"
        script += "\n\nF8::\n"
        
        for _ in range(2 ** self.address_size):
            script += self.send_address()
            script += f"\tSleep, {input_delay}\n"
            self.increment_address()
        
        self.address = [0] * self.address_size
        script += self.send_address()
        
        self.reset()
        
        return script
            
    def write_encoded_data(self, encode:str):
        with open("input.ahk", 'w') as fp:
            fp.write(encode + "Return")
            fp.close()
