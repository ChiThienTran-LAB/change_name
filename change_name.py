from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFileDialog, QMessageBox
import os
from unidecode import unidecode
from PIL import Image

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Rename and resize photos by Thien Tran'
        self.left = 500 #vị trí xuất hiện của cửa sổ
        self.top = 100 #vị trí xuất hiện của cửa sổ
        self.width = 370 #chiều rộng cửa sổ
        self.height = 230 #chiều cao cửa sổ
        self.initUI() #khởi tạo giao diện
        self.folder_selected = False #biến kiểm tra xem đã chọn thư mục hay chưa

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.label = QLabel('Chọn đường dẫn thư mục:', self)
        self.label.move(20, 20)

        self.path_label = QLabel(self) # Tạo một QLabel để hiển thị đường dẫn
        self.path_label.move(20, 80) # Đặt vị trí của QLabel
        self.path_label.setFixedWidth(350) # Tăng chiều rộng của QLabel để chứa đoạn text đường dẫn

        self.select_label = QLabel('Chọn ảnh:', self)
        self.select_label.move(20, 100)

        self.selected_files_label = QLabel(self) # Tạo một QLabel để hiển thị tên các file được chọn
        self.selected_files_label.move(20, 130) # Đặt vị trí của QLabel
        self.selected_files_label.setFixedWidth(350) # Tăng chiều rộng của QLabel để chứa đoạn text các file được chọn

        self.button = QPushButton('Chọn thư mục', self)
        self.button.move(20, 50)
        self.button.clicked.connect(self.showDialog)

        self.select_button = QPushButton('Chọn ảnh', self)
        self.select_button.move(140, 50)
        self.select_button.clicked.connect(self.selectItem)

        self.check_button = QPushButton('Kiểm tra thư mục', self)
        self.check_button.move(260, 50)
        self.check_button.clicked.connect(self.openFolder)

        self.delete_path_button = QPushButton('Xóa đường dẫn', self)
        self.delete_path_button.move(20, 160)
        self.delete_path_button.clicked.connect(self.deletePath)

        self.delete_file_button = QPushButton('Xóa ảnh', self)
        self.delete_file_button.move(140, 160)
        self.delete_file_button.clicked.connect(self.deleteFile)

        self.button = QPushButton('Thực hiện', self)
        self.button.move(260, 160) # Tăng độ cao của nút
        self.button.clicked.connect(self.startRename)
        
        self.button = QPushButton('Cảm ơn cái coi', self)
        self.button.move(200, 200) # Tăng độ cao của nút
        self.button.clicked.connect(self.buttonThanks)
        
        self.show()

    def showDialog(self):
        self.folder_path = QFileDialog.getExistingDirectory(self, 'Chọn thư mục')
        self.path_label.setText('Đường dẫn thư mục: ' + self.folder_path) # Cập nhật nội dung của QLabel với đường dẫn được chọn
        self.folder_selected = True # Đặt biến kiểm tra là True khi đã chọn thư mục
    
    def selectItem(self):
        if not self.folder_selected: # Kiểm tra xem đã chọn thư mục hay chưa
            self.file_paths = QFileDialog.getOpenFileNames(self, 'Chọn ảnh', '', 'Images (*.png *.jpg *.jpeg)')[0]
            self.selected_files_label.setText('Các file được chọn: ' + ', '.join([os.path.basename(file_path) for file_path in self.file_paths]))
        else:
            msgBox = QMessageBox()
            msgBox.setWindowTitle('Thông báo')
            msgBox.setText('Không thể chọn ảnh khi đã chọn thư mục!')
            msgBox.exec_()
    
    def openFolder(self):
        if hasattr(self, 'folder_path'):
            os.startfile(self.folder_path)
        else:
            msgBox = QMessageBox()
            msgBox.setWindowTitle('Thông báo')
            msgBox.setText('Vui lòng chọn thư mục trước khi kiểm tra!')
            msgBox.exec_()
    
    def deletePath(self):
        if hasattr(self, 'folder_path'):
            del self.folder_path
            self.path_label.setText('')
            self.folder_selected = False # Đặt biến kiểm tra là False khi xóa đường dẫn thư mục
        else:
            msgBox = QMessageBox()
            msgBox.setWindowTitle('Thông báo')
            msgBox.setText('Không có đường dẫn thư mục để xóa!')
            msgBox.exec_()

    def deleteFile(self):
        if hasattr(self, 'file_paths'):
            del self.file_paths
            self.selected_files_label.setText('')
        else:
            msgBox = QMessageBox()
            msgBox.setWindowTitle('Thông báo')
            msgBox.setText('Không có ảnh để xóa!')
            msgBox.exec_()
    
    def buttonThanks(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('Cảm ơn')
        msgBox.setText('Donate me: <a href="https://www.paypal.me/chithientran">https://www.paypal.me/chithientran</a>')
        msgBox.setStyleSheet("QLabel{min-width: 300px;}")
        label = msgBox.findChild(QLabel, "qt_msgbox_label")
        if label is not None:
            label.setOpenExternalLinks(True)
        msgBox.exec_()
    
    def startRename(self):
        if not self.folder_selected and not hasattr(self, 'file_paths'): # Kiểm tra xem đã chọn thư mục hoặc chọn ảnh chưa
            msgBox = QMessageBox()
            msgBox.setWindowTitle('Thông báo')
            msgBox.setText('Vui lòng chọn thư mục hoặc ảnh để đổi tên và chỉnh sửa kích thước!')
            msgBox.exec_()
            return
        if self.folder_selected:
            for filename in os.listdir(self.folder_path):
                if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
                    new_filename = unidecode(filename).replace(' ', '-').lower()
                    old_file_path = os.path.join(self.folder_path, filename)
                    new_file_path = os.path.join(self.folder_path, new_filename)
                    im = Image.open(old_file_path)
                    width, height = im.size
                    new_width = 700 # Tính chiều rộng ảnh mới
                    new_height = int(new_width * height / width)
                    im_resized = im.resize((new_width, new_height))
                    im_resized.save(new_file_path)
                    os.remove(old_file_path)
            msgBox = QMessageBox()
            msgBox.setWindowTitle('Thông báo')
            msgBox.setText('Chuyển đổi tên và chỉnh sửa kích thước ảnh hoàn tất!')
            msgBox.exec_()
            print('Đổi tên và chỉnh sửa kích thước các file thành công!')
        elif hasattr(self, 'file_paths'):
            for file_path in self.file_paths:
                new_filename = unidecode(os.path.basename(file_path)).replace(' ', '-').lower()
                old_file_path = file_path
                new_file_path = os.path.join(os.path.dirname(file_path), new_filename)
                im = Image.open(old_file_path)
                width, height = im.size
                new_width = 700 # Tính chiều rộng ảnh mới
                new_height = int(new_width * height / width)
                im_resized = im.resize((new_width, new_height))
                im_resized.save(new_file_path)
                os.remove(old_file_path)
            msgBox = QMessageBox()
            msgBox.setWindowTitle('Thông báo')
            msgBox.setText('Chuyển đổi tên và chỉnh sửa kích thước ảnh hoàn tất!')
            msgBox.exec_()
            print('Đổi tên và chỉnh sửa kích thước các file thành công!')

if __name__ == '__main__':
    app = QApplication([])
    ex = App()
    app.exec_()