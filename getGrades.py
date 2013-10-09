import sys
import re
import getpass

#set up twill, declare browser for capturing output, then import commands to match the 'b'.
from twill import get_browser
b = get_browser()
from twill.commands import *

USERNAME="";
#PASSWORD="";
CLASSES = "";
GRADES = "";

#check for args user and pass, if no args, prompt.
if(len(sys.argv)>1):
	USERNAME = sys.argv[1]
	PASSWORD = sys.argv[2]
else:
	USERNAME = raw_input("KSU Username:")
	PASSWORD = getpass.getpass()


b.go ("https://connect.ksu.edu")
formvalue("loginForm","username",USERNAME)
formvalue("loginForm","password",PASSWORD)
submit()
#navigate to KSOL from connect.ksu.edu
follow("https://online.ksu.edu/Axio/")
go("https://online.ksu.edu/Axio/UMS/CourseListing")
#get classes to analyze KSOLMainSource
KSOLMainSource = show()
#class titles appear to be in dd tag. regex:
CLASSES = re.findall("<dd>(.*?)</dd>",KSOLMainSource,re.S)
CLASSLINKS = re.findall("<dt> <a href=\"(.*?)\".*</dt>", KSOLMainSource, re.S)

for match in CLASSES :
	print match + "\n"
for link in CLASSLINKS :
	print link + "\n"