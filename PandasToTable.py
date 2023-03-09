"""
    No se maltrataron pandas creando este código!!!
    PandasToTable rellena tablas con pandas dataframe

    Ejemplo de Uso:
        dataFrame = pd.DataFrame(diccionario)
        model = PandasModel(dataFrame)
        tableView.setModel(model)

"""
# Se agregaron metodos de ordenación a los modelados que no lo tenian
# Se agregan clases para llenar table view con pandas dataframe
import sys
#from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QToolBar, QGroupBox, QLineEdit, QGridLayout, QLabel
from PyQt5 import QtCore, Qt
from PyQt5.Qt import *
from PyQt5.QtWidgets import *
import numpy as np
import pandas as pd #run pip install pandas

class PandasModel(QtCore.QAbstractTableModel):
    """
        Class to populate a table view with a pandas dataframe
        muestra indices y soporta ordenar por columnas
    """
    def __init__(self, df = pd.DataFrame(), parent=None): 
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self._df = df.copy()

    def toDataFrame(self):
        return self._df.copy()

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if orientation == QtCore.Qt.Horizontal:
            try:
                return self._df.columns.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()
        elif orientation == QtCore.Qt.Vertical:
            try:
                # return self.df.index.tolist()
                return self._df.index.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if not index.isValid():
            return QtCore.QVariant()

        return QtCore.QVariant(str(self._df.iloc[index.row(), index.column()]))
        
    def setData(self, index, value, role):
        row = self._df.index[index.row()]
        col = self._df.columns[index.column()]
        if hasattr(value, 'toPyObject'):
            # PyQt4 gets a QVariant
            value = value.toPyObject()
        else:
            # PySide gets an unicode
            dtype = self._df[col].dtype
            if dtype != object:
                value = None if value == '' else dtype.type(value)
        self._df.set_value(row, col, value)
        return True

    def rowCount(self, parent=QtCore.QModelIndex()): 
        return len(self._df.index)

    def columnCount(self, parent=QtCore.QModelIndex()): 
        return len(self._df.columns)

    def sort(self, column, order):
        colname = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(colname, ascending= order == QtCore.Qt.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()

class DataFrameModel(QtCore.QAbstractTableModel):
    """
        Class to populate a table view with a pandas dataframe
        muestra indices y soporta ordenar por columnas
    """
    DtypeRole = QtCore.Qt.UserRole + 1000
    ValueRole = QtCore.Qt.UserRole + 1001

    def __init__(self, df=pd.DataFrame(), parent=None):
        super(DataFrameModel, self).__init__(parent)
        self._dataframe = df

    def setDataFrame(self, dataframe):
        self.beginResetModel()
        self._dataframe = dataframe.copy()
        self.endResetModel()

    def dataFrame(self):
        return self._dataframe

    dataFrame = QtCore.pyqtProperty(pd.DataFrame, fget=dataFrame, fset=setDataFrame)

    @QtCore.pyqtSlot(int, QtCore.Qt.Orientation, result=str)
    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self._dataframe.columns[section]
            else:
                return str(self._dataframe.index[section])
        return QtCore.QVariant()

    def rowCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0
        return len(self._dataframe.index)

    def columnCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0
        return self._dataframe.columns.size

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < self.rowCount() \
            and 0 <= index.column() < self.columnCount()):
            return QtCore.QVariant()
        row = self._dataframe.index[index.row()]
        col = self._dataframe.columns[index.column()]
        dt = self._dataframe[col].dtype

        val = self._dataframe.iloc[row][col]
        if role == QtCore.Qt.DisplayRole:
            return str(val)
        elif role == DataFrameModel.ValueRole:
            return val
        if role == DataFrameModel.DtypeRole:
            return dt
        return QtCore.QVariant()

    def roleNames(self):
        roles = {
            QtCore.Qt.DisplayRole: b'display',
            DataFrameModel.DtypeRole: b'dtype',
            DataFrameModel.ValueRole: b'value'
        }
        return roles

    def sort(self, column, order):
        colname = self._dataframe.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._dataframe.sort_values(colname, ascending= order == QtCore.Qt.AscendingOrder, inplace=True)
        self._dataframe.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()

