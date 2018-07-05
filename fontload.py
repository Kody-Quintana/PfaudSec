import sys
import os
import random
import struct
from Crypto.Cipher import AES
from PyQt5 import QtGui, QtWidgets
from fontTools import ttLib
import hashlib

def font_check():
    return False

class Prompt(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Prompt, self).__init__(parent)
        self.label = QtWidgets.QLabel('Fonts not detected!\nEnter password to decrypt fonts')
        self.textPass = QtWidgets.QLineEdit(self)
        self.textPass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.buttonLogin = QtWidgets.QPushButton('Decrypt', self)
        self.buttonLogin.clicked.connect(lambda: self.try_decrypt(self.textPass.text()))
        self.setModal(True)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)

        self.font_dir = 'TeX/font/OTF/'

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
                    'TeX folder not found!\nCopy TeX folder before running.')
            sys.exit()
            
        if has_a_font_flag == 1:
            return True
        else:
            return False

    def try_decrypt(self, passphrase):
        key = hashlib.sha256(passphrase.encode('utf-8')).digest()

        for i in os.listdir(self.font_dir):
            if i.endswith('.enc'):
                decrypt_file(key, self.font_dir + i)

        self.textPass.setText('')
        if self.check_success() == False:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Password incorrect')
        else:
            self.accept()


def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    """ Encrypts a file using AES (CBC mode) with the
        given key.

        key:
            The encryption key - a string that must be
            either 16, 24 or 32 bytes long. Longer keys
            are more secure.

        in_filename:
            Name of the input file

        out_filename:
            If None, '<in_filename>.enc' will be used.

        chunksize:
            Sets the size of the chunk which the function
            uses to read and encrypt the file. Larger chunk
            sizes can be faster for some files and machines.
            chunksize must be divisible by 16.
    """
    if not out_filename:
        out_filename = in_filename + '.enc'

    iv = os.urandom(16)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b" " * (16 - len(chunk) % 16)
                            #^ must be byte string because python3 behavior

                outfile.write(encryptor.encrypt(chunk))

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
