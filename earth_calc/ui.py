# -*- coding: utf-8 -*-

import os
import re

from PyQt5.QtWidgets import QMessageBox

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import (
	QVBoxLayout,
	QFormLayout,
	QHBoxLayout,
	QRadioButton,
	QLabel,
	QSpinBox,
	QComboBox,
	QDialogButtonBox,
	QDialog
)

class TestDialog(QDialog):
	def __init__(self, parent=None):
		super().__init__()

		## Create all Widgets first
		# Combo boxes 
		self.pointsComboBox = QComboBox()
		self.terrainComboBox = QComboBox()
		self.trackersComboBox = QComboBox()

		# Spin boxes
		self.minSpinBox = QSpinBox()
		self.maxSpinBox = QSpinBox()		
		self.pilesSpinBox = QSpinBox()		

		# Radio buttons [ created last bc radio.click() calls upon the above widgets ]
		self.createPointsButton = QRadioButton('Create Points')
		self.createPointsButton.toggled.connect(self.createPointsAction)
		self.createPointsButton.click()
		self.pointsFromLayerButton = QRadioButton('Points from Layer')
		self.pointsFromLayerButton.toggled.connect(self.pointsFromLayerAction)

		# Standard buttons and button box
		self.buttonBox = QDialogButtonBox()
		self.buttonBox.addButton('Ok',QDialogButtonBox.AcceptRole)
		self.buttonBox.addButton('Cancel',QDialogButtonBox.RejectRole)
		self.buttonBox.accepted.connect(self.okAction)
		self.buttonBox.rejected.connect(self.cancelAction)

		## Create and organize panels (layouts)
		# radio button panel
		radioPanel = QVBoxLayout()
		radioPanel.addWidget(self.createPointsButton)
		radioPanel.addWidget(self.pointsFromLayerButton)

		# spin box panels
		numPanel = QFormLayout()
		numPanel.addRow('Piles per Point',self.pilesSpinBox)
		numPanel.addRow('Min Reveal',self.minSpinBox)
		numPanel.addRow('Max Reveal',self.maxSpinBox)
		
		# combo box panel
		layerPanel = QFormLayout()
		layerPanel.addRow('Points',self.pointsComboBox)
		layerPanel.addRow('Terrain',self.terrainComboBox)
		layerPanel.addRow('Trackers',self.trackersComboBox)

		# standard button panel
		buttonPanel = QVBoxLayout()
		buttonPanel.addWidget(self.buttonBox)

		## put panels into layouts
		# left
		leftPanel = QVBoxLayout()
		leftPanel.addLayout(radioPanel)
		leftPanel.addLayout(numPanel)
		
		# right
		rightPanel = QVBoxLayout()
		rightPanel.addLayout(layerPanel)
		rightPanel.addLayout(buttonPanel)

		# merge
		layout = QHBoxLayout()
		layout.addLayout(leftPanel)
		layout.addLayout(rightPanel)
		
		# set
		self.setLayout(layout)

	# radio create Points toggle
	def createPointsAction(self):
		self.pointsComboBox.setDisabled(True)
		self.pointsComboBox.setCurrentText('')
		self.pilesSpinBox.setDisabled(False)

	# radio select Points layer toggle
	def pointsFromLayerAction(self):
		self.pointsComboBox.setDisabled(False)
		self.pilesSpinBox.setDisabled(True)
		self.pilesSpinBox.setValue(0)

	# called after Dialog creation in test.py (main).
	# qgis instance must exist
	def initComboBoxOptions(self, layers):
		layer_names = ['']
		for L in layers:
			layer_names.append(L)
		self.pointsComboBox.addItems(layer_names)
		self.terrainComboBox.addItems(layer_names)
		self.trackersComboBox.addItems(layer_names)

	# Organizes inputs into a dict variable
	def getVals(self):
		self.inputs = {
			'terrain_layer': self.terrainComboBox.currentText(),
			'trackers_layer': self.trackersComboBox.currentText(),
			'points_layer': self.pointsComboBox.currentText(),
			'num_piles': self.pilesSpinBox.value(),
			'max_reveal': self.maxSpinBox.value(),
			'min_reveal': self.minSpinBox.value(),
		}
		

	# Ensures all options are valid before moving along
	def validate(self):
		cond1 = ( self.inputs['num_piles'] > 0 ) | ( len(self.inputs['points_layer']) > 0 )
		cond2 = self.inputs['max_reveal'] > self.inputs['min_reveal']
		cond3 = len(self.inputs['terrain_layer']) > 0
		cond4 = len(self.inputs['trackers_layer']) > 0
		return cond1 & cond2 & cond3 & cond4

	# message displayed if inputs are not valid
	def invalidMessage(self):
		msg = QMessageBox(text='One or more inputs is missing or invalid!')
		msg.exec_()

	# action for Ok
	def okAction(self):
		self.getVals()
		if self.validate():
			self.accept()
		else:
			self.invalidMessage()
	
	# action for Cancel
	def cancelAction(self):
		self.close()

