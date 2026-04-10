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

Version: Beta 1.12
Last Update: 31.03.26

@author: quentin.raball
"""

# Importation des modules
import uuid
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from tkinter import messagebox
from Extractor.DataFilter import FilterData
from Extractor.DataImporter import import_data
from Extractor.DataAnalyzer import DataAnalyzer

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
        self.base_time_channel = 1
        self.time_channel = 1
        self.base_force_channel = 2
        self.force_channel = 2
        self.base_stroke_channel = 3
        self.stroke_channel = 3
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
        self.subsamples = []
        self.L0 = None
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
        self.coef_re_unformatted = self.master.get_coef_re()
        self.coef_re = float(self.coef_re_unformatted.strip('%'))
        self.end_filter = 0
        self.show_sample_name = self.master.get_option_sample_name()
        self.scale_kN = self.master.get_option_scale_kN()
        self.show_Fmax_Allong_value = self.master.get_option_show_force_stroke()
        self.defo_percent = self.master.get_option_defo_percent()
        self.show_rp02 = self.master.get_option_show_rp()
        self.show_legend = self.master.get_option_show_legend()
        self.show_grid = self.master.get_option_grid()
        self.clean_end = self.master.get_option_filter()
        self.filter_pipeline = FilterData(normalize=True, method="mixed")
        self.analyzed_sample = False
        self.configured_sample = False
        self.last_mode_chosen = 0
        self.last_geometry_chosen = "Section Ronde"
        self.sample_id = uuid.uuid4()
      
    def import_data(self):
        return import_data(self)
    
    # Fonction d'analyse. Conversion vers contrainte-déformation
    def analyze(self):
        analysis = DataAnalyzer(self).analyze()
        self.update_results(analysis)
        self.display_results()
        return analysis
    
    def update_results(self, analysis):
        """Mettre à jour les résultats dans Sample à partir des résultats de DataAnalyzer."""
        self.F_max = analysis[0]
        self.Rm = analysis[1]
        self.Re = analysis[2]
        self.E = analysis[3]
        self.Allong = analysis[4]
        self.Defo = analysis[5]
        self.elastic_retreat = analysis[6]
        self.stress_values = analysis[7]
        self.deformation_values = analysis[8]

    
    def export_preview(self, graph_type=None, directory='output/IMG'):
        if graph_type == 'Force-Déplacement':
            force_stroke_path = self.export_graph(
                directory, 
                'Force-Déplacement', 
                'Déplacement [mm]', 
                'Force [kN]' if self.master.get_option_scale_kN() else 'Force [N]',  
                self.displacement_values, 
                self.force_values, 
                f"graphique_force_déplacement_{os.path.basename(self.file_path)} - {self.sample_name}.png",
                'A_max', 'F_max'
            )
            return force_stroke_path
    
        elif graph_type == 'Force-Temps':
            force_time_path = self.export_graph(
                directory, 
                'Force-Temps', 
                'Temps [s]', 
                'Force [kN]' if self.master.get_option_scale_kN() else 'Force [N]', 
                self.time_values, 
                self.force_values, 
                f"graphique_force_temps_{os.path.basename(self.file_path)} - {self.sample_name}.png",
                't_max', 'F_max'
            )
            return force_time_path
    
        elif graph_type == 'Contrainte-Déformation':
            stress_deformation_path = self.export_graph(
                directory, 
                'Contrainte-Déformation', 
                'Déformation [%]', 
                'Contrainte [MPa]', 
                self.deformation_values, 
                self.stress_values, 
                f"graphique_contrainte_deformation_{os.path.basename(self.file_path)} - {self.sample_name}.png",
                'ε_max', 'Rm'
            )
            return stress_deformation_path
    
        elif graph_type == 'Contrainte-Déplacement':
            stress_displacement_path = self.export_graph(
                directory, 
                'Contrainte-Déplacement', 
                'Déplacement [mm]', 
                'Contrainte [MPa]', 
                self.displacement_values, 
                self.stress_values, 
                f"graphique_contrainte_deplacement_{os.path.basename(self.file_path)} - {self.sample_name}.png",
                'A_max', 'Rm'
            )
            return stress_displacement_path
    
        else:
            # Si aucun type de graphique n'est spécifié ou reconnu
            raise ValueError(f"Type de graphique non pris en charge : {graph_type}")
    
    def export_graph(self, directory, subfolder, x_label, y_label, x_values, y_values, file_name, max_x_label, max_y_label):
        image_path = os.path.join(directory, subfolder)
        if not os.path.exists(image_path):
            os.makedirs(image_path)
    
        print(f"Génération du graphique {y_label} - {x_label}.\n")
    
        plt.figure()
    
        if y_label == 'Force [kN]':
            force_values_plot = [val / 1000 for val in y_values] 
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
        
        self.show_sample_name = self.master.get_option_sample_name()
        self.show_grid = self.master.get_option_grid()
        if self.show_grid:
            plt.grid(zorder=0, linestyle='--', alpha=0.5)
        title = self.get_plot_title()
        plt.title(title)
        
        plt.gca().set_xlim(0, 1.2 * (data_plot[x_label].max() - data_plot[x_label].iloc[1]))
        plt.gca().set_ylim(0, 1.3 * data_plot[y_label].max())
        
        if y_label in ['Force [N]', 'Force [kN]']:
            plt.ylabel('Force [kN]' if self.master.get_option_scale_kN() else 'Force [N]')
        elif y_label == 'Contrainte [MPa]':
            plt.ylabel('Contrainte [MPa]')
            
        if x_label == 'Déplacement [mm]':
            plt.xlabel('Déplacement [mm]')
        elif x_label == 'Temps [s]':
            plt.xlabel('Temps [s]')
        elif x_label in ['Déformation [%]', 'Déformation [-]']:
            plt.xlabel('Déformation [%]' if self.master.get_option_defo_percent() else 'Déformation [-]')
        
        
        plt.legend().remove()
        
        if self.master.get_option_show_force_stroke():
            self.add_table_to_plot(data_plot, x_label, y_label, max_x_label, max_y_label)
        
        self.show_rp02 = self.master.get_option_show_rp()
        
        if self.show_rp02 and y_label == 'Contrainte [MPa]' and x_label == 'Déformation [%]' and float(self.Defo) > float(self.coef_re):
            self.add_elastic_limit_line(data_plot, x_label)
    
    def add_elastic_limit_line(self, data_plot, x_label):
        if self.defo_percent:
            E = self.E*10
        else:
            E = self.E*1000
        x_start = self.coef_re
        y_start = 0
        x_end = data_plot[x_label].max()
        y_end = E * (x_end - x_start)
        
        plt.plot([x_start, x_end], [y_start, y_end], label='Limite élastique', linestyle='--', color='orange')
        self.show_legend = self.master.get_option_show_legend()
        if self.show_legend :
            plt.legend()
    
    def add_table_to_plot(self, data_plot, x_label, y_label, max_x_label, max_y_label):
        if max_x_label == 'A_max':
            max_x_value = self.Allong
        elif max_x_label == 'ε_max':
            max_x_value = self.Defo
        elif max_x_label == 't_max':
            max_x_value = self.t_max
        
        if max_y_label == 'F_max':
            max_y_value = self.F_max
        elif max_y_label == 'Rm':
            max_y_value = self.Rm
        
        if self.round_val != 0:
            max_y_value = self.format_sign(max_y_value, self.master.get_round_val())
            max_x_value = self.format_sign(max_x_value, self.master.get_round_val())
        
        if max_x_label == 't_max':
            max_x_unit = '[s]'
        elif max_x_label == 'ε_max':
            max_x_unit = '[%]' if self.defo_percent else '[-]'
        else:
            max_x_unit = '[mm]'
        
        if max_y_label == 'F_max':
            max_y_unit = '[kN]' if self.master.get_option_scale_kN() else '[N]'
        elif max_y_label == 'Rm':
            max_y_unit = '[MPa]'
        
        table_data = [[max_y_label, max_x_label],
                      [max_y_unit, max_x_unit],
                      [max_y_value, max_x_value]]
        
        if x_label == 'Déformation [%]' and y_label == 'Contrainte [MPa]':
            if self.Defo > self.coef_re:
                table_data[0].append('Re')  # Ajoute le label "Re"
                table_data[1].append('[MPa]')  # Ajoute l'unité "[MPa]"
                table_data[2].append(self.Re)  # Ajoute la valeur de Re
        
        table = plt.table(cellText=table_data, loc='lower right', colWidths=[0.15, 0.15, 0.15, 0.15])
        table.set_zorder(10)
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.5)
    
    def get_plot_title(self):
        if self.show_sample_name:
            return f"{self.sample_name}"
        else:
            return ""
    
    def update_max_values(self):
        if self.master.get_round_val() != 0:
            self.F_max = self.format_sign(self.F_max, self.master.get_round_val())
            self.t_max = self.format_sign(self.t_max, self.master.get_round_val())            
            
    def display_results(self):
        print("\nDonnées Individuelles Extraites :\n\nForce Max = ", self.F_max, " [N]\nRm = ", self.Rm, " [MPa]\nRp0.2 = ", self.Re, " [MPa]\nE = ", self.E, " [GPa]\nAllongement max = ", self.Allong, " [mm]\nDéformation Max = ", self.Defo, " [%]\nRetour élastique: ", self.elastic_retreat, " [%]\n")
        
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
