# work in progress, still contains test-site info

# brute-force sript to convert an org file into something similar in html.
# colors are based on emacs slate-gray bg and aurora color theme.
# fonts should be readable at any res, depends on browser/device though.
# nothing is interactive besides folding... that's a job fore a real programmer.
# there is no java/javascript in the output, external files are whatever is linked in the orgfile, and a couple of fonts.
# written by cpbrown in 2020, with help form w3 help docs.
# <meta charset=utf-8> is needed for block characters from org-plot (chrome defaults to uft-16, which breaks it).

# TODO: make headline and article fonts optional args
# TODO: copy all linked files to /pub, not just fonts
# TODO: delete everything in /pub before copying stuff over

import shutil
import codecs
import os
import sys
from datetime import datetime

pth = os.path.split(os.path.realpath('org.py'))[0] + '/'
myorg = pth + sys.argv[1]


# the endless quest for the right font...
fontheader = 'nk57-monospace-ex-eb' # great header font
#fontarticle = 'range-mono-medium-webfont' #bit too serify and cramped, block char isn't mono
#fontarticle = 'robotomono-m' #right proportions, clean style, but block char isn't mono :(
#fontarticle = 'saxmono' #more consistent with header style, but browser doesn't like it
#fontarticle = 'iosevka-eb' #blockchar is mono, but font a bit too curly. last resort...
#fontarticle = 'ocr-b10-bt' #not really mono, fugly comma, otherwise looks great
fontarticle = 'cinecavd-mono' #works with headline style, no monospace issues, very wide tho

