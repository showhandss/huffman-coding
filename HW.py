from huffman import HuffmanCoding
import sys

path = "sample.txt"

hw = HuffmanCoding(path)

hw.compress()

hw.decompress(encoded_text)