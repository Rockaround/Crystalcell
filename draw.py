#This programs draws a crystallographic cell in vectorial format
#The external software "epstool" is needed to resize the eps
#Requires vplot.py  (for the eps files)
#         geom3.py  (for the objects (atoms, lines, texts)

#Informations about the different available options in readme.txt

#To do List
#1. Change colors to a dictionary. It will make changing the color of the links and of the atoms easier
#2. Change the operations to do to a dictionary of function. This should make the main part of the code easier to read, and avoid the neverending if conditions.
#2bis. Create several dictionaries: Struct={"BCC":BCC(), ...}, Mod=...
#3. Allow for uncommun structures to be read if needed. Primary cell that should be repeted.
#4. Functions to change all the atoms of one size/color to another size/color
#5. Allow for non predefined sizes
#6. Add a type to atoms to permit easier changes
#7. Add other easter eggs
#8. Can I get rid of epstool?
#9. Graphical interface
#10. Add arrows and surfaces objects
#11. Is deleting an item that might not exist before adding one to avoid duplicates really the best solution?
#12. change x,z,y to x,y,z
#13. Fix the text position in a smart way

#Structure of the code
#The code reads the input file in a sequential way. Several conflicting operations on the same object will lead to the last operation being used.
#The first word of each line is a key word that is starting an action. The key words are recognized thanks to a gazillion if conditions
#Everything pertaining to drawing (perspective, shadows of shadows one day, etc...) Is done at the end, once the input file is read.


#Proposition for a new structure of the input file (and reading part of the code)
#All of the structures should have the new form STRUCT BCC/FCC/HCP/CUBIC/SURFX/.../CUSTOM  X Y Z
#The function should then ressemble: if STRUCT: Struct{BCC}(X,Y,Z)  with all of the functions defined elsewhere
#All of the texts should have the new form TEXT w/wd/wu/... ...
#All of the new atoms/links/etc should have the new form ELEMENT +a/+as/... ...
#All of the operations on color, size and thickness should have the new form APPEARANCE ... ...
#All of the easter eggs should have the new form OTHER ... ...



import sys, re, getopt, vplot, math, random, os
from geom3 import sphere, line, texte

graph=vplot.eps_class(fname='Oct3.eps',bbx=500,bby=500)
graph.linewidth(1)

#Treat arguments
for arg in sys.argv:
   fichier=arg
booleen2=0
if fichier=="draw.py":
    booleen2=0
else:
    fichier+=".eps"
    booleen2=1
   

#Read the file
struct = open("test.txt","r")
contenu = struct.read()
print(contenu)
struct.close()
tab=contenu.split()

#Initialisation of the lists
atoms=[]
links=[]
writing=[]
nb=0

#Functions
def deleteatom(aa,bb,cc):
    for ai in atoms:
	if ai.count([aa,bb,cc])>0:
	   del atoms[atoms.index(ai)]

def sizeatom(aa,bb,cc):
    booleen=0
    for ai in atoms:
	if ai.count([aa,bb,cc])>0:
	   size=ai[1]
	   booleen=1
    if booleen==1:
	return size
    else:
	return "n"   

def coloratom(ai,vacancy):
	if atoms[ai][2]=="white":
        	atoms2[ai-vacancy].col=[1.,1.,1.]
	if atoms[ai][2]=="grey":
        	atoms2[ai-vacancy].col=[0.6,0.6,0.6]
	if atoms[ai][2]=="black":
        	atoms2[ai-vacancy].col=[0.,0.,0.]
	if atoms[ai][2]=="red":
        	atoms2[ai-vacancy].col=[1.,0.,0.]
	if atoms[ai][2]=="green":
        	atoms2[ai-vacancy].col=[0.,1.,0.]
	if atoms[ai][2]=="blue":
        	atoms2[ai-vacancy].col=[0.,0.,1.]
	if atoms[ai][2]=="yellow":
        	atoms2[ai-vacancy].col=[1.,1.,0.]
	if atoms[ai][2]=="orange":
        	atoms2[ai-vacancy].col=[1.,0.55,0.]
	if atoms[ai][2]=="brown":
        	atoms2[ai-vacancy].col=[0.55,0.27,0.07]
	if atoms[ai][2]=="bluesv":
        	atoms2[ai-vacancy].col=[0.,0.415,0.655]
	if atoms[ai][2]=="yellowsv":
        	atoms2[ai-vacancy].col=[0.99,0.8,0.0]

def deletelink(a,b,c,d,e,f):
    for li in links:
            if li.count([a,b,c])>0 and li.count([d,e,f])>0:
                del links[links.index(li)]

