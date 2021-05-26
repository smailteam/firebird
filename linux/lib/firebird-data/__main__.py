from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTreeView, QPushButton, QLineEdit, QMessageBox, QTextEdit, QGridLayout, QShortcut
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont
from extra import about_page,vinstance,sendi
from functools import partial
import PyQt5.QtGui as QtGui, PyQt5.QtCore as QtCore, xml.etree.ElementTree as ET
import os, sys, mail, time, getpass, sqlite3, requests, threading

class Var:
	def __init__(self):
		self.mdic={}
	def __add__(self,name,content):
		self.mdic.update({name:content})
	def __get__(self,name):
		return self.mdic[name]
	def __set__(self,name,content):
		self.mdic[name]=content

variable=Var()
variable.__add__('finish',False)
variable.__add__('rootdir',None)
variable.__add__('onstart',False)
variable.__add__('raw',False)
variable.__add__('theme','')

def log():
	conn.close()
	try:
		os.remove(variable.__get__('rootdir')+'/.firebird/user.db')
	except:
		pass
	try:
		os.remove(variable.__get__('rootdir')+'/.firebird/mails.xml')
	except:
		pass
	app.exit()



def connect():
	global conn,info,mails
	if (getpass.getuser()=='root')==False:
		variable.__set__('rootdir','/home/'+getpass.getuser())
		try:
			os.mkdir(variable.__get__('rootdir')+'.firebird')
		except:
			pass
		conn=sqlite3.connect(variable.__get__('rootdir')+'/.firebird/user.db')
		try:
			conn.execute('CREATE TABLE users(instance STRING,user STRING,password STRING)')
		except:
			pass
		info=conn.execute('SELECT * FROM users').fetchall()
		if os.path.isfile(variable.__get__('rootdir')+'/.firebird/mails.xml'):
			mails_raw=ET.fromstring(open(variable.__get__('rootdir')+'/.firebird/mails.xml','r').read())
			mails=[]
			for i in mails_raw:
				mails.append({'id':i.attrib['id'],'date':i.find('date').text,'box':i.find('box').text,'mail':i.find('sender').text})
	else:
		variable.__set__('rootdir','/root')
		try:
			os.mkdir(variable.__get__('rootdir')+'/.firebird')
		except:
			pass
		conn=sqlite3.connect(variable.__get__('rootdir')+'/.firebird/user.db')
		try:
			conn.execute('CREATE TABLE users(instance STRING,user STRING,password STRING)')
		except:
			pass
		info=conn.execute('SELECT * FROM users').fetchall()
		if os.path.isfile(variable.__get__('rootdir')+'/.firebird/mails.xml'):
			mails_raw=ET.fromstring(open(variable.__get__('rootdir')+'/.firebird/mails.xml','r').read())
			mails=[]
			for i in mails_raw:
				mails.append({'id':i.attrib['id'],'date':i.find('date').text,'box':i.find('box').text,'mail':i.find('sender').text})

connect()
count1=-1

@QtCore.pyqtSlot(QtCore.QModelIndex)
def onItemClicked(index):
	global count1
	print('SEL: '+str(index.row()))
	if index.row()==count1:
		dat=(tview.selectedIndexes()[0].data())
		print('Getting '+info[0][0]+'api/xmlmail.php?id='+dat)
		data=(variable.__get__('raw').get(dat,verify=False))
		popup=QWidget()
		popup.setWindowTitle(dat)
		popgrid=QGridLayout(popup)
		
		l1=QLabel('Sender: '+data['sender'],popup)
		l2=QLabel('Date  : '+data['date'],popup)
		l3=QLabel('Text  : '+data['data'],popup)
		b1=QPushButton('Close',popup)
		
		popgrid.addWidget(l1,1,1,1,1)
		popgrid.addWidget(l2,2,1,1,1)
		popgrid.addWidget(l3,3,1,1,1)
		popgrid.addWidget(b1,4,1,1,1)

		b1.clicked.connect(lambda: popup.close())

		popup.setStyleSheet(theme)
		popup.show()
		count1=-1
	else:
		count1=index.row()

def deleteThem():
	dat=tview.selectedIndexes()
	if len(dat)==0:
		pass
	else:
		r=variable.__get__('raw').delete(dat[2].data(),dat[0].data())
		itemModel.removeRow(count1)


app=QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon('/usr/share/firebird/icons/icon.ico'))
widget=QWidget()
widget.setWindowTitle('SMail Official Client')
widget.resize(700,400)
grid=QGridLayout(widget)
shortcut=QShortcut(QtGui.QKeySequence("Ctrl+A"), widget)

title=QLabel('Firebird',widget)
title.setFont(QFont('Verdana',15))
itemModel=QStandardItemModel()
itemModel.setHorizontalHeaderLabels(['ID','SMail','Box','Date'])
tview=QTreeView(widget)
tview.clicked.connect(onItemClicked)
tview.setGeometry(20, 50, 460, 300)
tview.setModel(itemModel)
tview.header().setDefaultSectionSize(200)
tview.setFont(QFont('Verdana',15))
reload=QPushButton('Reload', widget)
send=QPushButton('Send', widget)
logout=QPushButton('Logout', widget)
delete1=QPushButton('Delete', widget)

version=QPushButton('Instance Version')

