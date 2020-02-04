def close(a, T, v):
	q = [a]
	p = [a]
	i=0
	while(i<len(p)):
		for j in T[p[i]][v]:
			if(j!=-1 and j not in q):
				q.append(j)
				p.append(j)
		i+=1
	q = list(dict.fromkeys(q))
		
	return(q)

def closenew(a, T, v):
	q = []
	for j in T[a][v]:
		if(j!=-1 and j not in q):
			q.append(j)
	q = list(dict.fromkeys(q))
		
	return(q)
	
def do(ans, state, tr, template, count, name_track): 
	a = []
	for i in state:
		a += close(i,tr,0)
	a.sort()
	a = list(dict.fromkeys(a))
	
	abc = []
	for i in template:
		abc.append(i)
	ans.append(abc)
	ans[count][0] = name_track
	legend[str(a)] = name_track
	name_track += 1
	
#	print("epsilon closure == "+str(a)+" for states == "+str(state))
	
	for j in range(var-1):
		p = []
		for i in a:
			p += closenew(i, tr, j+1)
		p.sort()
		p = list(dict.fromkeys(p))
		z = []
		for i in p:
			z += close(i, tr, 0)
		z.sort()
		z = list(dict.fromkeys(z))
		
		if(str(z) in legend):
			ans[count][j+1] = legend[str(z)]
		elif(len(z)!=0):
			ans = do(ans, z, tr, template, count+1, name_track)
			ans[count][j+1] = legend[str(z)]
			
	return(ans)		
		
			

n = int(input("no of states"))
var = int(input("variables"))+1

tr = []

for i in range(n):
	tr.append([])
	for j in range(var):
		p = 9999
		q = []
		while(p!=-1):
			p = int(input("from "+str(i)+" var "+str(j)+" -1 for null"))
			q.append(p)
		q.pop()
		if(len(q)==0):
			q.append(-1)
		q.sort()
		tr[i].append(q)
'''
print("eNFA transition table")
for i in tr:
	print(i)
'''
final = []
start = int(input("enter start state"))	

k=0
print("enter final states (-1 to end)")
while(k!=-1):
	k = int(input())
	final.append(k)
final.pop()

ans = []
template = ["name"]
for i in range(var-1):
	template.append("trap")
i=0
name_track=0

legend = {}

ans = do([], [0], tr, template, 0, 0)

print("Final dfa transition state")
print("States\tNew\t", end="")

for i in range(var-1):
	print("var", i,end = "\t")
	
print()

all_states = list(legend.keys())

for j in range(len(legend)):
	print(all_states[j], end="\t")
	print(legend[all_states[j]], end="\t")
	index = 0    
	for i in range(len(ans)):
		if(ans[i][0] == legend[all_states[j]]):
			index = i
			break    

	for p in range(var-2):
		print(ans[index][p+1], end="\t")
	
	print(ans[index][var-1])
	
new_final = []
for i in all_states:
	for j in final:
		if(str(j) in i):
			new_final.append(legend[i])

print("Final states : ")
for i in new_final:
	print(i)


