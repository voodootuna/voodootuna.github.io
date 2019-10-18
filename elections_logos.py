# -*- coding: utf-8 -*-

import json
import os
import io

path = './logoparty'
folder = os.fsencode(path)
logo_data = {}
for filename in os.listdir(folder):
	if filename.endswith(b".svg"):
		#print(os.path.join(folder, filename))
		filepath = os.path.join(folder, filename)
		with io.open(filepath, 'r', newline=None) as f:
			new_data = ''
			for line in f:
			   new_data += line.replace("\n", "")
			logo_data[filename.decode('utf-8').replace('.svg','')] = new_data;


#print(logo_data)


with open("./logos.json", "w") as f:
	#print(save_data)
	json.dump(logo_data, f)