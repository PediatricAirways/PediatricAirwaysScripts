# Replaces a string in a file with another string, and saves
# the results to another file.

import string
import sys

##########################################################
def FindReplaceInFile(inputFile, find, replace, outputFile):
  with open(inputFile, 'r') as f:
    read_data = f.read()
  
  replaced_text = read_data.replace(find, replace)
  
  with open(outputFile, 'w') as f:
    f.write(replaced_text)

##########################################################
if __name__ == "__main__":
  if (len(sys.argv) < 5):
    print "Usage:", sys.argv[0], "<input file> <find string> <replace string> <output file>"
    sys.exit(-1)

  FindReplaceInFile(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
