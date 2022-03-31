import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel, QPushButton
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QRadioButton, QButtonGroup, QGroupBox


class Gui(QWidget):
    def __init__(self):
        super().__init__()

        self.drawGui()

    def drawGui(self):
        self.setWindowTitle("Portfolio Manager")
        centerpoint = QDesktopWidget().availableGeometry().center()
        self.setGeometry(centerpoint.x()/4,centerpoint.y()/2,1000,500)
        layout = QHBoxLayout()
        leftVertLayout = QVBoxLayout()
        rightVertLayout = QVBoxLayout()
        leftHAddLayout = QHBoxLayout()
        leftHAmountLayout = QHBoxLayout()

        addBtn = QPushButton("Add")
        assetLineEdit = QLineEdit()
        assetLineEdit.setPlaceholderText("Enter comma-delineated assets of form: APPL, AMD, ...")
    
        unlimitedRadioBtn = QRadioButton("Unlimited")
        limitedRadioBtn = QRadioButton("Limited")
        longRadioBtn = QRadioButton("Long")
        computePortfolioBtn = QPushButton("Compute Portfolio") # Included in bottom-right

        amountLbl = QLineEdit("Amount")
        amountLbl.setReadOnly(True)
        amountInputLbl = QLineEdit()
        amountInputLbl.setPlaceholderText("Enter amount here")
        amountLbl.setMaximumWidth(75)
        numAssetsLbl = QLineEdit("X Total Assets") # Included in top-right
        numAssetsLbl.setReadOnly(True)
        assetListLbl = QLineEdit("Assets will appear here when added") # Included in top-right
        assetListLbl.setReadOnly(True) 


        leftHAmountLayout.addWidget(amountLbl)
        leftHAmountLayout.addWidget(amountInputLbl)

        leftHAddLayout.addWidget(assetLineEdit)
        leftHAddLayout.addWidget(addBtn)

        # Make the left side of screen
        leftVertLayout.addLayout(leftHAddLayout)
        leftVertLayout.addWidget(unlimitedRadioBtn)
        leftVertLayout.addWidget(limitedRadioBtn)
        leftVertLayout.addWidget(longRadioBtn)
        leftVertLayout.addLayout(leftHAmountLayout)
        leftVertLayout.addStretch(1)
        
        # Make the right side of screen
        rightVertLayout.addWidget(numAssetsLbl)
        rightVertLayout.addWidget(assetListLbl)
        rightVertLayout.addWidget(computePortfolioBtn)
        rightVertLayout.addStretch(1)

        # Add the left and right sides of screen to the layout
        layout.addLayout(leftVertLayout)
        layout.addLayout(rightVertLayout)
        
        # set the layout
        self.setLayout(layout)

        self.show()


def main():
    app = QApplication(sys.argv)
    gui = Gui()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()