import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel, QPushButton
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QRadioButton, QButtonGroup, QGroupBox
from portfolioQuery import Portfolio

class Gui(QWidget):
    def __init__(self):
        super().__init__()
        self.drawGui()
        self.portfolio = None

    def drawGui(self):
        self.setWindowTitle("Portfolio Manager")
        centerpoint = QDesktopWidget().availableGeometry().center()
        self.setGeometry(centerpoint.x()/4,centerpoint.y()/2,1000,500)
        layout = QHBoxLayout()
        self.leftVertLayout = QVBoxLayout()
        self.rightVertLayout = QVBoxLayout()
        self.leftHAddLayout = QHBoxLayout()
        self.leftHAmountLayout = QHBoxLayout()

        self.addBtn = QPushButton("Add")
        self.assetLineEdit = QLineEdit()
        self.assetLineEdit.setPlaceholderText("Enter comma-delineated assets of form: APPL, AMD, ...")
    
        self.unlimitedRadioBtn = QRadioButton("Unlimited")
        self.limitedRadioBtn = QRadioButton("Limited")
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


        self.leftHAmountLayout.addWidget(self.amountLbl)
        self.leftHAmountLayout.addWidget(self.amountInputLbl)

        self.leftHAddLayout.addWidget(self.assetLineEdit)
        self.leftHAddLayout.addWidget(self.addBtn)

        # Make the left side of screen
        self.leftVertLayout.addLayout(self.leftHAddLayout)
        self.leftVertLayout.addWidget(self.unlimitedRadioBtn)
        self.leftVertLayout.addWidget(self.limitedRadioBtn)
        self.leftVertLayout.addWidget(self.longRadioBtn)
        self.leftVertLayout.addLayout(self.leftHAmountLayout)
        self.leftVertLayout.addStretch(1)
        
        # Make the right side of screen
        self.rightVertLayout.addWidget(self.numAssetsLbl)
        self.rightVertLayout.addWidget(self.assetListLbl)
        self.rightVertLayout.addWidget(self.computePortfolioBtn)
        self.rightVertLayout.addStretch(1)

        # Add the left and right sides of screen to the layout
        layout.addLayout(self.leftVertLayout)
        layout.addLayout(self.rightVertLayout)
        
        # set the layout
        self.setLayout(layout)

        # Set up action listeners for buttons and other widgets
        self.computePortfolioBtn.clicked.connect(self.portfolioBtnClicked)
        self.addBtn.clicked.connect(self.addBtnClicked)

        self.show()

    def portfolioBtnClicked(self):
        # Get the toggled radio button:
        if self.unlimitedRadioBtn.isChecked():
            print("Unlimited clicked")
        elif self.limitedRadioBtn.isChecked():
            print("Limited Clicked")
        elif self.longRadioBtn.isChecked():
            print("Long is clicked")

    def addBtnClicked(self):
        text = self.assetLineEdit.text()
        assets = text.split(",")
        self.assetLineEdit.setText("")
        self.portfolio = Portfolio(assets)
        self.assetListLbl.setText(str(self.portfolio))

def main():
    app = QApplication(sys.argv)
    gui = Gui()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()