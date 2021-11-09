"""
Software Name : SQL Table Viewer


Description : This is a Simple Software creating using the PyQt5 (version 5) python framework for 
			  Software development, that will allow us to see the data of a 
     		  SQL Database (local file, of extension .db) in graphical and tabular form.
         

Code Contributed by group of 3 : 1) Bhumika Rawat, class 12th (B), Roll no : 12
								 2) Mohit Devli, class 12th (A), Roll no : 21
								 3) Mayank Bhatt, class 12th (a), Roll no : 19
"""

#import required modules
import sys
from PyQt5.QtWidgets import *
import sqlite3 as sql


#Main class of Application
class Main():
    
    #function to setup our App
	def windowSetup(self):
		#creating a app
		self.app = QApplication(sys.argv)
		
		#creatig a App Window
		self.startingWin = QWidget()

		#set window title
		self.startingWin.setWindowTitle("SQL Table Viewer")

		#set geomety of window, i.e, postion and size
		self.startingWin.setGeometry(self.app.desktop().screen().width()/4, self.app.desktop().screen().height()/4, self.app.desktop().screen().width()/2, self.app.desktop().screen().height()/6)
		"""
		setGeometry() function's arguments are - (position-x, position-y, width, height)
    	"""
		
		#verticle BoxLayout
		vBoxLayout = QVBoxLayout(self.startingWin)
		
		
		#1st Horizontal BoxLayout
		hBoxLayout_1 = QHBoxLayout(self.startingWin)
		
		#2nd Horizontal BoxLayout
		hBoxLayout_2 = QHBoxLayout(self.startingWin)		

		#Label Widget for Text "Enter the path of your SQL Database"
		filePathLabel = QLabel(self.startingWin)
		filePathLabel.setText("Enter the path of your SQL Database")

		#set "filePathLabel" i.e, our Label Widget into  hBoxLayout_1 i.e, 1st Horizontal Boxlayout
		hBoxLayout_1.addWidget(filePathLabel)

		#create a text Input widget i.e, QLineEdit Widget
		self.filePath = QLineEdit(self.startingWin)
		hBoxLayout_1.addWidget(self.filePath)
		
		#create a button that will allow us to choose database file
		self.fileChooseButton = QPushButton(self.startingWin)
		
  		#set label of button to text "Choose File"
		self.fileChooseButton.setText("Choose File")
		
  		#connect or bind a function ChooseFile() that will execute when button is pressed
		self.fileChooseButton.clicked.connect(self.ChooseFile)

		hBoxLayout_1.addWidget(self.fileChooseButton)
		
		#Create a label that says "Enter tthe table Name: "
		self.Tablelabel = QLabel(self.startingWin)
		self.Tablelabel.setText("Enter tthe table Name: ")
		hBoxLayout_2.addWidget(self.Tablelabel)
		
		#Create a text input that will take the name of Table which will being open
		self.tableName = QLineEdit(self.startingWin)
		self.tableName.setText("MyTable") #---------------
		hBoxLayout_2.addWidget(self.tableName)
		
		#Create a button that will show the Content of Databsae
		self.startButton = QPushButton(self.startingWin)
		self.startButton.setText("Open DataBase")
		self.startButton.clicked.connect(self.DBMSWindow)
		
		#Add the 1st and 2nd Horizontal Layout in our main Verticle layout
		vBoxLayout.addLayout(hBoxLayout_1)
		vBoxLayout.addLayout(hBoxLayout_2)
  
		#add startButton in verticle Boxlayout as a widget
		vBoxLayout.addWidget(self.startButton)
  
		"""
		"startButton" widget added to "vBoxLayout" after "hBoxLayout_1" and "hBoxLayout_2"
		as we want to display the startButton after two Horizontal Layouts.
		"""

		#set a main parent layout i.e, vBoxLayout to our main window
		self.startingWin.setLayout(vBoxLayout)
  
		#show our app window
		self.startingWin.show()
		#Terminate the app when Window is being closed.
		sys.exit(self.app.exec_())    
		
	
	#Function is called when we clicked "fileChooseButton"
	def ChooseFile(self):
		#create a file Dialogbox widget to choose a file from system
		self.fileDialog = QFileDialog(self.startingWin)
		fileName=self.fileDialog.getOpenFileName(self.fileDialog, "Choose SQL DataBase File", "","Database (*.db)")
  
		"""
		getOpenFileName() function returns a tuple having two elements 1) the path of the file that will be choosed
		user and 2) extention and type of file, here is 'Database (*.db)'.

		arguments : (fileDialog widget name, Title of Dialog widget, directory, filter i.e, filetype)
		here fitler is set to choose the only file end with extension .db
		"""	
        
		self.databaseFileName=fileName[0]
		"""
		fileName is tuple in which 1st element is database file name so we store the name or path 
		of the Database file in variable "databaseFileName"
		"""
  
		#set the "filePath" textinput's label as sama as the path of file which is stored in variable "databaseFileName"
		self.filePath.setText(self.databaseFileName)

	
	def DBMSWindow(self):
		"""
		Function executes when "startButton" clicks..
		FUnction will open a new window which will show a table representing the data store inside
			the database.
  		"""
     
		#try to connect the database with our Software
		try:
			
			#established a connection with sql database with filename stored in variable "databaseFileName"
			self.connection = sql.connect(self.databaseFileName)

			#creating a database cursor that will help us to crawl data from our database
			self.crsr = self.connection.cursor()
			
			#execute a SQL Query that will select all the 
			self.database = self.crsr.execute("""SELECT * FROM """+str(self.tableName.text()))
			colscount=0
			
			for row in self.database:
				#this loop will give the data in tuple form of each row in each iteration
				colscount=len(row) #count total no of column

				"""
				"row" variable has tuple value for example a database has various rows in SQL table
				so in each iteration "row" variable contain the data of each row.

				data-format of "row" variable: 
    				('column-1', 'column-2', 'column-3', column-4) 
        		i.e, a tuple.
          
          
				Logic Applied for count total column present in database.
    
				 	"Total number of column is equal to the total values in a row."
      
    			"""
       
			HeaderLabel=[]  #the list will contain the Table Header values
			"""
			for example if database is like
   			"""
		
			for l in range(colscount):
				#SQL query to select all Table Header values from database
				self.crsr.execute("PRAGMA table_info("+self.tableName.text()+")")
				HeaderLabel.append(self.crsr.fetchall()[l][1])
		
			
			#Creating a other new window that will show a Table
			self.DBMSWin = QWidget()
			#Setting Window title as "DataBase Managment System"
			self.DBMSWin.setWindowTitle("DataBase Managment System")
			self.DBMSWin.setGeometry(0,0,self.app.desktop().size().width(), self.app.desktop().size().height())
			
			#Creating a Table Widget that will contain the data from database
			self.tableWidget = QTableWidget(self.DBMSWin)
			self.tableWidget.setGeometry(0,0,self.DBMSWin.size().width(), self.DBMSWin.size().height()-300)
			
			#SQL query to select all data from database
			self.crsr.execute("""SELECT * FROM """+self.tableName.text())
			#variable contain total count of rows
			rowcount=len(self.crsr.fetchall())

			"""
			fetchall() function returns the all data fetch by SQL Cursor
   			"""

			#set total number of rows in table widget
			self.tableWidget.setRowCount(rowcount)
   			#set total number of columns in table widget
			self.tableWidget.setColumnCount(colscount)
			
			database = self.crsr.execute("""SELECT * FROM """+str(self.tableName.text()))
			
			cor =[]
			values=[]
	
			"""
		list "cor" will contain a list of cordinates or postion if each entry in database.
		each cordinates will be in tuple form, for example let assume we hava a database 
		having 3 colums and 4 rows then elements in list "cor" will as:
		
			[(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2), (3, 0), (3, 1), (3, 2)]

		  1st Column    2nd Column  3rd Column
			(0, 0), 	  (0, 1), 	 (0, 2)  : cordinates of each elements in 1st row
			(1, 0), 	  (1, 1),    (1, 2)  : cordinates of each elements in 2nd row
			(2, 0),       (2, 1),    (2, 2)  : cordinates of each elements in 3rd row
			(3, 0),       (3, 1),    (3, 2)  : cordinates of each elements in 4th row
        
        --------------------------------------------------------------------------------------
        
		list "values" will contain values or data of each entry in database for example, for
		same case of databse having 3 columns and 4 rows then its elements will be like:

			["data of (0, 0)","data of (0, 1)","data of (0, 2)",
   			 "data of (1, 0)","data of (1, 1)","data of (1, 2)",
       		 "data of (2, 0)","data of (2, 1)","data of (2, 2)",
          	 "data of (3, 0)","data of (2, 1)","data of (2, 2)"]
      
			"""
   
			for rows in database:
				for i in range(colscount):
					values.append(rows[i])
			
			for i in range(rowcount):
				for j in range(colscount):
					cor.append((i,j))
	
			#in each iteration this will set the value from database to table Widget
			for i in range(rowcount*colscount):
					self.tableWidget.setItem(cor[i][0],cor[i][1],QTableWidgetItem(str(values[i])))
			
			#Set Table Header values
			self.tableWidget.setHorizontalHeaderLabels(HeaderLabel)
			
			self.tableWidget.horizontalHeader().setStretchLastSection(True)
			self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
			
		
			#Closing the starting win before showing the databse table window 
			self.startingWin.close()	
			#show the Database table window
			self.DBMSWin.show()
		
		#execute if some error occurs while fetching data from database
		except Exception as e:
			"""
			here variable "e" will contain the information about the error.
 		  	"""

			#Creating A Popup Messagebox or Alertbox which will display the info about error
			errorDialog = QMessageBox(self.startingWin)
			#set the icon of dialog bos as Critical, which let user know the error is serious
			errorDialog.setIcon(QMessageBox.Critical)
			#set the title of Message Dialog Box
			errorDialog.setWindowTitle("Error while Connection database file.")
			#set content of Message Dialog Box
			errorDialog.setText("Please check the file path or confirm the database must be SQL.\n"+str(e))
			#show the error Dialog Box
   			errorDialog.show()

#Execute the Program
if __name__=="__main__":
	Main().windowSetup()
