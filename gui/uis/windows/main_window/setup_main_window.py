# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
import time
from typing import Set
from search_image_by_text.search_images_by_text import search_images_by_text

from . functions_main_window import *
from utils.face_functions import get_duplicate_pics, search_person_pics, sorter_main, sorter_main1
from utils.embedder import differ_paths, get_image_paths
from tensorflow.keras.models import load_model
import utils.embedder as EMBEDDER

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from gui.core.qt_core import *

# IMPORT SETTINGS
# ///////////////////////////////////////////////////////////////
from gui.core.json_settings import Settings

# IMPORT THEME COLORS
# ///////////////////////////////////////////////////////////////
from gui.core.json_themes import Themes

# IMPORT PY ONE DARK WIDGETS
# ///////////////////////////////////////////////////////////////
from gui.widgets import *

# LOAD UI MAIN
# ///////////////////////////////////////////////////////////////
from . ui_main import *

# MAIN FUNCTIONS 
# ///////////////////////////////////////////////////////////////
from . functions_main_window import *

from . flow_layout import *


# PY WINDOW
# ///////////////////////////////////////////////////////////////
class SetupMainWindow:
    def __init__(self):
        super().__init__()
        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

    # ADD LEFT MENUS
    # ///////////////////////////////////////////////////////////////
    add_left_menus = [
        {
            "btn_icon" : "icon_home.svg",
            "btn_id" : "btn_home",
            "btn_text" : "Front page",
            "btn_tooltip" : "Front page",
            "show_top" : True,
            "is_active" : True
        },
        {
            "btn_icon": "icon_folder_open.svg",
            "btn_id": "btn_page_pics1",
            "btn_text": "Face Classification Results",
            "btn_tooltip": "Face Classification Results",
            "show_top": True,
            "is_active": False
        },
        {
            "btn_icon": "icon_folder_open.svg",
            "btn_id": "btn_page_pics",
            "btn_text": "Classification result",
            "btn_tooltip": "Classification result",
            "show_top": True,
            "is_active": False
        },
        {
            "btn_icon": "icon_search.svg",
            "btn_id": "btn_page_search",
            "btn_text": "Search results",
            "btn_tooltip": "Search results",
            "show_top": True,
            "is_active": False
        },
        {
            "btn_icon": "icon_signal.svg",
            "btn_id": "btn_page_duplicate",
            "btn_text": "Plagiarism report",
            "btn_tooltip": "Plagiarism report",
            "show_top": True,
            "is_active": False
        }
    ]

     # ADD TITLE BAR MENUS
    # ///////////////////////////////////////////////////////////////
    add_title_bar_menus = []

    # SETUP CUSTOM BTNs OF CUSTOM WIDGETS
    # Get sender() function when btn is clicked
    # ///////////////////////////////////////////////////////////////
    def setup_btns(self):
        if self.ui.title_bar.sender() != None:
            return self.ui.title_bar.sender()
        elif self.ui.left_menu.sender() != None:
            return self.ui.left_menu.sender()
        elif self.ui.left_column.sender() != None:
            return self.ui.left_column.sender()
        elif self.ui.left_column.menus.verticalLayout.sender() != None:
            return self.ui.left_column.menus.verticalLayout.sender()

    # SETUP MAIN WINDOW WITH CUSTOM PARAMETERS
    # ///////////////////////////////////////////////////////////////
    def setup_gui(self):
        # APP TITLE
        # ///////////////////////////////////////////////////////////////
        self.setWindowTitle(self.settings["app_name"])
        
        # REMOVE TITLE BAR
        # ///////////////////////////////////////////////////////////////
        if self.settings["custom_title_bar"]:
            self.setWindowFlag(Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)

        # ADD GRIPS
        # ///////////////////////////////////////////////////////////////
        if self.settings["custom_title_bar"]:
            self.left_grip = PyGrips(self, "left", self.hide_grips)
            self.right_grip = PyGrips(self, "right", self.hide_grips)
            self.top_grip = PyGrips(self, "top", self.hide_grips)
            self.bottom_grip = PyGrips(self, "bottom", self.hide_grips)
            self.top_left_grip = PyGrips(self, "top_left", self.hide_grips)
            self.top_right_grip = PyGrips(self, "top_right", self.hide_grips)
            self.bottom_left_grip = PyGrips(self, "bottom_left", self.hide_grips)
            self.bottom_right_grip = PyGrips(self, "bottom_right", self.hide_grips)

        # LEFT MENUS / GET SIGNALS WHEN LEFT MENU BTN IS CLICKED / RELEASED
        # ///////////////////////////////////////////////////////////////
        # ADD MENUS
        self.ui.left_menu.add_menus(SetupMainWindow.add_left_menus)

        # SET SIGNALS
        self.ui.left_menu.clicked.connect(self.btn_clicked)
        self.ui.left_menu.released.connect(self.btn_released)

        # TITLE BAR / ADD EXTRA BUTTONS
        # ///////////////////////////////////////////////////////////////
        # ADD MENUS
        self.ui.title_bar.add_menus(SetupMainWindow.add_title_bar_menus)

        # SET SIGNALS
        self.ui.title_bar.clicked.connect(self.btn_clicked)
        self.ui.title_bar.released.connect(self.btn_released)

        # ADD Title
        if self.settings["custom_title_bar"]:
            self.ui.title_bar.set_title(self.settings["app_name"])
        else:
            self.ui.title_bar.set_title("Welcome to PyOneDark")

        # LEFT COLUMN SET SIGNALS
        # ///////////////////////////////////////////////////////////////
        self.ui.left_column.clicked.connect(self.btn_clicked)
        self.ui.left_column.released.connect(self.btn_released)

        # SET INITIAL PAGE / SET LEFT AND RIGHT COLUMN MENUS
        # ///////////////////////////////////////////////////////////////
        MainFunctions.set_page(self, self.ui.load_pages.page_1)
        MainFunctions.set_left_column_menu(
            self,
            menu = self.ui.left_column.menus.menu_1,
            title = "Result",
            icon_path = Functions.set_svg_icon("icon_settings.svg")
        )
        MainFunctions.set_right_column_menu(self, self.ui.right_column.menu_1)
