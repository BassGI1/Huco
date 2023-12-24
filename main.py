from sys import argv
from subprocess import run
from os import remove
from os.path import isfile
from lexer import lex
from importlib import import_module
from shutil import rmtree

def reverseMap(lMap):
	m = {}
	for key, value in lMap.items():
		m[value] = key
	return m

# this function parses the Hfile
def parseHfile( path="Hfile" ):

	Hfile = open(path)
	optionsArray = [s for s in Hfile.read().replace(" ", "").replace("\n", ", ").split(", ") if len(s)]
	Hfile.close()

	op = {
		"language": None,
		"persist": False,
		"overwrite": False,
		"mode": None
	}

	for option in optionsArray:
		key, value = option.split(":")
		value = value.lower() if key != "language" else value
		
		if key == "language": op["language"] = value

		elif key == "persist":
			if value == "true": op["persist"] = True
			elif value == "false": op["persist"] = False
			else: raise Exception(f"{key} value ({value}) not acceptable")

		elif key == "overwrite":
			if value == "true": op["overwrite"] = True
			elif value == "false": op["overwrite"] = False
			else: raise Exception(f"{key} value ({value}) not acceptable")

		elif key == "mode":
			if value == "reverse": op["mode"] = "reverse"
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
languageMap = import_module(f"languages.{options['language']}").languageMap
if options["mode"]: languageMap = reverseMap(languageMap)

# opening the files
inputFile = open(cmdArgs["inputFile"])
rawInputText = inputFile.read()
outputFile = open(cmdArgs["outputFile"], "wb+")

# doing the translation
rawInputText = lex(rawInputText, languageMap)

# writing the translated file and executing it
outputFile.write(rawInputText.encode("utf-8"))
outputFile.close()
if options["mode"] != "reverse": run(["python3", cmdArgs["outputFile"]])

if not options["persist"]: remove(cmdArgs["outputFile"])
rmtree("__pycache__")
rmtree("./languages/__pycache__")

inputFile.close()