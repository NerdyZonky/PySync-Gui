import sys
import os
from getpass import getpass
from PyQt4 import QtCore, QtGui
from pysync_window1 import Ui_MainWindow
from PyQt4.QtGui import*
from subprocess import Popen, PIPE
import pexpect
import getpass


class window1(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.src)
        self.ui.pushButton_2.clicked.connect(self.sync)
        self.ui.pushButton_3.clicked.connect(self.dst)
        self.ui.radioButton_2.toggled.connect(self.radiossh)
        self.ui.radioButton.toggled.connect(self.radiolocal)
        self.ui.lineEdit_3.hide()
        self.ui.lineEdit_4.hide()
        self.ui.lineEdit_5.hide()
        self.ui.progressBar.hide()



    def src(self):
        f = QFileDialog.getExistingDirectory(self,"Open a folder","/home")
        file = self.ui.lineEdit.setText(f)


    def dst(self):
        f = QFileDialog.getExistingDirectory(self,"Open a folder","/home")
        file = self.ui.lineEdit_2.setText(f)


    def radiossh(self,enabled):
        if enabled:
            self.ui.lineEdit_3.show()
            self.ui.lineEdit_4.show()
            self.ui.lineEdit_5.show()

    def radiolocal(self,enabled):
        if enabled:
            self.ui.lineEdit_3.hide()
            self.ui.lineEdit_4.hide()
            self.ui.lineEdit_5.hide()


    def sync(self):
        src = self.ui.lineEdit.text()
        dst = self.ui.lineEdit_2.text()
        user = self.ui.lineEdit_3.text()
        server = self.ui.lineEdit_4.text()
        passwd = self.ui.lineEdit_5.text()
        passbyte = str.encode(passwd)

        pRsyncssh = ("-e ssh " + user + "@" + server)



        if src == "" and dst == "":
            message = QMessageBox.critical(self,"Fehler" ,"Bitte geben sie das QUELLVERZECIHNIS, sowie das ZIELVERZEICHNIS ein!")

        else:
            if src == "":
                message = QMessageBox.critical(self,"Fehler", "Bitte ein QUELLVERZECIHNIS angeben!")

            if dst == "":
                message = QMessageBox.critical(self,"Fehler", "Bitte ein ZIELVERZEICHNIS angeben!")


        if self.ui.radioButton_2.isChecked():
            if user == "" and server == "" and passwd == "":
                message = QMessageBox.critical(self,"Fehler", "Bitte Geben Sie den REMOTEUSER,den REMOTESERVER, sowie das PASSWORT an")

            else:
                if user == "" and server == "":
                    message = QMessageBox.critical(self,"Fehler", "Bitte Geben Sie den REMOTEUSER, sowie den REMOTESERVER an")

                else:
                    if user == "" and passwd == "":
                        message = QMessageBox.critical(self,"Fehler", "Bitte Geben Sie den REMOTEUSER, sowie das PASSWORT an")

                    else:
                        if server == "" and passwd == "":
                            message = QMessageBox.critical(self,"Fehler", "Bitte Geben Sie den REMOTESERVER, sowie das PASSWORT an")


                        else:
                            if user == "":
                                message = QMessageBox.critical(self,"Fehler", "Bitte Geben Sie den REMOTEUSER an")

                            if server == "":
                                message = QMessageBox.critical(self,"Fehler", "Bitte Geben Sie den REMOTESERVER an")

                            if passwd == "":
                               message = QMessageBox.critical(self,"Fehler", "Bitte Geben Sie das PASSWORT an")



        self.ui.progressBar.show()
        self.ui.progressBar.setValue(10)
        ssh_newkey = 'Are you sure you want to continue connecting'
        # my ssh command line
        p=pexpect.spawn('rsync -av --progress '+ src + ' -e ssh ' + user + '@' +server +':' + dst)

        self.ui.progressBar.setValue(20)

        i=p.expect([ssh_newkey,'password:',pexpect.EOF])

        self.ui.progressBar.setValue(40)
        if i==0:
            print ("I say yes")
            p.sendline('yes')
            i=p.expect([ssh_newkey,'password:',pexpect.EOF])
        self.ui.progressBar.setValue(60)
        if i==1:
            print ("I give password"),
            p.sendline(passwd)
            p.expect(pexpect.EOF)
        self.ui.progressBar.setValue(80)
        self.ui.progressBar.setValue(100)
        print("fertig")


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = window1()
    myapp.show()
    sys.exit(app.exec_())