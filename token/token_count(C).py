l = ['auto', 'const', 'double', 'float', 'int', 'short', 'struct', 'unsigned', 'break', 'continue', 'else', 'for', 'long', 'signed', 'switch', 'void', 'case', 'default', 'enum', 'goto', 'register', 'sizeof', 'typedef', 'volatile', 'char', 'do', 'extern', 'if', 'return', 'static', 'union', 'while']

alpha = "qwertyuioplkjhgfdsazxcvbnm"
op = ['(', ')', '{', '}', '[', ']', '+', '-', '*', '/', '++', '--', '%', '=', '==', '!=']

f = open('check.c')
token = 0
var = []
func = ['main', 'printf', 'scanf']
flag = 0
for i in f:
	b = ""
	for j in i:
		if(j=='"'):
			flag = (flag+1)%2
		if(j=="/"):
			a = i.find(j)
			x = i[a]+i[a+1]
			if(x=="/*"):
				flag = 1
				
		if((j in " ;," or j in op) and flag==0):
			if((b in l or b in var or b in func or j in op) and b!=""):
#				print(b, "00")
				token += 1
				b = ""
			elif(b!=""):
				var.append(b)
				var.append("&"+b)
#				print(b, "01")
				token += 1
				b = ""
			if(j in op):
				a = i.find(j)
				x = i[a-1]+i[a] 
				y = i[a-2]+x
				if((x!="==" or x!="++" or x!="--" or x!="!=")):
#					print(j, x, y, "02")
					token += 1
				if(y=="+++"or y=="++-"or y=="--+"or y=="---"):
					token -= 1
			if(j in ";,"):
#				print(j, "03")
				token += 1
		else:
			b += j
		if(j=="/"):
			a = i.find(j)
			x = i[a-1]+i[a]
			if(x=="*/"):
				flag = 0
				token += 1
print(token)

