import module
import json
import copy

def turn(pos,table):
	tablemap=copy.deepcopy(table)

	return tablemap

def canplace(pos,table,playnum):

	return 0

def checkfield(x,y):

	return (1) if (0 <= x <= 7 and 0 <= y <= 7) else  0

def nullmap(table):
	#マップに空白があればreturn 0
	#なければreturn 1
	ysize=len(table)
	xsize=len(table[0])
	for i in range(ysize):
		for k in range(xsize):
			if(table[i][k]==0):
				return 0
	return 1

def canflg( X, Y, I, table, playernumber):
	#投げられたplayernumberがその場所におけるかどうかの判定を行う再帰関数。おけたら1,おけなかったら2を返す
	flg = 0;
	map=copy.deepcopy(table)

	if (map[Y + module.diry[I]][X + module.dirx[I]] == -1 * playernumber and checkfield(X + module.dirx[I], Y + module.diry[I]) == 1):
		flg = canflg(Y + module.diry[I], X + module.dirx[I], I, map, playernumber)
	elif (map[Y + module.diry[I]][X + module.dirx[I]] == 1 * playernumber and checkfield(X + module.dirx[I], Y + module.diry[I]) == 1):
		return 1
	elif (map[Y + module.diry[I]][X + module.dirx[I]] == 0 and checkfield(X + module.dirx[I], Y + module.diry[I]) == 1):
		return 0;
	return flg


roottable=[
[ 0, 0, 0, 0, 0, 0, 0, 0],
[ 0, 0, 0, 0, 0, 0, 0, 0],
[ 0, 0, 0, 0, 0, 0, 0, 0],
[ 0, 0, 0, 1,-1, 0, 0, 0],
[ 0, 0, 0,-1, 1, 0, 0, 0],
[ 0, 0, 0, 0, 0, 0, 0, 0],
[ 0, 0, 0, 0, 0, 0, 0, 0],
[ 0, 0, 0, 0, 0, 0, 0, 0]
]

def main():
	return 0

if __name__=="__main__":
	pos=module.pos()
	pos.y=2
	pos.x=4
	for I in range(8):
		print(canflg( pos.x, pos.y, I, roottable, 1))
