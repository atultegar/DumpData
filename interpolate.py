import clr
import math
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
#The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN

featurePoints = IN[0]
startStation = IN[1]
sPileLength = IN[2]

pointList = []
pointStationList = []
pointListNew = []
featurePoints1 = []
primaryList = []
secondaryList = []
pStationList = []
sStationList = []
pointThetaList = []
pThetaList = []
sThetaList = []

def getIntersectionPoint(center, radius, p1, p2):
    """ find the two points where secant intersects a circle """

    dx, dy = p2.X - p1.X, p2.Y - p1.Y

    a = dx**2 + dy**2
    b = 2 * (dx*(p1.X-center.X) + dy*(p1.Y-center.Y))
    c = (p1.X - center.X)**2 + (p1.Y-center.Y)**2 - radius**2

    discriminant = b**2 - 4*a*c
    assert (discriminant > 0), 'Not a secant!'

    t1 = (-b + discriminant**0.5) / (2*a)
    t2 = (-b - discriminant**0.5) / (2*a)

    point1X = round(dx*t1+p1.X,3)
    point1Y =  round(dy*t1+p1.Y,3)
    
    v1 = Vector.ByTwoPoints(p1, p2)
    v1Length = (v1.X**2 + v1.Y**2)**0.5
    u1X = v1.X/v1Length
    u1Y = v1.Y/v1Length
    u1Z = v1.Z/v1Length
    s1X = round(((point1X-p1.X)**2 + (point1Y-p1.Y)**2)**0.5,3)
    
    point1Z = round(p1.Z + (s1X)*u1Z,3)
    
    point1 = Point.ByCoordinates(point1X, point1Y, point1Z)

    return point1
 
def disBetweenPoints(p1, p2):
	dis = ((p2.X-p1.X)**2 + (p2.Y-p1.Y)**2)**0.5
	return dis

#def stationPoint(station):
oStation = startStation
for i in range(len(featurePoints)-1):
	rStation = featurePoints[i][0]
	nStation = featurePoints[i+1][0]
	if oStation >= rStation and oStation < nStation:
		x0 = featurePoints[i][1]
		y0 = featurePoints[i][2]
		z0 = featurePoints[i][3]
		x1 = featurePoints[i+1][1]
		y1 = featurePoints[i+1][2]
		z1 = featurePoints[i+1][3]
			
		P0 = Point.ByCoordinates(x0, y0, z0)
		P1 = Point.ByCoordinates(x1, y1, z1)
			
		v = Vector.ByTwoPoints(P0, P1)			
		vLength = disBetweenPoints(P0, P1)
		ux = v.X/vLength
		uy = v.Y/vLength
		uz = v.Z/vLength
		
		sX = round(x0 + (oStation - rStation)*ux,3)
		sY = round(y0 + (oStation - rStation)*uy,3)
		sZ = round(z0 + (oStation - rStation)*uz,3)

		sPoint = Point.ByCoordinates(sX, sY, sZ)
		k = i
#for i in range(len(featurePoints)):
#	Station = featurePoints[i][0]
#	X1 = featurePoints[i][1]
#	Y1 = featurePoints[i][2]
#	Z1 = featurePoints[i][3]

radius = sPileLength
center = Point.ByCoordinates(sX, sY, 0)
pointList.append(sPoint)

pStation = oStation
pointStationList.append(pStation)
for j in range(k, len(featurePoints)-1):
	x2 = featurePoints[j][1]
	y2 = featurePoints[j][2]
	z2 = featurePoints[j][3]
	x3 = featurePoints[j+1][1]
	y3 = featurePoints[j+1][2]
	z3 = featurePoints[j+1][3]
	
	p1 = Point.ByCoordinates(x2, y2, z2)
	p2 = Point.ByCoordinates(x3, y3, z3)
	
	lLength = disBetweenPoints(p1, p2)
	div = disBetweenPoints(center, p2)
	
	while div >= radius:
		intPoint = getIntersectionPoint(center, radius, p1, p2)
		pointList.append(intPoint)
		pStation = round(pStation+sPileLength,3)
		pointStationList.append(pStation)
		center = Point.ByCoordinates(intPoint.X, intPoint.Y,0)
		div = disBetweenPoints(center, p2)
	
	

#Assign your output to the OUT variable.
OUT = pointList, pointStationList