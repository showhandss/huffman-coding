import heapq
import os


class HuffmanCoding:
	# 宣告地址，栈，字典以及
	def __init__(self, path):
		self.path = path
		self.heap = []
		self.codes = {}
		self.reverse_mapping = {}

	class HeapNode:
		def __init__(self, char, freq):
			self.char = char
			self.freq = freq
			self.left = None
			self.right = None

		# defining comparators less_than and equals
		def __lt__(self, other):
			return self.freq < other.freq

		def __eq__(self, other):
			if(other == None):
				return False
			if(not isinstance(other, HeapNode)):
				return False
			return self.freq == other.freq

	# functions for compression:

	# 制作频率字典frequency
	def make_frequency_dict(self, text):
		frequency = {}
		for character in text:
			if not character in frequency:
				frequency[character] = 0
			frequency[character] += 1
		return frequency

	# 将字符的出现次数塞入与字符相匹配的字典队列
	def make_heap(self, frequency):
		for key in frequency:
			node = self.HeapNode(key, frequency[key])
			heapq.heappush(self.heap, node)

	# huffman建树
	def merge_nodes(self):
		while(len(self.heap)>1):
			# 获取栈中最前的两个节点
			node1 = heapq.heappop(self.heap)
			node2 = heapq.heappop(self.heap)

			# 将两个节点上面接一个新的父节点 将得到的父节点重新存入栈
			merged = self.HeapNode(None, node1.freq + node2.freq)
			merged.left = node1
			merged.right = node2
			heapq.heappush(self.heap, merged)

	# 建完树后，给每个字符设置二进制代号
	def make_codes_helper(self, root, current_code):
		# 若为空 则跳出
		if(root == None):
			return

		# 若节点带字符 则递归中止 返回上一层
		if(root.char != None):
			self.codes[root.char] = current_code
			self.reverse_mapping[current_code] = root.char
			return

		# 先左再右，左0右1
		self.make_codes_helper(root.left, current_code + "0")
		self.make_codes_helper(root.right, current_code + "1")

	# 创建树并把树丢入make_codes_helper进行编号
	def make_codes(self):
		root = heapq.heappop(self.heap)
		current_code = ""
		self.make_codes_helper(root, current_code)

	# 把字母转为编号
	def get_encoded_text(self, text):
		encoded_text = ""
		# 遍历文本，codes[character]为文本对应的编码
		for character in text:
			encoded_text += self.codes[character]	
		return encoded_text

	# # 先给encoded_text凑成8的倍数长度，然后将最后剩余的长度转为二进制存在encoded_text最前面
	# def pad_encoded_text(self, encoded_text):
	# 	extra_padding = 8 - len(encoded_text) % 8
	# 	for i in range(extra_padding):
	# 		encoded_text += "0"

	# 	padded_info = "{0:08b}".format(extra_padding)
	# 	encoded_text = padded_info + encoded_text
	# 	return encoded_text

	# 将原本二进制文本8个8个转为数字存入bytearray
	# def get_byte_array(self, padded_encoded_text):
	# 	if(len(padded_encoded_text) % 8 != 0):
	# 		print("Encoded text not padded properly")
	# 		exit(0)

	# 	b = bytearray()
	# 	for i in range(0, len(padded_encoded_text), 8):
	# 		byte = padded_encoded_text[i:i+8]
	# 		b.append(int(byte, 2))
	# 	return b

	# 压缩
	def compress(self):
		filename, file_extension = os.path.splitext(self.path)
		# 用二进制文件存储
		output_path = filename + "_encode.txt"

		with open(self.path, 'r+') as file, open(output_path, 'w+') as output:
			#文本读取
			text = file.read()
			#结尾清洁
			text = text.rstrip()
			print(text)

			frequency = self.make_frequency_dict(text)
			self.make_heap(frequency)
			self.merge_nodes()
			self.make_codes()

			encoded_text = self.get_encoded_text(text)
			#padded_encoded_text = self.pad_encoded_text(encoded_text)

			#b = self.get_byte_array(padded_encoded_text)
			output.write(encoded_text)

		# 导入与导出
		# with open(self.path, 'r+') as file, open(output_path, 'wb') as output:
		# 	#文本读取
		# 	text = file.read()
		# 	#结尾清洁
		# 	text = text.rstrip()

		# 	frequency = self.make_frequency_dict(text)
		# 	self.make_heap(frequency)
		# 	self.merge_nodes()
		# 	self.make_codes()

		# 	encoded_text = self.get_encoded_text(text)
		# 	padded_encoded_text = self.pad_encoded_text(encoded_text)

		# 	b = self.get_byte_array(padded_encoded_text)
		# 	output.write(bytes(b))

		print("Compressed")
		# return output_path
		return


	""" 解码程序: """


	# 还原源码
	# def remove_padding(self, padded_encoded_text):
	# 	# 提取前8个字符
	# 	padded_info = padded_encoded_text[:8]
	# 	extra_padding = int(padded_info, 2)
		
	# 	# 提取8以后的字符
	# 	padded_encoded_text = padded_encoded_text[8:] 
	# 	# 去除后加的字符
	# 	encoded_text = padded_encoded_text[:-1*extra_padding]

	# 	return encoded_text

	# 解码
	def decode_text(self, encoded_text):
		current_code = ""
		decoded_text = ""

		for bit in encoded_text:
			current_code += bit
			# 如果成功找到符合字典中存在字符的编码，则转换为编码
			if(current_code in self.reverse_mapping):
				character = self.reverse_mapping[current_code]
				decoded_text += character
				current_code = ""

		return decoded_text


	def decompress(self, encoded_text):
		filename, file_extension = os.path.splitext(self.path)
		output_path = filename + "_decompressed" + ".txt"

		with open(output_path, 'w') as output:
			
			# byte = file.read(1)
			# while(len(byte) > 0):
			# 	byte = ord(byte)
			# 	bits = bin(byte)[2:].rjust(8, '0')
			# 	bit_string += bits
			# 	byte = file.read(1)

			#encoded_text = self.remove_padding(bit_string)

			decompressed_text = self.decode_text(encoded_text)
			
			output.write(decompressed_text)

		print("Decompressed")
		return output_path

