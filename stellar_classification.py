# -*- coding: utf-8 -*-
"""Stellar_classification.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1hexQyWMEBMCHh1I5muaK0NsyKAF1qnmO

Sujet Choisi : https://www.kaggle.com/datasets/fedesoriano/stellar-classification-dataset-sdss17

# But du modèle : apprendre a identifier la nature d'un astre avec 6 paramètres Système photométrique

Import des librairies necessaires
"""

from google.colab import files
import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
import csv
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical

"""**Entrées du dataset :**
1. obj_ID = Object Identifier, the unique value that identifies the object in the image catalog used by the CAS
2. alpha = Right Ascension angle (at J2000 epoch)
3. delta = Declination angle (at J2000 epoch)
4. u = Ultraviolet filter in the photometric system
5. g = Green filter in the photometric system
6. r = Red filter in the photometric system
7. i = Near Infrared filter in the photometric system
8. z = Infrared filter in the photometric system
9. run_ID = Run Number used to identify the specific scan
10. rereun_ID = Rerun Number to specify how the image was processed
11. cam_col = Camera column to identify the scanline within the run
12. field_ID = Field number to identify each field
13. spec_obj_ID = Unique ID used for optical spectroscopic objects (this means that 2 different observations with the same spec_obj_ID must share the output class)
14. class = object class (galaxy, star or quasar object)
15. redshift = redshift value based on the increase in wavelength
16. plate = plate ID, identifies each plate in SDSS
17. MJD = Modified Julian Date, used to indicate when a given piece of SDSS data was taken
18. fiber_ID = fiber ID that identifies the fiber that pointed the light at the focal plane in each observation

**Entrées à garder :**
1. u = Ultraviolet filter in the photometric system
2. g = Green filter in the photometric system
3. r = Red filter in the photometric system
4. i = Near Infrared filter in the photometric system
5. z = Infrared filter in the photometric system
7. class = object class (galaxy, star or quasar object)
6. redshift = redshift value based on the increase in wavelength

"""

uploadedFiles = files.upload()

csvfile = uploadedFiles['star_classification.csv'].decode('utf-8').splitlines()

#On prend uniquement 5000 ligne pour le moment
data = list(csv.reader(csvfile))[:5000]

for row in data[1:]:
    print(f"[{row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}, {row[5]}] = {row[6]}")

"""On converti le type de l'objet stellaire en numéro pour le modèle :"""

class_mapping = {"GALAXY": 0, "QSO": 1, "STAR": 2}

for row in data[1:]:
    row[6] = class_mapping[row[6]]


for row in data[1:]:
    print(f"[{row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}, {row[5]}] = {row[6]}")

"""Préparation des datas pour la construction du modèle"""

# Séparation des caractéristiques et de la classe d'objet
data = np.array(data[1:], dtype=float)
X = data[:, :-1]  # Caractéristque de l'objet celeste
y = to_categorical(data[:, -1])  # classe de l'objet


#Normalisation des datas entre 0 et 1 :

X = (X - np.min(X, axis=0)) / (np.max(X, axis=0) - np.min(X, axis=0))
print(X)

# 1. Define the model
model = Sequential()
model.add(Dense(32, input_shape=(6,), activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(3, activation='softmax'))

# 2. Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()
# 3. Train the model and store training history
history = model.fit(X, y, epochs=100, validation_split=0.2)

# 4. Evaluate the model
loss, accuracy = model.evaluate(X, y)
print(f'Loss: {loss}')
print(f'Accuracy: {accuracy}')

# Plot training & validation history
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Loss History')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Accuracy History')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

plt.tight_layout()
plt.show()