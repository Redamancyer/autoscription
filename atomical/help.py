from PyQt5.QtWidgets import QVBoxLayout, QWidget
from atomical.tool import executeCommand
from PyQt5.QtWidgets import ( QWidget, QVBoxLayout, QTextEdit, QScrollArea,)
class HelpFunctions:
    def __init__(self,tabs):
        self.tabs = tabs
        self.path = "/Users/running/Documents/Vscode/atomicals-js"

    # 命令帮助
    def openCLIhelpTab(self):
        newTab = QWidget()
        layout = QVBoxLayout()
        newTab.setLayout(layout)

        # 创建输出显示区域
        outputTextEdit = QTextEdit()
        outputTextEdit.setReadOnly(True)
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(outputTextEdit)
        layout.addWidget(scrollArea)

        executeCommand(self,self.path,"yarn cli --help",outputTextEdit)

        self.tabs.addTab(newTab, "命令帮助")
    
     # 版本
    def openCLIversionTab(self):
        newTab = QWidget()
        layout = QVBoxLayout()
        newTab.setLayout(layout)

        # 创建输出显示区域
        outputTextEdit = QTextEdit()
        outputTextEdit.setReadOnly(True)
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(outputTextEdit)
        layout.addWidget(scrollArea)

        executeCommand(self,self.path,"yarn cli --version",outputTextEdit)

        self.tabs.addTab(newTab, "版本")

    # 服务器版本
    def openServerVersionTab(self):
        newTab = QWidget()
        layout = QVBoxLayout()
        newTab.setLayout(layout)

        # 创建输出显示区域
        outputTextEdit = QTextEdit()
        outputTextEdit.setReadOnly(True)
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(outputTextEdit)
        layout.addWidget(scrollArea)

        executeCommand(self,self.path,"yarn cli server-version",outputTextEdit)

        self.tabs.addTab(newTab, "服务器版本")

    def openAboutTab(self):
        newTab = QWidget()
        layout = QVBoxLayout()
        newTab.setLayout(layout)

        # 创建输出显示区域
        outputTextEdit = QTextEdit()
        outputTextEdit.setReadOnly(True)
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(outputTextEdit)
        layout.addWidget(scrollArea)

        # 定义一个格式化函数，用于对齐文本
        def format_line(label, content):
            return f"{label}{'   '}{content}"

        # 使用格式化函数来创建对齐的文本
        aboutStr = '\n'.join([
            format_line('atomicals-js 版本:', 'v0.1.58'),
            format_line('atomicals-js-qt-gui 版本:', 'v1.8'),
            '',
            '注意: 开源脚本，风险自负！'
        ])
        outputTextEdit.setText(aboutStr)
        self.tabs.addTab(newTab, "关于")

