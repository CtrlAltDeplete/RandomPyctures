from HSV import HSVImage, generate_band
from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets


class UI:
    def __init__(self, HSV):
        # Flags for generation
        self.hue_changed = True
        self.previous_hue = None
        self.saturation_changed = True
        self.previous_saturation = None
        self.value_changed = True
        self.previous_value = None

        self.frame = HSV

        font_database = QtGui.QFontDatabase()
        font_id = font_database.addApplicationFont('Montserrat-Bold.ttf')
        font = QtGui.QFont('Montserrat')
        font.setPointSize(10)

        # HSV Image
        self.hsv = HSVImage(600, 400)
        self.image = None

        # HSV
        HSV.setObjectName("HSV")
        HSV.setStyleSheet(open("style.css").read())
        HSV.resize(600, 600)
        HSV.setMinimumSize(QtCore.QSize(600, 600))
        HSV.setMaximumSize(QtCore.QSize(600, 600))
        HSV.setBaseSize(QtCore.QSize(600, 600))

        # TOP THIRD
        # Grid Layout
        self.gridLayoutWidget = QtWidgets.QWidget(HSV)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(8, 0, 584, 158))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayoutWidget.mousePressEvent = self.mousePressEvent
        self.gridLayoutWidget.mouseMoveEvent = self.mouseMoveEvent
        self.gridLayout.setObjectName("gridLayout")

        # Close and Labels
        self.closeButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.closeButton.setMinimumSize(QtCore.QSize(20, 20))
        self.closeButton.setMaximumSize(QtCore.QSize(20, 20))
        self.closeButton.setObjectName("closeButton")
        self.closeButton.clicked.connect(self.close_button)
        self.gridLayout.addWidget(self.closeButton)

        self.treeLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.treeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.treeLabel.setObjectName("treeLabel")
        self.treeLabel.setFont(font)
        self.gridLayout.addWidget(self.treeLabel, 0, 1, 1, 1)

        self.shiftLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.shiftLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.shiftLabel.setObjectName("shiftLabel")
        self.shiftLabel.setFont(font)
        self.gridLayout.addWidget(self.shiftLabel, 0, 2, 1, 1)

        self.rangeLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.rangeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.rangeLabel.setObjectName("rangeLabel")
        self.rangeLabel.setFont(font)
        self.gridLayout.addWidget(self.rangeLabel, 0, 3, 1, 1)

        self.visibleLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.visibleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.visibleLabel.setObjectName("visibleLabel")
        self.visibleLabel.setFont(font)
        self.gridLayout.addWidget(self.visibleLabel, 0, 4, 1, 1)

        # Hue Elements
        self.hueLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.hueLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.hueLabel.setObjectName("hueLabel")
        self.hueLabel.setFont(font)
        self.gridLayout.addWidget(self.hueLabel, 1, 0, 1, 1)

        self.hueTreeButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.hueTreeButton.setObjectName("hueTreeButton")
        self.hueTreeButton.clicked.connect(lambda: self.new_hue_tree())
        self.gridLayout.addWidget(self.hueTreeButton, 1, 1, 1, 1)

        self.hueShiftSlider = QtWidgets.QSlider(self.gridLayoutWidget)
        self.hueShiftSlider.setMaximum(255)
        self.hueShiftSlider.setValue(self.hsv.hue["shift"])
        self.hueShiftSlider.setOrientation(QtCore.Qt.Horizontal)
        self.hueShiftSlider.setObjectName("hueShiftSlider")
        self.hueShiftSlider.valueChanged.connect(self.hue_shift_changed)
        self.hueShiftSlider.sliderReleased.connect(self.hue_shift_changed)
        self.gridLayout.addWidget(self.hueShiftSlider, 1, 2, 1, 1)

        self.hueRangeSlider = QtWidgets.QSlider(self.gridLayoutWidget)
        self.hueRangeSlider.setMaximum(255)
        self.hueRangeSlider.setValue(self.hsv.hue["range"])
        self.hueRangeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.hueRangeSlider.setObjectName("hueRangeSlider")
        self.hueRangeSlider.valueChanged.connect(self.hue_range_changed)
        self.hueRangeSlider.sliderReleased.connect(self.hue_range_changed)
        self.gridLayout.addWidget(self.hueRangeSlider, 1, 3, 1, 1)

        self.hueCheckbox = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.hueCheckbox.setEnabled(True)
        self.hueCheckbox.setChecked(True)
        self.hueCheckbox.setTristate(False)
        self.hueCheckbox.setObjectName("hueCheckbox")
        self.hueCheckbox.stateChanged.connect(lambda: self.hue_checkbox_changed())
        self.gridLayout.addWidget(self.hueCheckbox, 1, 4, 1, 1)

        # Saturation Elements
        self.saturationLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.saturationLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.saturationLabel.setObjectName("saturationLabel")
        self.saturationLabel.setFont(font)
        self.gridLayout.addWidget(self.saturationLabel, 2, 0, 1, 1)

        self.saturationTreeButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.saturationTreeButton.setObjectName("saturationTreeButton")
        self.saturationTreeButton.clicked.connect(self.new_saturation_tree)
        self.gridLayout.addWidget(self.saturationTreeButton, 2, 1, 1, 1)

        self.saturationShiftSlider = QtWidgets.QSlider(self.gridLayoutWidget)
        self.saturationShiftSlider.setMaximum(255)
        self.saturationShiftSlider.setValue(self.hsv.sat["shift"])
        self.saturationShiftSlider.setOrientation(QtCore.Qt.Horizontal)
        self.saturationShiftSlider.setObjectName("saturationShiftSlider")
        self.saturationShiftSlider.valueChanged.connect(self.saturation_shift_changed)
        self.saturationShiftSlider.sliderReleased.connect(self.saturation_shift_changed)
        self.gridLayout.addWidget(self.saturationShiftSlider, 2, 2, 1, 1)

        self.saturationRangeSlider = QtWidgets.QSlider(self.gridLayoutWidget)
        self.saturationRangeSlider.setMaximum(255)
        self.saturationRangeSlider.setValue(self.hsv.sat["range"])
        self.saturationRangeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.saturationRangeSlider.setObjectName("saturationRangeSlider")
        self.saturationRangeSlider.valueChanged.connect(self.saturation_range_changed)
        self.saturationRangeSlider.sliderReleased.connect(self.saturation_range_changed)
        self.gridLayout.addWidget(self.saturationRangeSlider, 2, 3, 1, 1)

        self.saturationCheckbox = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.saturationCheckbox.setEnabled(True)
        self.saturationCheckbox.setChecked(True)
        self.saturationCheckbox.setTristate(False)
        self.saturationCheckbox.setObjectName("saturationCheckbox")
        self.saturationCheckbox.stateChanged.connect(self.saturation_checkbox_changed)
        self.gridLayout.addWidget(self.saturationCheckbox, 2, 4, 1, 1)

        # Value Elements
        self.valueLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.valueLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.valueLabel.setObjectName("valueLabel")
        self.valueLabel.setFont(font)
        self.gridLayout.addWidget(self.valueLabel, 3, 0, 1, 1)

        self.valueTreeButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.valueTreeButton.setObjectName("valueTreeButton")
        self.valueTreeButton.clicked.connect(lambda: self.new_value_tree())
        self.gridLayout.addWidget(self.valueTreeButton, 3, 1, 1, 1)

        self.valueShiftSlider = QtWidgets.QSlider(self.gridLayoutWidget)
        self.valueShiftSlider.setMaximum(255)
        self.valueShiftSlider.setValue(self.hsv.val["shift"])
        self.valueShiftSlider.setOrientation(QtCore.Qt.Horizontal)
        self.valueShiftSlider.setObjectName("valueShiftSlider")
        self.valueShiftSlider.valueChanged.connect(self.value_shift_changed)
        self.valueShiftSlider.sliderReleased.connect(self.value_shift_changed)
        self.gridLayout.addWidget(self.valueShiftSlider, 3, 2, 1, 1)

        self.valueRangeSlider = QtWidgets.QSlider(self.gridLayoutWidget)
        self.valueRangeSlider.setMaximum(255)
        self.valueRangeSlider.setValue(self.hsv.val["range"])
        self.valueRangeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.valueRangeSlider.setObjectName("valueRangeSlider")
        self.valueRangeSlider.valueChanged.connect(self.value_range_changed)
        self.valueShiftSlider.sliderReleased.connect(self.value_shift_changed)
        self.gridLayout.addWidget(self.valueRangeSlider, 3, 3, 1, 1)

        self.valueCheckbox = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.valueCheckbox.setEnabled(True)
        self.valueCheckbox.setChecked(True)
        self.valueCheckbox.setTristate(False)
        self.valueCheckbox.setObjectName("valueCheckbox")
        self.valueCheckbox.stateChanged.connect(self.value_checkbox_changed)
        self.gridLayout.addWidget(self.valueCheckbox, 3, 4, 1, 1)

        # MIDDLE THIRD (Image)
        # Save image for displaying
        self.save()

        # Image Label
        self.image = QtWidgets.QLabel(HSV)
        self.image.setEnabled(True)
        self.image.setGeometry(QtCore.QRect(0, 160, 600, 400))
        self.image.setMinimumSize(QtCore.QSize(600, 400))
        self.image.setMaximumSize(QtCore.QSize(600, 400))
        self.image.setAutoFillBackground(True)
        self.image.setPixmap(QtGui.QPixmap("_temp.png"))
        self.image.setObjectName("image")
        self.image.show()

        # BOTTOM THIRD
        # Horizontal Layout
        self.horizontalLayoutWidget = QtWidgets.QWidget(HSV)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(8, 560, 584, 40))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # New Button
        self.newButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.newButton.setObjectName("newButton")
        self.newButton.clicked.connect(self.new_image)
        self.horizontalLayout.addWidget(self.newButton)

        # Name Entry
        self.nameEntry = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.nameEntry.setObjectName("nameEntry")
        self.nameEntry.setClearButtonEnabled(True)
        self.horizontalLayout.addWidget(self.nameEntry)

        # Save Button
        self.saveButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.saveButton.setObjectName("saveButton")
        self.saveButton.clicked.connect(lambda: self.save(self.nameEntry.text(), (1200, 800)))
        self.horizontalLayout.addWidget(self.saveButton)

        self.translate_ui(HSV)
        QtCore.QMetaObject.connectSlotsByName(HSV)

    def disable_gui(self):
        QtGui.QGuiApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

    def enable_gui(self):
        QtWidgets.QApplication.restoreOverrideCursor()

    def save(self, name="_temp", size=(600, 400)):
        visibility = (
            self.hueCheckbox.isChecked(),
            self.saturationCheckbox.isChecked(),
            self.valueCheckbox.isChecked()
        )
        color = self.hsv.hue, self.hsv.sat, self.hsv.val
        if size != (600, 400):
            self.disable_gui()
            bands = (generate_band(size[0], size[1], visibility[i], color[i]["tree"], color[i]["shift"],
                                   color[i]["range"]) for i in range(3))
            bands = list(bands)
        else:
            if self.hue_changed:
                self.previous_hue = generate_band(size[0], size[1], visibility[0], color[0]["tree"], color[0]["shift"],
                                                  color[0]["range"])
                self.hue_changed = False
            if self.saturation_changed:
                self.previous_saturation = generate_band(size[0], size[1], visibility[1], color[1]["tree"],
                                                         color[1]["shift"], color[1]["range"])
                self.saturation_changed = False
            if self.value_changed:
                self.previous_value = generate_band(size[0], size[1], visibility[2], color[2]["tree"],
                                                    color[2]["shift"], color[2]["range"])
                self.value_changed = False
            bands = [self.previous_hue, self.previous_saturation, self.previous_value]
        img = Image.merge("HSV", bands).convert("RGB")
        img.save(name + ".png", "PNG")
        if name == "_temp" and self.image:
            self.image.setPixmap(QtGui.QPixmap("_temp.png"))
        else:
            self.enable_gui()

    def new_hue_tree(self, save=True):
        self.disable_gui()
        self.hue_changed = True
        self.hsv._new_hue()
        self.hueShiftSlider.blockSignals(True)
        self.hueRangeSlider.blockSignals(True)
        self.hueShiftSlider.setValue(self.hsv.hue["shift"])
        self.hueRangeSlider.setValue(self.hsv.hue["range"])
        self.hueShiftSlider.blockSignals(False)
        self.hueRangeSlider.blockSignals(False)
        if save:
            self.save()
        self.enable_gui()

    def new_saturation_tree(self, save=True):
        self.disable_gui()
        self.saturation_changed = True
        self.hsv._new_sat()
        self.saturationShiftSlider.blockSignals(True)
        self.saturationRangeSlider.blockSignals(True)
        self.saturationShiftSlider.setValue(self.hsv.sat["shift"])
        self.saturationRangeSlider.setValue(self.hsv.sat["range"])
        self.saturationShiftSlider.blockSignals(False)
        self.saturationRangeSlider.blockSignals(False)
        if save:
            self.save()
        self.enable_gui()

    def new_value_tree(self, save=True):
        self.disable_gui()
        self.value_changed = True
        self.hsv._new_val()
        self.valueShiftSlider.blockSignals(True)
        self.valueRangeSlider.blockSignals(True)
        self.valueShiftSlider.setValue(self.hsv.val["shift"])
        self.valueShiftSlider.setValue(self.hsv.val["range"])
        self.valueShiftSlider.blockSignals(False)
        self.valueRangeSlider.blockSignals(False)
        if save:
            self.save()
        self.enable_gui()

    def hue_shift_changed(self):
        if self.hueShiftSlider.isSliderDown():
            return
        self.disable_gui()
        self.hue_changed = True
        self.hsv.hue["shift"] = self.hueShiftSlider.value()
        self.save()
        self.enable_gui()

    def hue_range_changed(self):
        if self.hueRangeSlider.isSliderDown():
            return
        self.disable_gui()
        self.hue_changed = True
        self.hsv.hue["range"] = self.hueRangeSlider.value()
        self.save()
        self.enable_gui()

    def saturation_shift_changed(self):
        if self.saturationShiftSlider.isSliderDown():
            return
        self.disable_gui()
        self.saturation_changed = True
        self.hsv.sat["shift"] = self.saturationShiftSlider.value()
        self.save()
        self.enable_gui()

    def saturation_range_changed(self):
        if self.saturationRangeSlider.isSliderDown():
            return
        self.disable_gui()
        self.saturation_changed = True
        self.hsv.sat["range"] = self.saturationRangeSlider.value()
        self.save()
        self.enable_gui()

    def value_shift_changed(self):
        if self.valueShiftSlider.isSliderDown():
            return
        self.disable_gui()
        self.value_changed = True
        self.hsv.val["shift"] = self.valueShiftSlider.value()
        self.save()
        self.enable_gui()

    def value_range_changed(self):
        if self.valueRangeSlider.isSliderDown():
            return
        self.disable_gui()
        self.value_changed = True
        self.hsv.val["range"] = self.valueRangeSlider.value()
        self.save()
        self.enable_gui()

    def hue_checkbox_changed(self):
        self.disable_gui()
        self.hue_changed = True
        self.save()
        self.enable_gui()

    def saturation_checkbox_changed(self):
        self.disable_gui()
        self.saturation_changed = True
        self.save()
        self.enable_gui()

    def value_checkbox_changed(self):
        self.disable_gui()
        self.value_changed = True
        self.save()
        self.enable_gui()

    def new_image(self):
        self.disable_gui()
        self.hue_changed, self.saturation_changed, self.value_changed = True, True, True
        self.new_hue_tree(False)
        self.new_saturation_tree(False)
        self.new_value_tree(False)
        self.save()
        self.enable_gui()

    def close_button(self):
        self.frame.close()

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()
        event.accept()

    def mouseMoveEvent(self, event):
        self.frame.move(self.frame.pos() + event.globalPos() - self.dragPos)
        self.dragPos = event.globalPos()
        event.accept()

    def translate_ui(self, HSV):
        _translate = QtCore.QCoreApplication.translate
        HSV.setWindowTitle(_translate("HSV", "HSV"))
        self.treeLabel.setText(_translate("HSV", "TREE"))
        self.valueLabel.setText(_translate("HSV", "VALUE"))
        self.saturationCheckbox.setText(_translate("HSV", "sat"))
        self.hueTreeButton.setText(_translate("HSV", "New"))
        self.rangeLabel.setText(_translate("HSV", "RANGE"))
        self.valueCheckbox.setText(_translate("HSV", "val"))
        self.hueCheckbox.setText(_translate("HSV", "hue"))
        self.hueLabel.setText(_translate("HSV", "HUE"))
        self.saturationLabel.setText(_translate("HSV", "SATURATION"))
        self.shiftLabel.setText(_translate("HSV", "SHIFT"))
        self.visibleLabel.setText(_translate("HSV", "VISIBLE"))
        self.valueTreeButton.setText(_translate("HSV", "New"))
        self.saturationTreeButton.setText(_translate("HSV", "New"))
        self.newButton.setText(_translate("HSV", "New Image"))
        self.saveButton.setText(_translate("HSV", "Save"))
        self.closeButton.setText(_translate("HSV", "x"))


if __name__ == "__main__":
    import atexit
    import os
    import sys
    app = QtWidgets.QApplication(sys.argv)
    HSV = QtWidgets.QWidget()
    HSV.setWindowFlag(QtCore.Qt.FramelessWindowHint)
    ui = UI(HSV)
    HSV.show()
    atexit.register(lambda: os.remove("_temp.png") if os.path.exists("_temp.png") else None)
    sys.exit(app.exec_())
