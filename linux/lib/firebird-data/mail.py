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

import xml.etree.ElementTree as ET
import requests
import sqlite3
import json
import time
import sys
import re
import os

class HttpResponseNot200Error(Exception):
	pass
class RawMail:
	def __init__(self,instance,user,password,verify=True):
		self.session=requests.session()
		self.instance=instance
		r=self.session.post(instance+'api/login.php',data={'mail':user,'password':password},allow_redirects=False,verify=verify)
		print(r.text)
		if (json.loads(r.text)['code']==200)==False:
			raise HttpResponseNot200Error('Unknow Error in the login')
		else:
			pass
	def get(self,id,verify=True):
		r=self.session.get(self.instance+'api/xmlmail.php?id='+id,verify=verify)
		fromstr=ET.fromstring(r.text)
		return {'data':fromstr.find('data').text,'sender':fromstr.find('sender').text,'date':fromstr.find('date').text}
	def send(self,reiciver,content,verify=True):
		if str(type(reiciver.split(',')))=="<class 'list'>":
			for i in reiciver.split(','):
				r=self.session.post(self.instance+'api/send.php',data={'mail_r':i,'content':content},allow_redirects=True,verify=verify)
				if (json.loads(r.text)['code']=='200')==False:
					print(r.text)
					#raise HttpResponseNot200Error('Unknow Error in the send')
				else:
					return 200
		else:
			try:
				r=self.session.post(reiciver.split('@')[1]+'api/send.php',data={'mail_r':reiciver,'content':content},allow_redirects=True,verify=verify)
			except IndexError:
				r=self.session.post(self.instance+'api/send.php',data={'mail_r':reiciver,'content':content},allow_redirects=True,verify=verify)
			if (r.status_code=='200')==False:
				print(r)
				#raise HttpResponseNot200Error('Unknow Error in the send ')
			else:
				print('Succefully sended')
	def mailbox(self,mbox,verify=True):
		if mbox==None:
			petition=self.session.get(self.instance+'api/raw_mails.php').text
			self.root=ET.fromstring(petition)
			list1=[]
			try:
				for i in self.root:
					list1.append({'id':i.attrib['id'],'date':i.find('date').text,'box':i.find('box').text,'mail':i.find('sender').text})
			except:
				list1.append({'id':'0','date':time.strftime('%h:%m:%s %d/%m/%Y'),'box':'infomail','mail':'none'})
			return list1
		else:
			self.root=ET.fromstring(self.session.get(self.instance+'mailbox/raw_mails.php?box='+mbox).text)
			list1=[]
			for i in self.root:
				list1.append({'id':i.attrib['id'],'date':i.find('date').text,'box':i.find('box').text,'mail':i.find('sender').text})
			return list1
	def change_password(self,old,new,verify=True):
		r=self.session.post(self.instance+'mailbox/change_p.php',data={'old':old,'new':new})
		if ('login.html' in r.url)==False:
			print('Error')
		else:
			return 200
	def delete(self,box,id):
		r=self.session.get(self.instance+'api/xmlmail.php?box={0}&delthem={1}'.format(box,id))
		return r
	def version(self):
		r=self.session.get(self.instance+'VERSION')
		return r.text


raw=RawMail('https://reisub.nsupdate.info/smail/','borisdaniel','test')
print(raw.send('borisdaniel','hola'))
