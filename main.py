import sys
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QFormLayout, QGridLayout, QApplication, QMessageBox, QTableWidget, QHeaderView, QTableWidgetItem, QWidget, QPushButton, QFileDialog, QLabel, QMessageBox, QLineEdit
import sqlite3 as sql
from PyQt5.QtCore import pyqtSlot

class Main():
	
	def windowSetup(self):
		self.app = QApplication(sys.argv)
		
		#Starting Window
		self.startingWin = QWidget()
		self.startingWin.setWindowTitle("Open DataBase.")
		self.startingWin.setGeometry(self.app.desktop().screen().width()/4, self.app.desktop().screen().height()/4, self.app.desktop().screen().width()/2, self.app.desktop().screen().height()/2)
		
		
		#VBoxLayout
		vboxLayout = QHBoxLayout(self.startingWin)
		
		
		#HBoxLayout
		startingScreenBoxLayout = QHBoxLayout(self.startingWin)
		startingScreenBoxLayout.setContentsMargins(10,0,10,self.startingWin.size().height()-100)
		
		startingScreenOtherBoxLayout = QHBoxLayout(self.startingWin)
		startingScreenOtherBoxLayout.setContentsMargins(10,0,10,self.startingWin.size().height()-100)
		
	
		
		vboxLayout.addLayout(startingScreenBoxLayout)
		vboxLayout.addLayout(startingScreenOtherBoxLayout)
	
	
		filePathLabel = QLabel(self.startingWin)
		filePathLabel.setText("File Path")
		startingScreenBoxLayout.addWidget(filePathLabel)


		self.filePathEditText = QLineEdit(self.startingWin)
		startingScreenBoxLayout.addWidget(self.filePathEditText)
		
		
		self.fileChooseButton = QPushButton(self.startingWin)
		self.fileChooseButton.setText("Choose File")
		self.fileChooseButton.clicked.connect(self.ChooseFile)
		startingScreenBoxLayout.addWidget(self.fileChooseButton)
		
		
		self.Tablelabel = QLabel(self.startingWin)
		self.Tablelabel.setText("Enter tthe table Name: ")
		startingScreenOtherBoxLayout.addWidget(self.Tablelabel)
		
		self.tableName = QLineEdit(self.startingWin)
		self.tableName.move(self.startingWin.size().width()/2-60, self.startingWin.size().height()/2-50)
		self.tableName.setText("MyTable")
		startingScreenOtherBoxLayout.addWidget(self.tableName)
		
	
		self.startButton = QPushButton(self.startingWin)
		self.startButton.setText("Open DataBase")
		self.startButton.move(self.startingWin.size().width()/2-60, self.startingWin.size().height()/2)
		self.startButton.clicked.connect(self.DBMSWindow)


		self.startingWin.setLayout(vboxLayout)
		self.startingWin.setMaximumSize(self.app.desktop().screen().width()/2, self.app.desktop().screen().height()/2)
		self.startingWin.show()
		
		sys.exit(self.app.exec_())    
		
	
	
	def ChooseFile(self):
		self.fileDialog = QFileDialog(self.startingWin)
		fileName=self.fileDialog.getOpenFileName(self.fileDialog, "Choose SQL DataBase File", "", "Database (*.db)")
		self.databaseFileName=fileName[0]
		self.filePathEditText.setText(self.databaseFileName)
		
	def DBMSWindow(self):
		#DataBase Connectivity
	
		try:
			self.connection = sql.connect(self.databaseFileName)
			self.crsr = self.connection.cursor()
			
			self.database = self.crsr.execute("""SELECT * FROM """+str(self.tableName.text()))
			colscount=0
			
			for row in self.database:
				colscount=len(row)
			
			
			HeaderLabel=[]
		
			for l in range(colscount):
				self.crsr.execute("PRAGMA table_info("+self.tableName.text()+")")
				HeaderLabel.append(self.crsr.fetchall()[l][1])
		
			
			
			self.DBMSWin = QWidget()
			self.DBMSWin.setWindowTitle("DataBase Managment System")
			self.DBMSWin.setGeometry(0,0,self.app.desktop().size().width(), self.app.desktop().size().height())
			
			self.tableWidget = QTableWidget(self.DBMSWin)
			self.tableWidget.setGeometry(0,0,self.DBMSWin.size().width(), self.DBMSWin.size().height()-300)
			
			self.crsr.execute("""SELECT * FROM """+self.tableName.text())
			
			rowcount=len(self.crsr.fetchall())
		
			self.tableWidget.setRowCount(rowcount)
			self.tableWidget.setColumnCount(colscount)
			
			database = self.crsr.execute("""SELECT * FROM """+str(self.tableName.text()))
			
			cor =[]
			values=[]
			for rows in database:
				for i in range(colscount):
					values.append(rows[i])
			
			for i in range(rowcount):
				for j in range(colscount):
					cor.append((i,j))
	
			
			for i in range(rowcount*colscount):
					self.tableWidget.setItem(cor[i][0],cor[i][1],QTableWidgetItem(str(values[i])))
			
			
			self.tableWidget.setHorizontalHeaderLabels(HeaderLabel)
			
			self.tableWidget.horizontalHeader().setStretchLastSection(True)
			self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
			
		
			
			self.startingWin.close()	
			self.DBMSWin.show()
			
		except Exception as e:
			errorDialog = QMessageBox(self.startingWin)
			errorDialog.setIcon(QMessageBox.Critical)
			errorDialog.setWindowTitle("Error while Connection database file.")
			errorDialog.setText("Please check the file path or confirm the database must be SQL.\n"+str(e))
			errorDialog.show()
	
		

	
if __name__=="__main__":
	Main().windowSetup()
