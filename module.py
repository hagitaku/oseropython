import copy
import random
import sys

sys.setrecursionlimit(9999999)

width=20
tablevalue=1000
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
	elif table[y][x]==0:
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
	#送られた座標にコマを置けるか判断する処理
	if table[y][x]!=0:
		return 0
	if checkfield(x,y)==0:
		return 0
	for i in range(8):
		if checkfield(x+dirx[i],y+diry[i])==1 and table[y+diry[i]][x+dirx[i]]==-1*playernumber:
			if canputflg(x+dirx[i],y+diry[i],table,i,playernumber)==1:
				return 1
	return 0

def launchmonte(table,playernumber,pos,i,valuelist):
	Depth=1
	tablemap=copy.deepcopy(table)
	tablemap=turned(pos,tablemap,playernumber)
	tabletimes=[0 for i in range(tablevalue)]
	valuelist[i]=monte(tablemap,-playernumber,playernumber,Depth,i,tabletimes)/tablevalue
	return 0

def judge(table,playernumber):
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

def monte(table,playernumber,color,Depth,d,tabletimes):
	randlist=[]
	if tabletimes[d]==tablevalue:
		return 0
	if nullmap(table)==1 or len(getcanpos(table,1))==0 and len(getcanpos(table,-1))==0:
		tabletimes[d]+=1
		return judge(table,color)
	poslist=getcanpos(table,playernumber)
	count=0
	wi=len(poslist)
	if wi==0:
		return monte(table,-playernumber,playernumber,Depth,d,tabletimes)
	
	for i in range(min(wi,width)):
		randindex=0
		while True:
			randindex=random.randint(0,wi-1)
			if randindex in randlist:
				continue
			randlist.append(randindex)
			break

		tablemap=copy.deepcopy(table)
		tablemap=turned(poslist[i],tablemap,playernumber)
		count+=monte(tablemap,-playernumber,playernumber,Depth+1,d,tabletimes)
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

def drawmap(table,playernumber):
	posli=getcanpos(table,playernumber)
	size=len(posli)
	print(end="  ")
	for i in range(len(table)):
		print(i,end=" ")
	print()
	for i in range(len(table)):
		print(i,end=" ")
		for k in range(len(table[i])):
			flg=0
			for j in range(size):
				if posli[j].y==i and posli[j].x==k:
					flg=1
					break
			if flg==1:
				print("✖︎",end=" ")
			elif table[i][k]==0:
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
	#範囲内だったら1,範囲外だったら0
	return (1) if (0 <= x and x <= 7 and 0 <= y and y <= 7) else  0

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
