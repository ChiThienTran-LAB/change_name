from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFileDialog, QMessageBox
import os
from unidecode import unidecode
from PIL import Image

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Đổi tên và chỉnh sửa kích thước ảnh trong thư mục'
        self.left = 500
        self.top = 100
        self.width = 400
        self.height = 200
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.label = QLabel('Chọn đường dẫn thư mục:', self)
        self.label.move(20, 20)

        self.path_label = QLabel(self) # Tạo một QLabel để hiển thị đường dẫn
        self.path_label.move(20, 70) # Đặt vị trí của QLabel
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

        self.button = QPushButton('Đổi tên và chỉnh sửa kích thước ảnh', self)
        self.button.move(20, 160) # Tăng độ cao của nút
        self.button.clicked.connect(self.startRename)

        self.show()

    def showDialog(self):
        self.folder_path = QFileDialog.getExistingDirectory(self, 'Chọn thư mục')
        self.path_label.setText('Đường dẫn thư mục: ' + self.folder_path) # Cập nhật nội dung của QLabel với đường dẫn được chọn
    
    def selectItem(self):
        self.file_paths = QFileDialog.getOpenFileNames(self, 'Chọn ảnh', '', 'Images (*.png *.jpg *.jpeg)')[0]
        self.selected_files_label.setText('Các file được chọn: ' + ', '.join([os.path.basename(file_path) for file_path in self.file_paths]))
    
    def startRename(self):
        if hasattr(self, 'folder_path'):
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
        else:
            msgBox = QMessageBox()
            msgBox.setWindowTitle('Thông báo')
            msgBox.setText('Vui lòng chọn thư mục hoặc ảnh để đổi tên và chỉnh sửa kích thước!')
            msgBox.exec_()

if __name__ == '__main__':
    app = QApplication([])
    ex = App()
    app.exec_()