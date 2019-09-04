#!/usr/bin/env python

import argparse
import colorama
import random
import ctypes
import sys
import re

if sys.version[0] == '2': input = raw_input

def parse_line(line):
	text, translations = split_line(line)
	text = decode_string(text)
	translations = [decode_string(i) for i in translations]
	return text, translations

def split_line(line):
	splitted = re.split(r'(?<!\\)-', line, 1)
	text = splitted[0].strip()
	translations = split_translations(splitted[1]) if len(splitted) > 1 else []
	return text, translations

def split_translations(string):
	trans = parse_optional(re.split(r'(?<!\\)\|', string))
	return [i.strip().replace('  ', ' ') for i in trans]

def parse_optional(seq):
	i, seqlen = 0, len(seq)
	while i < seqlen:
		beg, end = find_brackets_pair(seq[i])
		if beg == -1 or end == -1:
			i += 1
			continue
		without_optional, with_optional = split_optional(seq[i], beg, end)
		seq.insert(i+1, without_optional)
		seq.insert(i+2, with_optional)
		del seq[i]
		seqlen += 1
	return seq

def find_brackets_pair(string):
	begin = find_non_escaped('(', string)
	if begin == -1: return begin, find_non_escaped(')', string)
	end, ratio = -1, 1
	for i in range(begin+1, len(string)):
		if string[i-1] == '\\': continue
		if string[i] == '(': ratio += 1
		elif string[i] == ')': ratio -= 1
		if ratio == 0:
			end = i
			break
	return begin, end

def find_non_escaped(char, string):
	pos = -1
	while True:
		pos = string.find(char, pos+1)
		if pos <= 0 or string[pos-1] != '\\': break
	return pos

def split_optional(string, beg, end):
	return remove_optional(string, beg, end), remove_brackets(string, beg, end)

def remove_optional(string, beg, end):
	return string[:beg] + string[end+1:]

def remove_brackets(string, f, s):
	return string[:f] + string[f+1:s] + string[s+1:]

def decode_string(string):
	for c in '-|()': string = string.replace('\\' + c, c)
	return string

def run(lines):
	points = max_points = 0
	if not lines: return
	for line in lines:
		text, translations = parse_line(line)
		try: answer = input(text + ' - ')
		except EOFError:
			print('\n')
			break
		if answer in translations:
			show_correct_answer_message()
			points += 1
		else:
			show_wrong_answer_message(translations)
		max_points += 1
	result = points * 100 // (max_points or 1)
	print('Result: {0}%'.format(str(result)))

def show_correct_answer_message():
	print(green('Correct answer!\n'))

def show_wrong_answer_message(answers):
	message = red('Wrong answer!\n') + 'Should be: '
	if len(answers): message += green(answers[0])
	for answer in answers[1:]:
		message += ' or ' + green(answer)
	print(message + '\n')

def green(string):
	return change_color(string, 'GREEN')

def red(string):
	return change_color(string, 'RED')

def change_color(string, color):
	return colorama.Fore.__dict__[color] + string + colorama.Fore.RESET

def load_lines(*files, **kwargs):
	limit = kwargs.pop('limit', None)
	lines = []
	if limit == None:
		lines += list(fileinput(*files))
	else:
		for line in fileinput(*files):
			if not limit: break
			lines.append(line)
			limit -= 1
	return lines

def load_lines_randomly(*files, **kwargs):
	limit = kwargs.pop('limit', None)
	lines = list(fileinput(*files))
	random.shuffle(lines)
	return lines[0:limit]

def fileinput(*files):
	try:
		for file in files:
			if file == '-':
				for line in sys.stdin.readlines():
					if line.strip(): yield line
				sys.stdin = get_console_descriptor()
			else:
				with open(file, 'r') as f:
					for line in f:
						if line.strip(): yield line
	except IOError as e:
		sys.stderr.write("{0}: '{1}'\n".format(e.strerror, file))
		raise e

def get_console_descriptor():
	console = None
	try:
		console = open("/dev/tty")
	except IOError:
		concp = 'cp{}'.format(ctypes.windll.kernel32.GetConsoleCP())
		console = open('con', encoding=concp)
	return console

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-n', '--lines', type=int, metavar='NUM',
		help='''load NUM lines or all if NUM is greater than the number of
		all lines''')
	parser.add_argument('-o', '--order', type=str,
		choices=['random', 'file'], default='random',
		help='specify order in which lines are loaded')
	parser.add_argument('files', nargs='*', metavar='file',
		default=['-'])
	return parser.parse_args()

def main():
	colorama.init()
	args = parse_args()
	lines = []
	try:
		if args.order == 'file':
			lines += load_lines(*args.files, limit=args.lines)
		else:
			lines += load_lines_randomly(*args.files, limit=args.lines)
	except IOError as e:
		return e.errno
	run(lines)
	colorama.deinit()

if __name__ == '__main__':
	sys.exit(main())
