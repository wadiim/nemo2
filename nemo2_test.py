from nemo2 import parse_line, find_brackets_pair, split_optional
import unittest

class ParseLineTest(unittest.TestCase):

	def test_empty_line(self):
		self.assertEqual(parse_line(''), ('', []))

	def test_text_without_translations(self):
		self.assertEqual(parse_line('foo'), ('foo', []))

	def test_text_with_empty_translation(self):
		self.assertEqual(parse_line('foo-'), ('foo', ['']))

	def test_empty_text_with_nonempty_translation(self):
		self.assertEqual(parse_line('-foo'), ('', ['foo']))

	def test_empty_text_with_empty_translation(self):
		self.assertEqual(parse_line('-'), ('', ['']))

	def test_text_with_translation(self):
		self.assertEqual(parse_line('foo-bar'), ('foo', ['bar']))
	
	def test_multiple_nonescaped_hyphens(self):
		self.assertEqual(parse_line('foo-bar-baz'), ('foo', ['bar-baz']))

	def test_multiple_translations(self):
		self.assertEqual(parse_line('foo-bar|baz'), ('foo', ['bar', 'baz']))

	def test_multiple_empty_translations(self):
		self.assertEqual(parse_line('foo-||'), ('foo', ['', '', '']))
	
	def test_removing_extra_spaces(self):
		self.assertEqual(parse_line(' foo - bar  baz '), ('foo', ['bar baz']))
		
	def test_optional_text(self):
		self.assertEqual(parse_line('a-(b) c'), ('a', ['c', 'b c']))

	def test_optional_without_closing_bracket(self):
		self.assertEqual(parse_line('a-(b c'), ('a', ['(b c']))

	def test_optional_without_opening_bracket(self):
		self.assertEqual(parse_line('a-b) c'), ('a', ['b) c']))

	def test_nested_optionals(self):
		self.assertEqual(parse_line('-f(g(x))'), ('', ['f', 'fg', 'fgx']))

	def test_multiple_optionals(self):
		self.assertEqual(parse_line('-f(x)(y)'), ('', ['f', 'fy', 'fx', 'fxy']))

	def test_escaped_hyphens(self):
		self.assertEqual(parse_line('a\-b-c\-d'), ('a-b', ['c-d']))
	
	def test_escaped_pipe(self):
		self.assertEqual(parse_line('a\|b-c|d\|e'), ('a|b', ['c', 'd|e']))

	def test_escaped_brackets(self):
		self.assertEqual(parse_line('\(a\)b-(\()d\)'), ('(a)b', ['d)', '(d)']))

	def test_pipe_inside_brackets(self):
		self.assertEqual(parse_line('foo-(bar|baz)'), ('foo', ['(bar', 'baz)']))

class FindBracketsPairTest(unittest.TestCase):

	def test_empty_string(self):
		self.assertEqual(find_brackets_pair(''), (-1, -1))

	def test_lack_of_brackets(self):
		self.assertEqual(find_brackets_pair('foo'), (-1, -1))

	def test_lack_of_right_bracket(self):
		self.assertEqual(find_brackets_pair('f(x'), (1, -1))
	
	def test_lack_of_left_bracket(self):
		self.assertEqual(find_brackets_pair('fx)'), (-1, 2))

	def test_single_pair_of_brackets(self):
		self.assertEqual(find_brackets_pair('f(x)'), (1, 3))

	def test_multiple_pairs_of_brackets(self):
		self.assertEqual(find_brackets_pair('f(x)(y)(z)'), (1, 3))
	
	def test_nested_brackets(self):
		self.assertEqual(find_brackets_pair('f(g(h(x)))'), (1, 9))

	def test_swapped_brackets(self):
		self.assertEqual(find_brackets_pair('f)x('), (3, -1))

	def test_mismatched_brackets(self):
		self.assertEqual(find_brackets_pair('f)(x)'), (2, 4))

class SplitOptionalTest(unittest.TestCase):

	def test_splitting_optional(self):
		self.assertEqual(split_optional('(a)b', 0, 2), ('b', 'ab'))

if __name__ == '__main__':
	unittest.main()
