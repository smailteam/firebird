import os
import sys
import getpass
import sqlite3
import requests
import mail
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
import xml.etree.ElementTree as ET
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTreeView, QPushButton, QLineEdit, QMessageBox, QTextEdit, QGridLayout, QShortcut

if getpass.getuser()=='root':
	raise ValueError('Unsopported user root')

def connect():
	global conn,info,mails
	try:
		os.mkdir('/home/'+getpass.getuser()+'/.firebird')
	except:
		pass
	conn=sqlite3.connect('/home/'+getpass.getuser()+'/.firebird/user.db')
	try:
		conn.execute('CREATE TABLE users(instance STRING,user STRING,password STRING)')
	except:
		pass
	info=conn.execute('SELECT * FROM users').fetchall()
	if os.path.isfile('/home/'+getpass.getuser()+'/.firebird/mails.xml'):
		mails_raw=ET.fromstring(open('/home/'+getpass.getuser()+'/.firebird/mails.xml','r').read())
		mails=[]
		for i in mails_raw:
			mails.append({'id':i.attrib['id'],'date':i.find('date').text,'box':i.find('box').text,'mail':i.find('sender').text})

def about_page():
	main=QWidget()
	mgrid=QGridLayout(main)
	l1=QLabel("FireBird SMail Client",main)
	iml=QLabel(main)
	l2=QLabel("Copyright 2021 X93\n Licensed into GPL V3",main)
	b1=QPushButton("Close",main)
	b1.clicked.connect(lambda:main.close())
	image=QtGui.QPixmap('talonflame.webp')
	iml.setPixmap(image)

	mgrid.setColumnStretch(0, 1)
	mgrid.setColumnStretch(3, 1)
	mgrid.setRowStretch(0, 1)
	mgrid.setRowStretch(3, 1)

	mgrid.addWidget(l1,1,1,1,1)
	mgrid.addWidget(iml,2,1,1,1)
	mgrid.addWidget(l2,3,1,1,1)
	mgrid.addWidget(b1,4,1,1,1)
	main.setStyleSheet(theme)
	main.show()



connect()
count1=-1

@QtCore.pyqtSlot(QtCore.QModelIndex)
def onItemClicked(index):
	global count1
	print('SEL: '+str(index.row()))
	if index.row()==count1:
		dat=(tview.selectedIndexes()[0].data())
		print('Getting '+info[0][0]+'api/xmlmail.php?id='+dat)
		data=(raw.get(dat,verify=False))
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
	print(dat[0].data())
	if len(dat)==0:
		pass
	else:
		r=raw.delete(dat[2].data(),dat[0].data())
		itemModel.removeRow(count1)
	print(r.text)

def vinstance():
	main=QWidget()
	mgrid=QGridLayout(main)
	
	l1=QLabel('Instance Version: '+raw.version())
	b1=QPushButton('Close')
	b1.clicked.connect(lambda: main.close())
	
	mgrid.addWidget(l1,1,1,1,1)
	mgrid.addWidget(b1,2,1,1,1)
	
	main.setStyleSheet(theme)
	main.show()


app=QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon('/usr/share/firebird/icons/icon.ico'))
widget=QWidget()
widget.setWindowTitle('SMail Official Client')
widget.resize(700,400)
grid=QGridLayout(widget)

shortcut=QShortcut(QtGui.QKeySequence("Ctrl+A"), widget)
shortcut.activated.connect(about_page)

title=QLabel('Firebird',widget)
title.setFont(QFont('Verdana',15))

itemModel=QStandardItemModel()
itemModel.setHorizontalHeaderLabels(['ID','SMail','Box','Date'])

tview=QTreeView(widget)
tview.clicked.connect(onItemClicked)
tview.setGeometry(20, 50, 460, 300)
tview.setModel(itemModel)
tview.header().setDefaultSectionSize(150)
tview.setFont(QFont('Verdana',15))

reload=QPushButton('Reload', widget)

send=QPushButton('Send', widget)

logout=QPushButton('Logout', widget)

delete1=QPushButton('Delete', widget)
delete1.clicked.connect(deleteThem)

version=QPushButton('Instance Version')
version.clicked.connect(vinstance)

close=QPushButton("Close",widget)
close.clicked.connect(lambda: widget.close())

