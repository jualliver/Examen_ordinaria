import bcrypt
import os

from PySide6.QtSql import QSqlQuery

from afegir import Ui_Dialog
from database import Database


def test_new_Product(qtbot):
    database_path = os.path.join(os.path.dirname(__file__), 'products.db')

    product = Ui_Dialog(database_path)    
    qtbot.addWidget(product)

    # Omple els camps de text
    producte= 'huevo'
    qtbot.keyClicks(product.lineEdit, producte)
    preu= 'password3'
    qtbot.keyClicks(product.lineEdit_2, preu)
    categoria= 'cogelat'
    qtbot.keyClicks(product.lineEdit_3, categoria)

    product.db.create_table()

    product.pushButton.click()

    if product.db.open():
        query = QSqlQuery()
        query.prepare("SELECT name, price, category FROM products WHERE name = ?")
        query.addBindValue(producte)
        query.exec()
        query.next()
        user_db = query.value(0)
        hashed_password_db = query.value(1)

        # assert bcrypt.checkpw(password_db.encode('utf-8'), hashed_password.encode('utf-8')):
        assert user_db == producte
        assert bcrypt.checkpw(preu.encode('utf-8'), hashed_password_db.encode('utf-8'))

    os.remove(database_path)