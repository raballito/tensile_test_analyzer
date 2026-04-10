# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 16:01:46 2026

Importation related function

Saving all informations about current sample.
Available functions:
-show_var()
-import_data() to import datas from the file to the structure
-export_preview() to export graphics and tables
-analyze() to analyze the samples with mode and geometry

Version: Beta 1.12
Last Update: 31.03.26

@author: quentin.raball
"""

import pandas as pd

def import_data(sample_struct):
    print(f"Importation des données de {sample_struct.sample_name}. Veuillez patienter...")

    # Lire tout le fichier, enlever les guillemets doubles, puis séparer chaque ligne par le séparateur
    with open(sample_struct.file_path, 'r', encoding='latin-1') as file:
        content = file.read().replace('"', '')
        lines = content.split('\n')

    # Convertir les lignes en une liste de listes en utilisant le séparateur
    data_list = [line.split(sample_struct.separator) for line in lines]
    raw_data = pd.DataFrame(data_list)
    data_width = raw_data.shape[1]
    if data_width < sample_struct.repeat_every:
        return

    force_column = sample_struct.force_channel - 1
    displacement_column = sample_struct.stroke_channel - 1
    time_column = sample_struct.time_channel - 1
    print(f"Taille actuelle du tableau de données brutes : {raw_data.shape}")

    # Extraction des données de force et de déplacement
    time_data = pd.to_numeric(raw_data.iloc[:, time_column], errors='coerce')
    force_data = pd.to_numeric(raw_data.iloc[:, force_column], errors='coerce')
    displacement_data = pd.to_numeric(raw_data.iloc[:, displacement_column], errors='coerce')
    
    # Créer le DataFrame avec les données
    data = pd.DataFrame({'Temps [s]': time_data, 'Force [N]': force_data, 'Déplacement [mm]': displacement_data})
    
    # Correction facteur force
    data['Force [N]'] = data['Force [N]'].apply(lambda x: x * sample_struct.force_unit)
    
    # Ajout de la normalisation des signaux et filtration des données de fin
    data.dropna(inplace=True)
    option_clean_end = sample_struct.master.get_option_filter()
    data = sample_struct.filter_pipeline.process(data, option_clean_end=option_clean_end, selected_channel=sample_struct.selected_channel)
    data.dropna(inplace=True)
    
    # Récupérer les valeurs
    sample_struct.time_values = data['Temps [s]'].tolist()
    sample_struct.force_values = data['Force [N]'].tolist()
    sample_struct.displacement_values = data['Déplacement [mm]'].tolist()
    sample_struct.F_max = sample_struct.format_sign(data['Force [N]'].max(), sample_struct.round_val)
    sample_struct.t_max = sample_struct.format_sign(data['Temps [s]'].max(), sample_struct.round_val)
    sample_struct.Allong = sample_struct.format_sign(data['Déplacement [mm]'].max() - data['Déplacement [mm]'].iloc[1], sample_struct.round_val)
    
    # Calcul des limites de la plage linéaire
    def_min = sample_struct.format_sign(float(sample_struct.F_max) * 0.2, sample_struct.round_val)
    def_max = sample_struct.format_sign(float(sample_struct.F_max) * 0.4, sample_struct.round_val)
    sample_struct.lin_range = [def_min, def_max]
    
    print(f"Nouvelle taille du tableau post-importation : {data.shape}")
    print(f"Importation des données spécifiques de {sample_struct.sample_name} terminée.\n")
    
    return sample_struct.time_values, sample_struct.force_values, sample_struct.displacement_values