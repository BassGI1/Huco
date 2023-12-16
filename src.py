from sys import argv
from json import load
from subprocess import run
from os import remove
from os.path import isfile

# this function parses the Hfile
def parseHfile( path="Hfile" ):

	Hfile = open(path)
	optionsArray = [s for s in Hfile.read().replace(" ", "").replace("\n", ", ").split(", ") if len(s)]
	Hfile.close()

	op = {
		"language": None,
		"preserveVariableNames": False,
		"persist": False,
		"overwrite": False
	}

	for option in optionsArray:
		key, value = option.split(":")
		key = key
		value = value.lower()
		
		if key == "language":
			if value == "arabic": op["language"] = "Arabic"
			else: raise Exception(f"{key} value ({value}) not acceptable")

		elif key == "preserveVariableNames":
			if value == "true": op["preserveVariableNames"] = True
			elif value == "false": op["preserveVariableNames"] = False
			else: raise Exception(f"{key} value ({value}) not acceptable")

		elif key == "persist":
			if value == "true": op["persist"] = True
			elif value == "false": op["persist"] = False
			else: raise Exception(f"{key} value ({value}) not acceptable")

		elif key == "overwrite":
			if value == "true": op["overwrite"] = True
			elif value == "false": op["overwrite"] = False
			else: raise Exception(f"{key} value ({value}) not acceptable")

		else: raise Exception(f"{key} not allowed")

	if not op["language"]: raise Exception(f"{key} setting missing")

	return op
		
# this function parses the command line args
def parseCommandLine():
	if len(argv) < 3: raise Exception("unexpected usage - the command line arguments are of the form 'huco (input file) (output file) (optional - path to Hfile)'")
	cmdArgs = {}
	cmdArgs["inputFile"] = argv[1]
	cmdArgs["outputFile"] = argv[2]
	if len(argv) == 4: cmdArgs["pathToHfile"] = argv[3]
	return cmdArgs


# setting up command line arguments and parsing Hfile
cmdArgs = parseCommandLine()
options = None
if "pathToHfile" in cmdArgs: options = parseHfile(cmdArgs["pathToHfile"])
else: options = parseHfile()

# checking if the output file already exists and if the overwrite option is set
if isfile(cmdArgs["outputFile"]) and not options["overwrite"]: raise Exception(f"file '{cmdArgs['outputFile']}' already exists!")

# dynamically loading the appropriate language map
languageMap = None
with open(f"languages/{options['language']}.json") as f:
	languageMap = load(f)

# opening the files
inputFile = open(cmdArgs["inputFile"])
rawInputText = inputFile.read()
outputFile = open(cmdArgs["outputFile"], "w+")

# doing the translation
for tokenType, tokenObj in languageMap.items():
	for token, value in tokenObj.items():

		if tokenType == "keywords":
			rawInputText = rawInputText.replace(" " + token, " " + value).replace(token + " ", value + " ").replace(token + ":", value + ":")

		elif tokenType == "functions":
			rawInputText = rawInputText.replace(token + "(", value + "(").replace(token + " (", value + " (")


# writing the translated file and executing it
outputFile.write(rawInputText)
outputFile.close()
run(["python3", cmdArgs["outputFile"]])

if not options["persist"]: remove(cmdArgs["outputFile"])

inputFile.close()