'''
	Created by DangerBlack on 23/01/2015.
	
	Usage:
	python collect_chapter.py
	it must be in the same folder of personaggi.txt,  and there must be a folder named as res,
	where it put the results.
	This program generate the file named elenco_finale.txt,elenco_finale.csv that contains the value aggregated,
	it must be launched after ricerca.py
	
	
	This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
book_file_name="volume1.txt"
player_file_name="personaggi.txt"
out_put_name="elenco_finale";
#Thist const define how many times in the book a specific character had to appear in order not to be filtered by the system
const=135;


def load_names(personaggi_file):
	in_file = open(personaggi_file,"r")
	lista=in_file.read()
	in_file.close()
	pg_name=[]
	for nome in lista.split('\n'):
		pg_name.append(nome.split(',')[0])
	return pg_name
	
def load_numbersOfpg(personaggi_file):
	in_file = open(personaggi_file,"r")
	cont =0
	lista=in_file.readlines()
	for line in lista:
		if(len(line)>0):
			cont=cont+1;
	in_file.close()
	return cont
	
def load_chapter_pg(pg_name,pg_index):
	in_file = open("res/working/chapter"+str(pg_index)+".txt","r")
	lines = in_file.readlines()
	lista =[]
	for q in range(0,len(lines)-1): #Rimuovo l'ultimo capitolo poiche e un capitolo virtuale costruito a tavolino, inutile
		lista.append([pg_name,q,lines[q][:-1]]);
	in_file.close()
	return lista

def sum_chapter_pg(pg_name,pg_index):
	in_file = open("res/working/chapter"+str(pg_index)+".txt","r")
	lines = in_file.readlines()
	lista =[]
	count = 0;
	for q in range(0,len(lines)-1): #Rimuovo l'ultimo capitolo poiche e un capitolo virtuale costruito a tavolino, inutile
		count=count+(int(lines[q][:-1]))
	lista.append([pg_name,count]);
	in_file.close()
	return lista
	
def save_presenziere(presenziere):
	out_file = open("res/finale/"+out_put_name+".csv","w")
	for pres in presenziere:
		out_file.write(pres[0]+","+str(pres[1])+","+str(pres[2])+"\n")
	out_file.close()
	out_file = open("res/finale/"+out_put_name+"_tab.txt","w")
	for pres in presenziere:
		out_file.write(pres[0]+"	"+str(pres[1])+"	"+str(pres[2])+"\n")
	out_file.close()

def save_curve(presenziere):
	out_file = open("res/finale/"+out_put_name+"_courve_tab.txt","w")
	count=0;
	for pres in presenziere:
		out_file.write(str(pres[0])+"	"+str(pres[1])+"\n")
	out_file.close()

def load_chapter_pg_n(pg_name,pg_index,start,end):
	in_file = open("res/working/chapter"+str(pg_index)+".txt","r")
	lines = in_file.readlines()
	lista =[]
	for q in range(start,end): #Rimuovo l'ultimo capitolo poiche e un capitolo virtuale costruito a tavolino, inutile
		lista.append([pg_name,q,lines[q][:-1]]);
	in_file.close()
	return lista
	
personaggi=load_numbersOfpg(player_file_name)

pg_names=load_names(player_file_name)

lista_totale=[]
lista_parziale=[];
lista_curva=[]
lista_num_curva=[];
lista_tripla=[[],[],[]];


for x in range(0,personaggi):
	importanza=sum_chapter_pg(pg_names[x],x);
	lista_curva.extend(importanza)
	if(importanza[0][1]>const):
		lista_parziale.extend(load_chapter_pg(pg_names[x],x))
	lista_totale.extend(load_chapter_pg(pg_names[x],x))

for x in range(0,personaggi):
	importanza=load_chapter_pg_n(pg_names[x],x,0,25)
	lista_tripla[0].extend(importanza)
	importanza=load_chapter_pg_n(pg_names[x],x,26,50)
	lista_tripla[1].extend(importanza)		
	importanza=load_chapter_pg_n(pg_names[x],x,51,72)
	lista_tripla[2].extend(importanza)
	
lista_curva=sorted(lista_curva, key=lambda student: student[1],reverse=True)

for x in range(0,personaggi):
	print(lista_curva[x][1]);
	lista_num_curva.append([str(x),lista_curva[x][1]]);
#print lista_totale
save_presenziere(lista_totale)
save_curve(lista_curva)
temp_name=out_put_name
out_put_name=temp_name+'filtered'
save_presenziere(lista_parziale)
out_put_name=temp_name+'_special'
save_curve(lista_num_curva)
out_put_name=temp_name+'_0'
save_presenziere(lista_tripla[0])
out_put_name=temp_name+'_1'
save_presenziere(lista_tripla[1])
out_put_name=temp_name+'_2'
save_presenziere(lista_tripla[2])

print "Saved in "+out_put_name
