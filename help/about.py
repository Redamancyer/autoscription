from PyQt5.QtWidgets import QVBoxLayout, QWidget
from PyQt5.QtWidgets import ( QWidget, QVBoxLayout, QTextEdit, QScrollArea,)
class AboutFunctions:
    def __init__(self,tabs):
        self.tabs = tabs

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
            format_line('脚本作者:', 'wusimpl,quantalmatrix'),
            format_line('日期:', '2023.12.13'),
            format_line('个人推特:', '@wusimpl'),
            '',
            '注意: 使用相应的功能前请在设置中配置脚本的执行路径！',
            '注意: 开源脚本，风险自负！'
        ])
        outputTextEdit.setText(aboutStr)
        self.tabs.addTab(newTab, "关于")