def thicknesslink(a,b,c,d,e,f):
    booleen3=0
    for li in links:
	if li.count([a,b,c])>0 and li.count([d,e,f])>0:
	   thick=li[2]
	   booleen3=1
    if booleen3==1:
	return thick
    else:
	return "n"

def colorlink(ai):
	if links[ai][3]=="white":
        	links2[ai].col=[1.,1.,1.]
	if links[ai][3]=="grey":
        	links2[ai].col=[0.6,0.6,0.6]
	if links[ai][3]=="black":
        	links2[ai].col=[0.,0.,0.]
	if links[ai][3]=="red":
        	links2[ai].col=[1.,0.,0.]
	if links[ai][3]=="green":
        	links2[ai].col=[0.,1.,0.]
	if links[ai][3]=="blue":
        	links2[ai].col=[0.,0.,1.]
	if links[ai][3]=="yellow":
        	links2[ai].col=[1.,1.,0.]
	if links[ai][3]=="orange":
        	links2[ai].col=[1.,0.55,0.]
	if links[ai][3]=="brown":
        	links2[ai].col=[0.55,0.27,0.07]

#starting special operations
while len(tab)>0:
    ope=tab[0]
    aa=float(tab[1])
    bb=float(tab[2])
    cc=float(tab[3])
    del tab[0]
    del tab[0]
    del tab[0]
    del tab[0]

    #Create base structure, atoms and links
    if ope=="BCC":
        for i in range(int(aa)+1):
         for j in range(int(bb)+1):
          for k in range(int(cc)+1):
             deleteatom(aa,bb,cc)
             atoms.append([[1.0*i,1.0*j,1.0*k],"n","white"])
             if i < aa:
               deletelink(i,j,k,i+1,j,k) 
               links.append([[1.0*i,1.0*j,1.0*k],[1.0+i,1.0*j,1.0*k],"n","black"])      
             if j < bb:
               deletelink(i,j,k,i,j+1,k)
               links.append([[1.0*i,1.0*j,1.0*k],[1.0*i,1.0+j,1.0*k],"n","black"])
             if k < cc:
                 deletelink(i,j,k,i,j,k+1)
                 links.append([[1.0*i,1.0*j,1.0*k],[1.0*i,1.0*j,1.0+k],"n","black"])
             nb+=1
             if i<aa and j<bb and k<cc:
                 deleteatom(aa,bb,cc)
                 atoms.append([[i+0.5,j+0.5,k+0.5],"n","white"])
                 nb+=1
    if ope=="FCC":
        for i in range(int(aa)+1):
         for j in range(int(bb)+1):
          for k in range(int(cc)+1):
             deleteatom(aa,bb,cc)
             atoms.append([[1.0*i,1.0*j,1.0*k],"n","white"])
             if i < aa:
                 deletelink(i,j,k,i+1,j,k)
                 links.append([[1.0*i,1.0*j,1.0*k],[1.0+i,1.0*j,1.0*k],"n","black"])      
             if j < bb:
                 deletelink(i,j,k,i,j+1,k)
                 links.append([[1.0*i,1.0*j,1.0*k],[1.0*i,1.0+j,1.0*k],"n","black"])
             if k < cc:
                 deletelink(i,j,k,i,j,k+1)
                 links.append([[1.0*i,1.0*j,1.0*k],[1.0*i,1.0*j,1.0+k],"n","black"])
             nb+=1
             if i<aa and j<bb:
                 deleteatom(aa,bb,cc)
                 atoms.append([[i+0.5,j+0.5,k],"n","white"])
                 nb+=1
             if i<aa and k<cc:
                 deleteatom(aa,bb,cc)
                 atoms.append([[i+0.5,j,k+0.5],"n","white"])
                 nb+=1
             if k<cc and j<bb:
                 deleteatom(aa,bb,cc)
                 atoms.append([[i,j+0.5,k+0.5],"n","white"])
                 nb+=1
    if ope=="ROCKSALT":
        for i in range(int(aa)+1):
         for j in range(int(bb)+1):
          for k in range(int(cc)+1):
             deleteatom(i,j,k)
             atoms.append([[1.0*i,1.0*j,1.0*k],"n","white"])
             if i < aa:
                 deletelink(i,j,k,i+1,j,k)
                 links.append([[1.0*i,1.0*j,1.0*k],[1.0+i,1.0*j,1.0*k],"n","black"])      
             if j < bb:
                 deletelink(i,j,k,i,j+1,k)
                 links.append([[1.0*i,1.0*j,1.0*k],[1.0*i,1.0+j,1.0*k],"n","black"])
             if k < cc:
                 deletelink(i,j,k,i,j,k+1)
                 links.append([[1.0*i,1.0*j,1.0*k],[1.0*i,1.0*j,1.0+k],"n","black"])
             nb+=1
             if i<aa and j<bb:
                 deleteatom(i+0.5,j+0.5,k)
                 atoms.append([[i+0.5,j+0.5,k],"n","white"])
                 nb+=1
             if i<aa and k<cc:
                 deleteatom(i+0.5,j,k+0.5)
                 atoms.append([[i+0.5,j,k+0.5],"n","white"])
                 nb+=1
             if k<cc and j<bb:
                 deleteatom(i,j+0.5,k+0.5)
                 atoms.append([[i,j+0.5,k+0.5],"n","white"])
                 nb+=1
             if i<aa:
                 deleteatom(i+0.5,j,k)
                 atoms.append([[i+0.5,j,k],"ss","black"])
             if j<bb:
                 deleteatom(i,j+0.5,k)
                 atoms.append([[i,j+0.5,k],"ss","black"])
             if k<cc:
                 deleteatom(i,j,k+0.5)
                 atoms.append([[i,j,k+0.5],"ss","black"])
             if i<aa and j<<bb and k<cc:
                 deleteatom(i+0.5,j+0.5,k+0.5)
                 atoms.append([i+0.5,j+0.5,k+0.5],"ss","black"])
    if ope=="CUBIC":
        for i in range(int(aa)+1):
         for j in range(int(bb)+1):
          for k in range(int(cc)+1):
             deleteatom(aa,bb,cc)
             atoms.append([[1.0*i,1.0*j,1.0*k],"n","white"])
             if i < aa:
                 deletelink(i,j,k,i+1,j,k)
                 links.append([[1.0*i,1.0*j,1.0*k],[1.0+i,1.0*j,1.0*k],"n","black"])      
             if j < bb:
                 deletelink(i,j,k,i,j+1,k)
                 links.append([[1.0*i,1.0*j,1.0*k],[1.0*i,1.0+j,1.0*k],"n","black"])
             if k < cc:
                 deletelink(i,j,k,i,j,k+1)
                 links.append([[1.0*i,1.0*j,1.0*k],[1.0*i,1.0*j,1.0+k],"n","black"])
             nb+=1
    if ope=="PLANY":
        aa2=cc
        bb2=float(tab[0])
        cc2=float(tab[1])
        del tab[0]
        del tab[0]
        for i in range(int(aa)+1):
            for j in range(int(bb)+1):
                deleteatom(aa2+i,bb2+j,cc2)
                atoms.append([[aa2+i,bb2+j,cc2],"n","white"])
                if i < aa:
                    deletelink(i+aa2,j+bb2,cc2,i+1+aa2,j+bb2,cc2)
                    links.append([[1.0*i+aa2,1.0*j+bb2,1.0*cc2],[1.0+i+aa2,1.0*j+bb2,1.0*cc2],"n","black"])      
                if j < bb:
                    deletelink(i+aa2,j+bb2,cc2,i+aa2,1+j+bb2,cc2)
                    links.append([[1.0*i+aa2,1.0*j+bb2,1.0*cc2],[1.0*i+aa2,1.0+j+bb2,1.0*cc2],"n","black"])
    if ope=="PLANZ":
        aa2=cc
        bb2=float(tab[0])
        cc2=float(tab[1])
        del tab[0]
        del tab[0]
        for i in range(int(aa)+1):
            for k in range(int(bb)+1):
                deleteatom(aa2+i,bb2,cc2+k)
                atoms.append([[aa2+i,bb2,cc2+k],"n","white"])
                if i < aa:
                    deletelink(i+aa2,bb2,k+cc2,i+1+aa2,bb2,k+cc2)
                    links.append([[1.0*i+aa2,1.0*bb2,1.0*k+cc2],[1.0+i+aa2,1.0*bb2,1.0*k+cc2],"n","black"])      
                if k < bb:
                    deletelink(i+aa2,bb2,k+cc2,i+aa2,bb2,k+1+cc2)
                    links.append([[1.0*i+aa2,1.0*bb2,1.0*k+cc2],[1.0*i+aa2,1.0*bb2,1.0+k+cc2],"n","black"])
    if ope=="PLANX":
        aa2=cc
        bb2=float(tab[0])
        cc2=float(tab[1])
        del tab[0]
        del tab[0]
        for j in range(int(aa)+1):
            for k in range(int(bb)+1):
                deleteatom(aa2,bb2+j,cc2+k)
                atoms.append([[aa2,bb2+j,cc2+k],"n","white"])
                if k < aa:
                    deletelink(aa2,j+bb2,k+cc2,aa2,j+bb2,k+1+cc2)
                    links.append([[1.0*aa2,1.0*j+bb2,1.0*k+cc2],[1.0*aa2,1.0*j+bb2,1.0+k+cc2],"n","black"])      
                if j < bb:
                    deletelink(aa2,j+bb2,k+cc2,aa2,1+j+bb2,k+cc2)
                    links.append([[1.0*aa2,1.0*j+bb2,1.0*k+cc2],[1.0*aa2,1.0+j+bb2,1.0*k+cc2],"n","black"])
    if ope=="FIA110":  
        sizeatom=tab[0]
        coloratom2=tab[1]
        sizelink=tab[2]
        colorlink2=tab[3]
        del tab[0]
        del tab[0]
        del tab[0]
        del tab[0]
        deleteatom(aa,bb,cc)
        atoms.append([[aa-0.1,bb,cc-0.1],sizeatom,coloratom2])
        atoms.append([[aa+0.1,bb,cc+0.1],sizeatom,coloratom2])
        links.append([[aa-0.5,bb-0.5,cc-0.5],[aa-0.1,bb,cc-0.1],sizelink,colorlink2])      
        links.append([[aa-0.5,bb+0.5,cc-0.5],[aa-0.1,bb,cc-0.1],sizelink,colorlink2])      
        links.append([[aa+0.5,bb-0.5,cc+0.5],[aa+0.1,bb,cc+0.1],sizelink,colorlink2])      
        links.append([[aa+0.5,bb+0.5,cc+0.5],[aa+0.1,bb,cc+0.1],sizelink,colorlink2])      
        links.append([[aa-0.1,bb,cc-0.1],[aa+0.1,bb,cc+0.1],sizelink,colorlink2])      
    if ope=="FIA111":  
        sizeatom=tab[0]
        coloratom2=tab[1]
        sizelink=tab[2]
        colorlink2=tab[3]
        del tab[0]
        del tab[0]
        del tab[0]
        del tab[0]
        deleteatom(aa,bb,cc)
        atoms.append([[aa-0.1,bb-0.1,cc-0.1],sizeatom,coloratom2])
        atoms.append([[aa+0.1,bb+0.1,cc+0.1],sizeatom,coloratom2])
        links.append([[aa-0.5,bb-0.5,cc-0.5],[aa-0.1,bb-0.1,cc-0.1],sizelink,colorlink2])      
        links.append([[aa+0.5,bb+0.5,cc+0.5],[aa+0.1,bb+0.1,cc+0.1],sizelink,colorlink2])      
        links.append([[aa-0.1,bb-0.1,cc-0.1],[aa+0.1,bb+0.1,cc+0.1],sizelink,colorlink2])      
    if ope=="FIA100":
        sizeatom=tab[0]
        coloratom2=tab[1]
        sizelink=tab[2]
        colorlink2=tab[3]
        del tab[0]
        del tab[0]
        del tab[0]
        del tab[0]
        deleteatom(aa,bb,cc)
        atoms.append([[aa-0.1,bb,cc],sizeatom,coloratom2])
        atoms.append([[aa+0.1,bb,cc],sizeatom,coloratom2])
        links.append([[aa-0.5,bb-0.5,cc-0.5],[aa-0.1,bb,cc],sizelink,colorlink2])      
        links.append([[aa-0.5,bb+0.5,cc-0.5],[aa-0.1,bb,cc],sizelink,colorlink2])      
        links.append([[aa+0.5,bb-0.5,cc+0.5],[aa+0.1,bb,cc],sizelink,colorlink2])      
        links.append([[aa+0.5,bb+0.5,cc+0.5],[aa+0.1,bb,cc],sizelink,colorlink2])      
        links.append([[aa-0.5,bb-0.5,cc+0.5],[aa-0.1,bb,cc],sizelink,colorlink2])      
        links.append([[aa-0.5,bb+0.5,cc+0.5],[aa-0.1,bb,cc],sizelink,colorlink2])      
        links.append([[aa+0.5,bb-0.5,cc-0.5],[aa+0.1,bb,cc],sizelink,colorlink2])      
        links.append([[aa+0.5,bb+0.5,cc-0.5],[aa+0.1,bb,cc],sizelink,colorlink2])      
        links.append([[aa-0.1,bb,cc],[aa+0.1,bb,cc],sizelink,colorlink2])      
    if ope=="HCP":  #notfinished
        for i in range(int(aa)+1):
         for j in range(int(bb)+1):
          for k in range(int(cc)+1):
             deleteatom(aa,bb,cc)
             atoms.append([[1.0*i,1.0*j,1.6*k],"n","white"])
             if i < aa:
               deletelink(i,j,1.6*k,i+1,j,1.6*k) 
               links.append([[1.0*i,1.0*j,1.6*k],[1.0+i,1.0*j,1.6*k],"n","black"])      
             if j < bb:
               deletelink(i,j,1.6*k,i,j+1,1.6*k)
               links.append([[1.0*i,1.0*j,1.6*k],[1.0*i,1.0+j,1.6*k],"n","black"])
             if k < cc:
                 deletelink(i,j,1.6*k,i,j,1.6*(k+1))
                 links.append([[1.0*i,1.0*j,1.6*k],[1.0*i,1.0*j,1.6*(1+k)],"n","black"])
             nb+=1
             if i<aa and j<bb and k<cc:
                 deleteatom(aa,bb,cc)
                 atoms.append([[i+0.5,j+0.5,k+0.5],"n","white"])
                 nb+=1
    if ope=="NOEL":
        links.append([[0.5,0.,0.],[1.,0.,0.],"b","brown"])
        links.append([[0.5,0.,0.],[0.5,0.5,0.],"b","brown"])
        links.append([[1.,0.,0.],[1.,0.5,0.],"b","brown"])
        links.append([[0.5,0.5,0.],[1.,0.5,0.],"b","brown"])
        for i in range(int(aa)): 
            count=0
            links.append([[0+i*0.75/aa,i*1.0/2+0.5,0.],[0.75-0.25*(aa-i)/aa,i*1.0/2+0.5,0.],"n","green"])
            links.append([[0.75+0.25*(aa-i)/aa,i*1.0/2+0.5,0.],[1.5-i*0.75/aa,i*1.0/2+0.5,0.],"n","green"])
            links.append([[0+i*0.75/aa,i*1.0/2+0.5,0.],[0.75-0.25*(aa-(i+1))/aa,(i+1)*1.0/2+0.5,0.],"n","green"])
            links.append([[0.75+0.25*(aa-(i+1))/aa,(i+1)*1.0/2+0.5,0.],[1.5-i*0.75/aa,i*1.0/2+0.5,0.],"n","green"])
            if bb==1:
                   atoms.append([[0+i*0.75/aa+(1.5-i*0.75/aa-0-i*0.75/aa)/2,i*1.0/2+0.87,0.],"s","red"])
            if bb==2:
                   atoms.append([[0+i*0.75/aa+(1.5-i*0.75/aa-0-i*0.75/aa)*(1./3+i*1./aa/7),i*1.0/2+0.67,0.],"s","red"])
                   atoms.append([[0+i*0.75/aa+(1.5-i*0.75/aa-0-i*0.75/aa)*(2./3-i*1./aa/7),i*1.0/2+0.82,0.],"s","red"])
            if bb==3:
                   atoms.append([[0+i*0.75/aa+(1.5-i*0.75/aa-0-i*0.75/aa)*(1./4+i*1./aa/5),i*1.0/2+0.67,0.],"s","red"])
                   atoms.append([[0+i*0.75/aa+(1.5-i*0.75/aa-0-i*0.75/aa)*(2./3-i*1./aa/7),i*1.0/2+0.77,0.],"s","red"])
                   atoms.append([[0+i*0.75/aa+(1.5-i*0.75/aa-0-i*0.75/aa)*(3./7-i*1./aa/15),i*1.0/2+0.90,0.],"s","red"])
     #       while count<bb:
      #            nb1=random.random()
       #           nb2=random.random()
        #          atoms.append([[0+(i+0.2)*0.75/aa+nb1*(1.5-2*i*0.9*0.75/aa),0.5+i*1.0/2+nb2*0.5,0.],"s","red"])
         #         count+=1
            if cc>0:
                 links.append([[0+i*0.75/aa,i*1.0/2+0.5,0.],[0.75+0.25*(aa-(i+1))/aa+(1.5-i*0.75/aa-(0.75+0.25*(aa-(i+1))/aa))/2,(i+1)*1.0/2+0.25,0.],"b","yellow"])
            if cc>1:
                 links.append([[1.5-i*0.75/aa,(i)*1.0/2+0.5,0.],[0.75-0.25*(aa-(i+1))/aa+(0+i*0.75/aa-(0.75-0.25*(aa-(i+1))/aa))/2,(i+1)*1.0/2+0.25,0.],"b","yellow"])
    if ope=="+an":   #add a normal atom
        deleteatom(aa,bb,cc)
        atoms.append([[aa,bb,cc],"n","white"])
    if ope=="+as":   #add a small atom
        deleteatom(aa,bb,cc)
        atoms.append([[aa,bb,cc],"s","black"])
    if ope=="+ab":   #add a big atom
        deleteatom(aa,bb,cc)
        atoms.append([[aa,bb,cc],"b","grey"])
    if ope=="+av":   #add a vacancy
        deleteatom(aa,bb,cc)
        atoms.append([[aa,bb,cc],"v","white"])
    if ope=="-a":    #delete atom keeping links
        deleteatom(aa,bb,cc)
    if ope=="-al":   #delete atom and links
        deleteatom(aa,bb,cc)
        ind=[]
        for li in links:
            if li.count([aa,bb,cc])>0:
                ind.append(links.index(li))
        for i in range(len(ind)):
            del links[ind.pop()]
    if ope=="-l":    #delete a link
        aa2=float(tab[0])
        bb2=float(tab[1])
        cc2=float(tab[2])
        del tab[0]
        del tab[0]
        del tab[0]
        deletelink(aa,bb,cc,aa2,bb2,cc2)
    if ope=="+ln":    #add a normal link
        aa2=float(tab[0])
        bb2=float(tab[1])
        cc2=float(tab[2])
        del tab[0]
        del tab[0]
        del tab[0]
        deletelink(aa,bb,cc,aa2,bb2,cc2)
        links.append([[aa,bb,cc],[aa2,bb2,cc2],"n","black"])
    if ope=="+lt":    #add a thin link
        aa2=float(tab[0])
        bb2=float(tab[1])
        cc2=float(tab[2])
        del tab[0]
        del tab[0]
        del tab[0]
        deletelink(aa,bb,cc,aa2,bb2,cc2)
        links.append([[aa,bb,cc],[aa2,bb2,cc2],"t","black"])
    if ope=="+lb":    #add a bold link
        aa2=float(tab[0])
        bb2=float(tab[1])
        cc2=float(tab[2])
        del tab[0]
        del tab[0]
        del tab[0]
        deletelink(aa,bb,cc,aa2,bb2,cc2)
        links.append([[aa,bb,cc],[aa2,bb2,cc2],"b","black"])
    if ope=="cola":
        col=tab[0]
	del tab[0]
        print(aa,bb,cc)
	size=sizeatom(aa,bb,cc)
	deleteatom(aa,bb,cc)
        atoms.append([[aa,bb,cc],size,col])
