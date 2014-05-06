#!/usr/bin/env python
import cgi,os,sys
import cgitb; cgitb.enable() 
#print 'Content-Type: text/html\n\n'
#print ''
#print 'test'
form = cgi.FieldStorage() # instantiate only once!
asin = form.getvalue("asin", "")

#os.chdir("")
os.system("cd cgi-bin/tobuyornot/ ; python Aggregator.py > result.dat")

print "hello"
buy = false

# Avoid script injection escaping the user input
if 'GO FOR IT' in open('result.txt').read():
    buy = true


print "Content-Type: text/html"
print
print """
<html><body>
<p>The submited asin was "%s"</p>
<p>"%s"</p>
</body></html>
""" % asin, result