headpart = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.1//EN">
<meta charset=utf-8>
<HTML>
<head>
<style type="text/css">
	@font-face {
		font-family: fhead;
		font-size: 12pt;
		src: url(""" + fontheader + """.ttf);
		src: url(""" + fontheader + """.woff);
	}
	@font-face {
		font-family: article;
		font-size: 12pt;
		src: url(""" + fontarticle + """.ttf);
		src: url(""" + fontarticle + """.woff);
	}
	body {
		background: #263238;
	}
	div {
		font-family: article;
		font-size: clamp(5px,0.7vw,20px);
		font-weight: 900;
		text-decoration: none;
		text-align: left;
	}
	td {
		font-family: article;
		font-size: clamp(10px,1.3vw,20px);
		font-weight: 900;
		text-decoration: none;
		text-align: left;
	}
	pre {
		font-family: article;
		font-size: clamp(5px,0.8vw,20px);
		font-weight: 700;
		text-decoration: none;
		white-space: pre-wrap;
		-webkit-text-size-adjust: none;
		text-size-adjust: none;
	}
	xmp {
		font-family: article;
		font-size: clamp(5px,1.0vw,20px);
		font-weight: 700;
		text-decoration: none;
		white-space: pre-wrap;
		-webkit-text-size-adjust: none;
		text-size-adjust: none;
	}
	.widetable {
		font-size: clamp(5px,0.7vw,20px);
	}
	a {
		font-family: article;
		color: inherit;
		text-decoration: underline;
		text-align: left;
	}
	summary {
		font-family: fhead;
		font-size: clamp(5px,3.5vw,30px);
		padding: 10px;
	}
	img {
		opacity: 0.8;
	}
	table {
		max-width: 100%;
	}
	div.a { margin-left: 1.0vw; color:#C2E982; background: #364440; }
	div.b { margin-left: 1.0vw; color:#F77669; background: #3C383C; }
	div.c { margin-left: 1.0vw; color:#82B1FF; background: #303E4C; }
	div.d { margin-left: 1.0vw; color:#CC9F52; background: #41484C; }
	div.e { margin-left: 1.0vw; color:#FF516D;}
	div.f { margin-left: 1.0vw; color:#9FC59F;}
	div.x { margin-left: 0px; color:#546D7A; font-size: 12pt; font-family: fhead; }
	div.xs { margin-left: 0px; color:#546D7A; font-size: 8pt; font-family: fhead; }
	summary.a { background: #364440; }
	summary.b { background: #3C383C; }
	summary.c { background: #303E4C; }
	summary.d { background: #41484C; }
	summary.e { background: rgba(255, 81, 109, 0.05); }
</style>
</head>
<body>
<div style="width: 95vw; align: left; margin-left: 0px;">
"""
import codecs
with codecs.open(myorg, encoding='utf-8') as f:
	lines = f.read().split('\n')
f.close()

ltr = ['', 'a', 'b', 'c', 'd', 'e', 'f']
orghtml = ''

def getdepth(line) :
	o = -1
	if len(line) > 0 :
		if line[0] == '*' :
			o = 0
			for i in range(len(line)) :
				if line[i] == '*' :
					o = o + 1
				else :
					break
	return o

def getsubs(lines,depth) :
	o = False
	for i in range(len(lines)) :
		d = getdepth(lines[i])
		if d > depth :
			o = True
			break
		else :
			if d >= 0 and d <= depth :
				o = False
				break
	return o

def getother(line) :
	o = [False,-1]
	d = getdepth(line)
	o[1] = d
	o[0] = d == -1
	return o                      

linedepth = -99
isaheader = False
hassubs = False
hasarticle = False
followsarticle = False
isanarticle = False
beginrecord = False
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
firstheader = True
currentdepth = 0
previousdepth = 0
amverbatim = False
amblock = False
nextline = [False,-1]
pauserecord = 99
orgtitle = ""
orgauthndate = ""
orgsubtitle = ""

for l in range(len(lines)) :
	linedepth = getdepth(lines[l]) - 1
	if not beginrecord :
		if "#+TITLE" in lines[l] :
			parts = lines[l].strip().split(':')
			if len(parts) > 1 : orgtitle = parts[1]
		if "#+AUTHOR :" in lines[l] and orgtitle != "" : 
			parts = lines[l].strip().split(':')
			nw = datetime.today()
			dord = nw.day
			# add a whiggle, because English... 
			# this clever oneliner posted by 'Frosty Snowman' here: https://stackoverflow.com/questions/3644417/python-format-datetime-with-st-nd-rd-th-english-ordinal-suffix-like
			whiggle = ("th" if 4<=dord%100<=20 else {1:"st",2:"nd",3:"rd"}.get(dord%10, "th"))
			# assemble title as title. author. month dayth year
			if len(parts) > 1 : orgauthndate = ". " + parts[1] + ". " + datetime.strftime(nw,"%B %-d") + whiggle + " " + datetime.strftime(nw,"%Y")
		if "#+SUBTITLE :" in lines[l] : 
			parts = lines[l].strip().split(':')
			if len(parts) > 1 : orgsubtitle = parts[1]
		if orgtitle != "" and orgauthndate != "" :
			orghtml = orghtml + '<div class="x"># ' + orgtitle + orgauthndate + '</div>\n'
			orgtitle = ""; orgauthndate = ""
		if orgsubtitle != "" : 
			orghtml = orghtml + '<div class="xs"><i># ' + orgsubtitle + '</i></div>\n<BR><BR>\n'
			orgsubtitle = ""
		beginrecord = linedepth >= 0
	isaheader = linedepth >= 0
	if isaheader : 
		currentdepth = linedepth
		if pauserecord >= linedepth :
			pauserecord = 99
	if beginrecord :
		hassubs = False
		hasarticle = False
		followsparentheader = False
		followssiblingheader = False
		followschildheader = False
		isanarticle = linedepth < 0
		if isaheader and ":noexport:" in lines[l] : 
			isanarticle = False
			isaheader = False
			pauserecord = linedepth
		if pauserecord > currentdepth :
			if l < (len(lines) - 1) and isaheader :
				hassubs = getsubs(lines[(l+1):],linedepth+1)
				nextline = getother(lines[l+1])
				hasarticle = nextline[0]
			followsarticle = False
			if isaheader :
				if l > 0 :
					checkprevious = getother(lines[l-1])
					followsarticle = checkprevious[0]
					if not followsarticle :
						followsparentheader = checkprevious[1] < linedepth
						followssiblingheader = checkprevious[1] == linedepth
						followschildheader = checkprevious[1] > linedepth
			linestring = ""             
			indent = ""
			if isaheader and not firstheader  :
				indent = ''.ljust((previousdepth)*4,' ')
				if followsarticle : 
					linestring = linestring + indent + '\t</TD></TR></TABLE>\n'
				diffdepth = linedepth - previousdepth
				if diffdepth < 0  :
					for x in range(abs(diffdepth)+1) :
						indent = ''.ljust(((previousdepth - x)*4),' ')
						linestring = linestring + indent + '</details>\n'
						linestring = linestring + indent + '</div>\n'
				if diffdepth == 0 :
					linestring = linestring + indent + '</details>\n'
					linestring = linestring + indent + '</div>\n'
			if isaheader  :
				indent = ''.ljust((linedepth)*4,' ')
				ltr = letters[linedepth]
				linestring = linestring + indent + '<div class=\"' + ltr + '\">\n'
				linestring = linestring + indent + '<details><summary class=\"' + ltr + '\">' + lines[l].replace('*','').strip() + '</summary>\n'
				if hasarticle : 
					linestring = linestring + indent + '\t<TABLE  BORDER=0 CELLPADDING=25 CELLSPACING=10 height="10" align="BLEEDLEFT"><TR><TD>\n'
			if isanarticle :
				xmpme = False
				capxmp = False
				checktag = lines[l].strip()
				if checktag == '<pre>' : amverbatim = True
				if checktag == '<xmp>' : amverbatim = True
				if checktag == '<xmp class=\"widetable\">' : amverbatim = True
				if checktag == '</pre>' : amverbatim = False
				if checktag == '</xmp>' : amverbatim = False
				checkblock = lines[l].strip().lower()
				if '#+begin_src ' in checkblock and amverbatim == False: amverbatim = True; amblock = True; xmpme = True
				if '#+begin_example' in checkblock and amverbatim == False : amverbatim = True; amblock = True; xmpme = True
				if '#+end_src' in checkblock and amblock == True : amverbatim = False; amblock = False; capxmp = True
				if '#+end_example' in checkblock  and amblock == True : amverbatim = False; amblock = False; capxmp = True
				indent = ''.ljust((currentdepth)*8,' ')
				nwl = '<BR>\n'
				if amverbatim : nwl = '\n'
				if len(lines[l]) > 0 :
					whatline = lines[l] + nwl
					if xmpme : whatline = '<xmp>\n'
					if capxmp : whatline = '</xmp>\n'
					for c in range(len(lines[l])) :
						if lines[l][c] == '[' :
							if lines[l][c+1] == '[' :
								hpart = lines[l][:c]
								linkpart = lines[l][c:]
								tailpart = ''
								linkh = ''
								linkl = linkpart.strip().replace('[','').replace(']',';').split(';')
								linkf = linkl[0].strip()
								if len(linkl) > 1 : tailpart = tailpart.join(linkl[2:])
								isimage = False
								if '.png' in linkf or '.jpg' in linkf or '.gif' in linkf :
									linkf = linkf.replace('./', '')
									linkh = '<img src=\"' + linkf + '\">'
									isimage = True
								if 'http' in linkf :
									linkh = '<a href=\"' + linkf + '\" target="_new">'
								if len(linkl) > 0 :
									whatline = hpart + linkh + linkl[1].strip() + '</a>' + tailpart + '<BR>\n'
									if isimage : 
										whatline = hpart + linkh + '\n<figcaption>' + linkl[1].strip() + '</figcaption>' + tailpart + '<BR>\n'
								else : 
									whatline = hpart + linkh + linkf + '</a><BR>\n'
									if isimage: whatline = hpart + linkh + '<BR>\n'
								break
					if '- [ ]' in whatline :
						bc = '- <span style="box-shadow: 1px 1px 1px #111A1E;">[ ]</span>'
						whatline = whatline.replace('- [ ]', bc)
					if '- [X]' in lines[l] :
						bc = '- <span style="box-shadow: 1px 1px 1px #111A1E;">[X]</span>'
						whatline = whatline.replace('- [X]', bc)
					if '- [-]' in lines[l] :
						bc = '- <span style="box-shadow: 1px 1px 1px #111A1E;">[-]</span>'
						whatline = whatline.replace('- [-]', bc)
					if amverbatim : whatline = whatline.replace('\u00A0',' ')
					linestring = linestring + whatline    
				else :
					linestring = linestring + nwl
			orghtml = orghtml + linestring
			if isaheader : 
				firstheader = False 
				previousdepth = linedepth
linestring = ""
diffdepth = 0 - previousdepth
if getother(lines[len(lines)-1])[0] :
	indent = ''.ljust(((previousdepth)*4),' ')
	linestring = linestring + indent + '\t</TD></TR></TABLE>\n'
if diffdepth <= 0  :
	for x in range(abs(diffdepth)+1) :
		indent = ''.ljust(((previousdepth - x)*4),' ')
		linestring = linestring + indent + '</details>\n'
		linestring = linestring + indent + '</div>\n'
orghtml = orghtml + linestring
orghtml = orghtml + '</div>\n'
orghtml = orghtml + '</body>\n'
orghtml = orghtml + '</html>'
orghtml = headpart + orghtml              
f = open (pth + 'index.html','w')
for n in orghtml :
	f.write(n)
f.close()

shutil.copyfile(pth+"index.html", pth+"pub/index.html")
try:
	shutil.copyfile(pth+fontheader+".ttf", pth+"pub/"+fontheader+".ttf")
except:
	print("no ttf font for header")
try:
	shutil.copyfile(pth+fontheader+".woff", pth+"pub/"+fontheader+".woff")
except:
	print("no woff font for header")
try:
	shutil.copyfile(pth+fontarticle+".ttf", pth+"pub/"+fontarticle+".ttf")
except:
	print("no ttf font for article")
try:
	shutil.copyfile(pth+fontarticle+".woff", pth+"pub/"+fontarticle+".woff")
except:
	print("no woff font for article")
try:
	shutil.copyfile(pth+fontarticle+".woff2", pth+"pub/"+fontarticle+".woff2")
except:
	print("no woff2 font for article")
