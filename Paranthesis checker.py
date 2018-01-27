#Stack Implementation to check the balance of paranthesis
#!/bin/python3

import sys

def isBalanced(symbolstring):
    s = []
    balanced =True
    index = 0
    while index < len(symbolstring) and balanced:
        symbol = symbolstring[index]
        if symbol in "([{":
            s.append(symbol)
            #print(symbol)
        else:
            if len(s) == 0:
                balanced = False
            else:
                top = s.pop()
                #print(top)
                if not matches(top, symbol):
                    balanced = False
        index = index+1
    if balanced and len(s)==0:
        return("YES")
    else:
        return("NO")
def matches(a,b):
    opens = "([{"
    closers = ")]}"
    if opens.index(a) == closers.index(b):
        return(True)
    else:
        return(False)

if __name__ == "__main__":
    t = int(input().strip())
    for a0 in range(t):
        s = input().strip()
        result = isBalanced(s)
        print(result)
