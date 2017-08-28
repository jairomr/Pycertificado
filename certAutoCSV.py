# -*-coding=utf-8 -*-
# encoding: utf-8 
import sys
import os
import pdfkit
import imgkit
import csv
from unicodedata import normalize
import re

"""
Funçao de carregar a lista de nome e gera certificado com a lista, ou carregar um nomer e gerar o certificado
lista pode ser uma string informando o local do arquivo txt com os nomes ou uma string com o nome
"""
def gerarCert(lista,data,contFileName="conteudo.txt",binPdf="C:/Program Files/wkhtmltopdf/bin/wkhtmlto"):
	if(lista[-4:]==".txt"):
		f=open(lista, 'rU')
		for line in f: 
			print "Gerando cetificado para "+line
			geradorCert(line,data,contFileName,binPdf)
	elif(lista[-4:]==".csv"):
		with open(lista) as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				print("\n"+row['name'])
				geradorCert(row['name'],data,contFileName,binPdf,row['pres'])
	else:
		print "Gerando cetificado para "+lista
		geradorCert(lista,data,contFileName,binPdf)

"""
Funcap de gera certificado aprartir de um nome
"""
def geradorCert(name,data,contFileName="conteudo.txt",binPdf="C:/Program Files/wkhtmltopdf/bin/wkhtmlto", pres=0):
	configPdf = pdfkit.configuration(wkhtmltopdf=binPdf+"pdf.exe")
	configImg = imgkit.config(wkhtmltoimage=binPdf+"image.exe")
	name=name.replace('\n', '')
	#Carregar os arquivos
	contFile=open(contFileName, "r") 
	html=open('templat.html', "r")
	 
	#Le os arquivos
	cont = contFile.read()
	htmlF = html.read()

	#Faz as subustituição
	cont=cont.replace("%NOME%", name)
	if(pres!=0):
		cont=cont.replace("%PRES%",pres)
	htmlF=htmlF.replace("%NOME%",name)
	htmlF=htmlF.replace('%DATA%',data)
	htmlF=htmlF.replace('%CONT%',cont)

	#Criar os arquivos dos certificados
	hname='html/'+removeEspecial(name)+'.html'
	pdf='certPDF/'+removeEspecial(name)+'.pdf'
	png='certImg/'+removeEspecial(name)+'.png'
	f = open(hname,'w')
	f.write(htmlF)
	f.close()
	options = {
		'margin-bottom':'0mm',
  		'margin-left':'0mm',
  		'margin-right':'0mm',
  		'margin-top':'0mm',
		'dpi':'900',
		'orientation':'Landscape'
    	}

	pdfkit.from_file(hname ,pdf,configuration=configPdf,options=options)
	imgkit.from_file(hname ,png,config=configImg,options={'quality':'100'})
"""
A remoção de acentos foi baseada em uma resposta no Stack Overflow.
http://stackoverflow.com/a/517974/3464573
"""
def removeEspecial(txt, codif='utf-8'):
	return normalize('NFKD', txt.decode(codif)).encode('ASCII','ignore')

def encode(arg):
	print arg.encode('utf-8')
	return arg.encode('utf-8')

def cmd():
	if len(sys.argv)  == 3:
		gerarCert(encode(sys.argv[1]),encode(sys.argv[2]))
	elif len(sys.argv)  == 4:
		gerarCert( encode(sys.argv[1]),encode(sys.argv[2]),encode(sys.argv[3]))
	elif len(sys.argv)  == 5:
		gerarCert(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])

def help():
	helpf=open('readme.txt', "r")
	helpf = helpf.read()
	helpf=helpf.decode('utf-8')
	print helpf
"""
Genado certificado
"""
reload(sys)
sys.setdefaultencoding('Cp1252') 
if len(sys.argv)  >= 1:
	if len(sys.argv)  == 1:
		help()
	elif len(sys.argv)  == 2:
		if sys.argv[1][0]=="-":
			help()	
	else:
		cmd()