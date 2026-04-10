# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 16:08:08 2026

Data Analyzer
- Process filtered datas from sample and analyze them
- Return interesting values from the analysis

Version: Beta 1.13
Last Update: 10.04.26

@author: quentin.raball
"""
import numpy as np
from tkinter import messagebox

class DataAnalyzer:
    def __init__(self, sample):
        self.sample = sample
        self.master = sample.master
        # Attributs de la classe qui seront utilisés pour l'analyse
        self.scale_kN = None
        self.tested_mode = None
        self.tested_geometry = None
        self.stress_values = None
        self.original_deformation_values = None
        self.displacement_values = self.sample.displacement_values
        self.E = None
        self.Rm = None
        self.Re = None
        self.Allong = None
        self.Defo = None
        self.elastic_retreat = None
        self.Y_Offset = None
        self.X_Offset = None
        self.coef_re = None
        
    # Fonction d'analyse. Conversion vers contrainte-déformation
    def analyze(self):
        print("Début de l'analyse. Veuillez patienter...\n")
        self.scale_kN = self.sample.master.get_option_scale_kN()
        self.choose_analysis_mode()
        self.calculate_youngs_modulus()
        self.calculate_interesting_values()
        self.apply_significant_figures()
        self.sample.analyzed_sample = True
    
        return [self.sample.F_max, self.Rm, self.Re, self.E, self.Allong, self.Defo, self.elastic_retreat, self.stress_values, self.original_deformation_values]
    
    def choose_analysis_mode(self):
        disp_ini = self.sample.displacement_values[1]
        while True:
            analysis_mode = self.sample.tested_mode
            geometry_mode = self.sample.tested_geometry
            print(f"Mode d'analyse de la classe Sample : {analysis_mode}")
            try:
                if analysis_mode == "Traction":
                    self.traction_analysis(geometry_mode, disp_ini)
                    break
                elif analysis_mode == "Flexion 3pts":
                    self.flexion_3pts_analysis(geometry_mode, disp_ini)
                    break
                elif analysis_mode == "Flexion 4pts":
                    self.flexion_4pts_analysis(geometry_mode, disp_ini)
                    break
                elif analysis_mode == "Module Young":
                    self.mod_young_analysis(geometry_mode, disp_ini)
                    break
                
            except ValueError:
                message = "Mode d'analyse invalide.\nVeuillez configurer le fichier premièrement."
                print(message)
                messagebox.showinfo("Configuration du fichier incorrecte", message)
                
    def traction_analysis(self, geometry_mode, disp_ini):
        try:
            if geometry_mode == "Section Ronde":
                self.S0 = np.pi * (self.sample.D0**2) / 4
                print("Traitement des données en mode traction - Géométrie Ronde.")
            elif geometry_mode == "Section Rectangulaire":
                self.S0 = self.sample.H0 * self.sample.W0
                print("Traitement des données en mode traction - Géométrie Rectangulaire.")
            else:
                print("La géométrie choisie est incorrecte.")
                return
    
            self.stress_values = [force / self.S0 for force in self.sample.force_values]
            self.original_deformation_values = [(disp - disp_ini) / self.sample.L0 * 100 for disp in self.sample.displacement_values]
    
        except ValueError:
            print("Veuillez entrer une option valide.")
            
    def flexion_3pts_analysis(self, geometry_mode, disp_ini):
        try:
            if geometry_mode == "Section Ronde":
                r0 = 0.5 * self.sample.D0
                print("Traitement des données en mode flexion 3 points - Géométrie Ronde.")
                self.stress_values = [(force * self.sample.L0) / (np.pi * r0**3) for force in self.sample.force_values]
                self.original_deformation_values = [(disp - disp_ini) * 100 * (12 * r0 / (self.sample.L0**2)) for disp in self.sample.displacement_values]
            elif geometry_mode == "Section Rectangulaire":
                print("Traitement des données en mode flexion 3 points - Géométrie Rectangulaire.")
                self.stress_values = [(3 * force * self.sample.L0) / (2 * self.sample.W0 * self.sample.H0**2) for force in self.sample.force_values]
                self.original_deformation_values = [(disp - disp_ini) * 100 * (6 * self.sample.H0 / (self.sample.L0**2)) for disp in self.sample.displacement_values]
            else:
                print("La géométrie choisie est incorrecte.")
    
        except ValueError:
            print("Veuillez entrer une option valide.")
            
    def flexion_4pts_analysis(self, geometry_mode, disp_ini):
        try:
            if geometry_mode == "Section Ronde":
                print("Traitement des données en mode flexion 4 points - Géométrie Ronde.")
                self.stress_values = [(8*force * (self.sample.L0 - self.sample.L1)) / (np.pi * self.sample.D0**3) for force in self.sample.force_values]
                self.original_deformation_values = [(disp - disp_ini) * 100 * (6 * self.sample.D0 * (self.sample.L0-self.sample.L1)/(self.sample.L0**3-3*self.sample.L0*self.sample.L1**2+2*self.sample.L1**3)) for disp in self.sample.displacement_values]
            elif geometry_mode == "Section Rectangulaire":
                print("Traitement des données en mode flexion 4 points - Géométrie Rectangulaire.")
                self.stress_values = [(3 * force * (self.sample.L0-self.sample.L1)) / (2 * self.sample.W0 * self.sample.H0**2) for force in self.sample.force_values]
                self.original_deformation_values = [(disp - disp_ini) * 100 * (6 * self.sample.H0 * (self.sample.L0-self.sample.L1)/(self.sample.L0**3-3*self.sample.L0*self.sample.L1**2+2*self.sample.L1**3)) for disp in self.sample.displacement_values]
            else:
                print("La géométrie choisie est incorrecte.")
    
        except ValueError:
            print("Veuillez entrer une option valide.")
            
    def mod_young_analysis(self, geometry_mode, disp_ini):
        print("Début de l'analyse pour le Module de Young.")
    
        if geometry_mode == "Section Ronde":
            self.S0 = np.pi * (self.sample.D0**2) / 4
            print("Traitement des données en mode Module de Young - Géométrie Ronde.")
        elif geometry_mode == "Section Rectangulaire":
            self.S0 = self.sample.H0 * self.sample.W0
            print("Traitement des données en mode Module de Young - Géométrie Rectangulaire.")
        else:
            print("La géométrie choisie est incorrecte.")
            return
    
        # Conversion des valeurs de contrainte et déformation
        self.stress_values = [force / self.sample.S0 for force in self.sample.force_values]
        self.original_deformation_values = [(disp - disp_ini) / self.sample.L0 * 100 for disp in self.sample.displacement_values]
        
        # Détecter les intersections des lignes horizontales
        indices_min, indices_max = self.find_intersections(self.sample.force_values)
    
        # Créer des sous-échantillons basés sur les montées en force
        subsamples = self.create_subsamples(indices_min, indices_max)
        
        if len(subsamples) > 1:
            subsamples = subsamples[1:]
    
        # Ajouter les sous-échantillons aux valeurs de contrainte et de déformation
        self.subsamples = subsamples
    
    def find_intersections(self, force_values):
        force_min = self.sample.lin_range[0]
        force_max = self.sample.lin_range[1]
    
        # Assurez-vous que force_min est inférieur à force_max
        if force_min > force_max:
            force_min, force_max = force_max, force_min
    
        indices_min = []
        indices_max = []
    
        # Identifier les indices où force_values intersecte F_min et F_max
        for i in range(len(force_values) - 1):
            # Intersection avec F_min
            if (force_values[i] <= force_min <= force_values[i + 1]) or (force_values[i + 1] <= force_min <= force_values[i]):
                indices_min.append(i)
    
            # Intersection avec F_max
            if (force_values[i] <= force_max <= force_values[i + 1]) or (force_values[i + 1] <= force_max <= force_values[i]):
                indices_max.append(i)
    
        return indices_min, indices_max
        
    
    def create_subsamples(self, indices_min, indices_max):
        subsamples = []
    
        # Assure que les deux listes ont la même longueur et sont bien ordonnées
        if len(indices_min) == len(indices_max) or len(indices_min) == len(indices_max)+1 :
            if len(indices_min) == len(indices_max)+1:
                indices_min.pop()
            for i in range(len(indices_min)):
                start_idx = indices_min[i]
                end_idx = indices_max[i]
    
                # Crée un sous-échantillon basé sur ces indices
                subsample = {
                    'force': self.sample.force_values[start_idx:end_idx],
                    'displacement': self.sample.displacement_values[start_idx:end_idx],
                    'deformation': self.original_deformation_values[start_idx:end_idx],
                    'stress': self.stress_values[start_idx:end_idx],
                }
                # Assurez-vous que le sous-échantillon n'est pas vide
                if not (subsample['force'] and subsample['displacement'] and subsample['deformation'] and subsample['stress']):
                    print(f"Le sous-échantillon {i + 1} est incomplet.")
                    continue
                subsamples.append(subsample)
                
        else:
            print("Les indices de début et de fin ne correspondent pas. Vérifiez vos données.")
            
        print(f"Nombre de sous-échantillons créés: {len(subsamples)}")
        return subsamples
    
    def calculate_youngs_modulus(self):
        if self.tested_mode == "Module Young":
            young_modulus_values = []
            self.subsample_modulus = []
        
            for subsample in self.subsamples:
                # Utiliser les valeurs de déformation et contrainte du sous-échantillon directement
                x = subsample['deformation']
                y = subsample['stress']
    
                # On effectue la régression linéaire sur les valeurs du sous-échantillon
                coefficients = np.polyfit(x, y, 1)
                young_modulus = coefficients[0] / 10
                self.Y_Offset = coefficients[1]
                young_modulus = self.format_sign(young_modulus, self.sample.round_val)
                young_modulus_values.append(young_modulus)
                self.subsample_modulus.append(young_modulus)
    
            # Calculer la moyenne des modules de Young pour chaque sous-échantillon
            self.E = np.mean(young_modulus_values)
            self.X_Offset = -coefficients[1] / coefficients[0]
            self.original_deformation_values = [deformation - self.X_Offset for deformation in self.sample.original_deformation_values]
            print("Module de Young calculé pour chaque sous-échantillon :")
            for idx, young_modulus in enumerate(young_modulus_values):
                print(f"Sous-échantillon {idx + 1}: {young_modulus:.2f} [GPa]")
            print(f'Moyenne des {len(young_modulus_values)} sous-échantillons : {self.E} [GPa]')
    
        else:
            # Mode alternatif de calcul du module de Young
            indices_min, indices_max = self.find_intersections(self.sample.force_values)
    
            # Utiliser les indices des intersections pour récupérer les points correspondants
            if len(indices_min) > 0 and len(indices_max) > 0:
                start_idx = indices_min[0]
                end_idx = indices_max[0]
    
                # On effectue la régression linéaire sur les sous-ensembles trouvés
                x = self.original_deformation_values[start_idx:end_idx]
                y = self.stress_values[start_idx:end_idx]
    
                self.coef_re_unformatted = self.sample.master.get_coef_re()
                self.coef_re = float(self.coef_re_unformatted.strip('%'))
    
                coefficients = np.polyfit(x, y, 1)
                self.E = coefficients[0] / 10
                self.Y_Offset = coefficients[1]
                print(f"Y_Offset = {self.Y_Offset}")
                self.X_Offset = -coefficients[1] / coefficients[0]
                print("X_Offset =", self.X_Offset)
                print("coef_re =", self.coef_re)
    
                self.original_deformation_values = [deformation - self.X_Offset for deformation in self.original_deformation_values]
        
    def calculate_interesting_values(self):
        last_stress = self.stress_values[-1]
        y1 = (-self.coef_re * self.E * 10)
        self.elastic_retreat = last_stress / (self.E * 10)
        Rp02_sim_values = [x * self.E * 10 + y1 for x in self.original_deformation_values]
            
        def_ini = self.sample.displacement_values[1]
        self.Allong = max(self.sample.displacement_values) - def_ini
        self.F_max = max(self.sample.force_values) if not self.scale_kN else max(self.sample.force_values) / 1000
        self.Defo = max(self.original_deformation_values) - self.elastic_retreat            
    
        delta_values = [stress - rp02_sim for stress, rp02_sim in zip(self.stress_values, Rp02_sim_values)]
        self.idx0 = min(range(len(delta_values)), key=lambda i: abs(delta_values[i]))
        self.Re = self.stress_values[self.idx0]
        self.show_rp02_prev = self.sample.show_rp02
    
        if self.Defo < self.coef_re:
            if not self.tested_mode == "Module Young":
                message = "Attention: Rupture fragile détectée.\nVeuillez contrôler les résultats."
                messagebox.showwarning("Avertissement", message)
                print(message)
            self.Defo = 0
            self.Re = max(self.stress_values)
            self.sample.show_rp02 = False
            self.elastic_retreat = self.Allong
    
        self.Rm = max(self.stress_values)
        
            
    def format_sign(self, num, sig_figs):
        if num == None:
            formatted_num = ""
            return formatted_num
        try:
            # Vérifier si num est déjà un float, sinon tenter de le convertir
            if not isinstance(num, float):
                num = float(num)
            # Utiliser la notation scientifique pour formater avec les chiffres significatifs
            formatted_num = f"{num:.{sig_figs}g}"
            formatted_num = float(formatted_num)
        except ValueError:
            formatted_num = num
        return formatted_num
    
    def apply_significant_figures(self):
        self.round_val = self.master.get_round_val()
        if self.round_val != 0:
            self.F_max = self.format_sign(self.F_max, self.round_val)
            self.Rm = self.format_sign(self.Rm, self.round_val)
            self.Re = self.format_sign(self.Re, self.round_val)
            self.E = self.format_sign(self.E, self.round_val)
            self.Allong = self.format_sign(self.Allong, self.round_val)
            self.Defo = self.format_sign(self.Defo, self.round_val)
            self.elastic_retreat = self.format_sign(self.elastic_retreat, self.round_val)