#    if ope=="colas":  #color atom size
#        sizetochange=tab[0]
#        del tab[0]
#        newcol=tab[0]
#        del tab[0]
#        for ai in range(len(atoms)):
#           
#    if ope=="colac":  #color aton color
    if ope=="coll":
        aa2=float(tab[0])
        bb2=float(tab[1])
        cc2=float(tab[2])
	col=tab[3]
        del tab[0]
        del tab[0]
        del tab[0]
	del tab[0]
	thick=thicknesslink(aa,bb,cc,aa2,bb2,cc2)
	print(thick)
	deletelink(aa,bb,cc,aa2,bb2,cc2)
        links.append([[aa,bb,cc],[aa2,bb2,cc2],thick,col])
    if ope=="w":
	size=float(tab[0])	
	t=tab[1]
	del tab[0]
	del tab[0]
	writing.append([[aa,bb,cc],t,size])
    if ope=="wd":
	bb-=0.13
	size=float(tab[0])	
	t=tab[1]
        size2=float(len(t)+1)*(size+0.009)
        aa-=size2/2
        bb-=math.sin(10*math.pi/180)*math.sin(15*math.pi/180)*size2
	del tab[0]
	del tab[0]
	writing.append([[aa,bb,cc],t,size])
    if ope=="wu":
	bb+=0.11
	size=float(tab[0])	
	t=tab[1]
        size2=float(len(t)+1)*(size+0.009)
        aa-=size2/2
        bb-=math.sin(10*math.pi/180)*math.sin(15*math.pi/180)*size2
	del tab[0]
	del tab[0]
	writing.append([[aa,bb,cc],t,size])
    if ope=="wl":
	size=float(tab[0])	
	t=tab[1]
        size2=float(len(t)+1)*(size+0.009)+0.07
        aa-=size2
        bb-=math.sin(10*math.pi/180)*math.sin(15*math.pi/180)*size2
	del tab[0]
	del tab[0]
	writing.append([[aa,bb,cc],t,size])
    if ope=="wr":
	size=float(tab[0])	
	t=tab[1]
        aa+=0.13
	del tab[0]
	del tab[0]
	writing.append([[aa,bb,cc],t,size])
    if ope=="wur":
	bb+=0.08	
	size=float(tab[0])	
	t=tab[1]
        aa+=0.08
	del tab[0]
	del tab[0]
	writing.append([[aa,bb,cc],t,size])
    if ope=="wul":
	bb+=0.08	
	size=float(tab[0])	
	t=tab[1]
        size2=float(len(t)+1)*(size+0.009)
        aa-=size2
        bb-=math.sin(10*math.pi/180)*math.sin(15*math.pi/180)*size2
	del tab[0]
	del tab[0]
	writing.append([[aa,bb,cc],t,size])
    if ope=="wdl":
	bb-=0.12	
	size=float(tab[0])	
	t=tab[1]
        size2=float(len(t)+1)*(size+0.009)
        aa-=size2
        bb-=math.sin(10*math.pi/180)*math.sin(15*math.pi/180)*size2
	del tab[0]
	del tab[0]
	writing.append([[aa,bb,cc],t,size])
    if ope=="wdr":
	bb-=0.08	
	size=float(tab[0])	
	t=tab[1]
        aa+=0.07
	del tab[0]
	del tab[0]
	writing.append([[aa,bb,cc],t,size])

