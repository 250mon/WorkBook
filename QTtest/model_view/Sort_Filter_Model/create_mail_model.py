import sys
from PySide6.QtCore import (
    Qt, QAbstractItemModel, QDate, QTime, QDateTime,
    QObject
)
from PySide6.QtGui import QStandardItemModel


def add_mail(model: QAbstractItemModel, subject: str,
             sender: str, date: QDateTime):
    model.insertRow(0)
    model.setData(model.index(0, 0), subject)
    model.setData(model.index(0, 1), sender)
    model.setData(model.index(0, 2), date)

def create_mail_model(parent: QObject):
    model = QStandardItemModel(0, 3, parent)

    model.setHeaderData(0, Qt.Horizontal, QObject.tr("Subject"))
    model.setHeaderData(1, Qt.Horizontal, QObject.tr("Sender"))
    model.setHeaderData(2, Qt.Horizontal, QObject.tr("Date"))

    add_mail(model, "Happy New Year!", "Grace K. <grace@software-inc.com>",
            QDateTime(QDate(206, 12, 31), QTime(17, 3)))
    add_mail(model, "Radically new concept", "Grace K. <grace@software-inc.com>",
            QDateTime(QDate(206, 12, 22), QTime(9, 44)))
    add_mail(model, "Accounts", "pascale@nospam.com",
            QDateTime(QDate(206, 12, 31), QTime(12, 50)))
    add_mail(model, "Expenses", "Joe Bloggs <joe@bloggs.com>",
            QDateTime(QDate(206, 12, 25), QTime(11, 39)))
    add_mail(model, "Re: Expenses", "Andy <andy@nospam.com>",
            QDateTime(QDate(207, 1, 2), QTime(16, 5)))
    add_mail(model, "Re: Accounts", "Joe Bloggs <joe@bloggs.com>",
            QDateTime(QDate(207, 1, 3), QTime(14, 18)))
    add_mail(model, "Re: Accounts", "Andy <andy@nospam.com>",
            QDateTime(QDate(207, 1, 3), QTime(14, 26)))
    add_mail(model, "Sports", "Linda Smith <linda.smith@nospam.com>",
            QDateTime(QDate(207, 1, 5), QTime(11, 33)))
    add_mail(model, "AW: Sports", "Rolf Newschweinstein <rolfn@nospam.com>",
            QDateTime(QDate(207, 1, 5), QTime(12, 0)))
    add_mail(model, "RE: Sports", "Petra Schmidt <petras@nospam.com>",
            QDateTime(QDate(207, 1, 5), QTime(12, 1)))

    return model