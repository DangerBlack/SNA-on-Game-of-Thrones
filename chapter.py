'''
	Created by DangerBlack on 23/01/2015.
	
	Usage:
	python chapter.py
	it must be in the same folder of volume1.txt,  and there must be a folder named as res,
	where it put the results.
	This program generate the file named capitoli.txt that contains the chapter of the book.
	
	
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

import re

book_file_name="volume1.txt";
out_put_name="capitoli.txt";


def load_book(book_file):
	in_file = open(book_file,"r")
	book=in_file.read()
	in_file.close()
	return book

def save_presenziere(presenziere):
	out_file = open("res/working/"+out_put_name,"w")
	for pres in presenziere:
		out_file.write(pres[0]+","+str(pres[1])+"\n")
	out_file.close()
			   
def search_chapter(book_file):
	book=load_book(book_file)
	REGEXP="\n[A-Z][A-Z][A-Z][A-Z]*"
	titoli=re.findall(REGEXP,book)
	presenziere=[]
	index=0;
	for titolo in titoli:
		index=book.index(titolo,index)
		presenziere.append([titolo[1:],index])
	print presenziere
	print "\n\n"
	presenziere=sorted(presenziere, key=lambda student: student[1])
	print presenziere 
	save_presenziere(presenziere)

search_chapter(book_file_name)
