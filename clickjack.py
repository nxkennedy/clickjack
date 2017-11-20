#!/usr/bin/env python
##
# Author: Nolan Kennedy (nxkennedy)
#
# Description: Tool to quickly verify if a web page is vulnerable to clickjacking.
# 		Attempts to render the target site in an iframe and places another
#		iframe on top of it as an example attack. Built around the PoC
#		html boilerplate provided by OWASP.
#
# Use Case: Verifying web scanner findings to rule out false positives.
#
# Requirements: python 2.7
#
# Usage: python clickjack.py <url>
#
# About Clickjacking: https://www.owasp.org/index.php/Clickjacking
##

import os
import sys
import webbrowser

if len(sys.argv) != 2:
	print '\n[+] Description: %s can quickly verify if a web page is vulnerable to clickjacking' % __file__ 
	print '[+] Usage: python %s <url>\n' % __file__
	exit(0)

url = sys.argv[1]

html = '''
<html>
        <head>
                <title>Clickjacking Test Page</title>
        </head>

	<body>
		<div style = "postion: absolute; left: 10px; top: 10px;">
			<h1>Clickjacking Test Results</h2>
			<h2>Target: <a href="%s">%s</a></h2>
			<h3>If you see the target website rendered below, it is <font color="red">VULNERABLE</font>.</h3>
		</div>
		<iframe width= "900" height="600" src="%s"></iframe>
		<iframe style = "position: absolute; left: 20px; top 10px; opacity: 0.8; background: AliceBlue; font-weight: bold;" src="cj-attacker.html"></iframe>
        </body>
</html>
''' % (url, url, url)

html2 = '''
<html>
	<div style="opacity: 1.0; position: absolute; left: 10px; top: 50px; background: PapayaWhip; font-weight: bold;">
		<center><a href="#">THIS IS AN EXAMPLE CLICKJACKING IFRAME AND LINK</a>
		<br>(normally invisible)</center>
	</div>
</html>
'''

cjt = os.path.abspath('cj-target.html')
cja =  os.path.abspath('cj-attacker.html')
localurl = 'file://' + cjt

with open(cjt, 'w') as t, open(cja, 'w') as a:
	t.write(html)
	a.write(html2)

webbrowser.open(localurl)

print '\n[+] Target: %s' % cjt
print '[+] Created files "cj-target.html" and "cj-attacker.html"'
print '[+] If you see the target website in your browser window, it is vulnerable.'
print '[+] Test Complete!\n'
