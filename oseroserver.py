import tkinter as tk
import socket
from tkinter import font
import threading
import random
import module

drawflg=0
players=[-1,1]
port=50000
addres=socket.gethostbyname(socket.gethostname())
radius=30
socketstate=0
recvflg=0
#待ち受け状態:1,
roottable=[
[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[ 0, 0, 0, 0, 1,-1, 0, 0, 0, 0],
[ 0, 0, 0, 0,-1, 1, 0, 0, 0, 0],
[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

def checkfield(x,y):
	#範囲外か判断する処理
	#範囲内だったら1,範囲外だったら0
	return (1) if (0 <= x and x <= 9 and 0 <= y and y <= 9) else  0

def socketserver():
	#別スレッドでサーバーのプログラムを動かす
	global roottable
	playercount=0
	randplay=0
	player=[1,-1]
	turn=0
	put=module.pos()
	put.x=100
	put.y=100
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((addres, port))
		s.listen(1)
		while True:
			nowplayer=player[turn%2]
			print(nowplayer,playercount)
			conn, addr = s.accept()
			data = conn.recv(1024).decode()
			if data == '':
				conn.sendall("Invalid".encode())
				continue
			elif data.split(":")[0]=="info":
				if int(data.split(":")[1])==nowplayer:
					conn.sendall(("enemy:"+str(put.x)+","+str(put.y)).encode())
				elif int(data.split(":")[1])==-1*nowplayer:
					conn.sendall("wait".encode())
			if data=="Recruit" and playercount==0:
				playercount+=1
				playerid=random.choice(players)#
				players.remove(playerid)
				conn.sendall(str(playerid).encode())
			elif data=="Recruit" and playercount==1:
				playercount+=1
				playerid=random.choice(players)#
				players.remove(playerid)
				conn.sendall(str(playerid).encode())
			elif data=="Recruit" and playercount==2:
				conn.sendall("Invalid".encode())
			elif data.split(":")[0]=="turn" and int(data.split(":")[1])==nowplayer and playercount==2:
				position=data.split(":")[2].split(",")
				print("canput:",module.canput(int(position[0]),int(position[1]),roottable,int(data.split(":")[1])))
				if module.canput(int(position[0]),int(position[1]),roottable,int(data.split(":")[1]))==1:
					putpos=module.pos()
					putpos.x=int(position[0])
					putpos.y=int(position[1])
					put.x=int(position[0])
					put.y=int(position[1])
					roottable=module.turned(putpos,roottable,int(data.split(":")[1]))
					conn.sendall("accept".encode())
					turn+=1
					module.drawmap(roottable,0)
				else:
					conn.sendall("Invalid".encode())
			elif data.split(":")[0]=="turn" and int(data.split(":")[1])==-1*nowplayer and playercount==2:
				conn.sendall("wait".encode())


class Circle(): #円オブジェクト
    def __init__(self,canvas,x,y,r,color,tag):
        self.canvas = canvas
        self.x = x #中心のx座標
        self.y = y #中心のy座標
        self.r = r #円の半径
        self.color = color
        self.tag = tag

    def createCircle(self): #円を作るメソッド
        self.canvas.create_oval(self.x-self.r,self.y-self.r,self.x+self.r,self.y+self.r,fill=self.color,tag=self.tag)

class Application(tk.Frame):
	def __init__(self,master):
		super().__init__(master)

		self.pack()
		self.width=650
		self.height=700
		self.checkNumber=1

		master.geometry(str(self.width)+"x"+str(self.height)) #ウィンドウの作成
		master.title("10x10オセロ") #タイトル
		self.createCanvas() #キャンバスの作成
		master.after(1, self.update) #ループ処理

	def createCanvas(self): #キャンバスの作成
		self.canvas = tk.Canvas(self.master,width=self.width,height=self.height) #キャンバスの作成
		self.canvas.pack()

		self.circle1 = Circle(self.canvas,225,60,50,"red","circle1") #インスタンスcircle1の生成

	def update(self):
		#描画関数
		global roottable
		#module.drawmap(roottable,1)
		ysize=len(roottable)
		xsize=len(roottable[0])
		wcount=0
		bcount=0
		for i in range(ysize):
			for k in range(xsize):
				if roottable[i][k]==1:
					bcount+=1
				elif roottable[i][k]==-1:
					wcount+=1
		Label = tk.Label(text='white:'+str(wcount)+'  black:'+str(bcount),font=font.Font(size=30))
		Label.place(x=200, y=20)
		self.canvas.delete(self.circle1.tag)

		margin=50
		self.canvas.create_rectangle(margin-radius, 2*margin-radius, margin+xsize*radius*2-radius, 2*margin+2*radius*ysize-radius, fill = 'green')

		for i in range(ysize+1):
			self.canvas.create_line( margin-radius, 2*margin+radius*i*2-radius, margin+xsize*radius*2-radius, 2*margin+radius*i*2-radius, fill='black')
			for k in range(xsize+1):
				self.canvas.create_line( margin+radius*k*2-radius, 2*margin-radius, margin+radius*k*2-radius, 2*margin+2*radius*ysize-radius, fill='black')
				

		for i in range(ysize):
			for k in range(len(roottable[i])):
				if roottable[i][k]==1:
					self.circle1=Circle(self.canvas,margin+radius*k*2,2*margin+radius*i*2,radius-2,"black","circle1")
					self.circle1.createCircle()
				elif roottable[i][k]==-1:
					self.circle1=Circle(self.canvas,margin+radius*k*2,2*margin+radius*i*2,radius-2,"white","circle1")
					self.circle1.createCircle()

		self.master.after(50,self.update)
def main():
	win = tk.Tk()
	t = threading.Thread(target=socketserver)
	t.start()
	app = Application(master=win)
	app.mainloop()

if __name__ == "__main__":
	main()