#!/usr/bin/env python
import cgi,os,sys
import cgitb; cgitb.enable() 
#print 'Content-Type: text/html\n\n'
#print ''
#print 'test'
form = cgi.FieldStorage() # instantiate only once!
asin = form.getvalue("asin", "")

#os.chdir("")
os.system("cd cgi-bin/tobuyornot/ ; python Aggregator.py " + asin + "> result.dat")

print "hello"
buy = "CANNOT PREDICT, TRY YOUR LUCK"

# Avoid script injection escaping the user input
f = open('cgi-bin/tobuyornot/result.dat')
if 'GO FOR IT' in f.read():
    buy = 'GO FOR IT'
elif 'DONT BUY IT' in f.read():
	buy = 'DONT BUY IT'



print "Content-Type: text/html"
print
print "<html><body><p>The submited asin was", asin,"</p>"
print buy, "</p></body></html>"
