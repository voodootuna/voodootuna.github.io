# -*- coding: utf-8 -*-

data = """1;	AA;	Xavier Christian Barbe Government School;	2,704\n
2;	AAB;	New Pailles Government School;	2,555\n
3;	AAC;	Pailles State Secondary School (Girls);	3,376\n
4;	AB;	Richelieu Government School;	3,754\n
5;	AC;	Pointe aux Sables Government School;	5,133\n
6;	ACA;	J. M. Frank Richard State Secondary School;	2,266\n
7;	AD;	New La Tour Koenig Government School;	2,652\n
8;	AE;	La Tour Koenig Government School;	3,929\n
9;	AF;	Grand River North West Government School;	3,522\n
10;	AG;	Residence Vallijee Government School;	2,415\n
11;	AH;	Dr. James Burty David State Secondary School;	2,862\n
12;	AJ;	Renganaden Seeneevassen Government School;	4,344\n
13;	AK;	Medco Cassis Secondary School;	964\n
14;	AL;	Dr. Edgar Millien Government School;	1,060\n
  """


for i in data.splitlines():
	c = i.split(';')
	try:
		#print c[1].strip()
		no = c[0]
		reg = c[1].strip()
		station = c[2].strip()
		electors = c[3].strip()
		print "<tr><td>"+no+"</td><td>"+reg+"</td><td>"+station+"</td><td>"+electors+"</td></tr>"
	except:
		pass