#print(atoms)
#print(links)

#getting the scale factor
for ai in range(len(atoms)):
     x=atoms[ai][0][0]+math.sin(15.0/180*3.1415926)*atoms[ai][0][2] 
     y=atoms[ai][0][1]+math.cos(15.0/180*3.1415926)*atoms[ai][0][2]
#     print(atoms[ai][0][0],atoms[ai][0][1],atoms[ai][0][2])
 #    print(x,y)
     if ai<1:
       MINX=x
       MINY=y
       MAXX=x
       MAXY=y
     if x<MINX:
       MINX=x  
     if y<MINY:
       MINY=y  
     if x>MAXX:
       MAXX=x  
     if y>MAXY:
       MAXY=y  

MAX=max(MAXX,MAXY)
echelle=1.0/MAX
print(MINX, MINY)
print(MAX, MAXY)

links2=[]
for li in range(len(links)):
    if links[li][2]=="n":
      links2.append(line(links[li][0],links[li][1],2))
      links2[li].scale(echelle,[1.0,0.5,0.5])
      colorlink(li)
    if links[li][2]=="t":
      links2.append(line(links[li][0],links[li][1],1))
      links2[li].scale(echelle,[1.0,0.5,0.5])
      colorlink(li)
    if links[li][2]=="b":
      links2.append(line(links[li][0],links[li][1],3))
      links2[li].scale(echelle,[1.0,0.5,0.5])
      colorlink(li)

