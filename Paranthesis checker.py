#Stack Implementation to check the balance of paranthesis
def parChecker(symbolstring):
	s= Stack()
	balanced = True
	index = 0
	while index < len(symbolstring) and balanced:
		symbol = symbolstring[index]
		if symbol == '(':
			s.push(symbol)
		else:
			if s.isEmpty():
				balanced = False
			else:
				top = s.pop()
				if not matches(top, symbol):
					balanced = False
		index = index +1

	if balanced and s.isEmpty():
		return(True)
	else:
		return(False)

print(parChecker('((()))'))
print(parChecker('(()'))