#         MainFunctions.set_page(self, self.ui.load_pages.page_6)
#         MainFunctions.set_left_column_menu(
#             self,
#             menu = self.ui.left_column.menus.menu_1,
#             title = "人脸结果",
#             icon_path = Functions.set_svg_icon("icon_settings.svg")
#         )
#         MainFunctions.set_right_column_menu(self, self.ui.right_column.menu_1)

        # ///////////////////////////////////////////////////////////////
        # EXAMPLE CUSTOM WIDGETS
        # Here are added the custom widgets to pages and columns that
        # were created using Qt Designer.
        # This is just an example and should be deleted when creating
        # your application.
        #
        # OBJECTS FOR LOAD PAGES, LEFT AND RIGHT COLUMNS
        # You can access objects inside Qt Designer projects using
        # the objects below:
        #
        # <OBJECTS>
        # LEFT COLUMN: self.ui.left_column.menus
        # RIGHT COLUMN: self.ui.right_column
        # LOAD PAGES: self.ui.load_pages
        # </OBJECTS>
        # ///////////////////////////////////////////////////////////////

        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        settings = Settings()
        self.settings = settings.items

        # LOAD THEME COLOR
        # ///////////////////////////////////////////////////////////////
        themes = Themes()
        self.themes = themes.items
        self.ui.load_pages.page_1.setStyleSheet

        self.ui.credits.person_name.returnPressed.connect(lambda: MainFunctions.exec_edit_single_group_name(self, self.ui.credits.person_name))
        #################################################################
        # 选择文件夹
        self.func_btn_11 = PyPushButton(
            text = 'Select folder',
            radius = 8,
            color = self.themes['app_color']['white'],
            bg_color = self.themes['app_color']['dark_one'],
            bg_color_hover = self.themes['app_color']['orange'],
            bg_color_pressed = self.themes['app_color']['orange']
        )
        self.func_btn_11.setMaximumWidth(200)
        self.func_btn_11.setMinimumWidth(200)
        self.func_btn_11.setMinimumHeight(40)

        self.func_btn_11.clicked.connect(lambda: MainFunctions.select_image_directory(self))
        
        #################################################################
        # 人脸分类
        self.func_btn_13 = PyPushButton(
            text = 'Face classification',
            radius = 8,
            color = self.themes['app_color']['white'],
            bg_color = self.themes['app_color']['dark_one'],
            bg_color_hover = self.themes['app_color']['orange'],
            bg_color_pressed = self.themes['app_color']['orange']
        )
        self.func_btn_13.setMaximumWidth(200)
        self.func_btn_13.setMinimumWidth(200)
        self.func_btn_13.setMinimumHeight(40)
        #只制作了一个控件没有事件，要加东西??
        def detect_finished1():
            self.timer.stop()
            self.ui.credits.copyright_label.setText("Finish，tskes {} s".format(self.timer_count))
            QMessageBox.information(self, "Xml", "Finish")
        def detect_print_time1():
            try:
                processed_image = EMBEDDER.global_counter.value
            except AttributeError:
                processed_image = 0
            self.timer_count = int(time.time() - self.t0)
            if processed_image == 0:
                self.ui.credits.copyright_label.setText("loading model， {} s".format(self.timer_count))
                #print("正在加载模型，已开始 {} 秒".format(self.timer_count))
            elif processed_image == self.total_image:
                self.ui.credits.copyright_label.setText("sorting，{} s".format(self.timer_count))
            else:
                self.ui.credits.copyright_label.setText("identifying，{}/{}， {} s".format(processed_image, self.total_image, self.timer_count))
                #print("正在识别中，{}/{}，已识别 {} 秒".format(processed_image, self.total_image, self.timer_count))

        def create_detect_worker1():
            if self.settings['image_path'] == '':
                QMessageBox.information(self, "Xml", "No picture folder selected yet")
                return None

            self.t0 = time.time()
            self.timer_count = 0
            self.timer = QTimer()
            self.timer.timeout.connect(lambda: detect_print_time1())
            self.timer.start(100)

            image_paths = get_image_paths(self.settings['image_path'])
            image_paths = differ_paths(image_paths, self.settings['image_path'])
            self.total_image = len(image_paths)
            if self.total_image== 0:
                self.ui.credits.copyright_label.setText("A total of 0 new pictures were added, and the identification was canceled")
                return None

            #print("Found {} images..".format(self.total_image))

            self.worker_detect1 = Worker('facenet', image_paths)
            self.worker_detect1.start()
            self.worker_detect1.finished.connect(detect_finished1)

        self.worker_detect1 = Worker('facenet')
        self.func_btn_13.clicked.connect(lambda: create_detect_worker1())
        
        #################################################################
        # 识别分类
        self.func_btn_12 = PyPushButton(
            text = 'Photo classification',
            radius = 8,
            color = self.themes['app_color']['white'],
            bg_color = self.themes['app_color']['dark_one'],
            bg_color_hover = self.themes['app_color']['orange'],
            bg_color_pressed = self.themes['app_color']['orange']
        )
        self.func_btn_12.setMaximumWidth(200)
        self.func_btn_12.setMinimumWidth(200)
        self.func_btn_12.setMinimumHeight(40)

        def detect_finished():
            self.timer.stop()
            self.ui.credits.copyright_label.setText("Finish， {} s".format(self.timer_count))
            QMessageBox.information(self, "Xml", "Finish")
        def detect_print_time():
            try:
                processed_image = EMBEDDER.global_counter.value
            except AttributeError:
                processed_image = 0
            self.timer_count = int(time.time() - self.t0)
            if processed_image == 0:
                self.ui.credits.copyright_label.setText("loading model， {} s".format(self.timer_count))
                #print("正在加载模型，已开始 {} 秒".format(self.timer_count))
            elif processed_image == self.total_image:
                self.ui.credits.copyright_label.setText("sorting， {} s".format(self.timer_count))
            else:
                self.ui.credits.copyright_label.setText("identifying，{}/{}， {} s".format(processed_image, self.total_image, self.timer_count))
                #print("正在识别中，{}/{}，已识别 {} 秒".format(processed_image, self.total_image, self.timer_count))

        def create_detect_worker():
            if self.settings['image_path'] == '':
                QMessageBox.information(self, "Xml", "No picture folder selected yet")
                return None

            self.t0 = time.time()
            self.timer_count = 0
            self.timer = QTimer()
            self.timer.timeout.connect(lambda: detect_print_time())
            self.timer.start(100)

            image_paths = get_image_paths(self.settings['image_path'])
            image_paths = differ_paths(image_paths, self.settings['image_path'])
            self.total_image = len(image_paths)
            if self.total_image== 0:
                self.ui.credits.copyright_label.setText("A total of 0 new pictures were added, and the identification was canceled")
                return None

            #print("Found {} images..".format(self.total_image))

            self.worker_detect = Worker('Detect', image_paths)
            self.worker_detect.start()
            self.worker_detect.finished.connect(detect_finished)

        self.worker_detect = Worker('Detect')
        self.func_btn_12.clicked.connect(lambda: create_detect_worker())
        #################################################################
        # 智能搜索
        self.func_btn_21 = PyLineEdit(
            text = "",
            place_holder_text = "",
            radius = 8,
            border_size = 2,
            color = self.themes["app_color"]["text_foreground"],
            selection_color = self.themes["app_color"]["white"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_active = self.themes["app_color"]["dark_three"],
            context_color = self.themes["app_color"]["context_color"]
        )
       
        self.func_btn_21.setMaximumWidth(200)
        self.func_btn_21.setMinimumWidth(200)
        self.func_btn_21.setMinimumHeight(40)
#         describe=self.func_btn_21.text()
#         print(describe)

#         self.func_btn_21 = PyPushButton(
#             text = '选择图片',
#             radius = 8,
#             color = self.themes['app_color']['white'],
#             bg_color = self.themes['app_color']['dark_one'],
#             bg_color_hover = self.themes['app_color']['orange'],
#             bg_color_pressed = self.themes['app_color']['orange']
#         )
#         self.func_btn_21.setMaximumWidth(200)
#         self.func_btn_21.setMinimumWidth(200)
#         self.func_btn_21.setMinimumHeight(40)
#         self.func_btn_21.clicked.connect(lambda: MainFunctions.select_single_image(self))

        self.func_btn_22 = PyPushButton(
            text = 'Start searching',
            radius = 8,
            color = self.themes['app_color']['white'],
            bg_color = self.themes['app_color']['dark_one'],
            bg_color_hover = self.themes['app_color']['orange'],
            bg_color_pressed = self.themes['app_color']['orange']
        )
        self.func_btn_22.setMaximumWidth(200)
        self.func_btn_22.setMinimumWidth(200)
        self.func_btn_22.setMinimumHeight(40)
        
        self.func_btn_23 = QFrame()
        self.func_btn_23.setStyleSheet(u"background: transparent;")
        self.func_btn_23.setMaximumWidth(200)
        self.func_btn_23.setMinimumWidth(200)
        self.func_btn_23.setMinimumHeight(40)

        def search_finished(path):
            self.timer.stop()
            self.person_search_result = path
            self.ui.credits.copyright_label.setText("Finish，{} s".format(self.timer_count))
            QMessageBox.information(self, "Xml", "Finish")

        def search_print_time():
            self.timer_count = int(time.time() - self.t0)
            self.ui.credits.copyright_label.setText("searching， {} s".format(self.timer_count))

        def create_search_worker(path,text):

            self.t0 = time.time()
            self.timer_count = 0
            self.timer = QTimer()
            self.timer.timeout.connect(lambda: search_print_time())
            self.timer.start(100)
            
            self.search_changed = True
            self.has_searched = True
            #self.ui.credits.copyright_label.setText("正在进行搜索，请稍等")
            try:
                self.worker_search.start()
            except AttributeError:
                self.worker_search = Worker('Search',path, text)
                self.worker_search.start()
                self.worker_search.finished.connect(search_finished)
        def call_create_search_worker(photos_path):
            if self.func_btn_21.text()=='':
                QMessageBox.information(self, "Xml", "No query text has been entered")
            else:               
                try:
                    create_search_worker(photos_path,self.func_btn_21.text())
                except AttributeError:
                    QMessageBox.information(self, "Xml", "No query text has been entered")
        self.search_changed = False
        self.has_searched = False
        self.func_btn_22.clicked.connect(lambda: call_create_search_worker(self.settings['image_path']))
        
        ###################################################################

        self.func_btn_31 = PyPushButton(
            text = 'Start checking',
            radius = 8,
            color = self.themes['app_color']['white'],
            bg_color = self.themes['app_color']['dark_one'],
            bg_color_hover = self.themes['app_color']['orange'],
            bg_color_pressed = self.themes['app_color']['orange']
        )
        self.func_btn_31.setMaximumWidth(200)
        self.func_btn_31.setMinimumWidth(200)
        self.func_btn_31.setMinimumHeight(40)

        self.func_btn_32 = QFrame()
        self.func_btn_32.setStyleSheet(u"background: transparent;")
        self.func_btn_32.setMaximumWidth(200)
        self.func_btn_32.setMinimumWidth(200)
        self.func_btn_32.setMinimumHeight(40)
        
        self.func_btn_33 = QFrame()
        self.func_btn_33.setStyleSheet(u"background: transparent;")
        self.func_btn_33.setMaximumWidth(200)
        self.func_btn_33.setMinimumWidth(200)
        self.func_btn_33.setMinimumHeight(40)
        def dedup_finished(path):
            self.timer.stop()
            self.ui.credits.copyright_label.setText("Finish， {} s".format(self.timer_count))

            self.person_duplicate_result = path
            self.image_pages = []
            QMessageBox.information(self, "Xml", "Finish")

        def dedup_print_time():
            self.timer_count = int(time.time() - self.t0)
            self.ui.credits.copyright_label.setText("Checking， {} s".format(self.timer_count))
            
        def create_duplicate_worker(path):

            self.t0 = time.time()
            self.timer_count = 0
            self.timer = QTimer()
            self.timer.timeout.connect(lambda: dedup_print_time())
            self.timer.start(100)

            self.found_duplicate_image = True
            #self.ui.credits.copyright_label.setText("正在进行相似图片筛查，请稍等")
            self.worker_duplicate = Worker('Duplicate', path)
            self.worker_duplicate.start()
            self.worker_duplicate.finished.connect(dedup_finished)

        self.func_btn_31.clicked.connect(lambda: create_duplicate_worker(self.settings['image_path']))
        self.found_duplicate_image = False
        ###################################################################

        self.ui.load_pages.func_1_frame_1_layout.addWidget(self.func_btn_11,Qt.AlignCenter,Qt.AlignCenter)
        self.ui.load_pages.func_1_frame_2_layout.addWidget(self.func_btn_12,Qt.AlignCenter,Qt.AlignCenter)
        self.ui.load_pages.func_1_frame_3_layout.addWidget(self.func_btn_13,Qt.AlignCenter,Qt.AlignCenter)
        self.ui.load_pages.func_2_frame_1_layout.addWidget(self.func_btn_21,Qt.AlignCenter,Qt.AlignCenter)
        self.ui.load_pages.func_2_frame_2_layout.addWidget(self.func_btn_22,Qt.AlignCenter,Qt.AlignCenter)
        self.ui.load_pages.func_2_frame_3_layout.addWidget(self.func_btn_23,Qt.AlignCenter,Qt.AlignCenter)
        self.ui.load_pages.func_3_frame_1_layout.addWidget(self.func_btn_31,Qt.AlignCenter,Qt.AlignCenter)
        self.ui.load_pages.func_3_frame_2_layout.addWidget(self.func_btn_32,Qt.AlignCenter,Qt.AlignCenter)
        self.ui.load_pages.func_3_frame_3_layout.addWidget(self.func_btn_33,Qt.AlignCenter,Qt.AlignCenter)



        # ADD Widgets
        # ///////////////////////////////////////////////////////////////
        #SetupMainWindow.load_image(self)
        #MainFunctions.load_images(self)
        #MainFunctions.load_persons(self)

        # LEFT COLUMN
        # ///////////////////////////////////////////////////////////////

        # ///////////////////////////////////////////////////////////////
        # END - EXAMPLE CUSTOM WIDGETS
        # ///////////////////////////////////////////////////////////////

    # RESIZE GRIPS AND CHANGE POSITION
    # Resize or change position when window is resized
    # ///////////////////////////////////////////////////////////////
    def resize_grips(self):
        if self.settings["custom_title_bar"]:
            self.left_grip.setGeometry(5, 10, 10, self.height())
            self.right_grip.setGeometry(self.width() - 15, 10, 10, self.height())
            self.top_grip.setGeometry(5, 5, self.width() - 10, 10)
            self.bottom_grip.setGeometry(5, self.height() - 15, self.width() - 10, 10)
            self.top_right_grip.setGeometry(self.width() - 20, 5, 15, 15)
            self.bottom_left_grip.setGeometry(5, self.height() - 20, 15, 15)
            self.bottom_right_grip.setGeometry(self.width() - 20, self.height() - 20, 15, 15)
    
    def get_flow_layout(self):
        return self.flow_layout

    def get_frame(self):
        return self.frame

    def remove_pic(self):
        temp_widget = SetupMainWindow.get_flow_layout(self).itemAt(0).widget()
        #从flow_layout中删除第0张图片
        SetupMainWindow.get_flow_layout(self).removeWidget(temp_widget)
        SetupMainWindow.get_flow_layout(self).update()

class Worker(QThread):
    finished = Signal(dict)
    def __init__(self, mode, path = '',text =''):
        super().__init__()
        self.mode = mode 
        if path != '':
            self.path = path
        if text!='':
            self.text = text

    def run(self):
        if self.mode == "Detect":
            sorter_main(self.path)
            self.finished.emit({})
        elif self.mode == "facenet":
            sorter_main1(self.path)
            self.finished.emit({})
        elif self.mode == "Search":

            result = search_images_by_text(self.path,self.text)

            self.finished.emit(result)
        elif self.mode == "Duplicate":
            result = get_duplicate_pics(self.path)
            self.finished.emit(result)
        pass


