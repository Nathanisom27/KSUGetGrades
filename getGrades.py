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
CLASSLINKS = re.findall("<dt><a href=\"(.*?)\".*?</dt>", KSOLMainSource, re.S)

#links format: https://online.ksu.edu/SymMetrics/jsp/StudentAssignment/index.jsp?courseName=chm_210_lab
#assignments and grade page URL example: 
#https://online.ksu.edu/SymMetrics/jsp/StudentAssignment/index.jsp?courseName=chm_210_lab
#so split link by '=' and insert onto grading url
ListOfClasses = []
ListOfGrades = []

print "Detected the following classes:"
for match in CLASSES :
	print match
	ListOfClasses.append(match)
print "grades attached to classes:"
for link in CLASSLINKS :
	b.go("https://online.ksu.edu/SymMetrics/jsp/StudentAssignment/index.jsp?courseName="+link.split("=")[1])
	gradeTemp = re.findall("- [0-9\.]+%",show(), re.S)
	if(gradeTemp == None or gradeTemp == []):
		ListOfGrades.append("N/A")
	else:
		grade = str(gradeTemp[-1])
		ListOfGrades.append(grade)
	print link

for x in range(0,len(ListOfGrades)):
	print ListOfClasses[x] + " \t\t----- " + ListOfGrades[x]
