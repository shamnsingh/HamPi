# Parse the arguments given in a textfile.

# Given the path, parse the arguments and return the resulting dictionary.
def parse(path):
    args = {}

    f = open(path, 'r')

    for line in f:
        s = line.split('=')
        args[s[0]] = float(s[1]) 

    f.close()
    return args

def parseString(path):
    args = {}

    f = open(path, 'r')

    for line in f:
        s = line.split('=')
        args[s[0]] = s[1] 

    f.close()
    return args
