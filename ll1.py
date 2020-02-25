from collections import OrderedDict

def insert(grammar, lhs, rhs):
	if(lhs in grammar and rhs not in grammar[lhs] and grammar[lhs] != "null"):
		grammar[lhs].append(rhs)
	elif(lhs not in grammar or grammar[lhs] == "null"):
		grammar[lhs] = [rhs]
	return grammar
	
def first(state, grammar, grammar_first):
	global term
	global not_term
	global parse_table
	global ena
	rhs = grammar[state]
	for i in rhs:
		k = 0
		flag = 0
		confirm = 0
		flog = 0
		if(state in grammar and "`" in grammar_first[state]):
			flog = 1
		while(1):	
			check = []
			if(k>=len(i)):
				if(flag == 1 or confirm == k or flog == 1):
					grammar_first = insert(grammar_first, state, "`")
					parse_table[term.index(state)][not_term.index("`")] = [term.index(state),rhs.index(i)]					
					ena[term.index(state)] = [1,rhs.index(i)]
				break				
			if(i[k].isupper()):
				if(grammar_first[i[k]] == "null"):
					grammar_first = first(i[k], grammar, grammar_first)
				for j in grammar_first[i[k]]:
					grammar_first = insert(grammar_first, state, j)
					if(j!="`"):
						parse_table[term.index(state)][not_term.index(j)] = [term.index(state),rhs.index(i)]
					check.append(j)
			else:
				grammar_first = insert(grammar_first, state, i[k])
				check.append(i[k])
				if(i[k]!="`"):
					parse_table[term.index(state)][not_term.index(i[k])] = [term.index(state),rhs.index(i)]
			if(i[k]=="`"):
				flag = 1
			if("`" not in check):
				if(flog == 1):
					grammar_first = insert(grammar_first, state, "`")
					parse_table[term.index(state)][not_term.index("`")] = [term.index(state),rhs.index(i)]
					ena[term.index(state)] = [1,rhs.index(i)]
				break
			else:
				confirm += 1
				k+=1
				grammar_first[state].remove("`")
	return(grammar_first)

def for_follow(k, z, grammar_follow, i, grammar, start, grammar_first, state):
	global term
	global not_term
	global parse_table
	global ena
	if(len(k)==z):
		if(grammar_follow[i] == "null"):
			grammar_follow = follow(i, grammar, grammar_follow, start)
		for q in grammar_follow[i]:
			grammar_follow = insert(grammar_follow, state, q)
			if(ena[term.index(state)][0]==1):
				print()
				parse_table[term.index(state)][not_term.index(q)] = [term.index(state), ena[term.index(state)][1]]
	else:
		if(k[z].isupper()):
			for q in grammar_first[k[z]]:
				if(q=="`"):
					grammar_follow = for_follow(k, z+1, grammar_follow, i, grammar, start, grammar_first, state)		
				else:
					grammar_follow = insert(grammar_follow, state, q)
					if(ena[term.index(state)][0]==1):
						parse_table[term.index(state)][not_term.index(q)] = [term.index(state), ena[term.index(state)][1]]

		else:
			grammar_follow = insert(grammar_follow, state, k[z])
			if(ena[term.index(state)][0]==1):
				parse_table[term.index(state)][not_term.index(k[z])] = [term.index(state), ena[term.index(state)][1]]

			
	return(grammar_follow)
	
def follow(state, grammar, grammar_follow, start):
	for i in grammar:
		j = grammar[i]
		for k in j:
			if(state in k):
				z = k.index(state)+1
				grammar_follow = for_follow(k, z, grammar_follow, i, grammar, start, grammar_first, state)
	if(state==start):
		grammar_follow = insert(grammar_follow, state, "`")
	return(grammar_follow)

grammar = OrderedDict()
grammar_first = OrderedDict()
grammar_follow = OrderedDict()

f = open('grammar.c')
for i in f:
	i = i.replace("\n", "")
	lhs = ""
	rhs = ""
	flag = 1
	for j in i:
		if(j=="~"):
			flag = (flag+1)%2
			continue
		if(flag==1):
			lhs += j
		else:
			rhs += j
	grammar = insert(grammar, lhs, rhs)
	grammar_first[lhs] = "null"
	grammar_follow[lhs] = "null"

print("grammar == ", grammar)

parse_table = []
term = []
ena = []
not_term = []
for i in grammar:
	if(i not in term):
		term.append(i)
		ena.append([0,"null"])
	for j in grammar[i]:
		for k in j:
			if(k.islower() or k=="`"):
				if(k not in not_term):
					not_term.append(k)

for i in range(len(term)):
	parse_table.append([])
	for j in not_term:
		parse_table[i].append(["n","n"])
		


for i in grammar:
	if(grammar_first[i] == "null"):
		grammar_first = first(i, grammar, grammar_first)
print("first == ", grammar_first)

for i in grammar:
	if(grammar_follow[i] == "null"):
		grammar_follow = follow(i, grammar, grammar_follow, "S")
	
print("folllow == ",grammar_follow)
 
print(not_term)
for i in range(len(parse_table)):
	print(term[i], parse_table[i])
	
	
instr = input("Enter a valid string")

############################################################################################################################

stack = ["S","`"]
i = 0
while(1):
	if(stack[0] == "`"):
		break
	if(i< len(instr) and stack[0] == instr[i]):
		print(instr[i])
		i += 1
		stack.pop(0)
		continue
	k = parse_table[term.index(stack[0])][not_term.index(instr[i])]
	next = grammar[term[k[0]]][k[1]]
	next = next[::-1]
	stack.pop(0)
	for j in next:
		if(j != "`"):
			stack.insert(0,j)
