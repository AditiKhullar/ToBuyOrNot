#!/usr/bin/env python
import cgi,os,sys, re
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
#f = open('cgi-bin/tobuyornot/result.dat')
#if 'GO FOR IT' in open('cgi-bin/tobuyornot/result.dat').read():
#    buy = 'GO FOR IT'
#elif 'DONT BUY IT' in open('cgi-bin/tobuyornot/result.dat').read():
#	buy = 'DONT BUY IT'

f = open('cgi-bin/tobuyornot/result.dat')
for line in f:
	x = re.search('Verdict(.+?)Verdict', line)
	if x:
		buy = x.group(1)

f = open('cgi-bin/tobuyornot/result.dat')
for line in f:
	x = re.search('ProductName(.+?)ProductName', line)
	if x:
		productName = x.group(1)

f = open('cgi-bin/tobuyornot/result.dat')
for line in f:
	x = re.search('ProductURL(.+?)ProductURL', line)
	if x:
		productURL = x.group(1)

print "Content-Type: text/html"
print
print "<html><title>TO BUY OR NOT TO</title><body><p>Product ID is " + asin + "</p> <p>Product Name is <a target='_blank' href=" + productURL + ">" + productName + "</a></p>"
print "<p>", buy, "</p></body></html>"