grid.addWidget(title, 1, 0, 1, 3)
grid.addWidget(tview, 2, 0, 1, 3)
grid.addWidget(reload,3,0,1,1)
grid.addWidget(send,3,1,1,1)
grid.addWidget(logout,3,2,1,1)
grid.addWidget(delete1,4,0,1,1)
grid.addWidget(version,4,1,1,1)
grid.addWidget(close,4,2,1,1)

try:
	try:
		os.mkdir('/home/'+getpass.getuser()+'/.firebird/theme')
	except:
		pass
	theme=open('/home/'+getpass.getuser()+'/.firebird/'+'theme/main.css','r').read()
except:
	theme=''

widgets=[logout,send,reload]
for i in widgets:
	i.setFont(QFont('Verdana',10))

widget.setStyleSheet(theme)
widget.show()


def charge(reload):
	global count,raw
	if raw:
		pass
	else:
		raw=mail.RawMail(info[0][0],info[0][1],info[0][2],verify=False)
	for i in range(0,count):
		try:
			itemModel.removeRow(0)
		except:
			break
	count=0
	mbox=raw.mailbox(None)
	for i in mbox:
		count+=1
		itemModel.appendRow([QStandardItem(i['id']),QStandardItem(i['mail']),QStandardItem(i['box']),QStandardItem(i['date'])])
	ET.ElementTree(raw.root).write('/home/'+getpass.getuser()+'/.firebird/mails.xml')

	if reload:
		QMessageBox.question(widget,'INFO','Reloaded',QMessageBox.Yes)

count=0

def login():
	def login():
		global raw
		try:
			raw=mail.RawMail('https://'+e1.text().split('@')[1],e1.text(),e2.text(),verify=False)
			conn.execute('INSERT INTO users VALUES("https://'+e1.text().split('@')[1]+'","'+e1.text()+'","'+e2.text()+'")')
			conn.commit()
			QMessageBox.question(new,'Info','Succefully loged',QMessageBox.Yes)
			new.close()
			charge(False)
		except mail.HttpResponseNot200Error as e:
			QMessageBox.question(new,'Info','Incorrect user or password\n\n'+'Traceback: '+str(e),QMessageBox.Yes)
	new=QWidget()
	new.setWindowTitle('Login')
	grid1=QGridLayout(new)
	l1=QLabel('Login',new)
	l1.setFont(QFont('Verdana',15))
	grid1.addWidget(l1,1,1,1,1)
	e1=QLineEdit('',new)
	e1.setPlaceholderText('User')
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
		raw=mail.RawMail(info[0][0],info[0][1],info[0][2],verify=False)
		mails=raw.mailbox(None)
	except requests.exceptions.ConnectionError as e:
		QMessageBox.question(widget,'Error', 'You dont have internet, but you can see your database loged messages, but you not can see the content :) \n\nTraceback: '+str(e),QMessageBox.Yes)
		mails=''
	except mail.HttpResponseNot200Error as e:
		login()
		mails=''
	for i in mails:
		count+=1
		itemModel.appendRow([QStandardItem(i['id']),QStandardItem(i['mail']),QStandardItem(i['box']),QStandardItem(i['date'])])
else:
	login()

def log():
	conn.close()
	os.remove('/home/'+getpass.getuser()+'/.firebird/user.db')
	os.remove('/home/'+getpass.getuser()+'/.firebird/mails.xml')
	app.exit()

def sendi():
	global top
	def send_f():
		raw.send(e1.text(),e2.toPlainText())
		top.close()
	top=QWidget()
	top.setStyleSheet(theme)
	top.setWindowTitle('Send Message')
	grid1=QGridLayout(top)

	l1=QLabel('Send Message',top)
	l1.setFont(QFont('Verdana',16))
	
	e1=QLineEdit(top)
	e1.setPlaceholderText('SMail')

	e2=QTextEdit(top)
	e2.setPlaceholderText('Contenido')

	b1=QPushButton('Send',top)
	b1.clicked.connect(send_f)

	grid1.addWidget(l1,1,1,1,1)
	grid1.addWidget(e1,2,1,1,1)
	grid1.addWidget(e2,3,1,1,1)
	grid1.addWidget(b1,4,1,1,1)
	top.show()

reload.clicked.connect(lambda:charge(True))
logout.clicked.connect(log)
send.clicked.connect(sendi)

sys.exit(app.exec_())
