# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 16:01:46 2026

Data Manipulation class:
- Importation related function
- Transform datas


Version: Beta 1.12
Last Update: 31.03.26

@author: quentin.raball
"""

import pandas as pd

class DataManipulation:
    def __init__(self, sample_struct):
        self.sample = sample_struct
        self.deformation_values = []
        
    
    def import_data(self):
        print(f"Importation des données de {self.sample.sample_name}. Veuillez patienter...")
    
        # Lire tout le fichier, enlever les guillemets doubles, puis séparer chaque ligne par le séparateur
        with open(self.sample.file_path, 'r', encoding='latin-1') as file:
            content = file.read().replace('"', '')
            lines = content.split('\n')
    
        # Convertir les lignes en une liste de listes en utilisant le séparateur
        data_list = [line.split(self.sample.separator) for line in lines]
        raw_data = pd.DataFrame(data_list)
        data_width = raw_data.shape[1]
        if data_width < self.sample.repeat_every:
            return
    
        force_column = self.sample.force_channel - 1
        displacement_column = self.sample.stroke_channel - 1
        time_column = self.sample.time_channel - 1
        print(f"Taille actuelle du tableau de données brutes : {raw_data.shape}")
    
        # Extraction des données de force et de déplacement
        time_data = pd.to_numeric(raw_data.iloc[:, time_column], errors='coerce')
        force_data = pd.to_numeric(raw_data.iloc[:, force_column], errors='coerce')
        displacement_data = pd.to_numeric(raw_data.iloc[:, displacement_column], errors='coerce')
        
        # Créer le DataFrame avec les données
        data = pd.DataFrame({'Temps [s]': time_data, 'Force [N]': force_data, 'Déplacement [mm]': displacement_data})
        
        # Correction facteur force
        data['Force [N]'] = data['Force [N]'].apply(lambda x: x * self.sample.force_unit)
        
        # Ajout de la normalisation des signaux et filtration des données de fin
        data.dropna(inplace=True)
        option_clean_end = self.sample.master.get_option_filter()
        data = self.sample.filter_pipeline.process(data, option_clean_end=option_clean_end, selected_channel=self.sample.selected_channel)
        data.dropna(inplace=True)
        
        # Récupérer les valeurs
        self.sample.time_values = data['Temps [s]'].tolist()
        self.sample.force_values = data['Force [N]'].tolist()
        self.sample.displacement_values = data['Déplacement [mm]'].tolist()
        self.sample.F_max = self.sample.format_sign(data['Force [N]'].max(), self.sample.round_val)
        self.sample.t_max = self.sample.format_sign(data['Temps [s]'].max(), self.sample.round_val)
        self.sample.Allong = self.sample.format_sign(data['Déplacement [mm]'].max() - data['Déplacement [mm]'].iloc[1], self.sample.round_val)
        
        # Calcul des limites de la plage linéaire
        def_min = self.sample.format_sign(float(self.sample.F_max) * 0.2, self.sample.round_val)
        def_max = self.sample.format_sign(float(self.sample.F_max) * 0.4, self.sample.round_val)
        self.sample.lin_range = [def_min, def_max]
        
        print(f"Nouvelle taille du tableau post-importation : {data.shape}")
        print(f"Importation des données spécifiques de {self.sample.sample_name} terminée.\n")
        
        return self.sample.time_values, self.sample.force_values, self.sample.displacement_values
    
    
    def convert_deformation(self, original_defo_values):
        """ Conversion de la déformation en fonction de l'option choisie (pourcentage ou [-]) """
        defo_percent = self.sample.master.get_option_defo_percent()
        print(f"Etat de la case défo_percent : {defo_percent}")
        if defo_percent:  # Si l'option pourcentage est sélectionnée
            return original_defo_values
        else:  # Sinon, on utilise les valeurs sans unités [-]
            return [defo / 100 for defo in original_defo_values]