from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFileDialog, QMessageBox
import os
from unidecode import unidecode
from PIL import Image

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI() 
        self.folder_selected = False 

    def initUI(self):
        self.setWindowTitle('Rename and resize photos by Thien Tran')
        self.setGeometry(500, 100, 500, 230)

        self.label = QLabel('Chọn đường dẫn thư mục:', self)
        self.label.move(20, 20)

        self.path_label = QLabel(self) 
        self.path_label.move(20, 80) 
        self.path_label.setFixedWidth(350) 

        self.select_label = QLabel('Chọn ảnh:', self)
        self.select_label.move(20, 100)

        self.selected_files_label = QLabel(self) 
        self.selected_files_label.move(20, 130)
        self.selected_files_label.setFixedWidth(350)

        self.button = QPushButton('Chọn thư mục', self)
        self.button.move(20, 50)
        self.button.clicked.connect(self.showDialog)

        self.select_button = QPushButton('Chọn ảnh', self)
        self.select_button.move(140, 50)
        self.select_button.clicked.connect(self.selectItem)

        self.check_button = QPushButton('Kiểm tra thư mục', self)
        self.check_button.move(260, 50)
        self.check_button.clicked.connect(self.openFolder)
        
        self.check_image_button = QPushButton('Kiểm tra ảnh', self)
        self.check_image_button.move(380, 50)
        self.check_image_button.clicked.connect(self.openImageFolder)

        self.delete_path_button = QPushButton('Xóa đường dẫn', self)
        self.delete_path_button.move(20, 160)
        self.delete_path_button.clicked.connect(self.deletePath)

        self.delete_file_button = QPushButton('Xóa ảnh', self)
        self.delete_file_button.move(140, 160)
        self.delete_file_button.clicked.connect(self.deleteFile)

        self.button = QPushButton('Thực hiện', self)
        self.button.move(260, 160)
        self.button.clicked.connect(self.startRename)
        
        self.button = QPushButton('Cảm ơn cái coi', self)
        self.button.move(20, 200)
        self.button.clicked.connect(self.buttonThanks)
        
        self.exit_button = QPushButton('Thoát', self)
        self.exit_button.move(380, 160)
        self.exit_button.clicked.connect(self.close)
        
        self.show()

    def showDialog(self):
        self.folder_path = QFileDialog.getExistingDirectory(self, 'Chọn thư mục')
        self.path_label.setText('Đường dẫn thư mục: ' + self.folder_path)
        self.folder_selected = True
    
    def selectItem(self):
        if not self.folder_selected:
            self.file_paths = QFileDialog.getOpenFileNames(self, 'Chọn ảnh', '', 'Images (*.png *.jpg *.jpeg)')[0]
            self.selected_files_label.setText('Các file được chọn: ' + ', '.join([os.path.basename(file_path) for file_path in self.file_paths]))
        else:
            QMessageBox.warning(self, 'Thông báo', 'Không thể chọn ảnh khi đã chọn thư mục!')
    
    def openFolder(self):
        if hasattr(self, 'folder_path'):
            os.startfile(self.folder_path)
        else:
            QMessageBox.warning(self, 'Thông báo', 'Vui lòng chọn thư mục trước khi kiểm tra!')
    
    def openImageFolder(self):
        if self.folder_selected:
            os.startfile(self.folder_path)
        elif hasattr(self, 'file_paths'):
            os.startfile(os.path.dirname(self.file_paths[0]))
        else:
            QMessageBox.warning(self, 'Thông báo', 'Vui lòng chọn thư mục hoặc ảnh trước khi kiểm tra!')
    
    def deletePath(self):
        if hasattr(self, 'folder_path'):
            del self.folder_path
            self.path_label.setText('')
            self.folder_selected = False
        else:
            QMessageBox.warning(self, 'Thông báo', 'Không có đường dẫn thư mục để xóa!')

    def deleteFile(self):
        if hasattr(self, 'file_paths'):
            del self.file_paths
            self.selected_files_label.setText('')
        else:
            QMessageBox.warning(self, 'Thông báo', 'Không có ảnh để xóa!')
    
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
        if not self.folder_selected and not hasattr(self, 'file_paths'):
            QMessageBox.warning(self, 'Thông báo', 'Vui lòng chọn thư mục hoặc ảnh để đổi tên và chỉnh sửa kích thước!')
            return
        if self.folder_selected:
            for filename in os.listdir(self.folder_path):
                if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
                    new_filename = unidecode(filename).replace(' ', '-').lower()
                    old_file_path = os.path.join(self.folder_path, filename)
                    new_file_path = os.path.join(self.folder_path, new_filename)
                    im = Image.open(old_file_path)
                    new_width = 700
                    new_height = int(new_width * im.size[1] / im.size[0])
                    im_resized = im.resize((new_width, new_height))
                    im_resized.save(new_file_path)
                    os.remove(old_file_path)
            QMessageBox.information(self, 'Thông báo', 'Chuyển đổi tên và chỉnh sửa kích thước ảnh hoàn tất!')
            print('Đổi tên và chỉnh sửa kích thước các file thành công!')
        elif hasattr(self, 'file_paths'):
            for file_path in self.file_paths:
                new_filename = unidecode(os.path.basename(file_path)).replace(' ', '-').lower()
                old_file_path = file_path
                new_file_path = os.path.join(os.path.dirname(file_path), new_filename)
                im = Image.open(old_file_path)
                new_width = 700
                new_height = int(new_width * im.size[1] / im.size[0])
                im_resized = im.resize((new_width, new_height))
                im_resized.save(new_file_path)
                os.remove(old_file_path)
            QMessageBox.information(self, 'Thông báo', 'Chuyển đổi tên và chỉnh sửa kích thước ảnh hoàn tất!')
            print('Đổi tên và chỉnh sửa kích thước các file thành công!')

if __name__ == '__main__':
    app = QApplication([])
    ex = App()
    app.exec_()