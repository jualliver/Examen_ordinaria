from PySide6.QtWidgets import QApplication,QDialog,QMessageBox, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QHeaderView
from database import Database
from PySide6.QtGui import QAction

from afegir import Ui_Dialog
from modificar import Ui_Dialog1

import sys

class ProductApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestió de Productes")
        self.setGeometry(100, 100, 600, 500)
        self.db = Database()

        # Widget principal
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.layout = QVBoxLayout()
        main_widget.setLayout(self.layout)

        # Inputs per afegir i modificar
        barra_menus = self.menuBar()
        menu = barra_menus.addMenu("&Menu")
        accion1 = QAction("Nou Producte", self)
        accion1.triggered.connect(self.add_product)
        accion2 = QAction("Modificar Producte", self)
        accion2.triggered.connect(self.edit_product)
        menu.addAction(accion1)
        menu.addAction(accion2)


        self.edit_button = QPushButton("Eliminar Producte")
        self.edit_button.clicked.connect(self.dialogo_eliminar)
        self.layout.addWidget(self.edit_button)

        # Taula de productes
        self.table = self.create_table()
        self.layout.addWidget(self.table)

        self.load_products()

    def create_table(self):
        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Nom", "Preu", "Categoria"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        return table

    def load_products(self):
        self.table.setRowCount(0)
        products = self.db.get_products()
        for row_index, (product_id, name, price, category) in enumerate(products):
            self.table.insertRow(row_index)
            self.table.setItem(row_index, 0, QTableWidgetItem(name))
            self.table.setItem(row_index, 1, QTableWidgetItem(price))
            self.table.setItem(row_index, 2, QTableWidgetItem(category))

    def add_product(self):
        dialog = Nuevo_product()
        dialog.exec_()

        name = dialog.lineEdit.text()
        price = dialog.lineEdit_2.text()
        category = dialog.lineEdit_3.text()

        if name and price and category:
            self.db.add_product(name, price, category)
            self.load_products()

    def edit_product(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            return

        current_name = self.table.item(selected_row, 0).text()
        current_price = self.table.item(selected_row, 1).text()
        current_category = self.table.item(selected_row, 2).text()

        dialog = update_product()
        product_id = self.db.get_products()[selected_row][0]
        new_name = dialog.lineEdit.setText(current_name)
        new_price = dialog.lineEdit_2.setText(current_price)
        new_category = dialog.lineEdit_3.setText(current_category)
        dialog.exec_()

        new_name = dialog.lineEdit.text()
        new_price = dialog.lineEdit_2.text()
        new_category = dialog.lineEdit_3.text()

        if new_name and new_price and new_category and self.dialogo_editar()==True:
            self.db.update_product(product_id, new_name, new_price, new_category)
            self.load_products()

    def delete_product(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            return

        product_id = self.db.get_products()[selected_row][0]
        self.db.delete_product(product_id)
        self.load_products()

    def dialogo_eliminar(self):
            boton_pulsado = QMessageBox.critical(
                self,
                "Advertencia",
                "Estas seguro que quieres eliminar el Producto?",
                buttons=QMessageBox.Cancel | QMessageBox.Ok ,
                defaultButton=QMessageBox.Ok
            )

            if boton_pulsado == QMessageBox.Ok:
                self.delete_product()
            elif boton_pulsado == QMessageBox.Cancel:
                pass
    
    def dialogo_editar(self):
            boton_pulsado = QMessageBox.information(
                self,
                "Advertencia",
                "Estas seguro que quieres Aplicar estos cambios?",
                buttons=QMessageBox.Cancel | QMessageBox.Save ,
                defaultButton=QMessageBox.Save
            )

            if boton_pulsado == QMessageBox.Save:
                return True
            elif boton_pulsado == QMessageBox.Cancel:
                pass



class Nuevo_product(QDialog,Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.close)

class update_product(QDialog,Ui_Dialog1):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.close)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProductApp()
    window.show()
    sys.exit(app.exec())
