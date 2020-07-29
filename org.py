# henious brute-force 1st-attempt sript to convert an org file into something similar in html.
# colors are based on emacs slate-gray bg and aurora color theme.
# nothing is interactive besides folding... that's a job fore a real programmer.
# there is no java/javascript in the output, external files are whatever is linked in the orgfile, and a couple of fonts.
# written by cpbrown in 2020, with help form w3 help docs.

pth = '/home/cpb/Documents/txt/'

import shutil
import codecs

myorg = pth + 'cpbrown_notes.org'
myorg = pth + 'test.org'

fontpre = 'ankacoder-r'
#fontheader = 'nk57-monospace-ex-eb'
fontheader = 'nk57-monospace-ex-eb'

headpart = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.1//EN">
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
		src: url(""" + fontpre + """.ttf);
		src: url(""" + fontpre + """.woff2);
	}
	body {
		background: #263238;
	}
	div { 
		font-family: fhead;
		font-size: 12pt;
		font-weight: 900;
		text-decoration: none;
		text-align: left;
	}
	td {
		font-family: article;
		font-size: 12pt;
		font-weight: 900;
		text-decoration: none;
		text-align: left;
	}
	pre {
		font-family: article;
		font-size: 9pt;
		font-weight: 700;
		text-decoration: none;
		text-align: left;
	}
	xmp {
		font-family: article;
		font-size: 9pt;
		font-weight: 700;
		text-decoration: none;
		text-align: left;
	}
	a { 
		color: inherit;
		font-family: article;
		font-size: 12pt;
		font-weight: 900;
		text-decoration: underline;
		text-align: left;
	}
	summary {
		padding: 10px;
	}
	img {
		opacity: 0.8;
	}
	table {
		max-width: 800px;
	}
	div.a { margin-left: 10px; color:#C2E982; background: #364440; }
	div.b { margin-left: 20px; color:#F77669; background: #3C383C; }
	div.c { margin-left: 30px; color:#82B1FF; background: #303E4C; }
	div.d { margin-left: 40px; color:#CC9F52; background: #41484C; }
	div.e { margin-left: 50px; color:#FF516D;}
	div.f { margin-left: 60px; color:#9FC59F;}
	div.x { margin-left: 0px; color:#546D7A;}
	summary.a { background: #364440; }
	summary.b { background: #3C383C; }
	summary.c { background: #303E4C; }
	summary.d { background: #41484C; }
	summary.e { background: rgba(255, 81, 109, 0.05); }
</style>
</head>
<body>
<div class="x"># reference notes. by c.p.brown 2020</div>
<div class="x"><pre><i># information on this site is fictional</i></pre></div>
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

for l in range(len(lines)) :
	linedepth = getdepth(lines[l]) - 1
	isaheader = linedepth >= 0
	if not beginrecord : beginrecord = linedepth >= 0
	if beginrecord :
		hassubs = False
		hasarticle = False
		followsparentheader = False
		followssiblingheader = False
		followschildheader = False
		isanarticle = linedepth < 0
		if l < (len(lines) - 1) and isaheader :
			hassubs = getsubs(lines[(l+1):],linedepth+1)
			nextline = getother(lines[l+1])
			hasarticle = nextline[0]
		followsarticle = False
		if isaheader :
			currentdepth = linedepth
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
			if lines[l].strip() == '<pre>' : amverbatim = True
			if lines[l].strip() == '<xmp>' : amverbatim = True
			if lines[l].strip() == '</pre>' : amverbatim = False
			if lines[l].strip() == '</xmp>' : amverbatim = False
			indent = ''.ljust((currentdepth)*8,' ')
			nwl = '<BR>\n'
			if amverbatim : nwl = '\n'
			if len(lines[l]) > 0 :
				whatline = lines[l] + nwl
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
								whatline = hpart + linkh + linkl[1].strip() + '</a>' + tailpart + '\n'
								if isimage : 
									whatline = hpart + linkh + '\n<figcaption>' + linkl[1].strip() + '</figcaption>' + tailpart + '\n'
							else : 
								whatline = hpart + linkh + linkf + '</a>\n'
								if isimage: whatline = hpart + linkh + '\n'
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
	linestring = linestring + indent + '\t</TD></TR></TABLE>\n'
if diffdepth <= 0  :
	for x in range(abs(diffdepth)+1) :
		indent = ''.ljust(((previousdepth - x)*4),' ')
		linestring = linestring + indent + '</details>\n'
		linestring = linestring + indent + '</div>\n'
orghtml = orghtml + linestring
orghtml = orghtml + '</body>\n'
orghtml = orghtml + '</html>'
orghtml = headpart + orghtml              
f = open (pth + 'index.html','w')
for n in orghtml :
	f.write(n)
f.close()