close=QPushButton("Close",widget)
close.clicked.connect(lambda: widget.close())
infoLabel=QLabel("Welcome to Firebird 1.1 Beta 1")
grid.addWidget(title, 1, 0, 1, 3)
grid.addWidget(tview, 2, 0, 1, 3)
grid.addWidget(reload,3,0,1,1)
grid.addWidget(send,3,1,1,1)
grid.addWidget(logout,3,2,1,1)
grid.addWidget(delete1,4,0,1,1)
grid.addWidget(version,4,1,1,1)
grid.addWidget(close,4,2,1,1)
grid.addWidget(infoLabel,5,0,1,3)

variable.__set__('info',infoLabel)


try:
	try:
		os.mkdir(variable.__get__('rootdir')+'/.firebird/theme')
	except:
		pass
	theme=open(variable.__get__('rootdir')+'/.firebird/'+'theme/main.css','r').read()
except:
	theme=''

variable.__set__('theme',theme)
widget.setStyleSheet(theme)
widget.show()


def charge_th(reload):
	global count
	def charge_child():
		global mbox,finish,count
		if variable.__get__('raw'):
			pass
		else:
			variable.__set__('raw',mail.RawMail(info[0][0],info[0][1],info[0][2],verify=False))
		for i in range(0,count):
			try:
				itemModel.removeRow(0)
			except:
				break
		count=0
		mbox=variable.__get__('raw').mailbox(None)
		for i in mbox:
			count+=1
			itemModel.appendRow([QStandardItem(i['id']),QStandardItem(i['mail']),QStandardItem(i['box']),QStandardItem(i['date'])])
		ET.ElementTree(variable.__get__('raw').root).write(variable.__get__('rootdir')+'/.firebird/mails.xml')
		variable.__set__('finish',True)

	n=0
	th=threading.Thread(target=charge_child)
	th.start()
	while False==variable.__get__('finish'):
		time.sleep(0.2)
		if n==10:
			n=1
		else:
			n+=1
		infoLabel.setText('Loading '+'.'*n)
	infoLabel.setText('Loaded')
	variable.__set__('finish',False)
count=0

def charge(reload):
	th=threading.Thread(target=partial(charge_th,reload=reload))
	th.start()

def login():
	def login():
		if e1.text()=='' or e2.text()=='':
			infoLabel.setText('Please set a User and Password')
		elif '@' not in e1.text():
			infoLabel.setText('Please set the @ after the user')
		else:
			infoLabel.setText('Trying to login on {0} with user {1} \nPlease wait...'.format(e1.text().split('@')[1],e1.text()))
			try:
				try:
					variable.__set__('raw',mail.RawMail('https://'+e1.text().split('@')[1],e1.text(),e2.text(),verify=False))
					h='https'
				except mail.HttpResponseNot200Error as e:
					raise mail.HttpResponseNot200Error(str(e.args[0]))
				except:
					variable.__set__('raw',mail.RawMail('http://'+e1.text().split('@')[1],e1.text(),e2.text(),verify=False))
					h='http'
				sucess=True
			except mail.HttpResponseNot200Error as e:
				moreinfo='Incorrect user or password'
				QMessageBox.question(new,'Info','Incorrect user or password\n\n'+'Traceback: '+str(e),QMessageBox.Yes)
				sucess=False
			except Exception as e:
				moreinfo='You dont have internet or the server was offline'
				print(moreinfo)
				sucess=False
			if sucess:
				conn.execute('INSERT INTO users VALUES("'+h+'://'+e1.text().split('@')[1]+'","'+e1.text()+'","'+e2.text()+'")')
				conn.commit()
				QMessageBox.question(new,'Info','Succefully loged',QMessageBox.Yes)
				new.close()
				infoLabel.setText('Succefully Loged, loading messages')
				charge(False)
				infoLabel.setText('Succefully Loaded')
			else:
				infoLabel.setText(moreinfo)
	new=QWidget()
	new.setWindowTitle('Login')
	grid1=QGridLayout(new)
	l1=QLabel('Login',new)
	l1.setFont(QFont('Verdana',15))
	grid1.addWidget(l1,1,1,1,1)
	e1=QLineEdit('',new)
	e1.setPlaceholderText('user@example.com')
	grid1.addWidget(e1,2,1,1,1)
	e2=QLineEdit('',new)
	e2.setPlaceholderText('Password')
	e2.setEchoMode(QLineEdit.Password)
	grid1.addWidget(e2,3,1,1,1)
	b1=QPushButton('Login',new)
	grid1.addWidget(b1,4,1,1,1)
	b1.clicked.connect(login)
	new.setStyleSheet(theme)
	new.show()

if (len(info)==0)==False:
	try:
		variable.__set__('raw',mail.RawMail(info[0][0],info[0][1],info[0][2],verify=False))
		if variable.__get__('onstart'):
			mails=variable.__get__('raw').mailbox(None)
	except requests.exceptions.ConnectionError as e:
		QMessageBox.question(widget,'Error', 'You dont have internet, but you can see your database loged messages, but you not can see the content :) \n\nTraceback: '+str(e),QMessageBox.Yes)
		mails=''
	except mail.HttpResponseNot200Error as e:
		login()
		mails=''
	reload.clicked.connect(lambda:charge(True))
	logout.clicked.connect(log)
	send.clicked.connect(partial(sendi,var=variable))
	version.clicked.connect(partial(vinstance, var=variable,theme=theme))
	delete1.clicked.connect(deleteThem)
	for i in mails:
		count+=1
		itemModel.appendRow([QStandardItem(i['id']),QStandardItem(i['mail']),QStandardItem(i['box']),QStandardItem(i['date'])])
else:
	login()



sys.exit(app.exec_())
