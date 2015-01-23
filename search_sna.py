'''
	Created by DangerBlack on 23/01/2015.
	
	Usage:
	python search_sna.py
	it must be in the same folder of personaggi.txt, volume1.txt,  and there must be a folder named as res,
	where it put the results.
	In the res folder there must be a folder name working with the file capitoli.txt inside.
	
	You need to install pp http://www.parallelpython.com/
	
	
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

import pp

book_file_name="volume1.txt"
player_file_name="personaggi.txt"

job_server = pp.Server();


def load_book(book_file):
	in_file = open(book_file,"r")
	book=in_file.read()
	in_file.close()
	return book
	
def load_names(pid,personaggi_file):
	in_file = open(personaggi_file,"r")
	lista=in_file.read()
	in_file.close()
	return lista.split('\n')[pid].split(',')	

def load_numbersOfpg(personaggi_file):
	in_file = open(personaggi_file,"r")
	cont =0
	lista=in_file.readlines()
	for line in lista:
		if(len(line)>0):
			cont=cont+1;
	in_file.close()
	return cont
	
def load_chapters():
	chapter_file_name="capitoli.txt"
	in_file = open("res/working/"+chapter_file_name,"r")
	lines = in_file.readlines()
	lista =[]
	for line in lines:
		lista.append(line[:-1].split(','));
	in_file.close()
	return lista

def load_presenziere(pid):
	in_file = open("res/working/out"+str(pid)+".txt","r")
	lines = in_file.readlines()
	lista =[]
	for line in lines:
		lista.append(line[:-1].split(','));
	in_file.close()
	return lista
		
def search_names(pid,book_file,names):
	book=load_book(book_file)
	chapters=load_chapters()
	presenziere=[];
	capitolo_pg=[]
	for q in range(0,len(chapters)+2):
		capitolo_pg.append(0)
	#print "LA LUNGHEZZA e "+str(len(chapters))
	for name in names:
		index=0
		got_index=getNext(book,name,index)
		while((got_index)!=-1):
                        p=checkhere(presenziere,got_index,name)
                        if p==0 :
							appoggio=find_the_chapter(pid,chapters,got_index)
							#print str(pid)+": decisa la cella "+str(appoggio)
							capitolo_pg[appoggio]=capitolo_pg[appoggio]+1
							presenziere.append([name,got_index,appoggio])
			index=got_index+1
			got_index=getNext(book,name,index)
	save_presenziere(pid,presenziere)
	save_chapter_by_name(pid,capitolo_pg)

def find_the_chapter(pid,chapters,index):
	count = 0
	for q in range(0,len(chapters)):
		#print c
		if int(index) <= int(chapters[q][1]):
			#if(pid==30):
				#print str(index)+"<"+chapters[q][1]+" ["+chapters[q][0]+"] il valore di count "+str(q)
			return q-1
	return len(chapters)+1
def getNext(book,name,index):
       try:
               return book.index(name,index)
       except:
               return -1
def checkhere(presenziere,got_index,name):
        for occorrenza in presenziere:
                if(occorrenza[1]>got_index)and(occorrenza[1]+len(occorrenza[0])<got_index):
                        return 1
        return 0        
	
def save_presenziere(pid,presenziere):
	out_file = open("res/working/out"+str(pid)+".txt","w")
	for pres in presenziere:
		out_file.write(pres[0]+","+str(pres[1])+","+str(pres[2])+"\n")
	out_file.close()
	
def save_chapter_by_name(pid,capitolo_pg):
	out_file = open("res/working/chapter"+str(pid)+".txt","w")
	for p in capitolo_pg:
		out_file.write(str(p)+"\n")
	out_file.close()
	
def search_by_pid(pid,book_file_name,player_file_name):
	#pid=job_server.get_stats();
	#pid=0;
	print str(pid)+": run"
	personaggi_file=player_file_name
	names=load_names(pid,personaggi_file)
	book_file=book_file_name
	search_names(pid,book_file,names)

proc =[]
personaggi=load_numbersOfpg(player_file_name)

for x in range(0,personaggi):
        proc.append(job_server.submit(search_by_pid,(x,book_file_name,player_file_name),(save_presenziere,getNext,search_names,load_names,load_book,checkhere,load_chapters,find_the_chapter,save_chapter_by_name,)))


for x in range(0,personaggi):
        pid=x;
        print str(pid)+": stop"
        q=proc[x]()



print "finito"

#search_by_pid();
        
