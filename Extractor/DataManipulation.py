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
    def __init__(self, sample):
        self.sample = sample
        
    
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
    
        # Colonnes
        time_col = self.sample.time_channel - 1
        force_col = self.sample.force_channel - 1
        disp_col = self.sample.stroke_channel - 1
    
        time_data = pd.to_numeric(raw_data.iloc[:, time_col], errors='coerce')
        force_data = pd.to_numeric(raw_data.iloc[:, force_col], errors='coerce')
        disp_data = pd.to_numeric(raw_data.iloc[:, disp_col], errors='coerce')
        
        print(f"Canal Extenso: {self.sample.ext_channel}")
        
        # Extenso
        if self.sample.ext_channel is not None:
            ext_col = self.sample.ext_channel - 1
            ext_data = pd.to_numeric(raw_data.iloc[:, ext_col], errors='coerce')
       
        # Créer le DataFrame avec les données
        data = pd.DataFrame({'Temps [s]': time_data, 'Force [N]': force_data, 'Déplacement [mm]': disp_data, "Extenso [mm]": ext_data})
        print(f"Taille actuelle du tableau de données brutes : {raw_data.shape}")
        
        # Correction facteur force
        data['Force [N]'] = data['Force [N]'].apply(lambda x: x * self.sample.force_unit)
        
        # Récupérer les valeurs
        self.sample.raw_time_values = data['Temps [s]'].tolist()
        self.sample.raw_force_values = data['Force [N]'].tolist()
        self.sample.raw_displacement_values = data['Déplacement [mm]'].tolist()
        self.sample.raw_extenso_displacement_values = data['Extenso [mm]'].tolist()
        self.sample.F_max = self.sample.format_sign(data['Force [N]'].max(), self.sample.round_val)
        self.sample.t_max = self.sample.format_sign(data['Temps [s]'].max(), self.sample.round_val)
        self.sample.d_max = self.sample.format_sign(data['Déplacement [mm]'].max() - data['Déplacement [mm]'].iloc[1], self.sample.round_val)
        
        # Calcul des limites de la plage linéaire
        def_min = self.sample.format_sign(float(self.sample.F_max) * 0.2, self.sample.round_val)
        def_max = self.sample.format_sign(float(self.sample.F_max) * 0.4, self.sample.round_val)
        self.sample.lin_range = [def_min, def_max]
        
        print(f"Nouvelle taille du tableau post-importation : {data.shape}")
        print(f"Importation des données spécifiques de {self.sample.sample_name} terminée.\n")
        
        return self.sample.raw_time_values, self.sample.raw_force_values, self.sample.raw_displacement_values, self.sample.raw_extenso_displacement_values
    
    def process_data(self):
        """Applique filtre + sélection canal"""
        print("Application des filtres et sélection du canal")
        sample = self.sample
    
        data = pd.DataFrame({
            'Temps [s]': sample.raw_time_values,
            'Force [N]': sample.raw_force_values,
            'Déplacement [mm]': sample.raw_displacement_values,
            'Extenso [mm]' : sample.raw_extenso_displacement_values
        })
    
        data.dropna(inplace=True)
    
        option_clean_end = sample.master.get_option_filter()
    
        data = sample.filter_pipeline.process(
            data,
            option_clean_end=option_clean_end,
            selected_channel=sample.selected_channel
        )
    
        data.dropna(inplace=True)
    
        # Mise à jour des données utilisées
        sample.time_values = data['Temps [s]'].tolist()
        sample.force_values = data['Force [N]'].tolist()
        sample.displacement_values = data['Déplacement [mm]'].tolist() if self.sample.selected_channel == "Canal Traverse" else data['Extenso [mm]'].tolist()
        self.sample.analyzed_sample = False
        
        return sample.time_values, sample.force_values, sample.displacement_values
    
    def convert_deformation(self, original_defo_values):
        """ Conversion de la déformation en fonction de l'option choisie (pourcentage ou [-]) """
        defo_percent = self.sample.master.get_option_defo_percent()
        if defo_percent:  # Si l'option pourcentage est sélectionnée
            return original_defo_values
        else:  # Sinon, on utilise les valeurs sans unités [-]
            return [defo / 100 for defo in original_defo_values]