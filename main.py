import module
import json
import copy
import os
import random
import threading
import sys
import socket

sys.setrecursionlimit(999999999)

def bogoAI(table,playernumber):
    posli=module.getcanpos(table,playernumber)
    size=len(posli)
    if size==0:
        return 0
    return posli[random.randint(0,size-1)]

def runAI(table,playernumber):
	posli=module.getcanpos(table,playernumber)
	print("y,x:",end="")
	for i in range(len(posli)):
		print(posli[i].y,"",posli[i].x,end=",")
	parallel=len(posli)
	threads=[]
	value=[0.0 for i in range(parallel)]
#	for i in range(parallel):
#		module.launchmonte(table,playernumber,posli[i],i,value)
	for i in range(parallel):
		t = threading.Thread(target=module.launchmonte, args=(table,playernumber,posli[i],i,value,))
		threads.append(t)
		t.start()
	#	t.join()
	for i in range(parallel):
		threads[i].join()
	print(value)
	maxindex=0
	maxvalue=value[0]
	for i in range(1,parallel):
		if maxvalue<value[i]:
			maxindex=i
			maxvalue=value[i]
	return posli[maxindex]


roottable=[
[ 0, 0, 0, 0, 0, 0, 0, 0],
[ 0, 0, 0, 0, 0, 0, 0, 0],
[ 0, 0, 0, 0, 0, 0, 0, 0],
[ 0, 0, 0,-1, 1, 0, 0, 0],
[ 0, 0, 0, 1,-1, 0, 0, 0],
[ 0, 0, 0, 0, 0, 0, 0, 0],
[ 0, 0, 0, 0, 0, 0, 0, 0],
[ 0, 0, 0, 0, 0, 0, 0, 0]
]


def main():
	#os.system("cls")
	os.system("clear")
	global roottable
	playercolor=3
	while True:
		print("先攻の場合は1,後攻は-1:",end="")
		playercolor=input()
		if playercolor=="break":
			return 0
		#os.system("cls")
		os.system("clear")
		if playercolor=="1" or playercolor=="-1":
			playercolor=int(playercolor)
			break
		else:
			print("無効な入力です")
	playercon=[1,-1]
	turn=0
	while True:
		nowplayer=playercon[turn%2]
		module.drawmap(roottable,nowplayer)
		print("turn",turn,"nowplayer",nowplayer)
		if nowplayer!=playercolor:
			AIpos=runAI(roottable,nowplayer)
			#AIpos=bogoAI(roottable,nowplayer)
			#os.system("cls")
			os.system("clear")
			if AIpos==0:
				turn+=1
				continue
			roottable=module.turned(AIpos,roottable,nowplayer)
			turn+=1
			continue
		if len(module.getcanpos(roottable,nowplayer))==0:
			if len(module.getcanpos(roottable,-1*nowplayer))==0 or module.nullmap(roottable)==1:
				break
			os.system("clear")
			continue
		print("input y,x:",end="")
		inpu=input()
		if inpu=="break":
			break
		inp=inpu.split(",")
		if len(inp)!=2 or module.checkfield(int(inp[1]),int(inp[0]))!=1:
			#os.system("cls")
			os.system("clear")
			print("無効な入力です")
			continue
		place=module.pos()
		place.y=int(inp[0])
		place.x=int(inp[1])
		#os.system("cls")
		os.system("clear")
		if module.canput(place.x,place.y,roottable,nowplayer)==1:
			roottable=module.turned(place,roottable,nowplayer)
			turn+=1
		else:
			print("無効な入力です")
	module.drawmap(roottable,playercolor)
	return 0

if __name__=="__main__":
	main()

