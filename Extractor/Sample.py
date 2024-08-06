# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 12:27:44 2024

Sample related Class

Saving all informations about current sample.
Available functions:
-show_var()
-import_data() to import datas from the file to the structure
-export_preview() to export graphics and tables
-analyze() to analyze the samples with mode and geometry

Version: Beta 1.0
Last Update: 06.08.24

@author: quentin.raball
"""

# Importation des modules
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from tkinter import messagebox

class Sample:    
    def __init__(self, master):
        self.master = master
        self.file_name = None
        self.file_path = None
        self.test_bench = None
        self.number_of_test = None
        self.available_sample_names = None
        self.extensometer_choice_value = None
        self.sample_name = "Default"
        self.separator = ','
        self.header_index = 2
        self.force_channel = 2
        self.stroke_channel = 3
        self.time_channel = 1
        self.force_unit = 1
        self.repeat_every = None
        self.tested_mode = None
        self.tested_geometry = None
        self.time_values = []
        self.force_values = []
        self.displacement_values = []
        self.stress_values = []
        self.deformation_values = []
        self.samples_and_channels = []
        self.L0 = None
        self.L0_rect = None
        self.L1 = None
        self.S0 = None
        self.D0 = None
        self.W0 = None
        self.H0 = None
        self.lin_range = []
        self.F_max = None
        self.Allong = None
        self.t_max = None
        self.elastic_retreat = None
        self.Re = None
        self.Rm = None
        self.Defo = None
        self.E = None
        self.Y_Offset = None
        self.X_Offset = None
        self.idx0 = None
        self.selected_channel = "Canal Traverse"
        self.round_val = self.master.get_round_val()
        self.coef_rp_unformatted = self.master.get_coef_rp()
        self.coef_rp = float(self.coef_rp_unformatted.strip('%'))
        self.end_filter = 20
        self.show_file_path = self.master.get_option_file_path()
        self.show_sample_name = self.master.get_option_sample_name()
        self.scale_kN = self.master.get_option_scale_kN()
        self.show_Fmax_Allong_value = self.master.get_option_show_force_stroke()
        self.defo_percent = self.master.get_option_defo_percent()
        self.show_rp02 = self.master.get_option_show_rp()
        self.show_legend = self.master.get_option_show_legend()
        self.analyzed_sample = False
        self.last_mode_chosen = 0
        self.last_geometry_chosen = "Section Ronde"
        
      
    def show_var(self):
        print("\nCurrent Sample Vars:")
        print(f"File_Name: {self.file_name}")
        print(f"File_Path: {self.file_path}")
        print(f"Default Sample_Name: {self.sample_name}")
        print(f"Test_Bench: {self.test_bench}")
        print(f"Time_Channel: {self.time_channel}")
        print(f"Force_Channel: {self.force_channel}")
        print(f"Stroke_Channel: {self.stroke_channel}")
        print(f"Tested_Mode: {self.tested_mode}")
        print(f"Tested_Geometry: {self.tested_geometry}")
        print(f"L0: {self.L0} [mm]")
        print(f"D0: {self.D0} [mm]")
        print(f"W0: {self.W0} [mm]")
        print(f"H0: {self.H0} [mm]")
        print(f"Lin_range: {self.lin_range} [N]")
        print(f"Size of Datas_values: ({len(self.time_values)},3)")
        print(f"Max Force: {self.F_max} [N]")
        print(f"Max Stroke: {self.Allong} [mm]")
        print(f"Chiffres sign : {self.master.get_round_val()}")
        print(f"Rp definition : {self.master.get_coef_rp()}")
        print(f"Option Show file path : {self.master.get_option_file_path()}")
        print(f"Option Show sample name : {self.master.get_option_sample_name()}")
        print(f"Option Force in kN : {self.master.get_option_scale_kN()}")
        print(f"Option Show Force and Stroke : {self.master.get_option_show_force_stroke()}")
        print(f"Option Show Rp Line: {self.master.get_option_show_rp()}")
        print(f"Analyzed Sample: {self.analyzed_sample}")
        print(f"Analyzed Result: Rm: {self.Rm} [MPa]")
        print(f"Analyzed Result: Re: {self.Re} [MPa]")
        print(f"Analyzed Result: A%: {self.Defo} [%]")
        print(f"Analyzed Result: E: {self.E} [GPa]")
      
    def import_data(self):
        # Lire les données du fichier CSV
        print(f"Importation des données de {self.sample_name}. Veuillez patienter...")
        # Lire tout le fichier, enlever les guillemets doubles, puis séparer chaque ligne par le séparateur
        with open(self.file_path, 'r', encoding='latin-1') as file:
            content = file.read().replace('"', '')
            lines = content.split('\n')
        # Convertir les lignes en une liste de listes en utilisant le séparateur
        data_list = [line.split(self.separator) for line in lines]
        raw_data = pd.DataFrame(data_list)
        force_column = self.force_channel - 1
        displacement_column = self.stroke_channel - 1
        time_column = self.time_channel - 1
        print(f"Taille actuelle du tableau de données brutes : {raw_data.shape}")
        # Extraction des données de force et de déplacement
        time_data = pd.to_numeric(raw_data.iloc[:, time_column], errors='coerce')
        force_data = pd.to_numeric(raw_data.iloc[:, force_column], errors='coerce')
        displacement_data = pd.to_numeric(raw_data.iloc[:, displacement_column], errors='coerce')
        data = pd.DataFrame({'Temps [s]':time_data, 'Force [N]': force_data, 'Déplacement [mm]': displacement_data})
        # Correction facteur force
        data['Force [N]'] = data['Force [N]'].apply(lambda x: x * self.force_unit)
        data.dropna(inplace=True)
        if self.end_filter != 0 and self.end_filter is not None:
            data = data[:-self.end_filter]
        self.time_values = data['Temps [s]'].tolist()
        self.force_values = data['Force [N]'].tolist()
        self.displacement_values = data['Déplacement [mm]'].tolist()
        self.F_max = self.format_sign(data['Force [N]'].max(),self.round_val)
        self.t_max = self.format_sign(data['Temps [s]'].max(),self.round_val)
        self.Allong = self.format_sign(data['Déplacement [mm]'].max() - data['Déplacement [mm]'].iloc[1],self.round_val)
        def_min = self.format_sign(float(self.F_max)*0.2, self.round_val)
        def_max = self.format_sign(float(self.F_max)*0.4, self.round_val)
        self.lin_range = [def_min, def_max]
        
        print(f"Nouvelle taille du tableau post-importation : {data.shape}")
        print(f"Importation des données spécifiques de {self.sample_name} terminée.\n")
    
        return self.time_values, self.force_values, self.displacement_values
    
    
    def export_preview(self, graph_type=None):
        if graph_type == 'Force-Déplacement':
            force_stroke_path = self.export_graph(
                'Force-Déplacement', 
                'Déplacement [mm]', 
                'Force [N]', 
                self.displacement_values, 
                self.force_values, 
                f"graphique_force_déplacement_{os.path.basename(self.file_path)} - {self.sample_name}.png",
                'A_max', 'F_max'
            )
            return force_stroke_path
    
        elif graph_type == 'Force-Temps':
            force_time_path = self.export_graph(
                'Force-Temps', 
                'Time [s]', 
                'Force [N]', 
                self.time_values, 
                self.force_values, 
                f"graphique_force_temps_{os.path.basename(self.file_path)} - {self.sample_name}.png",
                't_max', 'F_max'
            )
            return force_time_path
    
        elif graph_type == 'Contrainte-Déformation':
            stress_deformation_path = self.export_graph(
                'Contrainte-Déformation', 
                'Déformation [%]', 
                'Contrainte [MPa]', 
                self.deformation_values, 
                self.stress_values, 
                f"graphique_contrainte_deformation_{os.path.basename(self.file_path)} - {self.sample_name}.png",
                'ε_max', 'σ_max'
            )
            return stress_deformation_path
    
        elif graph_type == 'Contrainte-Déplacement':
            stress_displacement_path = self.export_graph(
                'Contrainte-Déplacement', 
                'Déplacement [mm]', 
                'Contrainte [MPa]', 
                self.displacement_values, 
                self.stress_values, 
                f"graphique_contrainte_deplacement_{os.path.basename(self.file_path)} - {self.sample_name}.png",
                'A_max', 'σ_max'
            )
            return stress_displacement_path
    
        else:
            # Si aucun type de graphique n'est spécifié ou reconnu
            raise ValueError(f"Type de graphique non pris en charge : {graph_type}")
    
    def export_graph(self, subfolder, x_label, y_label, x_values, y_values, file_name, max_x_label, max_y_label):
        image_path = os.path.join('output', 'IMG', subfolder)
        if not os.path.exists(image_path):
            os.makedirs(image_path)
        
        print(f"Génération du graphique {y_label}-{x_label}.\n")
        
        plt.figure()
        
        if y_label == 'Force [N]':
            force_values_plot = [val / 1000 for val in y_values] if self.master.get_option_scale_kN() else y_values
        else:
            force_values_plot = y_values
        
        data_plot = pd.DataFrame({
            x_label: x_values,
            y_label: force_values_plot
        })
        
        self.update_plot_attributes(data_plot, x_label, y_label, max_x_label, max_y_label)
        
        graph_path = os.path.join(image_path, file_name)
        plt.savefig(graph_path, dpi=300)
        plt.close()
        
        print(f"Fin de l'exportation du graphique {y_label} - {x_label}.\n")
        
        return graph_path
    
    def update_plot_attributes(self, data_plot, x_label, y_label, max_x_label, max_y_label):
        data_plot.plot(x=x_label, y=y_label, kind='line')
        
        self.show_file_path = self.master.get_option_file_path()
        self.show_sample_name = self.master.get_option_sample_name()
        
        file_name_graph = os.path.basename(self.file_path)
        title = self.get_plot_title()
        plt.title(title)
        
        plt.gca().set_xlim(0, 1.2 * (data_plot[x_label].max() - data_plot[x_label].iloc[1]))
        plt.gca().set_ylim(0, 1.3 * data_plot[y_label].max())
        
        if y_label == 'Force [N]':
            plt.ylabel('Force [kN]' if self.master.get_option_scale_kN() else 'Force [N]')
        elif y_label == 'Contrainte [MPa]':
            plt.ylabel('Contrainte [MPa]')
            
        if x_label == 'Déplacement [mm]':
            plt.xlabel('Déplacement [mm]')
        elif x_label == 'Déformation [%]':
            plt.xlabel('Déformation [%]')
        elif x_label == 'Time [s]':
            plt.xlabel('Time [s]')
        
        plt.legend().remove()
        
        if self.master.get_option_show_force_stroke():
            self.add_table_to_plot(data_plot, x_label, y_label, max_x_label, max_y_label)
        
        self.show_rp02 = self.master.get_option_show_rp()
        
        if self.show_rp02 and y_label == 'Contrainte [MPa]' and x_label == 'Déformation [%]' and float(self.Defo) > float(self.coef_rp):
            self.add_elastic_limit_line(data_plot, x_label)
    
    def add_elastic_limit_line(self, data_plot, x_label):
        E = self.E*10
        x_start = self.coef_rp
        y_start = 0
        x_end = data_plot[x_label].max()
        y_end = E * (x_end - x_start)
        
        plt.plot([x_start, x_end], [y_start, y_end], label='Limite élastique', linestyle='-', color='orange')
        self.show_legend = self.master.get_option_show_legend()
        if self.show_legend :
            plt.legend()
    
    def add_table_to_plot(self, data_plot, x_label, y_label, max_x_label, max_y_label):
        if max_x_label == 'A_max':
            max_x_value = (data_plot['Déplacement [mm]'].max() - data_plot['Déplacement [mm]'].iloc[1])
        elif max_x_label == 'ε_max':
            max_x_value = data_plot['Déformation [%]'].max()
        elif max_x_label == 't_max':
            max_x_value = data_plot['Time [s]'].max()
        
        if max_y_label == 'F_max':
            max_y_value = data_plot['Force [N]'].max()
            if self.master.get_option_scale_kN():
                max_y_value /= 1000
        elif max_y_label == 'σ_max':
            max_y_value = data_plot['Contrainte [MPa]'].max()
        
        if self.round_val != 0:
            max_y_value = self.format_sign(max_y_value, self.master.get_round_val())
            max_x_value = self.format_sign(max_x_value, self.master.get_round_val())
        
        if y_label == 'Force [N]':
            force_label = 'Force [kN]' if self.master.get_option_scale_kN() else 'Force [N]'
        elif y_label == 'Contrainte [MPa]':
            force_label = 'σ [MPa]'
        
        if max_x_label == 't_max':
            max_x_unit = '[s]'
        elif max_x_label == 'ε_max':
            max_x_unit = '[%]'
        else:
            max_x_unit = '[mm]'
        
        if max_y_label == 'F_max':
            max_y_unit = '[kN]' if self.master.get_option_scale_kN() else '[N]'
        elif max_y_label == 'σ_max':
            max_y_unit = '[MPa]'
        
        table_data = [[max_y_label, max_x_label],
                      [max_y_unit, max_x_unit],
                      [max_y_value, max_x_value]]
        
        table = plt.table(cellText=table_data, loc='lower right', colWidths=[0.15, 0.15, 0.15, 0.15])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.5)
    
    def get_plot_title(self):
        if self.show_file_path and self.show_sample_name:
            return f"{os.path.relpath(self.file_path)} - {self.sample_name}"
        elif self.show_file_path:
            return f"{os.path.relpath(self.file_path)}"
        elif self.show_sample_name:
            return f"{self.sample_name}"
        else:
            return ""
    
    def update_max_values(self):
        if self.master.get_round_val() != 0:
            self.F_max = self.format_sign(self.F_max, self.master.get_round_val())
            self.t_max = self.format_sign(self.t_max, self.master.get_round_val())
            
    
    # Fonction d'analyse des valeurs en traction. Conversion vers contrainte-déformation
    def analyze(self):
        print("Début de l'analyse. Veuillez patienter...\n")
    
        self.choose_analysis_mode()
        self.convert_deformation()
        self.calculate_youngs_modulus()
        self.calculate_interesting_values()
        self.apply_significant_figures()
        self.display_results()
        self.analyzed_sample = True
    
        return [self.F_max, self.Rm, self.Re, self.E, self.Allong, self.Defo, self.elastic_retreat]
    
    def choose_analysis_mode(self):
        disp_ini = self.displacement_values[1]
        while True:
            analysis_mode = self.tested_mode
            geometry_mode = self.tested_geometry
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
                else:
                    message = "Mode d'analyse invalide.\nVeuillez configurer le fichier premièrement."
                    print(message)
                    messagebox.showinfo("Configuration du fichier incorrecte", message)
                    break
            except ValueError:
                print("Veuillez entrer une option valide.")
                
    def traction_analysis(self, geometry_mode, disp_ini):
        try:
            if geometry_mode == "Section Ronde":
                self.S0 = np.pi * (self.D0**2) / 4
                print("Traitement des données en mode traction - Géométrie Ronde.")
            elif geometry_mode == "Section Rectangulaire":
                self.S0 = self.H0 * self.W0
                print("Traitement des données en mode traction - Géométrie Rectangulaire.")
            else:
                print("La géométrie choisie est incorrecte.")
                return
    
            self.stress_values = [force / self.S0 for force in self.force_values]
            self.deformation_values = [(disp - disp_ini) / self.L0 * 100 for disp in self.displacement_values]
    
        except ValueError:
            print("Veuillez entrer une option valide.")
            
    def flexion_3pts_analysis(self, geometry_mode, disp_ini):
        try:
            if geometry_mode == "Section Ronde":
                r0 = 0.5 * self.D0
                print("Traitement des données en mode flexion 3 points - Géométrie Ronde.")
                self.stress_values = [(force * self.L0) / (np.pi * r0**3) for force in self.force_values]
                self.deformation_values = [(disp - disp_ini) * 100 * (12 * r0 / (self.L0**2)) for disp in self.displacement_values]
            elif geometry_mode == "Section Rectangulaire":
                print("Traitement des données en mode flexion 3 points - Géométrie Rectangulaire.")
                self.stress_values = [(3 * force * self.L0_rect) / (2 * self.W0 * self.H0**2) for force in self.force_values]
                self.deformation_values = [(disp - disp_ini) * 100 * (6 * self.H0 / (self.L0_rect**2)) for disp in self.displacement_values]
            else:
                print("La géométrie choisie est incorrecte.")
    
        except ValueError:
            print("Veuillez entrer une option valide.")
            
    def flexion_4pts_analysis(self, geometry_mode, disp_ini):
        try:
            if geometry_mode == "Section Ronde":
                print("Traitement des données en mode flexion 4 points - Géométrie Ronde.")
                self.stress_values = [(8*force * (self.L0 - self.L1)) / (np.pi * self.D0**3) for force in self.force_values]
                self.deformation_values = [(disp - disp_ini) * 100 * (6 * self.D0 * (self.L0-self.L1)/(self.L0**3-3*self.L0*self.L1**2+2*self.L1**3)) for disp in self.displacement_values]
            elif geometry_mode == "Section Rectangulaire":
                print("Traitement des données en mode flexion 4 points - Géométrie Rectangulaire.")
                self.stress_values = [(3 * force * (self.L0-self.L1)) / (2 * self.W0 * self.H0**2) for force in self.force_values]
                self.deformation_values = [(disp - disp_ini) * 100 * (6 * self.H0 * (self.L0-self.L1)/(self.L0**3-3*self.L0*self.L1**2+2*self.L1**3)) for disp in self.displacement_values]
            else:
                print("La géométrie choisie est incorrecte.")
    
        except ValueError:
            print("Veuillez entrer une option valide.")
            
    def mod_young_analysis(self, geometry_mode, disp_ini):
        print("Fonction pas encore implémentée")
        # Récupérer période et premier index
        # Séparer chaque partie dans une nouvelle classe Sample avec les même paramètres L0, D0, etc... sur une demi période
        # Pour chaque sample créé, analyser la contrainte
        return
    
    def convert_deformation(self):
        if not self.defo_percent:
            self.deformation_values = [disp / 100 for disp in self.displacement_values]
    
    def calculate_youngs_modulus(self):
        force_min = self.lin_range[0]
        force_max = self.lin_range[1]
        if force_min > force_max : 
            force_min, force_max = force_max, force_min
            
        differences_inf = [abs(force - force_min) for force in self.force_values]
        debut_range = differences_inf.index(min(differences_inf))
    
        differences_sup = [abs(force - force_max) for force in self.force_values]
        fin_range = differences_sup.index(min(differences_sup))
    
        x = self.deformation_values[debut_range:fin_range]
        y = self.stress_values[debut_range:fin_range]
        
        self.coef_rp_unformatted = self.master.get_coef_rp()
        self.coef_rp = float(self.coef_rp_unformatted.strip('%'))
        
        coefficients = np.polyfit(x, y, 1)
        if self.defo_percent:
            self.E = coefficients[0] / 10
            self.Y_Offset = coefficients[1]
        else:
            self.E = coefficients[0] / 1000
            self.Y_Offset = coefficients[1] / 100
            self.coef_rp = self.coef_rp / 100
    
        print("Y_Offset =", self.Y_Offset)
        self.X_Offset = -coefficients[1] / coefficients[0]
        print("X_Offset =", self.X_Offset)
        print("Coef_rp =", self.coef_rp)
    
        self.deformation_values = [deformation - self.X_Offset for deformation in self.deformation_values]
        
    def calculate_interesting_values(self):
        if self.defo_percent:
            y1 = (-self.coef_rp * self.E * 10)
        else:
            y1 = (-self.coef_rp * self.E * 1000)
    
        def_ini = self.displacement_values[1]
        self.Allong = max(self.displacement_values) - def_ini
        self.F_max = max(self.force_values)
    
        last_stress = self.stress_values[-1]
        if self.defo_percent:
            self.elastic_retreat = last_stress / (self.E * 10)
        else:
            self.elastic_retreat = last_stress / (self.E * 1000)
    
        print("Elastic retreat:", self.elastic_retreat)
    
        self.Defo = max(self.deformation_values) - self.elastic_retreat
    
        if self.defo_percent:
            Rp02_sim_values = [x * self.E * 10 + y1 for x in self.deformation_values]
        else:
            Rp02_sim_values = [x * self.E * 1000 + y1 for x in self.deformation_values]
    
        delta_values = [stress - rp02_sim for stress, rp02_sim in zip(self.stress_values, Rp02_sim_values)]
        self.idx0 = min(range(len(delta_values)), key=lambda i: abs(delta_values[i]))
        self.Re = self.stress_values[self.idx0]
        self.show_rp02_prev = self.show_rp02
    
        if self.Defo < self.coef_rp:
            message = "Attention: Rupture fragile détectée.\nVeuillez contrôler les résultats."
            messagebox.showwarning("Avertissement", message)
            print(message)
            self.Defo = 0
            self.Re = max(self.stress_values)
            self.show_rp02 = False
            self.elastic_retreat = self.Allong
    
        self.Rm = max(self.stress_values)
        
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
            
    def display_results(self):
        print("\nDonnées Individuelles Extraites :\n\nForce Max = ", self.F_max, " [N]\nRm = ", self.Rm, " [MPa]\nRp0.2 = ", self.Re, " [MPa]\nE = ", self.E, " [GPa]\nAllongement max = ", self.Allong, " [mm]\nDéformation Max = ", self.Defo, " [%]\nRetour élastique: ", self.elastic_retreat, " [mm]\n")
        
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
