from lib import configsUI as ui


# Preparação
app = ui.QtWidgets.QApplication([])
# Execução
ui.loginVendedor.show()
app.exec()
