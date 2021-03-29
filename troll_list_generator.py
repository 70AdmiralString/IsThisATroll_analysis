f = open("troll_list.txt", "r")

Trolls = []

def username(text: str) -> str:
	"""Enter a string of the form "u/george_BENTLEY	-1" and returns the username 'george_BENTLEY'"""
	text = text[2:]
	text2 = ''
	for l in text:
		if l == '\t':
			break
		else:
			text2 += l
	return text2

#Create the list of troll usernames
for x in f:
	Trolls.append(username(x))

f.close()

#Saves the list in a separate python file.
f2 = open("troll_list.py", "w")
f2.write('Trolls = ' + str(Trolls))
f2.close()