import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.uic import loadUi
from Connexion_Cassandra import Connexion


class Gestion_Etudiants(QMainWindow):
    def __init__(self):
        super(Gestion_Etudiants, self).__init__()

        loadUi(
            'C:/Users/Zakar/PycharmProjects/PyQt5Withcassandra/venv/Lib/site-packages/qt5_applications/Qt/bin'
            '/Cassandra.ui',
            self)
        self.bt_menu.clicked.connect(self.move_menu)
        self.data = Connexion()
        self.bt_restore.hide()

        self.bt_Mo_Rechercher.clicked.connect(self.recherche_etudiant_moyenne)
        self.bt_AjouterEt.clicked.connect(self.ajouter_etudiant)
        self.btAjjMatiere.clicked.connect(self.ajouter_matiere)
        self.bt_refresher.clicked.connect(self.affichage_Etudiants)
        self.BtRecherNote.clicked.connect(self.recher_matiere)
        self.bt_AjouterNote.clicked.connect(self.ajouter_note)
        self.BtRecherCodeApp.clicked.connect(self.recher_codeapoge)

        self.bt_mini.clicked.connect(self.bt_control_minimize)
        self.bt_restore.clicked.connect(self.bt_control_normal)
        self.bt_max.clicked.connect(self.bt_control_maximize)
        self.bt_fermer.clicked.connect(lambda: self.close())

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)

        # SizeGrip
        self.gripSize = 10
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)

        # move window
        self.frame_superior.mouseMoveEvent = self.move_window

        # connect buttons
        self.bt_liste.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_listeEt))
        self.bt_Etudiant.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_AddEt))
        self.bt_NOTE.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_noteEt))
        self.bt_Matiere.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_matiere))
        self.bt_Moyenne.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_Moyenne))

        # Adjustable column width
        self.tableMoyenne.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableEtudinats.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def bt_control_minimize(self):
        self.showMinimized()

    def bt_control_normal(self):
        self.showNormal()
        self.bt_restore.hide()
        self.bt_max.show()

    def bt_control_maximize(self):
        self.showMaximized()
        self.bt_max.hide()
        self.bt_restore.show()

    def resizeEvent(self, event):
        rect = self.rect()
        self.grip.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)

    def mousePressEvent(self, event):
        self.click_position = event.globalPos()

    def move_window(self, event):
        if self.isMaximized() == False:
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.click_position)
                self.click_position = event.globalPos()
                event.accept()
        if event.globalPos().y() <= 10:
            self.showMaximized()
            self.bt_max.hide()
            self.bt_restore.show()
        else:
            self.showNormal()
            self.bt_restore.hide()
            self.bt_max.show()

    def move_menu(self):
        if True:
            width = self.frame_control.width()
            normal = 0
            if width == 0:
                extender = 200
            else:
                extender = normal
            self.animation = QPropertyAnimation(self.frame_control, b'minimumWidth')
            self.animation.setDuration(300)
            self.animation.setStartValue(width)
            self.animation.setEndValue(extender)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()

    def ajouter_etudiant(self):
        CNE = self.ADDCNEEt.text().upper()
        code_apoge = self.ADDCODEAppET.text().upper()
        email = self.ADDEmailET.text().upper()
        nom = self.ADDNomET.text().upper()
        prenom = self.ADDPrenomEt.text().upper()
        ville = self.ADDvilleEt.text().upper()
        region = self.ADDregionEt.text().upper()
        if CNE != "" and code_apoge != "" and email != "" and nom != "" and prenom != "" and ville != "" and region != "":
            self.data.insert_etudiant(CNE, code_apoge, email, nom, prenom, ville, region)
            self.signalET.setText('Etudiant bien enregistrés')
            self.ADDCNEEt.clear()
            self.ADDCODEAppET.clear()
            self.ADDEmailET.clear()
            self.ADDNomET.clear()
            self.ADDPrenomEt.clear()
            self.ADDvilleEt.clear()
            self.ADDregionEt.clear()
        else:
            self.signalET.setText('Veillez remplir tous les champs')

    def ajouter_matiere(self):
        # id_mat = self.LEIDMatiere.text().upper()
        nom_mat = self.LEMatiere.text().upper()
        coeff = self.LEConficionMatiere.text().upper()
        if nom_mat != "" and coeff != "":
            self.data.insert_Matiere(nom_mat, float(coeff))
            self.signalMatiere.setText('Matiere bien enregistrés')
            # self.LEIDMatiere.clear()
            self.LEMatiere.clear()
            self.LEConficionMatiere.clear()
        else:
            self.signalMatiere.setText('Veillez remplir tous les champs')

    def set_RowCount(self):
        donnees = self.data.select_table_Etudiant()
        j = 0
        for i in donnees:
            j = j + 1
        return j

    def affichage_Etudiants(self):
        donnees = self.data.select_table_Etudiant()
        count = self.set_RowCount()
        self.tableEtudinats.setRowCount(count)
        tablerow = 0
        for row in donnees:
            self.tableEtudinats.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[3]))
            self.tableEtudinats.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[4]))
            self.tableEtudinats.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[1]))
            self.tableEtudinats.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[0]))
            self.tableEtudinats.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(row[2]))
            self.tableEtudinats.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(row[5]))
            self.tableEtudinats.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(row[6]))
            tablerow += 1

    def recher_matiere(self):
        id_producto = self.LENomMa.text().upper()
        if id_producto == "":
            self.signal_note.setText("Veillez remplir tous les champs")
            self.LE_Matiere.clear()
        else:
            self.producto = self.data.recherMatiere(id_producto)
            if self.producto != "Nane":
                self.LE_Matiere.setText(self.producto[0])
                self.signal_note.setText("ÇA EXISTE")
            elif self.producto == "Nane":
                self.LE_Matiere.clear()
                self.signal_note.setText("N'EXISTE PAS")

    def recher_codeapoge(self):
        LECodeApp = self.LECodeApp.text().upper()
        if LECodeApp == "":
            self.signal_note.setText("Veillez remplir tous les champs")
            self.LECodeMa.clear()
        else:
            self.codeApp = self.data.recher_codeapoge(LECodeApp)
            if self.codeApp != "Nane":
                self.LECodeMa.setText(self.codeApp)
                self.signal_note.setText("ÇA EXISTE")
            elif self.codeApp == "Nane":
                self.LECodeMa.clear()
                self.signal_note.setText("N'EXISTE PAS")

    def ajouter_note(self):
        if self.producto[0] != '':
            LE_Matiere = self.LE_Matiere.text().upper()
            LECodeMa = self.LECodeMa.text().upper()
            LENoteMa = self.LENoteMa.text().upper()
            id_mat = self.producto[1]
            if LECodeMa != "" and LENoteMa != "" and LE_Matiere != "":
                self.data.insert_Note_By_Etudiant(id_mat, LECodeMa, LENoteMa)
                self.data.insert_Note_By_Matiere(id_mat, LECodeMa, LENoteMa)
                self.signal_note.setText("La note est bien ajoute")
                self.LENomMa.clear()
                self.LE_Matiere.clear()
                self.LECodeApp.clear()
                self.LECodeMa.clear()
                self.LENoteMa.clear()
            else:
                self.signal_note.setText("Veillez remplir tous les champs")

    def recherche_etudiant_moyenne(self):
        code_apoge = self.CodeApMoyenne.text().upper()
        self.affiche_moyenne(code_apoge)

    def affiche_moyenne(self, code_apoge):
        try:
            donnees = self.data.select_Etudiant(code_apoge)
            res = self.data.selectmoyene()
            self.label_moyennedesnotes.setText(str(res[0][0]))
            count = self.set_RowCount_Recherche(code_apoge)
            self.tableMoyenne.setRowCount(count)
            tablerow = 0
        except Exception as e:
            print(e)
        for row in donnees:
            q = str(self.data.calcule_moyenne(row[0]))
            self.tableMoyenne.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.tableMoyenne.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.tableMoyenne.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[3]))
            self.tableMoyenne.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[4]))
            self.tableMoyenne.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(row[2]))
            self.tableMoyenne.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(q))
            tablerow += 1

    def set_RowCount_Recherche(self, code_apoge):
        donnees = self.data.select_Etudiant(code_apoge)
        j = 0
        for i in donnees:
            j = j + 1
        return j
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mi_app = Gestion_Etudiants()
    mi_app.show()
    sys.exit(app.exec_())
