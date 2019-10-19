import copy
import random
import sys

sys.setrecursionlimit(99999)

width=4

class pos:
	x=0
	y=0

dirx=[-1, 0, 1, 1, 1, 0,-1,-1]
diry=[-1,-1,-1, 0, 1, 1, 1, 0]

def turned(pos,table,playernumber):
	#ひっくり返されたあとの盤面を返す
	tablemap=copy.deepcopy(table)
	if canput(pos.x,pos.y,tablemap,playernumber)==1:
		tablemap[pos.y][pos.x]=playernumber
		for i in range(8):
			reverse(pos.x+dirx[i],pos.y+diry[i],i,tablemap,playernumber)
	return tablemap

def canputflg(x,y,table,i,playernumber):
	if checkfield(x,y)==0:#現在地が範囲外だったらすぐにおけないことを示す0を返す
		return 0
	elif table[y][x]==playernumber:
		return 1
	else:
		return canputflg(x+dirx[i],y+diry[i],table,i,playernumber)
	return 0

def nullmap(table):
	#マップに空白があればreturn 0
	#なければreturn 1。また、勝敗がついていても1が帰ってくる
	acount=0
	bcount=0
	ccount=0
	ysize=len(table)
	xsize=0
	if 1<ysize:
		xsize=len(table[0])
	for i in range(ysize):
		for k in range(xsize):
			if table[i][k]== 0:
				acount+=1
			if table[i][k]== 1:
				bcount+=1
			if table[i][k]==-1:
				ccount+=1
	if acount==0:
		return 1
	elif bcount==0 or ccount==0:
		return 1
	return 0

def	canput(x,y,table,playernumber):
	#送られた座標にコマを置けるか判断する処理処理
	if table[y][x]!=0:
		return 0
	for i in range(8):
		if checkfield(x+dirx[i],y+diry[i])==1 and table[y+diry[i]][x+dirx[i]]==-1*playernumber:
			if canputflg(x+dirx[i],y+diry[i],table,i,playernumber)==1:
				return 1
	return 0

def launchmonte(table,playernumber,pos,i,valuelist):
	print(i)
	tablemap=copy.deepcopy(table)
	tablemap=turned(pos,tablemap,playernumber)
	valuelist[i]=monte(tablemap,-playernumber,playernumber)
	return 0

def judge(table,playernumber,color):
	mikata=0
	teki=0
	for i in range(len(table)):
		for k in range(len(table[i])):
			if table[i][k]!=0:
				if table[i][k]==playernumber:
					mikata+=1
				else:
					teki+=1
	return 0 if teki>mikata else 1

def monte(table,playernumber,color):
	randlist=[]
	if nullmap(table)==1:
		return judge(table,color)
	poslist=getcanpos(table,playernumber)
	count=0
	wi=len(poslist)
	if wi==0:
		return monte(table,-playernumber,playernumber)
	
	for i in range(min(wi,width)):
		randindex=0
		while True:
			randindex=random.randint(0,wi-1)
			if randindex in randlist:
				continue
			randlist.append(randindex)
			break

		tablemap=copy.deepcopy(table)
		turned(poslist[i],tablemap,playernumber)
		count+=monte(tablemap,-playernumber,playernumber)
	return count


def getcanpos(table,playernumber):
	#playnumが置ける場所をposクラスのリストで返す処理。多分そこそこ計算量が多い
	poslist=[]
	for i in range(len(table)):
		for k in range(len(table[i])):
			if canput(k,i,table,playernumber)==1:
				putpos=pos()
				putpos.x=k
				putpos.y=i
				poslist.append(putpos)
	return poslist

def drawmap(table):
	print(end="  ")
	for i in range(8):
		print(i,end=" ")
	print()
	for i in range(len(table)):
		print(i,end=" ")
		for k in range(len(table[i])):
			if table[i][k]==0:
				print("-",end=" ")
			elif table[i][k]==1:
				print("○",end=" ")
			elif table[i][k]==-1:
				print("●",end=" ")
		print()
	print()
	return 0

def checkfield(x,y):
	#範囲外か判断する処理
	return (1) if (0 <= x <= 7 and 0 <= y <= 7) else  0

def reverse(x,y,i,table,playernumber):
	if checkfield(x,y)==0:
		return 0
	if table[y][x]==playernumber:
		return 1
	if checkfield(x,y)==0 or table[y][x]==0:
		return 0
	flg=reverse(x+dirx[i],y+diry[i],i,table,playernumber)
	if flg==1:
		table[y][x]=playernumber
		return 1
	return 0

if __name__=="__main__":
	pass

