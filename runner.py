import plex

class ParseError(Exception):
	pass

class ParseRun(Exception):
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
		if self.la==token:
			self.la,self.text=self.next_token()
		else:
			raise ParseError("Expected )")

	def parse(self,fp):
		self.create_scanner(fp)
		self.stmt_list()
		
	def stmt_list(self):
		if self.la == 'IDENTIFIER' or self.la == 'PRINT':
			self.stmt()
			self.stmt_list()
		elif self.la==None:
			return
		else:
			raise ParseError("Expected IDENTIFIER or PRINT")
	def stmt(self):
		if self.la == 'IDENTIFIER':
			varname = self.text
			self.match('IDENTIFIER')	
			self.match('=')
			e = self.expr()
			self.st[varname] = e
		elif self.la == 'PRINT':
			self.match('PRINT')
			e = self.expr()
			print('{:b}'.format(e))
		else:
			raise ParseError("Expected IDENTIFIER or PRINT")
	def expr(self):
		if self.la == '(' or self.la == 'IDENTIFIER' or self.la == 'DINARY_TOKEN':
			t = self.term()
			while self.la == 'xor':
				self.match('xor')
				t2 = self.term()
				t ^= t2
			if self.la == 'IDENTIFIER' or self.la == 'PRINT' or self.la == None or self.la == ')':
					return t
			else:
					raise ParseError("Expected ^")
		else:
			raise ParseError("Expected ( or IDENTIFIER or DINARY_TOKEN or )")
	def term(self):
		if self.la=='(' or self.la=='IDENTIFIER' or self.la == 'DINARY_TOKEN':	
			t=self.factor()
			while self.la == 'or':
				self.match('or')
				t2 = self.factor()
				t |= t2
			if self.la == 'xor' or self.la == 'IDENTIFIER' or self.la == 'PRINT' or self.la == None or self.la==')':
				return t
			else:
				print(self.la)
				raise ParseError("Expected ( or IDENTIFIER or DINARY_TOKEN or )")
		else:
			raise ParseError("Expected * or /")
	def factor(self):
		if self.la=='(' or self.la == 'IDENTIFIER' or self.la == 'DINARY_TOKEN':
			t=self.atom()
			while self.la == 'and':
				self.match('and')
				t2 = self.atom()
				t &= t2
			if self.la == 'xor' or self.la == 'or' or self.la == 'IDENTIFIER' or self.la == 'PRINT' or self.la == None or self.la==')':
				return t
			else:
				print(self.la)
				raise ParseError("Expected ( or IDENTIFIER or DINARY_TOKEN or )")
		else:
			raise ParseError("Expected Number, Dinary h (")
	def atom(self):
		if self.la=='(':
			self.match('(')
			e=self.expr()
			self.match(')')
			return e
		elif self.la=='IDENTIFIER':
			varname = self.text
			self.match('IDENTIFIER')
			if varname in self.st:
				return self.st[varname]
		elif self.la=='DINARY_TOKEN':
			value=int(self.text,2)
			self.match('DINARY_TOKEN')
			return value
		else:
			raise ParseError("Expected id bit or (")
parser = MyParser()

with open('text.txt','r') as fp:
	parser.parse(fp)
