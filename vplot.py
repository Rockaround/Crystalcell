# postscript files 
# v0.92 November 6, 2005
# Recommend you make a directory "python" in your home directory, and
# put vplot.py in there.  To access anywhere, set PYTHONPATH in your .bashrc,:
#      PYTHONPATH=$HOME/python
#      export PYTHONPATH


import math  #because we need sqrt, cos ,sin

# When a vplot.eps_class() object is created, the __init__ method is invoked.
# The Bounding Box is set, an output file is opened, a header is written. 
# Default scale factors are then set by invoking "scale". 
class eps_class:
	def __init__(self,fname='temp.eps',bbx=512,bby=512,prolog=''):

		self.bbx=bbx 
		self.bby=bby
		self.fname=fname
		self.eps=open(self.fname,'w')
		self.scale() #scale method is invoked, setting defaults, but it can be called again

#Next we write out the header, with our values inserted in the BoundingBox statement
#Notice the """ surrounding multi-line strings.
#The `int(bbx)` converts bbx into an integer and then the ` ` converts it into a string 
		self.eps.write("""%!PS-Adobe-2.0 EPSF-2.0
%%Creator: vplot.py
%%DocumentFonts: Geneva
%%BoundingBox: 0 0 """+`int(bbx)`+' '+`int(bby)`+""" 
%%EndComments
/fontsize 12 def
/csize {1 mul} def
/Geneva fontsize selectfont
/cshift fontsize neg def
/vshift fontsize -2 div def
/L {lineto} bind def
/M {moveto} bind def
/S {stroke} bind def
/CS {closepath stroke} bind def
/RP {reversepath} bind def
/F {closepath fill} bind def
/X {currentpoint stroke moveto} bind def
/N {newpath} bind def
/C {setrgbcolor} bind def
/R {rmoveto} bind def
/V {rlineto} bind def
/DON {[3 2] 0 setdash} bind def 
/DOFF {[] 0 setdash} bind def
/Cshow { currentpoint S M
  dup stringwidth pop -2 div cshift R 0 -2 R show } def   
/Rshow { dup stringwidth pop neg vshift R -4 2 R show } def    
1 setlinewidth
""")
		if prolog: self.eps.write(prolog)
		self.eps.write("%%EndProlog\n")

	def close(self):
		print "The file ",self.fname," was successfully written and closed by vplot"
		self.eps.close()

# METHODS FOR COORDINATES AND COORDINATE CONVERSION. The postscript eps files will
# use coordinates (think "i" and "j") measured in units of "points", or pts,
# which is 1/72 of an inch.  The origin for the postscript files is the extreme lower left. 
# User coordinates, (think "x" and "y") are linearly related to postscript coordinates,
# The origin starts at the lower-left margins.  It is expected that things are easier to
# plot in user coordinates.  A coordinate passed in as a real number is interpreted
# as a user coordinate.  A coordinate passed in as an integer is interpreted as a 
# postscript coordinate.  But there are two other forms of "user" coordinates that can also
# be passed in. Imajinary numbers are fractions of the bounding box, the acceptable
# being 0.0j to 1.0j.  Long integers are hi-resolution postscript coordinates,
# essentially the postscript coordinates multiplied by 100.
	def scale(self,xmin=0.,xmax=1.,ymin=0.,ymax=1., #sets the user coordinates
			leftmarg=50,rightmarg=50,botmarg=50,topmarg=50): 
		self.xmin=xmin
		self.xmax=xmax
		self.ymin=ymin
		self.ymax=ymax
		self.leftmarg=leftmarg
		self.rightmarg=rightmarg
		self.botmarg=botmarg
		self.topmarg=topmarg
		self.xscale=float(self.bbx-self.leftmarg-self.rightmarg)/(self.xmax-self.xmin)
		self.yscale=float(self.bby-self.botmarg -self.topmarg  )/(self.ymax-self.ymin)
		#self.translate(self.leftmarg,self.botmarg)

#the following are generally called just before writing the coordinate to the file:
	def ix(self,x): #postscript "i" coordinate as function of various types of user "x"
		if isinstance(x,float):
			return self.leftmarg+(x-self.xmin)*self.xscale
			#return (x-self.xmin)*self.xscale
		elif isinstance(x,complex):
			return x.imag*self.bbx
		elif isinstance(x,long):
			return x*.01
		else:
			return x 

	def jy(self,y): #postscript "j" coordinate as function of various types of user "y"
		if isinstance(y,float):
			return self.botmarg+(y-self.ymin)*self.yscale
			#return (y-self.ymin)*self.yscale
		elif isinstance(y,complex):
			return y.imag*self.bby
		elif isinstance(y,long):
			return y*.01
		else:
			return y
		
