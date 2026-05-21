from tkinter import *
import os
import json

class Node:
    def __init__(self, char=None, freq=0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

nodes = []


def calculate_frequences(contents):
        
        frequencies = {}
        for char in contents:
            if char not in frequencies:
                freq = contents.count(char)
                frequencies[char] = freq
                nodes.append(Node(char, freq))

def build_huffman_tree():
    while len(nodes) > 1:
        nodes.sort(key=lambda x: x.freq)
        left = nodes.pop(0)
        right = nodes.pop(0)

        merged = Node(freq=left.freq + right.freq)
        merged.left = left
        merged.right = right

        nodes.append(merged)

    return nodes[0]

def generate_huffman_codes(node, current_code, codes):
    if node is None:
        return
    
    if node.char is not None:
        codes[node.char] = current_code

    generate_huffman_codes(node.left, current_code + '0', codes)
    generate_huffman_codes(node.right, current_code + '1', codes)

def huffman_encoding(content):
    global nodes
    nodes = []
    calculate_frequences(content)
    root = build_huffman_tree()
    codes = {}
    generate_huffman_codes(root, '', codes)
    return codes

def encode_text(contents, codes):
    return ''.join(codes[char] for char in contents)

def write_binary_file(encoded_text, file):
    padding = 8 - len(encoded_text) % 8
    encoded_text = '0' * padding + encoded_text
    padded_info = "{0:08b}".format(padding)
    encoded_text = padded_info + encoded_text

    b = bytearray()
    for i in range(0, len(encoded_text), 8):
        byte = encoded_text[i:i+8]
        b.append(int(byte, 2))

    with open(file, 'wb') as f:
        f.write(b)

def save_codes(codes, file):
    with open(file, 'w') as f:
        json.dump(codes, f)

def read_binary_file(file):
    with open(file, 'rb') as f:
        bits = ''
        byte = f.read(1)
        while byte:
            bits += f"{ord(byte):08b}"
            byte = f.read(1)

    padding = int(bits[:8], 2)
    return bits[8:-padding]

def decode_text(encoded_bits, codes):
    reverse_code = {v: k for k, v in codes.items()}
    current = ''
    decoded_char = []

    for bit in encoded_bits:
        current += bit
        if current in reverse_code:
            decoded_char.append(reverse_code[current])
            current = ''
    return ''.join(decoded_char)

def decode():
    def enter2():
        base = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base, f"{entry2.get()}.bin")
        codes_path = os.path.join(base, f"{entry2.get()}_Codes.json")
        
        if os.path.exists(file_path) and os.path.exists(codes_path):

            with open(codes_path, 'r', encoding='utf-8') as f:
                loaded = json.load(f)

            encoded_bits = read_binary_file(file_path)
            decoded_text = decode_text(encoded_bits, loaded)
            
            txt_path = os.path.join(base, f"{entry2.get()}.txt")
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(decoded_text)
            
            os.remove(file_path)
            os.remove(codes_path)
            label10 = Label(window2, text=f"{entry2.get()}.bin is decoded Successfully!", font=("Ink Free", 30, "bold"), 
               fg= "#abbfde", bg= "#093273")
            
            label10.pack()
        else:
            label11 = Label(window2, text=f"{entry2.get()}.bin does not exist or\nits code has been deleted\nmake sure your file be in this directory or\nCheck file name...", font=("Ink Free", 30, "bold"), 
               fg= "#abbfde", bg= "#093273")
            label11.pack()
    
    window2 = Tk()
    window2.geometry("1250x680")
    window2.title("Dim")
    window2.config(bg="#093273")
    label9 = Label(window2, text="Please provide fullname not full path, without extension\nfile should be in this directory or folder\n extension would be .bin", font=("Ink Free", 20, "bold"), 
               fg= "#abbfde", bg= "#093273")
    entry2 = Entry(window2, font=("Ink Free", 30), bg="Black", fg="Yellow", width=30)
    entry2.insert(0, "filename without extension")
    button4 = Button(window2, text="Enter", font=("Roboto", 18, "bold","italic"), relief=RAISED, bd=7, command=enter2)

    window.destroy()
    label9.pack()
    entry2.pack(pady=(10, 0))
    button4.pack(pady=(0, 20))

def compress():
    
    def enter1():
        base = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base, f"{entry1.get()}.txt")
        if os.path.exists(file_path):
            
            old_size = os.path.getsize(file_path)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            huffman_codes = huffman_encoding(content)
            encoded = encode_text(content, huffman_codes)
            
            compress_path = os.path.join(base, f"{entry1.get()}.bin")
            write_binary_file(encoded, compress_path)
            
            compress_size = os.path.getsize(compress_path)

            codes_path = os.path.join(base, f"{entry1.get()}_Codes.json")

            save_codes(huffman_codes, codes_path)
            

            
            label5 = Label(window1, text=f"{entry1.get()} has been Compressed by {((old_size - compress_size)/old_size) * 100:.2f}%", font=("Ink Free", 30, "bold"), 
               fg= "#abbfde", bg= "#093273")
            
            label6 = Label(window1, text=f"Storage before Compression: {old_size} bytes", font=("Ink Free", 30, "bold"), 
               fg= "#abbfde", bg= "#093273")
            label7 = Label(window1, text=f"Storage after Compression: {compress_size} bytes", font=("Ink Free", 30, "bold"), 
               fg= "#abbfde", bg= "#093273")
            
            
            label5.pack()
            label6.pack()
            label7.pack()
            os.remove(file_path)
        
        else:
            label8 = Label(window1, text=f"{entry1.get()}.txt does not exist\nmake sure file be in this directory\nCheck file name...", font=("Ink Free", 30, "bold"), 
               fg= "#abbfde", bg= "#093273")
            
            label8.pack()
            

    window1 = Tk()
    window1.geometry("1250x680")
    window1.title("Dim")
    window1.config(bg="#093273")
    label4 = Label(window1, text="Please provide filename not file path, without extension\nfile should be in this directory or folder", font=("Ink Free", 20, "bold"), 
               fg= "#abbfde", bg= "#093273")
    entry1 = Entry(window1, font=("Ink Free", 30), bg="Black", fg="Yellow", width=30)
    entry1.insert(0, "filename without extension")
    button3 = Button(window1, text="Enter", font=("Roboto", 18, "bold","italic"), relief=RAISED, bd=7, command=enter1)
    
    window.destroy()
    label4.pack()
    entry1.pack(pady=(10, 0))
    button3.pack(pady=(0, 20))
    

window = Tk()
window.geometry("1250x680")
window.title("Dim")
window.config(bg="#093273")
label1 = Label(window, text="Introducing DIM", font=("Pacifico", 50, "bold"), 
               fg= "#abbfde", bg= "#093273")
label2 = Label(window, text="(Compress more, make more!)", font=("Ink Free", 30, "bold"), 
               fg= "#abbfde", bg= "#093273")
label3 = Label(window, text="Do you want to...", font=("Ink Free", 40, "bold"), 
               fg= "#abbfde", bg= "#093273")

button1 = Button(window, text="Compress file", font=("Roboto", 30, "bold","italic"), relief=RAISED, bd=15, command=compress)
button2 = Button(window, text="Decode \nyour Compress file", font=("Roboto", 30, "bold","italic"), relief=RAISED, bd=15, command=decode)

label1.pack(pady=(30, 0))
label2.pack(pady=(0, 70))
label3.pack(pady=(0,50))
button1.pack(pady=(0,30))
button2.pack()
window.mainloop()




