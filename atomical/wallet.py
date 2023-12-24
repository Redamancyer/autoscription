# wallet.py
import sys
from PyQt5.QtWidgets import QLineEdit, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QTextCursor
from atomical.tool import createScrollableLogDisplay,executeCommand

# 可能还需要导入其他模块

class WalletFunctions:
    def __init__(self, tabs):
        self.tabs = tabs
        self.createScrollableLogDisplay = createScrollableLogDisplay
        self.executeCommand = executeCommand
        self.path = "/Users/running/Documents/Vscode/atomicals-js"

    def openWalletInitTab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        tab.setLayout(layout)

        executeButton = QPushButton("初始化主钱包")
        scrollArea, outputDisplay = self.createScrollableLogDisplay()
        layout.addWidget(executeButton)
        layout.addWidget(scrollArea)
        self.tabs.addTab(tab, "初始化主钱包")
        executeButton.clicked.connect(lambda: self.executeCommand(self,self.path,"yarn cli wallet-init",outputDisplay))
        

    # 导出私钥
    def openExportPrivateKeyTab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        tab.setLayout(layout)

        phraseEdit = QLineEdit()
        phraseEdit.setPlaceholderText("请输入助记词短语")
        executeButton = QPushButton("导出私钥")
        scrollArea, outputDisplay = self.createScrollableLogDisplay()
        layout.addWidget(phraseEdit)
        layout.addWidget(executeButton)
        layout.addWidget(scrollArea)
        self.tabs.addTab(tab, "使用助记词导出私钥")

        executeButton.clicked.connect(lambda: self.executeCommand(
            self,self.path, f"yarn cli wallet-decode \"{phraseEdit.text()}\"", outputDisplay))

    # 导入钱包
    def openImportWalletTab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        tab.setLayout(layout)


        wifEdit = QLineEdit()
        wifEdit.setPlaceholderText("WIF格式的私钥")
        aliasEdit = QLineEdit()
        aliasEdit.setPlaceholderText("给钱包取一个别名")
        executeButton = QPushButton("导入私钥地址")
        scrollArea, outputDisplay = self.createScrollableLogDisplay()
        layout.addWidget(wifEdit)
        layout.addWidget(aliasEdit)
        layout.addWidget(executeButton)
        layout.addWidget(scrollArea)
        self.tabs.addTab(tab, "导入私钥地址")

        executeButton.clicked.connect(lambda: self.executeCommand(self,self.path,f"yarn cli wallet-import \"{wifEdit.text()}\" \"{aliasEdit.text()}\"", outputDisplay))

    # 获取地址信息
    def openAddressInfoTab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        tab.setLayout(layout)

        addressEdit = QLineEdit()
        addressEdit.setPlaceholderText("地址")
        executeButton = QPushButton("获取地址信息")
        scrollArea, outputDisplay = self.createScrollableLogDisplay()
        layout.addWidget(addressEdit)
        layout.addWidget(executeButton)
        layout.addWidget(scrollArea)
        self.tabs.addTab(tab, "获取地址信息")

        executeButton.clicked.connect(lambda: self.executeCommand(self,self.path,f"yarn cli address \"{addressEdit.text()}\"", outputDisplay))

    # 获取主钱包详细信息
    def openMainWalletDetailsTab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        tab.setLayout(layout)


        scrollArea, outputDisplay = self.createScrollableLogDisplay()
        layout.addWidget(scrollArea)
        self.tabs.addTab(tab, "主钱包详细信息")

        self.executeCommand(self,self.path,"yarn cli wallets", outputDisplay)
        outputDisplay.moveCursor(QTextCursor.Start)

    # 获取导入钱包详细信息
    def openImportedWalletDetailsTab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        tab.setLayout(layout)
        walletAliasEdit = QLineEdit()
        walletAliasEdit.setPlaceholderText("钱包别名")
        executeButton = QPushButton("获取导入钱包详细信息")
        scrollArea, outputDisplay = self.createScrollableLogDisplay()
        layout.addWidget(walletAliasEdit)
        layout.addWidget(executeButton)
        layout.addWidget(scrollArea)
        self.tabs.addTab(tab, "导入钱包详细信息")

        executeButton.clicked.connect(lambda: self.executeCommand(self,self.path,f"yarn cli wallets --alias {walletAliasEdit.text()}", outputDisplay))

# 需要将类实例化和集成到 main.py 中