#sizes of things are scaled a bit differently from a postion of a thing.
	def sx(self,x): #pt size for fonts, ticks, radius, etc., as function of user "x" size
		if isinstance(x,float):
			return x*self.xscale
		elif isinstance(x,complex):
			return x.imag*self.bbx
		elif isinstance(x,long):
			return x*.01
		else:
			return x 
		
	def sy(self,y): #pt size for fonts, ticks, radius, etc., as function of user "y" size
		if isinstance(y,float):
			return y*self.yscale
		elif isinstance(y,complex):
			return y.imag*self.bby
		elif isinstance(y,long):
			return y*.01
		else:
			return y 
		
	def ijxy(self,a): #converts an x,y  pair to postscript i,j pairs
			return self.ix(a[0]),self.iy(a[1])

#COLOR AND WIDTH METHODS
#	def color(self,red,green,blue):
#		self.eps.write( "%6.3f %6.3f %6.3f C\n" % (red,green,blue) )
	def color(self,*colors):
		if bool(colors):
			f=colors[0]
			if isinstance(f,list) or isinstance(f,tuple):
				r,g,b=f
			elif isinstance(f,str):
				if   f=="red":   r,g,b=1,0,0
				elif f=="green": r,g,b=0,1,0
				elif f=="blue":  r,g,b=0,0,1
				elif f=="yellow":r,g,b=1,1,0
				elif f=="cyan":  r,g,b=0,1,1
				elif f=="magenta":r,g,b=1,0,1
				else: r,g,b=0,0,0
			else: r,g,b=colors
		else:
			r,g,b=0,0,0
		self.eps.write( "%6.3f %6.3f %6.3f C\n" % (r,g,b) )
	def linewidth(self,width=1):
		self.eps.write("%6.2f setlinewidth\n" % (self.sx(width))) 

#SIMPLE DRAWING 
#Some simple, and useful drawing methods.
	def moveto(self,x,y): #move to, without drawing
		self.eps.write("N %8.2f %8.2f M\n"% 
		(self.ix(x),self.jy(y)))

	def lineto(self,x,y): #draw line to, from current point
		self.eps.write("%8.2f %8.2f L X\n"% 
		(self.ix(x),self.jy(y)))

	def line(self,x1,y1,x2,y2): #draw line between points
		self.moveto(x1,y1)
		self.eps.write("%8.2f %8.2f L S\n"%
		(self.ix(x2),self.jy(y2)))

	def linetos(self,alist): #connects a list of points
		i=0
		n=len(alist)
		x,y,i=next2(alist,i)
		self.moveto(x,y)
		while i < n:
			x,y,i=next2(alist,i)
			self.eps.write("%8.2f %8.2f L\n" % (self.ix(x),self.jy(y)))
            #note the stroke, connect, or fill command is not yet called
		
	def draw(self,alist):#draws a path connecting the list of points
		self.linetos(alist)
		self.eps.write("S\n")

	def dashdraw(self,alist): #like draw, but dashed 
		self.eps.write("DON\n") 
		self.draw(alist)
		self.eps.write("DOFF\n")

	def clip(self,alist):  #clips a path
		self.linetos(alist)
		self.eps.write("clip N\n")

#the followings accept an optional trailing argument 'F', to fill
	def poly(self,alist,*tags):  #like draw, but closes path
		self.linetos(alist)
		self.eps.write("%s\n" % (detag('CS',tags)))
		
	def rect(self,x1,y1,x2,y2,*tags):  
		self.poly([x1,y1,x2,y1,x2,y2,x1,y2],detag('',tags))

#CIRCLES, both accept optional trailing argument 'F', for fill
#circle with center at x,y with radius r :
	def circle(self,x,y,r,*tags):
		self.eps.write("N %8.2f %8.2f %8.2f csize 0 360 arc %s\n" %
				(self.ix(x), self.jy(y), self.sx(r), detag('CS',tags)))