vacancy=0
atoms2=[]
for ai in range(len(atoms)):
    if atoms[ai][1]=="n":
	atoms2.append(sphere(atoms[ai][0],0.08,2))
        atoms2[ai-vacancy].scale(echelle,[1.0,0.5,0.5])
	coloratom(ai,vacancy)
    if atoms[ai][1]=="s":
        atoms2.append(sphere(atoms[ai][0],0.05,2))
        atoms2[ai-vacancy].scale(echelle,[1.0,0.5,0.5])
        coloratom(ai,vacancy)
    if atoms[ai][1]=="ss":
        atoms2.append(sphere(atoms[ai][0],0.03,2))
        atoms2[ai-vacancy].scale(echelle,[1.0,0.5,0.5])
        coloratom(ai,vacancy)
    if atoms[ai][1]=="b":
        atoms2.append(sphere(atoms[ai][0],0.1,2))
        atoms2[ai-vacancy].scale(echelle,[1.0,0.5,0.5])
        coloratom(ai,vacancy)
    if atoms[ai][1]=="bb":
        atoms2.append(sphere(atoms[ai][0],0.12,2))
        atoms2[ai-vacancy].scale(echelle,[1.0,0.5,0.5])
        coloratom(ai,vacancy)
	
    if atoms[ai][1]=="v":
	vacancy=+1
        links2.append(line([atoms[ai][0][0]-0.04,atoms[ai][0][1]-0.04,atoms[ai][0][2]-0.04],[atoms[ai][0][0]-0.04,atoms[ai][0][1]-0.04,atoms[ai][0][2]+0.04],1))
        links2[len(links2)-1].scale(echelle,[1.0,0.5,0.5])
        links2.append(line([atoms[ai][0][0]-0.04,atoms[ai][0][1]-0.04,atoms[ai][0][2]-0.04],[atoms[ai][0][0]-0.04,atoms[ai][0][1]+0.04,atoms[ai][0][2]-0.04],1))
        links2[len(links2)-1].scale(echelle,[1.0,0.5,0.5])
        links2.append(line([atoms[ai][0][0]-0.04,atoms[ai][0][1]-0.04,atoms[ai][0][2]-0.04],[atoms[ai][0][0]+0.04,atoms[ai][0][1]-0.04,atoms[ai][0][2]-0.04],1))
        links2[len(links2)-1].scale(echelle,[1.0,0.5,0.5])
        links2.append(line([atoms[ai][0][0]+0.04,atoms[ai][0][1]-0.04,atoms[ai][0][2]-0.04],[atoms[ai][0][0]+0.04,atoms[ai][0][1]+0.04,atoms[ai][0][2]-0.04],1))
        links2[len(links2)-1].scale(echelle,[1.0,0.5,0.5])
        links2.append(line([atoms[ai][0][0]+0.04,atoms[ai][0][1]-0.04,atoms[ai][0][2]-0.04],[atoms[ai][0][0]+0.04,atoms[ai][0][1]-0.04,atoms[ai][0][2]+0.04],1))
        links2[len(links2)-1].scale(echelle,[1.0,0.5,0.5])
        links2.append(line([atoms[ai][0][0]-0.04,atoms[ai][0][1]+0.04,atoms[ai][0][2]-0.04],[atoms[ai][0][0]+0.04,atoms[ai][0][1]+0.04,atoms[ai][0][2]-0.04],1))
        links2[len(links2)-1].scale(echelle,[1.0,0.5,0.5])
        links2.append(line([atoms[ai][0][0]-0.04,atoms[ai][0][1]+0.04,atoms[ai][0][2]-0.04],[atoms[ai][0][0]-0.04,atoms[ai][0][1]+0.04,atoms[ai][0][2]+0.04],1))
        links2[len(links2)-1].scale(echelle,[1.0,0.5,0.5])
        links2.append(line([atoms[ai][0][0]-0.04,atoms[ai][0][1]-0.04,atoms[ai][0][2]+0.04],[atoms[ai][0][0]+0.04,atoms[ai][0][1]-0.04,atoms[ai][0][2]+0.04],1))
        links2[len(links2)-1].scale(echelle,[1.0,0.5,0.5])
        links2.append(line([atoms[ai][0][0]-0.04,atoms[ai][0][1]-0.04,atoms[ai][0][2]+0.04],[atoms[ai][0][0]-0.04,atoms[ai][0][1]+0.04,atoms[ai][0][2]+0.04],1))
        links2[len(links2)-1].scale(echelle,[1.0,0.5,0.5])
        links2.append(line([atoms[ai][0][0]+0.04,atoms[ai][0][1]+0.04,atoms[ai][0][2]-0.04],[atoms[ai][0][0]+0.04,atoms[ai][0][1]+0.04,atoms[ai][0][2]+0.04],1))
        links2[len(links2)-1].scale(echelle,[1.0,0.5,0.5])
        links2.append(line([atoms[ai][0][0]-0.04,atoms[ai][0][1]+0.04,atoms[ai][0][2]+0.04],[atoms[ai][0][0]+0.04,atoms[ai][0][1]+0.04,atoms[ai][0][2]+0.04],1))
        links2[len(links2)-1].scale(echelle,[1.0,0.5,0.5])
        links2.append(line([atoms[ai][0][0]+0.04,atoms[ai][0][1]-0.04,atoms[ai][0][2]+0.04],[atoms[ai][0][0]+0.04,atoms[ai][0][1]+0.04,atoms[ai][0][2]+0.04],1))
        links2[len(links2)-1].scale(echelle,[1.0,0.5,0.5])
        
