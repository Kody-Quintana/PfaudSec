import sys
import os
import random
import struct
import hashlib
#from Cryptodome.Cipher import AES
from PyQt5 import QtGui, QtWidgets
from fontTools import ttLib

class Prompt(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Prompt, self).__init__(parent)
        global AES

        try:
            from Cryptodome.Cipher import AES
        except:
            QtWidgets.QMessageBox.warning(self, 'Error',
                    """Couldn't load Cryptodome package!
Fonts must be manually installed before PfaudSec will work.""")
            self.accept()

        self.label = QtWidgets.QLabel(\
                'Fonts not detected!\nEnter password to decrypt fonts')
        self.textPass = QtWidgets.QLineEdit(self)
        self.textPass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.buttonLogin = QtWidgets.QPushButton('Decrypt', self)
        self.buttonLogin.clicked.connect(lambda\
                : self.try_decrypt(self.textPass.text()))
        self.setModal(True)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)

        self.font_dir = 'work_folder/font/OTF/'


    def check_success(self):
        """Check if font is valid by attempting to load with ttLib"""
        has_a_font_flag = 0
        try:
            for i in os.listdir(self.font_dir):
                if i.endswith('.otf'):
                    has_a_font_flag = 1
                    try:
                        ttLib.TTFont(self.font_dir + i)
                    except ttLib.TTLibError:
                        return False
        except FileNotFoundError:
            self.no_tex = QtWidgets.QMessageBox.warning(self, 'Error',
                    'font folder not found!\nCopy font folder before running.')
            sys.exit()
            
        if has_a_font_flag == 1:
            return True
        else:
            return False

    def try_decrypt(self, passphrase):
        """Decrypt then check if font is valid"""

        key = hashlib.sha256(passphrase.encode('utf-8')).digest()

        for i in os.listdir(self.font_dir):
            if i.endswith('.enc'):
                decrypt_file(key, self.font_dir + i)

        self.textPass.setText('')
        if self.check_success() == False:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Password incorrect')
        else:
            self.accept()


def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):
    """ Decrypts a file using AES (CBC mode) with the
        given key. Parameters are similar to encrypt_file,
        with one difference: out_filename, if not supplied
        will be in_filename without its last extension
        (i.e. if in_filename is 'aaa.zip.enc' then
        out_filename will be 'aaa.zip')
    """
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(origsize)
