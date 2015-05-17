#!/usr/bin/env python3
from bs4 import BeautifulSoup
import subprocess
import sys
import os.path
import os
import glob
import shutil
import re

deflist = list()
layerlist = list()
prefix = "0"
def svglayer(tagorder="open"):
	layeropen = "<g\n inkscape:groupmode=\"layer\"\n id=\"layer3\"\n inkscape:label=\"Ebene 3\">"
	layerclose = "</g>"
	if tagorder=="open":
		return(layeropen)
	elif tagorder=="close":
		return(layerclose)

if not shutil.which("pdf2svg"):
	print("pdf2svg not found")
	sys.exit(0)

originpdf = sys.argv[1]

if not os.path.isfile(originpdf):
	print('File not found: ' + originpdf)
	sys.exit(0)
subprocess.call(["pdf2svg", originpdf, "pages%d.svg", "all"])
pages = glob.glob("pages*.svg")
for page in pages:
	prefix = str(int(prefix)+1)
	with open(page) as f:
		svgcontent = f.read()
	soup = BeautifulSoup(svgcontent, 'lxml')
	for tag in soup.find_all(True):
		if tag.has_attr('id'):
			tag['id'] = prefix + tag['id']
		if tag.has_attr('xlink:href'):
			tag['xlink:href'] = '#' + prefix + tag['xlink:href'].strip('#')
	deflist.append(str(soup.svg.defs).replace("<defs>","").replace("</defs>",""))
	layerlist.append(soup.find_all('g',{'id':re.compile("surface+")})[0])

for page in pages:
	os.remove(page)
	pass

with open("svghead") as f:
	svghead = f.read()

with open("layeredup.svg","w+") as f:
	f.write(svghead)
	for definition in deflist:
		f.write(definition)
	for layer in layerlist:
		f.write(svglayer("open"))
		f.write(str(layer))
		f.write(svglayer("close"))
	f.write("</svg>")
