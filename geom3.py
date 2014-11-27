import math
# vplot

class point(list):
    def __init__(self,lin):
        if (len(lin) != 3):
            print 'error...'
        list.__init__(self,lin)        
    def rotate(self,alfa,beta,r0):
        alfa = alfa/360.*2*math.pi
        beta = beta/360.*2*math.pi
        sa = math.sin(alfa)
        ca = math.cos(alfa)
        sb = math.sin(beta)
        cb = math.cos(beta)
        self[0] = self[0]-r0[0]
        self[1] = self[1]-r0[1]
        self[2] = self[2]-r0[2]
        xp = cb*self[0]+sb*self[2]
        yp = -sa*sb*self[0]+ca*self[1]+sa*cb*self[2]
        zp = -ca*sb*self[0]-sa*self[1]+ca*cb*self[2]
        self[0],self[1],self[2] = xp+r0[0],yp+r0[1],zp+r0[2]
    def scale(self,scFact,center):
        for i in range(3):
            self[i] -= center[i]
            self[i] *= scFact
            self[i] += 0.5
    def dist(self,p1):
        return(math.sqrt((self[0]-p1[0])**2+(self[1]-p1[1])**2+(self[2]-p1[2])**2))

class line:
    def __init__(self,p0,p1,width=1,col=[0.,0.,0.],grayscale=0.0,type=0):
        self.p0 = point(p0)
        self.p1 = point(p1)
        self.mean=(self.p0[2]+self.p1[2])/2.
        self.width = width
        self.grayscale=grayscale
	self.col=col
        self.type=type
        self.__name__ = 'line'
    def rotate(self,alfa,beta,r0):
        self.p0.rotate(alfa,beta,r0)
        self.p1.rotate(alfa,beta,r0)
        self.mean=(self.p0[2]+self.p1[2])/2.
    def scale(self,scFact,center):
        self.p0.scale(scFact,center)
        self.p1.scale(scFact,center)
        self.mean=(self.p0[2]+self.p1[2])/2.
    def draw(self,fig):
        fig.gsave()
	fig.color(self.col[0],self.col[1],self.col[2])
        #fig.eps.write("%8.2f setgray\n"% self.grayscale)
        #if (self.type != 0):
        #    fig.eps.write("[10 13] %d setdash\n"% self.width)
        if (self.width != 1):
            fig.linewidth(self.width)
        fig.line(self.p0[0],self.p0[1],self.p1[0],self.p1[1])
        fig.color(0.,0.,0.)
        # else:
        #     print 'Not yet implemented...'
        fig.grestore()
    def trim(self,ind,d):
        xh = [self.p1[0]-self.p0[0],self.p1[1]-self.p0[1],self.p1[2]-self.p0[2]]
        dd = math.sqrt(xh[0]**2+xh[1]**2+xh[2]**2)
        xh[0] = xh[0]/dd;xh[1] = xh[1]/dd;xh[2] = xh[2]/dd
        if (ind == 0):
           self.p0[0] += xh[0]*d
           self.p0[1] += xh[1]*d
           self.p0[2] += xh[2]*d
        if (ind == 1):
           self.p1[0] -= xh[0]*d
           self.p1[1] -= xh[1]*d
           self.p1[2] -= xh[2]*d

class sphere:
    def __init__(self,p0,r,width=1,col=[1.,1.,1.]):
        self.p0 = point(p0)
        self.mean = self.p0[2]
        self.r = r
        self.width = width
        self.col = col
        self.__name__ = 'sphere'
    def rotate(self,alfa,beta,r0):
        self.p0.rotate(alfa,beta,r0)
        self.mean = self.p0[2]
    def scale(self,scFact,center):
        self.p0.scale(scFact,center)
        self.mean = self.p0[2]
        self.r *= scFact
    def draw(self,fig,shadow = False):
        fig.gsave()
        fig.linewidth(self.width)
        fig.color(self.col[0],self.col[1],self.col[2])
        fig.circle(self.p0[0],self.p0[1],self.r,'F')
        fig.color(0.,0.,0.)
        fig.circle(self.p0[0],self.p0[1],self.r)
        fig.grestore()
        
    def intersect(self,rA,dx,dy):
        d2 = self.r**2+rA**2
        K = math.sqrt(((rA+self.r)**2-d2)*(d2-(rA-self.r)**2))
        xm = 1/2*dx-1/2*dx*(rA**2-self.r**2)/d2-dy*K/d2
        xp = 1/2*dx-1/2*dx*(rA**2-self.r**2)/d2+dy*K/d2
        ym = 1/2*dy-1/2*dy*(rA**2-self.r**2)/d2-dx*K/d2
        yp = 1/2*dy-1/2*dy*(rA**2-self.r**2)/d2+dx*K/d2
        return xp,xm,yp,ym

class texte:
    def __init__(self,p0,texte=" ",size=10,col=[0.,0.,0.],r=1):
	self.p0=point(p0)
	self.mean=p0[2]
	self.texte=texte
	self.size=size
	self.col=col
	self.r=r
	self.__name__= 'texte'
    def rotate(self,alfa,beta,r0):
        self.p0.rotate(alfa,beta,r0)
        self.mean = self.p0[2]
    def scale(self,scFact,center):
        self.p0.scale(scFact,center)
        self.mean = self.p0[2]
        self.r *= scFact
    def draw(self,fig):
        fig.gsave()
        fig.color(self.col[0],self.col[1],self.col[2])
        fig.text(self.p0[0],self.p0[1],0,self.size,self.texte)
        fig.color(0.,0.,0.)
        fig.grestore()
