from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTranslator
import sys

from ui.mainwindow import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)

    from configparser import ConfigParser
    config = ConfigParser()
    config.read('config.ini')
    if config['DEFAULT']['i18n'] != 'English':
        from os import listdir
        from os.path import isfile, join
        mypath = 'src/ui/ui_files/'
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        files = list(filter(lambda f: f.endswith('.qm'), onlyfiles))
        files = list(map(lambda f: f[:-3], files))

        translators = []
        for f in files:
            translator = QTranslator()
            file = 'src/ui/ui_files/' + f
            translator.load(file)
            translators.append(translator)

        for t in translators:
            app.installTranslator(t)

        t = QTranslator()
        t.load('src/ui/mainwindow')
        app.installTranslator(t)

        settingTranslate = QTranslator()
        settingTranslate.load('src/ui/settingdialog_zh_CN')
        app.installTranslator(settingTranslate)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
