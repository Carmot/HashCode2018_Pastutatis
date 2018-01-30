# HashCode2018_Pastutatis

Resumen de algoritmo:
```
TTTTT
TMMMT
TTTTT
```
Buscamos slices minimas

f,c
ini 0,0 -> T
fin 0,1 -> T X
fin 1,0 -> T X

fin 1,1 -> M Y

Slice 1:
```
T1TTT
T1MMT
TTTTT
```
Slice 2:
f,c
0,2 -> T
0,3 -> T X
1,2 -> M Y
```
T12TT
T12MT
TTTTT
```
Slice 3:
f,c
0,3 -> T
0,4 -> T X
1,3 -> M Y
```
T123T
T123T
TTTTT
```
Slice 4:
f,c
0,4 -> T
0,5 -> NO
1,4 -> T X
0, 6 -> NO
2,4 -> T X
0, 7 -> NO
3,4 -> NO
camino sin salida
2,0 -> T
2,1 -> T X
2,2 -> T X
2,3 -> T X
2,4 -> T X
camino sin salida

3 slices

Ampliamos slices:
Slice 1
Lateral? -> IZQ 1
Vertical? -> ABAJO 1 ->
```
1123T
1123T
11TTT
```
Slice 2
Lateral? -> No puedo
Vertical? -> ABAJO 1 ->
```
1123T
1123T
112TT
```
Slice 3:
Lateral -> DCHA  1
VERTICAL -> ABAJO 1
```
11233
11233
11233
```
Completado!