#sector with center at user (x,y), but radius r1 and r2 are in pts:
	def sector(self,x,y,r1,r2,a1,a2,*tags):
		self.eps.write("N %8.2f %8.2f %8.2f csize %8.2f %8.2f arc RP\n" %
				(self.ix(x),self.jy(y),self.sx(r1),a1,a2))
		self.eps.write("  %8.2f %8.2f %8.2f csize %8.2f %8.2f arc %s\n" %
				(self.ix(x),self.jy(y),self.sx(r2),a1,a2,detag('CS',tags)))

#TEXT PLACEMENT
	def text(self,x,y,angle,size,text): 
		self.moveto(x,y)
		self.eps.write( "gsave /Geneva %d selectfont\n" % self.sx(size))
		self.eps.write( "%7.2f rotate\n" % angle )
		self.eps.write( "("+text+") show grestore\n")

#COMPOSITE DRAWING
	def arrow(self,x1,y1,x2,y2,headsize): #headsize is in pts
		i1,j1,i2,j2=self.ix(x1),self.jy(y1),self.ix(x2),self.jy(y2)
		headsize=self.sx(headsize)
		self.line(x1,y1,x2,y2)
		r=math.sqrt((i2-i1)**2+(j2-j1)**2)
		u=(i2-i1)/r
		v=(j2-j1)/r
		ai=-.8*u-.6*v
		aj=.6*u-.8*v
		self.line(lng(i2),lng(j2),lng(i2+headsize*ai),lng(j2+headsize*aj))
		ai=-.8*u+.6*v
		aj=-.6*u-.8*v
		self.line(lng(i2),lng(j2),lng(i2+headsize*ai),lng(j2+headsize*aj))


	def fatarrow(self,x1,y1,x2,y2,asize): #asize is the half-width of the fat arrow
		i1,j1,i2,j2=self.ix(x1),self.jy(y1),self.ix(x2),self.jy(y2)
		asize=self.sx(asize)
		r=math.sqrt((i2-i1)**2+(j2-j1)**2)
		u=asize*(i2-i1)/r
		v=asize*(j2-j1)/r
		self.poly(map(lng,[
			i1+v,j1-u,
			i2+v-u,j2-u-v,
			i2,j2,
			i2-v-u,j2+u-v,
			i1-v,j1+u]),'F')

	def windbarb(self,x,y,s,a,h):
		i1,j1=self.ix(x),self.jy(y)
		d=.13*h
		f=.5*h
		if s>=2.50:
			p=[0,0,-h,0]
			self.draw([lng(z) for z in shift(rotate(p,a),i1,j1)])
		else:
			self.circle(lng(i1),lng(j1),int(d))
		w=-h+d
		if s<47.50 and s>=7.50: w=-h
		while s>=47.50:
			p=[w,0,w-d,f,w-d,0]
			self.poly([lng(z) for z in shift(rotate(p,a),i1,j1)],'F')
			s=s-50.
			w=w+d
		while s>=7.50:
			p=[w,0,w-d,f]
			self.draw([lng(z) for z in shift(rotate(p,a),i1,j1)])
			s=s-10.
			w=w+d
		while s>=2.50:
			p=[w,0,w-.5*d,.5*f]
			self.draw([lng(z) for z in shift(rotate(p,a),i1,j1)])
			s=s-5.
			w=w+d
			
			
			

