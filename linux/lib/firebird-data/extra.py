#
#	Copyright 2021 Boris Daniel <borisdaniel@reisub.nsupdate.info/smail/> on SMail
#
#	This program is free software; you
#	can redistribute it and/or modify
#	it under the terms of the GNU General
#	Public License as the published by
#	the Free Software Fundation; either
#	version 3 of the License, or (at
#	your option) any later version.
#
#	This program is distributed in the
#	hope that it will be useful, but
#	WITHOUT ANY WARRANTY; without even
#	the implied in warranty of
#	MERCHANTABILITY or FITNESS FOR A
#	PARTICULAR PURPOSE. See the GNU
#	General Public License for more details.
#
#	You should have received a copy of
#	the GNU General Public License along
#	with this program; if not, write to
#	the Free Software Fundation, Inc., 51
#	Franklin Street, Fifth Floor, Boston
#	MA 02110-1301, USA.

from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout, QLineEdit, QTextEdit
from PyQt5.QtGui import QFont
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

def vinstance(raw,theme,var):
	main=QWidget()
	mgrid=QGridLayout(main)
	var.__get__('info').setText('Getting version')
	
	l1=QLabel('Instance Version: '+var.__get__('raw').version())
	b1=QPushButton('Close')
	b1.clicked.connect(lambda: main.close())
	
	mgrid.addWidget(l1,1,1,1,1)
	mgrid.addWidget(b1,2,1,1,1)
	var.__get__('info').setText('Sucess')
	
	main.setStyleSheet(theme)
	main.show()

def sendi(var):
	def send_f():
		var.__get__('raw').send(e1.text(),e2.toPlainText())
		top.close()
	top=QWidget()
	top.setStyleSheet(var.__get__('theme'))
	top.setWindowTitle('Send Message')
	grid1=QGridLayout(top)
	l1=QLabel('Send Message',top)
	l1.setFont(QFont('Verdana',16))
	e1=QLineEdit(top)
	e1.setPlaceholderText('user@example.com')
	e2=QTextEdit(top)
	e2.setPlaceholderText('content')
	b1=QPushButton('Send',top)
	b1.clicked.connect(send_f)
	grid1.addWidget(l1,1,1,1,1)
	grid1.addWidget(e1,2,1,1,1)
	grid1.addWidget(e2,3,1,1,1)
	grid1.addWidget(b1,4,1,1,1)
	top.show()