class PandasModel3(QtCore.QAbstractTableModel):
    """
        Class to populate a table view with a pandas dataframe
        no muestra indices pero soporta ordenar por columnas
    """
    def __init__(self, data):
        QtCore.QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

    def sort(self, column, order):
        colname = self._data.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._data.sort_values(colname, ascending= order == QtCore.Qt.AscendingOrder, inplace=True)
        self._data.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()

class PandasModel4(QtCore.QAbstractTableModel):
    """
        Class to populate a table view with a pandas dataframe
        no muestra indices pero soporta ordenar por columnas
    """
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return str(self._data.iloc[index.row()][index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._data.columns[col]
        return None

    def sort(self, column, order):
        colname = self._data.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._data.sort_values(colname, ascending= order == QtCore.Qt.AscendingOrder, inplace=True)
        self._data.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()

class NumpyArrayModel(QtCore.QAbstractTableModel):
    """
    Class to populate a table view with a Numpy.array
    """
    def __init__(self, array, headers, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self._array = array
        self._headers = headers
        self.r, self.c = np.shape(self.array)

    @property
    def array(self):
        return self._array

    @property
    def headers(self):
        return self._headers

    def rowCount(self, parent=QtCore.QModelIndex()):
        return self.r

    def columnCount(self, parent=QtCore.QModelIndex()):
        return self.c

    def headerData(self, p_int, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                if p_int < len(self.headers):
                    return self.headers[p_int]
            elif orientation == QtCore.Qt.Vertical:
                return p_int + 1
        return

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        row = index.row()
        column = index.column()
        if row < 0 or row >= self.rowCount():
            return None
        if column < 0 or column >= self.columnCount():
            return None
        if role == QtCore.Qt.DisplayRole:
            return float(self.array[row, column])
        return None

    def setData(self, index, value, role):
        if not index.isValid():
            return False
        if role != QtCore.Qt.EditRole:
            return False
        row = index.row()
        column = index.column()
        if row < 0 or row >= self.rowCount():
            return False
        if column < 0 or column >= self.columnCount():
            return False
        self.array.values[row][column] = value
        self.dataChanged.emit(index, index)
        return True

    def sort(self, column, order):
        self.layoutAboutToBeChanged.emit()
        argsort = self.array[:, column].argsort()
        if order == QtCore.Qt.DescendingOrder:
            argsort = argsort[::-1]
        self._array = self.array[argsort]
        self.layoutChanged.emit()

class PandasModel5(QtCore.QAbstractTableModel):
    """
        Class to populate a table view with a pandas dataframe
        muestra indices pero no soporta ordenar por columnas
    """
    def __init__(self, df = pd.DataFrame(), parent=None): 
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self._df = df.copy()

    def toDataFrame(self):
        return self._df.copy()

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if orientation == QtCore.Qt.Horizontal:
            try:
                return self._df.columns.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()
        elif orientation == QtCore.Qt.Vertical:
            try:
                # return self.df.index.tolist()
                return self._df.index.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if not index.isValid():
            return QtCore.QVariant()

        return QtCore.QVariant(str(self._df.iloc[index.row(), index.column()]))
        
    def setData(self, index, value, role):
        row = self._df.index[index.row()]
        col = self._df.columns[index.column()]
        if hasattr(value, 'toPyObject'):
            # PyQt4 gets a QVariant
            value = value.toPyObject()
        else:
            # PySide gets an unicode
            dtype = self._df[col].dtype
            if dtype != object:
                value = None if value == '' else dtype.type(value)
        self._df.set_value(row, col, value)
        return True

    def rowCount(self, parent=QtCore.QModelIndex()): 
        return len(self._df.index)

    def columnCount(self, parent=QtCore.QModelIndex()): 
        return len(self._df.columns)    