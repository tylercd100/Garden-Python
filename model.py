#!/usr/bin/env python
import MySQLdb

class Model:
	def fetch(self):
		self.getColumns()
		self.cur.execute("SELECT "+ self.getColumnString() +" FROM "+self.table+" WHERE id = %s ;",(self.id,))
		results = self.cur.fetchall()

		i = 0;
		for row in results:
			i = 0;
			for val in row:
				setattr(self,self.columns[i],val)
				i = i + 1

	def save(self,cols = []):
		self.getColumns()
		if(len(cols) <= 0):
			cols = self.columns

		values = []
		heads = ""
		i=0
		for col in cols:
			if(i > 0):
				heads = heads + ', ' + col + ' = %s'
			else:
				heads = heads + col + ' = %s'
			i = i + 1
			values.append(getattr(self,col))

		self.cur.execute("UPDATE "+self.table+" SET "+heads+" WHERE id="+str(self.id)+";",values)
		results = self.cur.fetchall()

		i = 0;
		for row in results:
			i = 0;
			for val in row:
				setattr(self,self.columns[i],val)
				i = i + 1

	def saveNew(self,cols = []):
		self.getColumns()
		if(len(cols) <= 0):
			cols = self.columns

		values = []
		heads = ""
		vals = ""
		i=0
		for col in cols:
			if(i > 0):
				vals = vals + ', ' + '%s'
				heads = heads + ', ' + col
			else:
				vals = vals + '%s'
				heads = heads + col
			i = i + 1
			values.append(getattr(self,col))

		self.cur.execute("INSERT INTO "+self.table+" ("+heads+") VALUES ("+vals+");",values)
		results = self.cur.fetchall()

		i = 0;
		for row in results:
			i = 0;
			for val in row:
				setattr(self,self.columns[i],val)
				i = i + 1

	def getColumns(self):
		if not hasattr(self,'columns'):
			self.columns = [] 
			self.cur.execute("SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA`='garden' AND `TABLE_NAME`='"+self.table+"';")
			results = self.cur.fetchall()
			for result in results:
				for r in result:
					self.columns.append(r);

	def getColumnString(self,cols = []):
		if(len(cols) <= 0):
			cols = self.columns
		select = ''
		i=0
		for col in cols:
			if(i > 0):
				select = select + ', ' + col
			else:
				select = select + col 
			i = i + 1

		return select
