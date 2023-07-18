from simpful import *

FS = FuzzySystem()

# SPO2 - Input
SPO2_1 = FuzzySet(function=Trapezoidal_MF(a=85, b=85, c=90, d=92.5), term="Rendah")
SPO2_2 = FuzzySet(function=Triangular_MF(a=90, b=92.5, c=95), term="Kurang")
SPO2_3 = FuzzySet(function=Trapezoidal_MF(a=92.5, b=95, c=100, d=100), term="Normal")
FS.add_linguistic_variable("SPO2", LinguisticVariable([SPO2_1, SPO2_2, SPO2_3], concept="Saturasi Oksigen", universe_of_discourse=[85, 100]))

# BPM - Input
BPM_1 = FuzzySet(function=Trapezoidal_MF(a=50, b=50, c=60, d=80), term="Rendah")
BPM_2 = FuzzySet(function=Triangular_MF(a=60, b=80, c=100), term="Normal")
BPM_3 = FuzzySet(function=Trapezoidal_MF(a=80, b=100, c=110, d=110), term="Tinggi")
FS.add_linguistic_variable("BPM", LinguisticVariable([BPM_1, BPM_2, BPM_3], concept="Denyut Nadi", universe_of_discourse=[50, 110]))

# TEMP - Input
TEMP_1 = FuzzySet(function=Trapezoidal_MF(a=35, b=35, c=35.5, d=36.5), term="Rendah")
TEMP_2 = FuzzySet(function=Triangular_MF(a=35.5, b=36.5, c=37.5), term="Normal")
TEMP_3 = FuzzySet(function=Trapezoidal_MF(a=36.5, b=37.5, c=38, d=38), term="Tinggi")
FS.add_linguistic_variable("TEMP", LinguisticVariable([TEMP_1, TEMP_2, TEMP_3], concept="Suhu Tubuh", universe_of_discourse=[35, 38]))

# Hipoksemia - Output
H_1 = FuzzySet(function=Trapezoidal_MF(a=0, b=0, c=0.2, d=0.4), term="Berat")
H_2 = FuzzySet(function=Triangular_MF(a=0.2, b=0.4, c=0.6), term="Sedang")
H_3 = FuzzySet(function=Triangular_MF(a=0.4, b=0.6, c=0.8), term="Ringan")
H_4 = FuzzySet(function=Trapezoidal_MF(a=0.6, b=0.8, c=1, d=1), term="Sehat")
FS.add_linguistic_variable("Hipoksemia", LinguisticVariable([H_1, H_2, H_3, H_4], universe_of_discourse=[0, 1]))

# Rules
R1 = "IF (SPO2 IS Rendah) AND (BPM IS Rendah) AND (TEMP IS Rendah) THEN (Hipoksemia IS Berat)"
R2 = "IF (SPO2 IS Rendah) AND (BPM IS Rendah) AND (TEMP IS Normal) THEN (Hipoksemia IS Berat)"
R3 = "IF (SPO2 IS Rendah) AND (BPM IS Rendah) AND (TEMP IS Tinggi) THEN (Hipoksemia IS Berat)"
R4 = "IF (SPO2 IS Rendah) AND (BPM IS Normal) AND (TEMP IS Rendah) THEN (Hipoksemia IS Berat)"
R5 = "IF (SPO2 IS Rendah) AND (BPM IS Normal) AND (TEMP IS Normal) THEN (Hipoksemia IS Berat)"
R6 = "IF (SPO2 IS Rendah) AND (BPM IS Normal) AND (TEMP IS Tinggi) THEN (Hipoksemia IS Berat)"
R7 = "IF (SPO2 IS Rendah) AND (BPM IS Tinggi) AND (TEMP IS Rendah) THEN (Hipoksemia IS Berat)"
R8 = "IF (SPO2 IS Rendah) AND (BPM IS Tinggi) AND (TEMP IS Normal) THEN (Hipoksemia IS Berat)"
R9 = "IF (SPO2 IS Rendah) AND (BPM IS Tinggi) AND (TEMP IS Tinggi) THEN (Hipoksemia IS Berat)"

R10 = "IF (SPO2 IS Kurang) AND (BPM IS Rendah) AND (TEMP IS Rendah) THEN (Hipoksemia IS Sedang)"
R11 = "IF (SPO2 IS Kurang) AND (BPM IS Rendah) AND (TEMP IS Normal) THEN (Hipoksemia IS Ringan)"
R12 = "IF (SPO2 IS Kurang) AND (BPM IS Rendah) AND (TEMP IS Tinggi) THEN (Hipoksemia IS Sedang)"
R13 = "IF (SPO2 IS Kurang) AND (BPM IS Normal) AND (TEMP IS Rendah) THEN (Hipoksemia IS Sedang)"
R14 = "IF (SPO2 IS Kurang) AND (BPM IS Normal) AND (TEMP IS Normal) THEN (Hipoksemia IS Ringan)"
R15 = "IF (SPO2 IS Kurang) AND (BPM IS Normal) AND (TEMP IS Tinggi) THEN (Hipoksemia IS Sedang)"
R16 = "IF (SPO2 IS Kurang) AND (BPM IS Tinggi) AND (TEMP IS Rendah) THEN (Hipoksemia IS Sedang)"
R17 = "IF (SPO2 IS Kurang) AND (BPM IS Tinggi) AND (TEMP IS Normal) THEN (Hipoksemia IS Ringan)"
R18 = "IF (SPO2 IS Kurang) AND (BPM IS Tinggi) AND (TEMP IS Tinggi) THEN (Hipoksemia IS Sedang)"

R19 = "IF (SPO2 IS Normal) AND (BPM IS Rendah) AND (TEMP IS Rendah) THEN (Hipoksemia IS Sehat)"
R20 = "IF (SPO2 IS Normal) AND (BPM IS Rendah) AND (TEMP IS Normal) THEN (Hipoksemia IS Sehat)"
R21 = "IF (SPO2 IS Normal) AND (BPM IS Rendah) AND (TEMP IS Tinggi) THEN (Hipoksemia IS Sehat)"
R22 = "IF (SPO2 IS Normal) AND (BPM IS Normal) AND (TEMP IS Rendah) THEN (Hipoksemia IS Sehat)"
R23 = "IF (SPO2 IS Normal) AND (BPM IS Normal) AND (TEMP IS Normal) THEN (Hipoksemia IS Sehat)"
R24 = "IF (SPO2 IS Normal) AND (BPM IS Normal) AND (TEMP IS Tinggi) THEN (Hipoksemia IS Sehat)"
R25 = "IF (SPO2 IS Normal) AND (BPM IS Tinggi) AND (TEMP IS Rendah) THEN (Hipoksemia IS Sehat)"
R26 = "IF (SPO2 IS Normal) AND (BPM IS Tinggi) AND (TEMP IS Normal) THEN (Hipoksemia IS Sehat)"
R27 = "IF (SPO2 IS Normal) AND (BPM IS Tinggi) AND (TEMP IS Tinggi) THEN (Hipoksemia IS Sehat)"

FS.add_rules([R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27])

# Set input
spo2 = 93
bpm = 109
temp = 36.21

FS.set_variable("SPO2", spo2)
FS.set_variable("BPM", bpm)
FS.set_variable("TEMP", temp)

result = FS.Mamdani_inference(["Hipoksemia"])
rsget = result.get('Hipoksemia')
print('{0:.3f}'.format(rsget))