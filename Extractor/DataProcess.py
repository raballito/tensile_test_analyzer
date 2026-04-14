# -*- coding: utf-8 -*-
"""
Data Filter
- Supression of useless data
- Transform negatives data into positives one

Version: Beta 1.13
Last Update: 10.04.26

@author: quentin.raball
"""

# Importation des modules
import numpy as np
from tkinter import messagebox

class ProcessData:
    def __init__(self,
                 normalize=True,
                 method="mixed",
                 smooth_window=5):

        self.normalize = normalize
        self.method = method
        self.smooth_window = smooth_window

    def process(self, data, option_clean_end=False, selected_channel=None):
        """
        Pipeline principal
        """

        if self.normalize:
            data = self.normalize_signals(data)

        if option_clean_end:
            data = self.clean_end_of_test(
                data,
                selected_channel=selected_channel,
                method=self.method,
                smooth_window=self.smooth_window
            )

        return data

    
    def normalize_signals(self, data):
        """
        Cette fonction normalise les signaux de force et de déplacement si nécessaire
        en fonction du signe moyen des données (force et déplacement).
        """
    
        # Convertir les listes en tableaux numpy pour faciliter le calcul
        force = data['Force [N]']
        disp = data['Déplacement [mm]']
        
        n = len(force)
        if n < 10:
            return data
    
        start_index = int(0.1 * n)
    
        force_sub = force.iloc[start_index:]
        disp_sub = disp.iloc[start_index:]
        
        # sécurité
        if force_sub.abs().max() < 1:
            print("Signal trop faible pour normalisation")
            return data
        
        # méthode robuste : proportion de valeurs négatives
        neg_force_ratio = (force_sub < 0).mean()
        neg_disp_ratio = (disp_sub < 0).mean()
    
        if neg_force_ratio > 0.5:
            data['Force [N]'] = -data['Force [N]']
            print("Inversion des valeurs de force (majorité négative).")
    
        if neg_disp_ratio > 0.5:
            data['Déplacement [mm]'] = -data['Déplacement [mm]']
            print("Inversion des valeurs de déplacement (majorité négative).")
    
        return data
            
    def clean_end_of_test(self, data, selected_channel=None, method="mixed", last_n_points=300, slope_threshold=-1000, drop_ratio=0.5, smooth_window=5):
        """
        Nettoie la fin d'un essai en supprimant la chute brutale de force.
    
        Parameters:
        - method: "slope", "drop", ou "mixed"
        - last_n_points: nombre de points analysés en fin de courbe
        - slope_threshold: seuil de dérivée (N/s)
        - drop_ratio: ratio de chute par rapport à Fmax (ex: 0.3 = 30%)
        - smooth_window: taille du lissage
    
        Returns:
        - DataFrame nettoyé
        """
    
        data = data.copy()
    
        # Lissage (optionnel mais recommandé)
        if smooth_window > 1:
            data['Force Smoothed'] = data['Force [N]'].rolling(window=smooth_window, center=True).mean()
        else:
            data['Force Smoothed'] = data['Force [N]']
    
        # Calcul dérivée
        data['Force Change [N/s]'] = data['Force Smoothed'].diff() / data['Temps [s]'].diff()
    
        # Nettoyage
        data.replace([np.inf, -np.inf], np.nan, inplace=True)
        data.dropna(subset=['Force Change [N/s]'], inplace=True)
    
        # Zone analysée
        recent_data = data.tail(last_n_points)
    
        cut_index = None
    
        # =========================
        # Méthode pente
        # =========================
        if method in ["slope", "mixed"]:
            drop_points = recent_data[recent_data['Force Change [N/s]'] < slope_threshold]
            if not drop_points.empty:
                cut_index = drop_points.index[0]
    
        # =========================
        # Méthode chute en %
        # =========================
        if method in ["drop", "mixed"]:
            max_force = data['Force [N]'].max()
            threshold_force = drop_ratio * max_force
    
            drop_zone = recent_data[recent_data['Force [N]'] < threshold_force]
    
            if not drop_zone.empty:
                drop_index = drop_zone.index[0]
    
                if cut_index is None:
                    cut_index = drop_index
                else:
                    # On prend le plus tôt des deux
                    cut_index = min(cut_index, drop_index)
        # =========================
        # Méthode extensomètre (plateau à 0)
        # =========================
        if method in ["extenso", "mixed"] and selected_channel == "Canal Extensomètre":
            if 'Extenso [mm]' in data.columns:
                depl = data['Extenso [mm]']
        
                near_zero_threshold = 0.1
                variation_threshold = 0.05
                window = 5
        
                # IGNORER LE DÉBUT
                start_ratio = 0.2
                start_index = int(len(depl) * start_ratio)
        
                depl_sub = depl.iloc[start_index:]
        
                # Conditions
                cond1 = depl_sub.abs() < near_zero_threshold
                cond2 = depl_sub.diff().abs() < variation_threshold
        
                cond1_roll = cond1.rolling(window=window).sum() == window
                cond2_roll = cond2.rolling(window=window).sum() == window
        
                combined = cond1_roll & cond2_roll
        
                indices = combined[combined].index
        
                if len(indices) > 0:
                    extenso_index = indices[0]
        
                    if cut_index is None:
                        cut_index = extenso_index
                    else:
                        cut_index = min(cut_index-10, extenso_index-10)
                        
                    message = f"Perte du signal de l'extensomètre détecté à l'index {extenso_index}.\nCoupure appliquée dès l'index {cut_index}."
                    messagebox.showwarning("Avertissement", message)
                    print(message)
    
        # Coupe finale
        if cut_index is not None:
            data = data.loc[:cut_index]
            
        print(f"Nettoyage appliqué : coupure à l'index {cut_index}")
        return data