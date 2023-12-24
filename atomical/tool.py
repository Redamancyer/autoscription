import subprocess
from PyQt5.QtWidgets import QTextEdit,QScrollArea,QWidget, QVBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal,Qt
from PyQt5.QtGui import QTextOption

def executeCommand(main,path, command, outputTextEdit):
    def onNewOutput(text):
        outputTextEdit.append(text)

    main.thread = CommandThread(command, path)
    main.thread.newOutput.connect(onNewOutput)
    main.thread.finished.connect(main.thread.deleteLater)  # 确保线程完成后删除
    main.thread.start()

def createScrollableLogDisplay():
    # 创建一个滚动区域
    scrollArea = QScrollArea()
    scrollAreaWidgetContents = QWidget()
    scrollAreaLayout = QVBoxLayout(scrollAreaWidgetContents)

    # 日志输出显示在 QTextEdit 中
    outputDisplay = QTextEdit()
    outputDisplay.setReadOnly(True)  # 设置为只读
    outputDisplay.setWordWrapMode(QTextOption.WordWrap)  # 允许文本换行
    scrollAreaLayout.addWidget(outputDisplay)
    outputDisplay.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard)  # 允许文本通过鼠标和键盘被选择和复制

    scrollArea.setWidget(scrollAreaWidgetContents)
    scrollArea.setWidgetResizable(True)  # 允许滚动区域内容自适应大小

    return scrollArea, outputDisplay

class CommandThread(QThread):
    newOutput = pyqtSignal(str)

    def __init__(self, command, path):
        super().__init__()
        self.command = command
        self.path = path
        self.process = None

    def run(self):
        try:
            self.process = subprocess.Popen(self.command, cwd=self.path, stdout=subprocess.PIPE, 
                                  stderr=subprocess.STDOUT, shell=True, text=True, bufsize=1)
            for line in iter(self.process.stdout.readline, ''):
                self.newOutput.emit(line)
            self.process.stdout.close()
        except Exception as e:
            self.newOutput.emit(f"Error: {str(e)}")
        finally:
            if self.process:
                self.process.wait()

    def stop(self):
        if self.process:
            self.process.terminate()  # 安全地终止进程
