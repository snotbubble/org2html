# henious brute-force 1st-attempt sript to convert an org file into something similar in html.
# colors are based on emacs slate-gray bg and aurora color theme.
# nothing is interactive besides folding... that's a job fore a real programmer.
# there is no java/javascript in the output, external files are whatever is linked in the orgfile, and a couple of fonts.
# written by cpbrown in 2020, with help form w3 help docs.

pth = '/home/cpb/Documents/txt/'

import shutil
import codecs

myorg = pth + 'cpbrown_notes.org'
#myorg = pth + 'test.org'


fontheader = 'nk57-monospace-ex-eb' # great header font
#fontarticle = 'range-mono-medium-webfont' #bit too serify and cramped, block char isn't mono
#fontarticle = 'robotomono-m' #right proportions, clean style, but block char isn't mono :(
#fontarticle = 'saxmono' #more consistent with header style, but browser doesn't like it
#fontarticle = 'iosevka-eb' #blockchar is mono, but font a bit too curly. last resort...
#fontarticle = 'ocr-b10-bt' #not really mono, fugly comma, otherwise looks great
fontarticle = 'cinecavd-mono' #works with headline style, no monospace issues, very wide tho

headpart = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.1//EN">
<HTML>
<head>
<!-- Range-Mono font is licensed from monolithfoundry.com. -->
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
		font-size: clamp(5px,3.0vw,20px);
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
	}
	xmp {
		font-family: article;
		font-size: clamp(5px,1.0vw,20px);
		font-weight: 700;
		text-decoration: none;
		white-space: pre-wrap;
	}
	.widetable {
		font-size: clamp(5px,0.8vw,20px);
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
<div class="x"># reference notes. c.p.brown 2020</div>
<div class="xs"><i># information on this site is fictional</i></div>
<BR>
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

linedepth = 0
isaheader = False
hassubs = False
hasarticle = False
followsblank = False
followsarticle = False
isanarticle = False
isblankarticle = False
beginrecord = False
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
firstheader = True
currentdepth = 0
previousdepth = 0
amverbatim = False
nextline = [False,-1]
pauserecord = 99

for l in range(len(lines)) :
	linedepth = getdepth(lines[l]) - 1
	isaheader = linedepth >= 0
	if isaheader : 
		currentdepth = linedepth
		if pauserecord >= linedepth :
			pauserecord = 99
	if not beginrecord : beginrecord = linedepth >= 0
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
			#print("found a noexport, pausing at depth: " + str(linedepth))
		#print("comparing : " + str(pauserecord) + " : " + str(currentdepth) + " : " + lines[l].strip())
		if pauserecord > currentdepth :
			if l < (len(lines) - 1) and isaheader :
				hassubs = getsubs(lines[(l+1):],linedepth+1)
				nextline = getother(lines[l+1])
				hasarticle = nextline[0]
			followsarticle = False
			if isaheader :
				#currentdepth = linedepth
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
				#print(str(linedepth) + " : " + str(previousdepth) + " : " + str(hassubs) + " : "  + lines[l])
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
				if '#+begin_src ' in checkblock : amverbatim = True; xmpme = True
				if '#+begin_example' in checkblock : amverbatim = True; xmpme = True
				if '#+end_src' in checkblock : amverbatim = False; capxmp = True
				if '#+end_example' in checkblock : amverbatim = False; capxmp = True
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
#print(str(linedepth) + " : " + str(previousdepth) + " : " + str(hassubs) + " : "  + lines[l])
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
