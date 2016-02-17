#!/usr/bin/python

from xmljson import yahoo as xml2json
from xml.etree.ElementTree import fromstring
from json import dumps
import sys, re

# ui2dgi.py
# YeboYebo S.L.U. 2016
# Ej: python ui2dgi.py /home/mihome/ruta/a/forms/familias.ui
# La salida será /home/mihome/ruta/a/forms/familias.dgi


# Claves a descartar (se descarta solamente esa propiedad)
# Ej: "images": "imagenEjemplo"
aPropsForbidden = ['images','includehints','layoutdefaults','slots','stdsetdef','stdset','version','spacer']
# Valores para la clave "name" a descartar (se descarta el objeto entero)
# Ej: {
# 	"name": "geometry",
# 	"propEjemplo": "valEjemplo",
# 	"propEjemplo2": "valEjemplo2"
# }
aObjsForbidden = ['geometry','sizePolicy','margin','spacing','frameShadow','frameShape','maximumSize','minimumSize','font','focusPolicy','iconSet']

def isInDgi(property, type):
	if type == "prop":
		if property in aPropsForbidden:
			return False
	else:
		if property in aObjsForbidden:
			return False
	return True

def manageProperties(obj):
	if isinstance(obj, dict):
		for property in obj:
			if isInDgi(property, "prop"):
				if property == "name" and not isInDgi(obj[property], "obj"):
					del obj
					return None
				else:
					prop = manageProperties(obj[property])
					if prop:
						obj[property] = prop
					else:
						del obj[property]
			else:
				del obj[property]
	elif isinstance(obj, list):
		ind = 0
		while ind < len(obj):
			it = manageProperties(obj[ind])
			if it:
				obj[ind] = it
				ind += 1
			else:
				del obj[ind]
	return obj

if len(sys.argv) != 2:
	print("Error. El numero de parametros debe ser 1")
	print("Ej: python ui2dgi.py rutaDelFichero.ui")
	sys.exit()

inputFile = sys.argv[1]
outputFile = re.search("\w+.ui", inputFile)

if outputFile == None:
	print("Error. El fichero debe tener extension .ui")
	sys.exit()

outputFile = re.sub(".ui", ".dgi", inputFile)

try:
	ui = open(inputFile, 'r')
	xml = ui.read()
except:
	print("Error. El fichero no existe o no tiene formato XML")
	sys.exit()

json = xml2json.data(fromstring(xml))
json = manageProperties(json)
strJson = dumps(json, sort_keys=True, indent=2)

try:
	dgi = open(outputFile, 'w')
	dgi.write(strJson)
	dgi.close()
except:
	print("Error. Ha habido un problema durante la escritura del fichero")
	sys.exit()

print("Hecho")