from PyQt5.QtWidgets import  QComboBox,QCheckBox,QGridLayout,QMessageBox,QScrollArea,QFileDialog,QLineEdit, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor
from PyQt5 import QtWidgets
from atomical.tool import createScrollableLogDisplay,executeCommand
import requests
import os
from PyQt5.QtGui import QPixmap, QImage
import json

class AtomicalsFunctions:
    def __init__(self, tabs):
        self.tabs = tabs
        self.createScrollableLogDisplay = createScrollableLogDisplay
        self.executeCommand = executeCommand
        self.path = "/Users/running/Documents/Vscode/atomicals-js"
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

    # 获取领域/子领域信息
    def openRealmInfoTab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        realmNameEdit = QLineEdit()
        realmNameEdit.setPlaceholderText("领域/子领域名称")
        executeButton = QPushButton("获取领域/子领域信息")
        scrollArea, outputDisplay = self.createScrollableLogDisplay()
        layout.addWidget(realmNameEdit)
        layout.addWidget(executeButton)
        layout.addWidget(scrollArea)
        self.tabs.addTab(tab, "领域/子领域信息")

        executeButton.clicked.connect(lambda: self.executeCommand(self,self.path,f"yarn cli resolve \"{realmNameEdit.text()}\"", outputDisplay))

    # mint 领域/子领域
    def openMintRealmTab(self):
        tab = QWidget()
        gridLayout = QGridLayout(tab)

        # 创建领域名称输入区域
        realmLayout = QHBoxLayout()
        realmLabel = QLabel("领域/子领域名称:")
        realmEdit = QLineEdit()
        realmEdit.setPlaceholderText("输入领域/子领域名称")
        checkButton = QPushButton("查重")
        
        realmLayout.addWidget(realmLabel)
        realmLayout.addWidget(realmEdit)
        realmLayout.addWidget(checkButton)
        realmLayout.setStretch(0, 1)  # QLabel的拉伸因子
        realmLayout.setStretch(1, 1)  # QLineEdit的拉伸因子
        realmLayout.setStretch(2, 1)  # QPushButton的拉伸因子
        
        # 添加钱包地址输入控件
        senderLabel = QLabel("钱包发送地址:")
        senderEdit = QLineEdit()
        # senderEdit.setStyleSheet("border:4px soild black;border-radius: 10px;")
        senderEdit.setStyleSheet("QLineEdit { border-radius: 10px; }")
        senderEdit.setPlaceholderText("留空默认为funding address")
        senderLayout = QHBoxLayout()
        senderLayout.addWidget(senderLabel)
        senderLayout.addWidget(senderEdit)

        receiverLabel = QLabel("接收地址:")
        receiverEdit = QLineEdit()
        receiverEdit.setPlaceholderText("留空默认为primary address")
        receiverLayout = QHBoxLayout()
        receiverLayout.addWidget(receiverLabel)
        receiverLayout.addWidget(receiverEdit)

        # 添加 satsoutput 和手续费率输入控件
        satsoutputLabel = QLabel("satsoutput:")
        satsoutputEdit = QLineEdit()
        satsoutputEdit.setPlaceholderText("留空则默认1000")
        satsoutputLayout = QHBoxLayout()
        satsoutputLayout.addWidget(satsoutputLabel)
        satsoutputLayout.addWidget(satsoutputEdit)

        feeRateLabel = QLabel("手续费率:")
        feeRateEdit = QLineEdit()
        feeRateEdit.setPlaceholderText("单位：satsbyte，留空默认40")
        feeRateLayout = QHBoxLayout()
        feeRateLayout.addWidget(feeRateLabel)
        feeRateLayout.addWidget(feeRateEdit)

        # 显示当前 gas 价格及刷新按钮
        gasPriceDisplay = QLabel()
        refreshGasButton = QPushButton("刷新")
        refreshGasButton.clicked.connect(lambda: self.fetchAndDisplayGasPrice(gasPriceDisplay))
        gasLayout = QHBoxLayout()
        gasLayout.addWidget(gasPriceDisplay)
        gasLayout.addWidget(refreshGasButton)
        self.fetchAndDisplayGasPrice(gasPriceDisplay)  # 初始获取 gas 价格

        # 执行按钮和输出显示
        executeButton = QPushButton("mint 领域/子领域")
        scrollArea, outputDisplay = self.createScrollableLogDisplay()

        

        gridLayout.addLayout(realmLayout, 0, 0, 1, 3)
        
        gridLayout.addWidget(senderLabel, 1, 0)
        gridLayout.addWidget(senderEdit, 1, 1, 1, 2)
        
        gridLayout.addWidget(receiverLabel, 2, 0)
        gridLayout.addWidget(receiverEdit, 2, 1, 1, 2)
        
        gridLayout.addWidget(satsoutputLabel, 3, 0)
        gridLayout.addWidget(satsoutputEdit, 3, 1, 1, 2)
        
        gridLayout.addWidget(feeRateLabel, 4, 0)
        gridLayout.addWidget(feeRateEdit, 4, 1, 1, 2)
        
        gridLayout.addWidget(gasPriceDisplay, 5, 0)
        gridLayout.addWidget(refreshGasButton, 5, 1, 1, 2)
        
        gridLayout.addWidget(executeButton, 1, 3, 4, 2)
        executeButton.setSizePolicy(
        QtWidgets.QSizePolicy.Expanding,
        QtWidgets.QSizePolicy.Expanding
        )

        gridLayout.addWidget(scrollArea, 6, 0, 1, 5)
        
        self.tabs.addTab(tab, "mint 领域/子领域")

        # 设置执行按钮的点击事件
        executeButton.clicked.connect(lambda: self.mintRealm(
            realmEdit.text(),
            senderEdit.text(),
            receiverEdit.text(),
            satsoutputEdit.text(),
            feeRateEdit.text(),
            outputDisplay
        ))

        # 设置刷新Gas按钮的点击事件
        refreshGasButton.clicked.connect(lambda: self.fetchAndDisplayGasPrice(gasPriceDisplay))

        # 绑定查重按钮事件
        checkButton.clicked.connect(lambda: self.checkRealmDuplicate(realmEdit.text(), outputDisplay))

    def checkRealmDuplicate(self, realmName, outputDisplay):
        if realmName:
            command = f"yarn cli resolve \"{realmName}\""
            self.executeCommand(self,self.path,command, outputDisplay)
        else:
            outputDisplay.append("领域名称不能为空！")
        
    def mintRealm(self, realm, sender, receiver, satsoutput, feeRate, displayWidget):
        # 检查领域名称是否存在和有效
        # [这里添加检查领域名称的代码]

        # 使用默认值处理可选参数
        sender = f"--funding {sender}" if sender else ""
        receiver = f"--initialowner {receiver}" if receiver else ""
        satsoutput = f"--satsoutput {satsoutput}" if satsoutput else "--satsoutput 1000"
        feeRate = f"--satsbyte {feeRate}" if feeRate else "--satsbyte 40"

        # 构建命令
        mint_realm_cmd = f"yarn cli mint-realm {realm} {feeRate} {sender} {receiver} {satsoutput}"
        # 在单独的线程中执行命令
        self.executeCommand(self,self.path,mint_realm_cmd, displayWidget)
        displayWidget.moveCursor(QTextCursor.Start)


    # mint NFT
    def openMintNftTab(self):
        tab = QWidget()
        gridLayout = QGridLayout(tab)

        # 创建文件路径输入区域
        fileLayout = QHBoxLayout()
        fileLabel = QLabel("选择文件路径:")
        filePathEdit = QLineEdit()
        # filePathEdit.setPlaceholderText("文件路径（最好使用全路径）")
        browseButton = QPushButton("浏览")
        browseButton.clicked.connect(lambda: self.openFileDialog(filePathEdit))
        fileLayout.addWidget(fileLabel)
        fileLayout.addWidget(filePathEdit)
        fileLayout.addWidget(browseButton)
        fileLayout.setStretchFactor(fileLabel, 2)
        fileLayout.setStretchFactor(filePathEdit, 3)
        fileLayout.setStretchFactor(browseButton, 1)
        

        # 创建其他输入控件
        bitworkcLayout = QHBoxLayout()
        bitworkcLabel = QLabel("bitworkc:")
        bitworkcEdit = QLineEdit()
        bitworkcEdit.setPlaceholderText("bitworkc")
        bitworkcLayout.addWidget(bitworkcLabel)
        bitworkcLayout.addWidget(bitworkcEdit)
        bitworkcLayout.setStretchFactor(bitworkcEdit, 2)
        bitworkcLayout.setStretchFactor(bitworkcLabel, 1)

        satsoutputLayout = QHBoxLayout()
        satsoutputLabel = QLabel("satsoutput:")
        satsoutputEdit = QLineEdit()
        satsoutputEdit.setPlaceholderText("留空则默认1000")
        satsoutputLayout.addWidget(satsoutputLabel)
        satsoutputLayout.addWidget(satsoutputEdit)
        satsoutputLayout.setStretchFactor(satsoutputEdit, 2)
        satsoutputLayout.setStretchFactor(satsoutputLabel,1)

        senderLayout = QHBoxLayout()
        senderLabel = QLabel("Sender:")
        senderEdit = QLineEdit()
        senderEdit.setPlaceholderText("留空默认为funding address")
        senderLayout.addWidget(senderLabel)
        senderLayout.addWidget(senderEdit)
        senderLayout.setStretchFactor(senderEdit, 2)
        senderLayout.setStretchFactor(senderLabel, 1)

        receiverLayout = QHBoxLayout()
        receiverLabel = QLabel("Receiver:")
        receiverEdit = QLineEdit()
        receiverEdit.setPlaceholderText("留空默认为primary address")
        receiverLayout.addWidget(receiverLabel)
        receiverLayout.addWidget(receiverEdit)
        receiverLayout.setStretchFactor(receiverEdit, 2)
        receiverLayout.setStretchFactor(receiverLabel, 1)

        feeRateLayout = QHBoxLayout()
        feeRateLabel = QLabel("手续费:")
        feeRateEdit = QLineEdit()
        feeRateEdit.setPlaceholderText("留空默认40")
        feeRateLayout.addWidget(feeRateLabel)
        feeRateLayout.addWidget(feeRateEdit)
        feeRateLayout.setStretchFactor(feeRateEdit, 2)
        feeRateLayout.setStretchFactor(feeRateLabel, 1)

        # 显示当前 gas 价格及刷新按钮
        gasLayout = QHBoxLayout()
        gasPriceDisplay = QLabel()
        refreshGasButton = QPushButton("刷新")
        refreshGasButton.clicked.connect(lambda: self.fetchAndDisplayGasPrice(gasPriceDisplay))
        gasLayout.addWidget(gasPriceDisplay)
        gasLayout.addWidget(refreshGasButton)
        gasLayout.setStretchFactor(gasPriceDisplay, 1)
        gasLayout.setStretchFactor(refreshGasButton, 2)
        self.fetchAndDisplayGasPrice(gasPriceDisplay)  # 初始获取 gas 价格

        # 执行按钮和输出显示
        executeButton = QPushButton("mint")
        
        scrollArea, outputDisplay = self.createScrollableLogDisplay()
        
        # 添加控件到布局
        gridLayout.addLayout(fileLayout, 0, 0,1,3)
        gridLayout.addLayout(bitworkcLayout, 1, 0,1,3)
        gridLayout.addLayout(satsoutputLayout, 2, 0,1,3)
        gridLayout.addLayout(senderLayout, 3, 0,1,3)
        gridLayout.addLayout(receiverLayout, 4, 0,1,3)
        gridLayout.addLayout(feeRateLayout, 5, 0,1,3)
        gridLayout.addLayout(gasLayout, 6, 0,1,3)
        
        gridLayout.addWidget(executeButton, 2, 3,4,2)
        executeButton.setSizePolicy(
        QtWidgets.QSizePolicy.Expanding,
        QtWidgets.QSizePolicy.Expanding
        )
        
        gridLayout.addWidget(scrollArea, 7, 0,1,5)
        self.tabs.addTab(tab, "mint NFT")

        # 设置执行按钮的点击事件
        executeButton.clicked.connect(lambda: self.mintNFT(filePathEdit.text(), bitworkcEdit.text(), satsoutputEdit.text(), senderEdit.text(), receiverEdit.text(), feeRateEdit.text(), outputDisplay))

    def openFileDialog(self, edit):
        fileName, _ = QFileDialog.getOpenFileName(self, "打开文件", "", "JSON文件 (*.json)")
        if fileName:
            edit.setText(fileName)

    def mintNFT(self, filePath, bitworkc, satsoutput, sender, receiver, feeRate, displayWidget):
        # 检查文件路径是否存在
        if not filePath or not os.path.exists(filePath):
            displayWidget.setText("文件路径不能为空或文件不存在")
            return

        # 使用默认值处理可选参数
        bitworkc = f"--bitworkc {bitworkc}" if bitworkc else ""
        satsoutput = f"--satsoutput {satsoutput}" if satsoutput else "--satsoutput 1000"
        feeRate = f"--satsbyte {feeRate}" if feeRate else "--satsbyte 40"
        sender = f"--funding {sender}" if sender else ""
        receiver = f"--initialowner {receiver}" if receiver else ""

        # 构建命令
        mint_nft_cmd = f"yarn cli mint-nft \"{filePath}\" {bitworkc} {satsoutput} {feeRate} {sender} {receiver}"
        print(mint_nft_cmd)
        # 在单独的线程中执行命令
        self.executeCommand(self,self.path,mint_nft_cmd, displayWidget)
        displayWidget.moveCursor(QTextCursor.Start)

    # mint FT
    def openMintFtTab(self):
        tab = QWidget()
        gridLayout = QGridLayout(tab)

        # Ticker 名称
        tickerLayout = QHBoxLayout()
        tickerLabel = QLabel("Ticker 名称:")
        tickerEdit = QLineEdit()
        tickerEdit.setPlaceholderText("Ticker 名称")
        tickerLayout.addWidget(tickerLabel)
        tickerLayout.addWidget(tickerEdit)
        tickerLayout.setStretchFactor(tickerLabel, 1)
        tickerLayout.setStretchFactor(tickerEdit, 2)

        # 钱包发送地址
        senderLayout = QHBoxLayout()
        senderLabel = QLabel("钱包发送地址:")
        senderEdit = QLineEdit()
        senderEdit.setPlaceholderText("留空则默认为funding address")
        senderLayout.addWidget(senderLabel)
        senderLayout.addWidget(senderEdit)
        senderLayout.setStretchFactor(senderLabel, 1)
        senderLayout.setStretchFactor(senderEdit, 2)

        # 接收地址
        receiverLayout = QHBoxLayout()
        receiverLabel = QLabel("接收地址:")
        receiverEdit = QLineEdit()
        receiverEdit.setPlaceholderText("留空则默认为primary address")
        receiverLayout.addWidget(receiverLabel)
        receiverLayout.addWidget(receiverEdit)
        receiverLayout.setStretchFactor(receiverLabel, 1)
        receiverLayout.setStretchFactor(receiverEdit, 2)

        # 重复mint的数量
        repeatMintLayout = QHBoxLayout()
        repeatMintLabel = QLabel("重复mint数量:")
        repeatMintEdit = QLineEdit()
        repeatMintEdit.setPlaceholderText("留空则默认1张")
        repeatMintLayout.addWidget(repeatMintLabel)
        repeatMintLayout.addWidget(repeatMintEdit)
        repeatMintLayout.setStretchFactor(repeatMintLabel, 1)
        repeatMintLayout.setStretchFactor(repeatMintEdit, 2)

        # 禁用实时挖矿记录
        disableChalkLayout = QHBoxLayout()
        disableChalkLabel = QLabel("禁用实时挖矿记录:")
        disableChalkCheckbox = QCheckBox("禁用")
        disableChalkLayout.addWidget(disableChalkLabel)
        disableChalkLayout.addWidget(disableChalkCheckbox)
        disableChalkLayout.setStretchFactor(disableChalkLabel, 1)
        disableChalkLayout.setStretchFactor(disableChalkCheckbox, 2)

        # 手续费率
        feeRateLayout = QHBoxLayout()
        feeRateLabel = QLabel("手续费率:")
        feeRateEdit = QLineEdit()
        feeRateEdit.setPlaceholderText("单位：satsbyte，留空默认40")
        feeRateLayout.addWidget(feeRateLabel)
        feeRateLayout.addWidget(feeRateEdit)
        feeRateLayout.setStretchFactor(feeRateLabel, 1)
        feeRateLayout.setStretchFactor(feeRateEdit, 2)

        # 显示当前 gas 价格
        gasLayout = QHBoxLayout()
        gasPriceDisplay = QLabel()
        refreshGasButton = QPushButton("刷新")
        refreshGasButton.clicked.connect(lambda: self.fetchAndDisplayGasPrice(gasPriceDisplay))
        gasLayout.addWidget(gasPriceDisplay)
        gasLayout.addWidget(refreshGasButton)
        gasLayout.setStretchFactor(gasPriceDisplay, 1)
        gasLayout.setStretchFactor(refreshGasButton, 2)
        self.fetchAndDisplayGasPrice(gasPriceDisplay)

        # 执行按钮和输出显示
        executeButton = QPushButton("mint FT")
        scrollArea, outputDisplay = self.createScrollableLogDisplay()

        # 添加控件到布局
        gridLayout.addLayout(tickerLayout, 0, 0, 1, 3)
        gridLayout.addLayout(senderLayout, 1, 0, 1, 3)
        gridLayout.addLayout(receiverLayout, 2, 0, 1, 3)
        gridLayout.addLayout(repeatMintLayout, 3, 0, 1, 3)
        gridLayout.addLayout(disableChalkLayout, 4, 0, 1, 3)
        gridLayout.addLayout(feeRateLayout, 5, 0, 1, 3)
        gridLayout.addLayout(gasLayout, 6, 0, 1, 3)

        gridLayout.addWidget(executeButton, 2, 3, 4, 2)
        executeButton.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        
        gridLayout.addWidget(scrollArea, 7, 0, 1, 5)

        self.tabs.addTab(tab, "mint FT（ARC20 Token）")

        # 设置执行按钮的点击事件
        executeButton.clicked.connect(lambda: self.mintFT(tickerEdit.text(), senderEdit.text(), receiverEdit.text(), repeatMintEdit.text(), disableChalkCheckbox.isChecked(), feeRateEdit.text(), outputDisplay))


    # mint Container Item
    def openMintContainerItemTab(self):
        tab = QWidget()
        gridLayout = QGridLayout(tab)

        # Container 名称
        containerNameLabelLayout = QVBoxLayout()
        containerNameLabel = QLabel("Container 名称:")
        containerNameLabel.setFixedHeight(15)
        containerNameEdit = QLineEdit()
        containerNameEdit.setPlaceholderText("Container 名称")
        containerCheckButton = QPushButton("查询元数据")
        containerNameLayout = QHBoxLayout()
        containerNameLabelLayout.addWidget(containerNameLabel)
        containerNameLayout.addWidget(containerNameEdit)
        containerNameLayout.addWidget(containerCheckButton)
        containerNameLabelLayout.setStretchFactor(containerNameLabel, 1)
        containerNameLayout.setStretchFactor(containerNameEdit, 3)
        containerNameLayout.setStretchFactor(containerCheckButton, 1)
        containerNameLabelLayout.addLayout(containerNameLayout)
        gridLayout.addLayout(containerNameLabelLayout, 0, 0, 1, 2)

        # Item 编号
        itemNameLabelLayout = QVBoxLayout()
        itemNameLabel = QLabel("Item 编号:")
        itemNameLabel.setFixedHeight(15)
        itemNameEdit = QLineEdit()
        checkButton = QPushButton("查重")
        itemNameEdit.setPlaceholderText("Item 编号")
        itemNameLayout = QHBoxLayout()
        itemNameLabelLayout.addWidget(itemNameLabel)
        itemNameLayout.addWidget(itemNameEdit)
        itemNameLayout.addWidget(checkButton)
        # itemNameLayout.setStretchFactor(itemNameLabel, 2)
        itemNameLayout.setStretchFactor(itemNameEdit, 3)
        itemNameLayout.setStretchFactor(checkButton, 1)
        itemNameLabelLayout.addLayout(itemNameLayout)
        
        gridLayout.addLayout(itemNameLabelLayout, 1, 0, 1, 2)

        # 清单文件路径
        manifestFilePathLabelLayout = QVBoxLayout()
        manifestFilePathLabel = QLabel("清单文件路径:")
        manifestFilePathLabel.setFixedHeight(15)
        manifestFilePathEdit = QLineEdit()
        manifestFilePathEdit.setPlaceholderText("json文件")
        browseButton = QPushButton("浏览")
        browseButton.clicked.connect(lambda: self.openFileDialog(manifestFilePathEdit))
        manifestFilePathLayout = QHBoxLayout()
        manifestFilePathLabelLayout.addWidget(manifestFilePathLabel)
        manifestFilePathLayout.addWidget(manifestFilePathEdit)
        manifestFilePathLayout.addWidget(browseButton)
        # manifestFilePathLayout.setStretchFactor(manifestFilePathLabel, 2)
        manifestFilePathLayout.setStretchFactor(manifestFilePathEdit, 3)
        manifestFilePathLayout.setStretchFactor(browseButton, 1)
        manifestFilePathLabelLayout.addLayout(manifestFilePathLayout)
        gridLayout.addLayout(manifestFilePathLabelLayout, 2, 0, 1, 2)


        


        # 钱包发送地址
        senderLabel = QLabel("钱包发送地址:")
        senderLabelLayout = QVBoxLayout()
        senderLabel.setFixedHeight(15)
        senderEdit = QLineEdit()
        senderEdit.setPlaceholderText("留空则默认为funding address")
        senderLayout = QHBoxLayout()
        senderLabelLayout.addWidget(senderLabel)
        senderLayout.addWidget(senderEdit)
        # senderLayout.setStretchFactor(senderLabel, 1)
        senderLayout.setStretchFactor(senderEdit, 1)
        senderLabelLayout.addLayout(senderLayout)
        gridLayout.addLayout(senderLabelLayout, 0, 2, 1, 2)
        

        # 接收地址
        receiverLabel = QLabel("接收地址:")
        receiverLabelLayout = QVBoxLayout()
        receiverLabel.setFixedHeight(15)
        receiverEdit = QLineEdit()
        receiverEdit.setPlaceholderText("留空则默认为primary address")
        receiverLayout = QHBoxLayout()
        receiverLabelLayout.addWidget(receiverLabel)
        receiverLayout.addWidget(receiverEdit)
        # receiverLayout.setStretchFactor(receiverLabel, 1)
        receiverLayout.setStretchFactor(receiverEdit, 1)
        receiverLabelLayout.addLayout(receiverLayout)
        gridLayout.addLayout(receiverLabelLayout, 1, 2, 1, 2)
        

        # 手续费率
        feeRateLabel = QLabel("手续费率:")
        feeRateLabelLayout = QVBoxLayout()
        feeRateLabel.setFixedHeight(15)
        feeRateEdit = QLineEdit()
        feeRateEdit.setPlaceholderText("单位：sats/byte，留空默认40")
        feeRateLayout = QHBoxLayout()
        feeRateLabelLayout.addWidget(feeRateLabel)
        feeRateLayout.addWidget(feeRateEdit)
        gasPriceDisplay = QLabel()
        refreshGasButton = QPushButton("刷新")
        refreshGasButton.clicked.connect(lambda: self.fetchAndDisplayGasPrice(gasPriceDisplay))
        feeRateLayout.addWidget(gasPriceDisplay)
        feeRateLayout.addWidget(refreshGasButton)
        # feeRateLayout.setStretchFactor(feeRateLabel, 1)
        feeRateLayout.setStretchFactor(feeRateEdit, 3)
        feeRateLayout.setStretchFactor(gasPriceDisplay, 2)
        feeRateLayout.setStretchFactor(refreshGasButton, 1)
        feeRateLabelLayout.addLayout(feeRateLayout)
        gridLayout.addLayout(feeRateLabelLayout, 3, 0, 1, 2)
        self.fetchAndDisplayGasPrice(gasPriceDisplay)

        

        # Bitworkc 工作量证明字符串
        bitworkcLabel = QLabel("Bitworkc 工作量证明字符串:")
        bitworkcLabelLayout = QVBoxLayout()
        bitworkcLabel.setFixedHeight(15)
        bitworkcEdit = QLineEdit()
        bitworkcEdit.setPlaceholderText("留空则默认不使用")
        bitworkcLayout = QHBoxLayout()
        bitworkcLabelLayout.addWidget(bitworkcLabel)
        bitworkcLayout.addWidget(bitworkcEdit)
        # bitworkcLayout.setStretchFactor(bitworkcLabel, 1)
        bitworkcLayout.setStretchFactor(bitworkcEdit, 1)
        bitworkcLabelLayout.addLayout(bitworkcLayout)
        gridLayout.addLayout(bitworkcLabelLayout, 2, 2, 1, 2)

        # 禁用实时挖矿记录
        # disableChalkLabel = QLabel("禁用实时挖矿记录:")
        disableChalkCheckbox = QCheckBox("是否禁用实时挖矿记录")
        disableChalkLayout = QHBoxLayout()
        # disableChalkLayout.addWidget(disableChalkLabel)
        disableChalkLayout.addWidget(disableChalkCheckbox)
        # disableChalkLayout.setStretchFactor(disableChalkLabel, 1)
        disableChalkLayout.setStretchFactor(disableChalkCheckbox,1)
        gridLayout.addLayout(disableChalkLayout, 3, 2, 1, 2)



        # 执行按钮和输出显示
        submitLayout = QHBoxLayout()
        executeButton = QPushButton("mint Container Item")
        clearButton = QPushButton("clear log")
        scrollArea, outputDisplay = self.createScrollableLogDisplay()
        # gridLayout.addWidget(executeButton, 3, 3, 4, 2)
        submitLayout.addWidget(executeButton)
        submitLayout.addWidget(clearButton)
        submitLayout.setStretchFactor(executeButton,1)
        submitLayout.setStretchFactor(clearButton,1)
        gridLayout.addLayout(submitLayout,4,0,1,4)
        gridLayout.addWidget(scrollArea, 9, 0, 1, 4)

        self.tabs.addTab(tab, "mint Container Item")

        # 设置执行按钮的点击事件
        executeButton.clicked.connect(lambda: self.mintContainerItem(containerNameEdit.text(), itemNameEdit.text(), manifestFilePathEdit.text(), senderEdit.text(), receiverEdit.text(), feeRateEdit.text(), disableChalkCheckbox.isChecked(), bitworkcEdit.text(), outputDisplay))
        checkButton.clicked.connect(lambda: self.checkContainerItemDuplicate(containerNameEdit.text(), itemNameEdit.text(), outputDisplay))
        containerCheckButton.clicked.connect(lambda: self.getContainerMetadata(containerNameEdit.text(), outputDisplay))
    
    def openContainerItemImagesTab(self,path):
        folder_path=''
        current_page = 0
        images = []
        image_labels = []
        text_labels = []  # 新增一个列表来存放文本标签
        cols = 10  # 假设有 10 列
        def show_image():
            print(len(images))
            for i, pixmap in enumerate(images):
                # 设置图片
                image_labels[i].setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))

                # 设置文本
                text = f"{current_page * 100 + i}"
                text_labels[i].setText(text)
        def page_selected(index):
            # 当选中新的页码时调用
            nonlocal current_page
            current_page = index
            nonlocal images
            images = load_images(folder_path, current_page, 100)
            show_image()
        
        def select_folder():
            nonlocal folder_path
            folder_path = QFileDialog.getExistingDirectory(tab, "Select Folder")
            nonlocal images
            if folder_path:
                current_page = 0
                images = load_images(folder_path, current_page, 100)
                show_image()

        def load_images(folder_path, page, images_per_page):
            images = []
            start = page * images_per_page
            end = start + images_per_page

            def is_valid_file(filename):
                parts = filename.split('-')
                return len(parts) == 2

            file_names = sorted(
                filter(is_valid_file, os.listdir(folder_path)),
                key=lambda x: int(x.split('-')[1].split('.')[0])
            )

            selected_files = file_names[start:end]
            print(len(file_names))

            for filename in selected_files:
                if filename.endswith('.json'):
                    file_path = os.path.join(folder_path, filename)
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        png_hex_data = data['data']['image.png'].get('$b')
                        png_data = bytes.fromhex(png_hex_data)
                        image = QImage.fromData(png_data)

                        if image.isNull():
                            print(f"Failed to load image from {file_path}")
                        else:
                            pixmap = QPixmap.fromImage(image)
                            images.append(pixmap)
            return images

        # 为页码选择器和选择文件夹按钮创建一个水平布局
        layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        tab = QWidget()

        # 添加选择文件夹按钮
        select_folder_button = QPushButton('Select Folder')
        select_folder_button.clicked.connect(select_folder)
        # self.layout.addWidget(self.select_folder_button)

        top_layout.addWidget(select_folder_button)

        # 创建下拉列表用于选择页码
        page_selector = QComboBox()
        for i in range(100):  # 假设总共有 100 页
            page_selector.addItem(f"Page {i}")
        page_selector.currentIndexChanged.connect(page_selected)
        # self.layout.addWidget(self.page_selector)\
        top_layout.addWidget(page_selector)
        

         # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        grid_layout = QGridLayout(scroll_widget)

        

        for i in range(100):  # 100 张图片
            # 图片标签
            image_label = QLabel()
            image_labels.append(image_label)
            grid_layout.addWidget(image_label, 2 * (i // cols), i % cols)

            # 文本标签
            text_label = QLabel("")  # 初始文本
            text_label.setAlignment(Qt.AlignCenter)  # 设置文本居中
            text_label.setStyleSheet("color: green; margin: 3px;")
            text_labels.append(text_label)
            grid_layout.addWidget(text_label, 2 * (i // cols) + 1, i % cols)

        scroll_area.setWidget(scroll_widget)

        layout.addLayout(top_layout)
        layout.addWidget(scroll_area)
        tab.setLayout(layout)
        
        self.tabs.addTab(tab, "mint Container Item")

        
    
    def checkContainerItemDuplicate(self, containerName, itemName, outputDisplay):
        if containerName == "" or itemName == "":
            outputDisplay.append("请输入容器名称/物品名称")
            return
        try:
            command = f"yarn cli get-container-item \"{containerName}\" \"{itemName}\" "
            self.executeCommand(self,self.path,command, outputDisplay)
        except Exception as e:
            QMessageBox.critical(None, "错误", f"发生了一个错误：{e}")

    def getContainerMetadata(self,containerName,outputDisplay):
        if containerName == "":
            outputDisplay.append("请输入容器名称")
            return
        try:
            command = f"yarn cli get-container \"{containerName}\" "
            self.executeCommand(self,self.path,command, outputDisplay)
        except Exception as e:
            QMessageBox.critical(None, "错误", f"发生了一个错误：{e}")

    def fetchAndDisplayGasPrice(self, displayWidget):
        try:
            response = requests.get("https://mempool.space/api/v1/fees/recommended")
            if response.status_code == 200:
                gasPrice = response.json()["fastestFee"]
                displayWidget.setText(f"当前 gas 价格: {gasPrice} sats/vB")
            else:
                displayWidget.setText(f"获取 gas 价格失败，状态码: {response.status_code}")
        except Exception as e:
            displayWidget.setText(f"获取 gas 价格时发生错误: {e}")
    def mintContainerItem(self,containerName,itemName,manifestFilePath,sender,receiver,feeRate,disableChalk,bitworkc,outputDisplay):
        if containerName=="" or itemName=="" or manifestFilePath == "" or feeRate== "":
            QMessageBox.critical(None, "错误", f"请检查必填项！")
            return
        command = f"yarn cli mint-item #{containerName} {itemName} {manifestFilePath} --satsbyte {feeRate}"
        if sender!="":
            command+= f" --funding {sender}"
        if receiver!="":
            command+=f" --initialowner {receiver}"
        try:
            self.executeCommand(self,self.path,command, outputDisplay)
            # print(command)
        except Exception as e:
            QMessageBox.critical(None, "错误", f"发生了一个错误：{e}")