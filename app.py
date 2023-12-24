import sys
from PyQt5.QtWidgets import (QApplication,QAction, QMainWindow, QTabWidget, QDesktopWidget)
from atomical.help import HelpFunctions
from atomical.wallet import WalletFunctions
from atomical.atomicals import AtomicalsFunctions
from help.about import AboutFunctions
class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    def closeTab(self, index):
        self.tabs.removeTab(index)
    def center(self):
        # 获取屏幕的尺寸
        screen = QDesktopWidget().screenGeometry()

        # 计算窗口在屏幕上的位置
        x = (screen.width() - self.width) // 2
        y = (screen.height() - self.height) // 2

        # 设置窗口的位置
        self.move(x, y)

    def initUI(self):
        self.setWindowTitle('Atomicals-JS Qt GUI')
        self.setMinimumSize(800, 700)  # 设置最小大小


        # 设置窗口的尺寸
        self.width = 1200
        self.height = 750
        self.setGeometry(0, 0, self.width, self.height)

        # 移动窗口到屏幕中央
        self.center()

        # 创建标签页控件
        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.closeTab)

        # 初始化各个功能的执行目录
        self.actomical_path = ''

        self.HelpFunctions = HelpFunctions(self.tabs)
        self.wallet_functions = WalletFunctions(self.tabs)
        self.atomicals_functions = AtomicalsFunctions(self.tabs)

        self.about_functions = AboutFunctions(self.tabs)
        
        # 假设你已经有了一个 QMainWindow 或类似的窗体，并创建了一个菜单栏
        menubar = self.menuBar()

        # 创建一级菜单
        settimg_menu = menubar.addMenu('设置')

        atom_menu = menubar.addMenu('Atomicals')

        about_menu = menubar.addMenu('帮助')

        # 创建“设置”二级菜单
        path_setting_action = QAction('执行路径', self)
        path_setting_action.triggered.connect(self.HelpFunctions.openAboutTab)
        settimg_menu.addAction(path_setting_action)

        # 创建“关于”二级菜单
        about_action = QAction('关于', self)
        about_action.triggered.connect(self.about_functions.openAboutTab)
        about_menu.addAction(about_action)

        # 创建“帮助”二级菜单
        help_menu = atom_menu.addMenu('帮助')
        cli_version_action = QAction('CLI 版本号', self)
        cli_version_action.triggered.connect(self.HelpFunctions.openCLIversionTab)
        help_menu.addAction(cli_version_action)

        cli_help_action = QAction('显示命令帮助', self)
        cli_help_action.triggered.connect(self.HelpFunctions.openCLIhelpTab)
        help_menu.addAction(cli_help_action)

        server_version_action = QAction('服务器版本信息', self)
        server_version_action.triggered.connect(self.HelpFunctions.openServerVersionTab)
        help_menu.addAction(server_version_action)


        # 创建“钱包”二级菜单
        wallet_menu = atom_menu.addMenu('钱包')
        init_wallet_action = QAction('初始化/创建主钱包', self)
        init_wallet_action.triggered.connect(self.wallet_functions.openWalletInitTab)
        wallet_menu.addAction(init_wallet_action)

        export_private_key_action = QAction('使用助记词导出私钥', self)
        export_private_key_action.triggered.connect(self.wallet_functions.openExportPrivateKeyTab)
        wallet_menu.addAction(export_private_key_action)

        import_wallet_action = QAction('导入私钥地址', self)
        import_wallet_action.triggered.connect(self.wallet_functions.openImportWalletTab)
        wallet_menu.addAction(import_wallet_action)

        address_info_action = QAction('获取地址信息', self)
        address_info_action.triggered.connect(self.wallet_functions.openAddressInfoTab)
        wallet_menu.addAction(address_info_action)

        main_wallet_action = QAction('获取主钱包详细信息', self)
        main_wallet_action.triggered.connect(self.wallet_functions.openMainWalletDetailsTab)
        wallet_menu.addAction(main_wallet_action)

        import_wallet_info_action = QAction('获取导入钱包详细信息', self)
        import_wallet_info_action.triggered.connect(self.wallet_functions.openAddressInfoTab)
        wallet_menu.addAction(import_wallet_info_action)

        # 创建“Atomicals”二级菜单
        atomicals_menu = atom_menu.addMenu('Atomicals')
        main_wallet_details_action = QAction('主钱包详细信息', self)
        main_wallet_details_action.triggered.connect(self.atomicals_functions.openMainWalletDetailsTab)
        atomicals_menu.addAction(main_wallet_details_action)

        imported_wallet_details_action = QAction('导入钱包详细信息', self)
        imported_wallet_details_action.triggered.connect(self.atomicals_functions.openImportedWalletDetailsTab)
        atomicals_menu.addAction(imported_wallet_details_action)

        realm_info_action = QAction('查询领域/子领域信息', self)
        realm_info_action.triggered.connect(self.atomicals_functions.openRealmInfoTab)
        atomicals_menu.addAction(realm_info_action)

        mint_realm_action = QAction('mint Realm/SubRealm', self)
        mint_realm_action.triggered.connect(self.atomicals_functions.openMintRealmTab)
        atomicals_menu.addAction(mint_realm_action)

        mint_nft_action = QAction('mint NFT', self)
        mint_nft_action.triggered.connect(self.atomicals_functions.openMintNftTab)
        atomicals_menu.addAction(mint_nft_action)

        mint_ft_action = QAction('mint FT（ARC20）', self)
        mint_ft_action.triggered.connect(self.atomicals_functions.openMintFtTab)
        atomicals_menu.addAction(mint_ft_action)

        mint_container_item_action = QAction('mint Container Item', self)
        mint_container_item_action.triggered.connect(self.atomicals_functions.openMintContainerItemTab)
        atomicals_menu.addAction(mint_container_item_action)

        container_item_image_action = QAction('Container Item images', self)
        container_item_image_action.triggered.connect(self.atomicals_functions.openContainerItemImagesTab)
        atomicals_menu.addAction(container_item_image_action)


        self.about_functions.openAboutTab()

    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