writing2=[]
for ti in range(len(writing)):
    writing2.append(texte(writing[ti][0],writing[ti][1],writing[ti][2]))
    writing2[ti].scale(echelle,[1.0,0.5,0.5])

#print(atoms2)
#print(links2)

#rotate
for ai in range(len(atoms2)):
    atoms2[ai].rotate(15.,10.,[0.5,0.5,0.5])
for li in range(len(links2)):
    links2[li].rotate(15.,10.,[0.5,0.5,0.5]) 
for ti in range(len(writing2)):
    writing2[ti].rotate(15.,10.,[0.5,0.5,0.5])

# Trim lines:
for ai in range(len(atoms2)):
  pa = atoms2[ai].p0
  ra = atoms2[ai].r
  for li in range(len(links2)):
    if links2[li].p0.dist(pa) < ra:
      links2[li].trim(0,ra)
    if links2[li].p1.dist(pa) < ra:
      links2[li].trim(1,ra)
                        
#plot
# Merge line and atom lists:
for ai in range(len(atoms2)):
  links2.append(atoms2.pop())
for ti in range(len(writing)):
  links2.append(writing2.pop())

#for li in range(len(links2)):
#  links2[li].rotate(15.,10.,[0.5,0.5,0.5])     

def cmp1(ax,bx): return cmp(ax.mean,bx.mean)
links2.sort(cmp1)
links2.reverse()
for li in range(len(links2)):
  links2[li].draw(graph)
graph.close()

if booleen2==0:
   os.system("epstool --copy --bbox Oct3.eps output.eps")
else:
   os.system("epstool --copy --bbox Oct3.eps " + fichier)
   
