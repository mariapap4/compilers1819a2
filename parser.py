import plex

class ParseError(Exception):
	pass

class MyParser:
	def __init__(self):
		keyword = plex.Str('print','PRINT')
		letter = plex.Range('azAZ')
		num = plex.Range('09')
		space = plex.Any(" \n\t")
		name = letter+plex.Rep(letter|num)
		digit = plex.Range('01')
		binary= plex.Rep1(digit)
		eq = plex.Str( '=')
		paren1 = plex.Str('(')
		paren2 = plex.Str(')')
		and_op = plex.Str('and')
		or_op = plex.Str('or')
		xor_op = plex.Str('xor')
		self.st = {}
		
		self.lexicon = plex.Lexicon([
			(binary, 'BINARY_TOKEN'),
			(keyword,'PRINT'),
			(name,'IDENTIFIER'),
			(space,plex.IGNORE),
			(and_op, plex.TEXT),
			(or_op, plex.TEXT),
            (xor_op, plex.TEXT),
            (eq, '='),
            (paren1, '('),
            (paren2, ')'),
			])

	def create_scanner(self,fp):
		self.scanner = plex.Scanner(self.lexicon,fp)
		self.la,self.text=self.next_token()

	def next_token(self):
		return self.scanner.read()

	def match(self,token):
		if self.la == token:
			self.la,self.text=self.next_token()
		else:
			raise ParseError(" (")

	def parse(self,fp):
		self.create_scanner(fp)
		self.stmt_list()
		
	def stmt_list(self):
		if self.la == 'IDENTIFIER' or self.la == 'PRINT':
			self.stmt()
			self.stmt_list()
		elif self.la == None:
			return
		else:
			raise ParseError("Expected IDENTIFIER or PRINT")
	def stmt(self):
		if self.la == 'IDENTIFIER':
			self.match('IDENTIFIER')	
			self.match('=')
			self.expr()
		elif self.la == 'PRINT':
			self.match('PRINT')
			self.expr()
		else:
			raise ParseError("Expected IDENTIFIER or PRINT")
	def expr(self):
		if self.la == '(' or self.la == 'IDENTIFIER' or self.la == 'BIT_TOKEN':
			self.term()
			self.term_tail()
		else:
			raise ParseError("Expected ( or IDENTIFIER or BIT_TOKEN or )")
	def term_tail(self):	
		if self.la == 'xor':
			self.match('xor')
			self.term()
			self.term_tail()
		elif self.la == 'IDENTIFIER' or self.la == 'PRINT' or self.la == None or self.la == ')':
			return
		else:
			raise ParseError("Expected xor")
	def term(self):
		if self.la == '(' or self.la == 'IDENTIFIER' or self.la == 'BIT_TOKEN':	
			self.factor()
			self.factor_tail()
		else:
			raise ParseError("Expected ( or IDENTIFIER or )")
	def factor_tail(self):
		if self.la == 'or':
			self.match('or')
			self.factor()
			self.factor_tail()
		elif self.la == 'xor' or self.la == 'IDENTIFIER' or self.la == 'PRINT' or self.la == None or self.la == ')':
			return
		else:
			raise ParseError("Expected or")
	def factor(self):
		if self.la == '(' or self.la == 'IDENTIFIER' or self.la == 'BIT_TOKEN':
			self.atom()
			self.atom_tail()
		else:
			raise ParseError("Expected ID,bit h (")
	def atom_tail(self):
		if self.la == 'and':
			self.match('and')
			self.atom()
			self.atom_tail()
		elif self.la == 'or' or self.la == 'xor' or self.la == 'IDENTIFIER' or self.la == 'PRINT' or self.la == None or self.la == ')':
			return
		else:
			raise ParseError("Expected and")
	def atom(self):
		if self.la == '(':
			self.match('(')
			self.expr()
			self.match(')')
		elif self.la == 'IDENTIFIER':
			self.match('IDENTIFIER')
		elif self.la == 'DINARY_TOKEN':
			self.match('DINARY_TOKEN')
		else:
			raise ParseError("Expected id bit or (")

parser = MyParser()
with open('text.txt','r') as fp:
	parser.parse(fp)
