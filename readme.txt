epstool is needed to reformat the pictures

Capital and small letters are important

List of geometries
BCC X Y Z
FCC X Y Z
CUBIC X Y Z
PLANX X Y x y z
PLANY Y Y x y z
PLANZ Z Y x y z
NOEL X Y Z


List of operations
-a x y z                           remove an atom
-al x y z                          remove an atom and its links
+as x y z                          add a small atom, default black
+an x y z                          add a normal atom
+ab x y z                          add a big atom, default grey
+av x y z                          add a vacancy
-l x1 y1 z1 x2 y2 z2               remove a link
+lt x1 y1 z1 x2 y2 z2              add a thin link
+ln x1 y1 z1 x2 y2 z2              add a normal link
+lb x1 y1 z1 x2 y2 z2              add a bold link
cola x y z color                   change the color of an atom
coll x1 y1 z1 x2 y2 z2 color       change the color of a link
w/wd/wr/wu/wl/wdr/wdl/wur/wul x y z size text   write a text in/up/down/left/right/... of the specified position


List of colors
black
grey
white
red
blue
yellow
orange
green

Exemple of an input file

BCC 2 1 1
+ab 0.5 0 0
+as 0 0.5 0
+as 0 0.5 0.5
+as 0 0.5 1
+as 0.5 0 1
+as 0.5 0.5 0
+as 0.5 1 0
+as 0.5 1.5 0
+as 0.5 1 0.5
+as 0.5 1 1
+as 1 1.5 0
+as 1 1.5 0.5
+as 1 1 0.5
+as 1.5 0 0
+as 1.5 0.5 0
+as 1.5 1 0
+as 1.5 1 0.5
+as 1.5 1 1
+as 2 0.5 0
+as 2 0.5 0.5
wdl 0 0.5 0 0.03 2
wu 0 0.48 0.5 0.03 3
wr -0.05 0.5 1 0.03 6
wul 0.5 0 1 0.03 4b
wl 0.52 0.5 0 0.03 1
wdr 0.5 1 0 0.03 4b
wl 0.52 1.5 0 0.03 8b
wdr 0.47 1 0.5 0.03 5b
wu 0.47 0.97 1 0.03 7b
wl 1.02 1.5 0 0.03 9b
wr 0.97 1.5 0.5 0.03 10b
wl 1.03 1 0.5 0.03 6
wd 1.5 0 0 0.03 4a
wd 1.5 0.5 0 0.03 5a
wd 1.5 1 0 0.03 7a
wdr 1.47 1 0.5 0.03 8a
wu 1.48 1 1 0.03 11
wdl 2 0.5 0 0.03 9a
wu 2 0.5 0.5 0.03 10a
+lt 0 0.5 0 2 0.5 0
+lt 0.5 0 0 0.5 1.5 0
+lt 1 1 0 1 1.5 0
+lt 1 1 0.5 1 1.5 0.5
