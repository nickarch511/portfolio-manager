import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel, QPushButton, QLineEdit, QRadioButton, QGroupBox
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QHBoxLayout, QVBoxLayout, QPlainTextEdit
from PyQt5.QtGui import QPixmap, QFont
from portfolioQuery import Portfolio

'''
This file contains the class and main function that runs the Graphical User 
Interface (GUI). This GUI uses the PyQt5 module and connects with the Portfolio
class through an instance variable defined as self.portfolio in the __init__ method
of the Gui class.

This class also deals with the interactive side of things (i.e. what happens when
a user clicks the add button, etc.) 

'''

class Gui(QWidget):
    HEIGHT = 500
    WIDTH = 1000

    def __init__(self):
        super().__init__()
        self.drawGui()
        self.portfolio = None

    def drawGui(self):
        self.setWindowTitle("Portfolio Manager")
        centerpoint = QDesktopWidget().availableGeometry().center()
        self.setGeometry(int(centerpoint.x()/4),int(centerpoint.y()/2),self.WIDTH,self.HEIGHT)
        self.layout = QVBoxLayout()
        self.inner_layout = QHBoxLayout()
        self.leftVertLayout = QVBoxLayout()
        self.rightVertLayout = QVBoxLayout()
        self.leftHAddLayout = QHBoxLayout()
        self.leftHAmountLayout = QHBoxLayout()

        self.addBtn = QPushButton("Add")
        self.assetLineEdit = QLineEdit()
        self.assetLineEdit.setPlaceholderText("Enter comma-delineated assets of form: APPL, AMD, ...")
    
        self.unlimitedRadioBtn = QRadioButton("Unlimited")
        self.longRadioBtn = QRadioButton("Long")
        self.computePortfolioBtn = QPushButton("Compute Portfolio") # Included in bottom-right

        self.amountLbl = QLineEdit("Amount")
        self.amountLbl.setReadOnly(True)
        self.amountInputLbl = QLineEdit()
        self.amountInputLbl.setPlaceholderText("Enter amount here")
        self.amountLbl.setMaximumWidth(75)
        self.numAssetsLbl = QLineEdit("X Total Assets") # Included in top-right
        self.numAssetsLbl.setReadOnly(True)
        self.assetListLbl = QLineEdit() # Included in top-right
        self.assetListLbl.setPlaceholderText("Assets will appear here when added")
        self.assetListLbl.setReadOnly(True) 

        # Make widgets for computer-picked long portfolio
        self.assetNumInputLabel = QLineEdit() # 
        self.assetNumInputLabel.setPlaceholderText("Enter number of assets")
        self.randomBtn = QPushButton("Get computer-selected portfolio")
        self.randomBtn.clicked.connect(self.randomBtnClicked)
        self.randomizedPortfolioLayout = QHBoxLayout()
        self.randomizedPortfolioLayout.addWidget(self.randomBtn)
        self.randomizedPortfolioLayout.addWidget(self.assetNumInputLabel)
        self.randomizedGroupBox = QGroupBox("Let the computer pick your assets (takes a while)")
        self.randomizedGroupBox.setLayout(self.randomizedPortfolioLayout)

        self.leftHAmountLayout.addWidget(self.amountLbl)
        self.leftHAmountLayout.addWidget(self.amountInputLbl)

        self.leftHAddLayout.addWidget(self.assetLineEdit)
        self.leftHAddLayout.addWidget(self.addBtn)

        # Make the left side of screen
        self.leftVertLayout.addLayout(self.leftHAddLayout)
        self.leftVertLayout.addWidget(self.unlimitedRadioBtn)
        self.leftVertLayout.addWidget(self.longRadioBtn)
        self.leftVertLayout.addLayout(self.leftHAmountLayout)
        self.leftVertLayout.addWidget(self.randomizedGroupBox)
        self.leftVertLayout.addStretch(1)
        
        # Make the right side of screen
        self.rightVertLayout.addWidget(self.numAssetsLbl)
        self.rightVertLayout.addWidget(self.assetListLbl)
        self.rightVertLayout.addWidget(self.computePortfolioBtn)
        self.rightVertLayout.addStretch(1)

        # Add the left and right sides of screen to the layout
        self.inner_layout.addLayout(self.leftVertLayout)
        self.inner_layout.addLayout(self.rightVertLayout)
        
        # Add inner horizontal layout to outer vertical layout
        self.layout.addLayout(self.inner_layout)
        
        # Add output box to layout
        self.output = QPlainTextEdit("")
        self.output.setReadOnly(True)
        self.output.setPlaceholderText("Portfolio allocations will appear here.")
        self.output.setFont(QFont("Arial", 25))
        self.layout.addWidget(self.output)


        
        # set the layout
        self.setLayout(self.layout)

        # Set up action listeners for buttons and other widgets
        self.computePortfolioBtn.clicked.connect(self.portfolioBtnClicked)
        self.addBtn.clicked.connect(self.addBtnClicked)

        self.show()

    def portfolioBtnClicked(self):
        # First get the amount
        if not self.portfolio is None:
            print("The portfolio type is {}".format(self.portfolio.portfolioType))
            # get amount from amountInputLbl
            try:
                text = "".join(filter(str.isalnum, self.amountInputLbl.text()))
                self.portfolio.amount = float(text)
                print("The amount is {}".format(self.portfolio.amount))
            except:
                print("Error occurred. Enter amount without any special characters.")

        # Get the toggled radio button and calculate corresponding portfolio
        result = ""
        if self.unlimitedRadioBtn.isChecked():
            if not self.portfolio is None: 
                self.portfolio.portfolioType = Portfolio.UNLIMITED_PORTFOLIO
                if self.portfolio.num_stocks > 1:
                    result = self.portfolio.getTangentPortfolio()
                else:
                    result = "Error. The number of stocks added is less than 2."
        elif self.longRadioBtn.isChecked():
            if not self.portfolio is None: 
                self.portfolio.portfolioType = Portfolio.LONG_PORTFOLIO
                if self.portfolio.num_stocks > 1:
                    result = self.portfolio.getLongPortfolio()
                else:
                    result = "Error. The number of stocks added is less than 2."

        self.output.document().setPlainText(str(result))
        
        

    def addBtnClicked(self):
        text = self.assetLineEdit.text()
        assets = text.split(",")
        self.assetLineEdit.setText("")
        if self.portfolio is None:
            self.portfolio = Portfolio(assets)
        else: self.portfolio.add_stocks(assets)
        self.assetListLbl.setText(str(self.portfolio))

        # Edit label to reflect number of stocks
        self.numAssetsLbl.setText(str(self.portfolio.num_stocks) + " Total Assets")

    def randomBtnClicked(self):
        try: numAssets = int(self.assetNumInputLabel.text())
        except: return
        if not self.portfolio: self.portfolio = Portfolio([])
        result = self.portfolio.pickLongPortfolio(numAssets)
        self.assetListLbl.setText(str(self.portfolio))

        # Edit label to reflect number of stocks
        self.numAssetsLbl.setText(str(self.portfolio.num_stocks) + " Total Assets")
        self.output.document().setPlainText(str(result))

def main():
    app = QApplication(sys.argv)
    gui = Gui()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()