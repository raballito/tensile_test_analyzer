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
                
        # Extenso
        extenso_data = pd.to_numeric(raw_data.iloc[:, self.sample.ext_channel - 1], errors='coerce') if self.sample.ext_channel else None
        # Créer le DataFrame avec les données
        data = pd.DataFrame({
            'Temps [s]': time_data,
            'Force [N]': force_data,
            'Déplacement [mm]': disp_data,
            'Extenso [mm]': extenso_data if extenso_data is not None else disp_data
        })
        data.dropna(inplace=True)
        print(f"Taille actuelle du tableau de données brutes : {raw_data.shape}")
        # Correction facteur force
        data['Force [N]'] = data['Force [N]'].apply(lambda x: x * self.sample.force_unit)

        print(f"Nouvelle taille du tableau post-importation : {data.shape}")
        print(f"Importation des données spécifiques de {self.sample.sample_name} terminée.\n")
        
        return data
    
    def process_data(self):
        """Applique filtre + sélection canal"""
        print("Application des filtres et sélection du canal")
        sample = self.sample
    
        # Récupère l'état actuel du filtre
        option_clean_end = sample.master.get_option_filter()
        
        # Si l'option filtre a changé, invalider les résultats
        if option_clean_end != sample.last_filter_state:
            print("Changement de l'état du filtre, invalidation des résultats.")
            sample.analyzed_sample = False  # Invalider les résultats existants
            sample.last_filter_state = option_clean_end  # Mettre à jour l'état du filtre
    
        # Charger les données brutes
        data = pd.DataFrame({
            'Temps [s]': sample.raw_time_values,
            'Force [N]': sample.raw_force_values,
            'Déplacement [mm]': sample.raw_displacement_values,
            'Extenso [mm]': sample.raw_extenso_displacement_values})
        
        # Appliquer le pipeline de filtrage
        data = sample.filter_pipeline.process(data, option_clean_end=option_clean_end, selected_channel=sample.selected_channel)
        data.dropna(inplace=True)
        
        self.update_disp_channel(data, sample)
        [self.sample.F_max, self.sample.t_max, self.sample.d_max] = self.get_max_raw_values(data)
        
        
        return sample.time_values, sample.force_values, sample.displacement_values
    
    def update_disp_channel(self, data, sample):
        # Mise à jour des données utilisées
        sample.time_values = data['Temps [s]'].tolist()
        sample.force_values = data['Force [N]'].tolist()
        sample.displacement_values = data['Déplacement [mm]'].tolist() if self.sample.selected_channel == "Canal Traverse" else data['Extenso [mm]'].tolist()
        if sample.selected_channel != sample.last_used_channel:
            # Invalider les résultats si le canal a changé
            sample.analyzed_sample = False
            sample.last_used_channel = sample.selected_channel
        return data
    
    def get_max_raw_values(self, data):
        # Détermination des premières valeurs max
        F_max = self.sample.format_sign(data['Force [N]'].max(), self.sample.round_val)
        t_max = self.sample.format_sign(data['Temps [s]'].max(), self.sample.round_val)
        d_max = self.sample.format_sign(data['Déplacement [mm]'].max() - data['Déplacement [mm]'].iloc[1], self.sample.round_val)
        
        return [F_max, t_max, d_max]
    
    
    