#AXES DRAWING
#If you don't use the defaults, you should call these using your user coordinates only,
#except for ticklen which can be passed as an integer
	def xaxis(self, y="", #where to intersect the y-axis
			x1="", #smallest x
			dx="", #increment for tick marks
			x2="", #largest x
			ticklen=10, #length of ticks, in pts
			grid=False,
			xticks=None,
			form='%5.1f'): #format string for numerical labels
		if y=="": y=self.ymin
		if x1=="": x1=self.xmin
		if x2=="": x2=self.xmax
		if dx=="": dx=(self.xmax-self.xmin)*.1
		if xticks==None: xticks=[]
		y,x1,x2,dx=map(float,[y,x1,x2,dx])
		if grid:
			y2=float(self.ymax)
			self.line(x1,y2,x2,y2)
			ticklen=self.jy(y2)-self.jy(y)
		else:
			ticklen=self.sy(ticklen)
		self.line(x1,y,x2,y)
		if not xticks:
			x=x1
			while x < x2*1.00001: #make tick marks
				xticks.append(x)
				x=x+dx
		for x in xticks: #make tick marks
			str=form % x
			self.line(x,y,x,lng(self.jy(y)+ticklen))
			self.cshow(x,y,str) #label tick marks

	def yaxis(self, x="", #where to intersect the x-axis
			y1="", #smallest y
			dy="", #increment for tick marks
			y2="", #largest y
			ticklen=10, #length of ticks, in pts
			grid=False,
			yticks=None,
			form='%5.1f'): #format for numerical labels
		if x=="": x=self.xmin
		if y1=="": y1=self.ymin
		if y2=="": y2=self.ymax
		if dy=="": dy=(self.ymax-self.ymin)*.1
		if yticks==None: yticks=[]
		x,y1,y2,dy=map(float,[x,y1,y2,dy])
		self.line(x,y1,x,y2)
		if grid:
			x2=float(self.xmax)
			self.line(x2,y1,x2,y2)
			ticklen=self.ix(x2)-self.ix(x)
		else:
			ticklen=self.sx(ticklen)
		if not yticks:
			y=y1
			while y < y2*1.00001: #make tick marks
				yticks.append(y)
				y=y+dy
		for y in yticks: #make tick marks
			str=form % y
			self.line(x,y,lng(self.ix(x)+ticklen),y)
			self.rshow(x,y,str) #label tick marks

	def cshow(self,x,y,text): #used for numerical labels on x-axis tick marks
		self.moveto(x,y)
		self.eps.write("("+text+") Cshow\n")

	def rshow(self,x,y,text): #used for numerical labels on y-axis tick marks
		self.moveto(x,y)
		self.eps.write("("+text+") Rshow\n")

### some useful postscript commands, that don't draw

	def comment(self,s):
		self.eps.write("% "+s+"\n")
	def raw(self,s):
		self.eps.write(s+"\n")
	def gsave(self):
		self.eps.write("gsave\n")
	def grestore(self):
		self.eps.write("grestore\n")
#the following do NOT work well with the vplot way of handling coordinates
#	def rotate(self,a):
#		self.eps.write("%8.2f rotate\n" % a)
#	def translate(self,x,y): 
#		self.eps.write("%8.2f %8.2f translate\n" % (self.ix(x),self.jy(y))) 
#	def scale(self,x,y): #yipes! name conflict 
#		self.eps.write("%8.2f %8.2f scale\n" % (self.ix(x),self.jy(y)))
	

### some functions independent of eps_class, used internally
def detag(default,tags): #overides default tag
	tag=default
	if tags and tags[0]: tag=tags[0]
	return tag
	
def lng(x): #converts postscript (pts) coordinates to hi-res coordinate type
	return long(100*x)

def next2(alist,i): #gets next 2 elements in list, even if they are found in a tuple
	x=alist[i]
	i+=1
	if isinstance(x,tuple) or isinstance(x,list):
		x,y=x
	else:
		y=alist[i]
		i+=1
	return x,y,i

### some list processing functions, independent of eps_class
def shift(alist,p,q):
	j=0
	slist=[]
	while j<len(alist):
		x,y,j=next2(alist,j)
		slist+=[p+x,q+y]
	return slist
	
def rotate(alist,a):
	th=math.pi*a/180.
	c=math.cos(th)
	s=math.sin(th)
	j=0
	slist=[]
	while j<len(alist):
		x,y,j=next2(alist,j)
		slist+=[c*x-s*y,s*x+c*y]
	return slist

##############
# A simple test program, which can be invoked as vplot.tester() from your
# python command line: 
def tester():
	import vplot
	print "A sample plot will be output as tester.eps"
	#this example makes a Japanese flag
	#the next line creates or "instantiates" an object vplot.eps_class
	a=vplot.eps_class(fname="tester.eps")  # argument fname is passed, overides default 'temp.eps'
	#next we invoke the methods of our object "a". The methods write out postscript commands.
	a.color('red')  #changes colors to red
	a.circle(.5,.5,100,'F') #filled circle at user coordinate (.5,.5) with radius=100 pts
	a.color() #change color back to black (default)
	a.rect(0.,.15,1.,.85) #draws a rectangle
	a.close() #close the output file

# The python tradition is that the test program is called if this module is invoked by itself,
# meaning if you type on your unix/linux command line: python vplot.py
if __name__ == '__main__':
	tester()
