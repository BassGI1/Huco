from random import randint

def generateRandomSequence() -> str:
	string = ""
	allowedChars = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789"
	for _ in range(15): string += allowedChars[randint(0, len(allowedChars) - 1)]
	return string

def lexStringArray(arr, words):
	for i in range(len(arr)):
		if arr[i][0] != "f": continue
		pointer = 0
		wordLen = len(arr[i])
		while pointer < wordLen:
			string = ""
			while pointer < wordLen and arr[i][pointer] != "{": pointer += 1
			pointer += 1
			while pointer < wordLen and arr[i][pointer] != "}":
				string += arr[i][pointer]
				pointer += 1
			arr[i] = arr[i].replace(string, lex(string, words), 1)
			wordLen = len(arr[i])
		

def lex(src, words) -> str:
	# define constants
	illegalChars = {"(", ")", "+", "-", "/", "*", "^", "&", "|", "\n", "\t", " ", ":", ";", "#", "%", "@", "!", "~", "[", "]", "\\", "?", "<", ">", ".", ",", "`", "$", "=", '"', "'"}
	flag = generateRandomSequence()

	# define variables
	LexArray = []
	stringArray = []
	srcPointer = 0
	srcLength = len(src)

	# lexing algorithm
	while srcPointer < srcLength:

		token = ""

		while srcPointer < srcLength and src[srcPointer] in illegalChars:

			if src[srcPointer] == '"':
				rightPointer = srcPointer + 1

				while rightPointer < srcLength and src[rightPointer] != '"': rightPointer += 1

				temp = src[srcPointer: rightPointer + 1] if LexArray[-1].lower() != "f" else "f" + src[srcPointer: rightPointer + 1]

				stringArray.append(temp)
				src = src.replace(temp, flag, 1)
				srcLength = len(src)
				srcPointer += 14

			elif src[srcPointer] == "'":
				rightPointer = srcPointer + 1

				while rightPointer < srcLength and src[rightPointer] != "'": rightPointer += 1
				
				temp = src[srcPointer: rightPointer + 1] if LexArray[-1].lower() != "f" else "f" + src[srcPointer: rightPointer + 1]
				
				stringArray.append(temp)
				src = src.replace(temp, flag, 1)
				srcLength = len(src)
				srcPointer += 14

			srcPointer += 1

		while srcPointer < srcLength and src[srcPointer] not in illegalChars:

			token += src[srcPointer]
			srcPointer += 1
			if srcPointer >= srcLength:
				LexArray.append(token)
				break

		LexArray.append(token)

	lexStringArray(stringArray, words)
	LexArray = [e for e in LexArray if e in words]

	for elem in LexArray: src = src.replace(elem, words[elem], 1)
	for string in stringArray:
		src = src.replace(flag, string, 1)

	return src