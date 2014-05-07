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
buy = "DONT BUY IT"

# Avoid script injection escaping the user input
if 'GO FOR IT' in open('cgi-bin/tobuyornot/result.dat').read():
    buy = 'GO FOR IT'


print "Content-Type: text/html"
print
print "<html><body><p>The submited asin was", asin,"</p>"
print buy, "</p></body></html>"
