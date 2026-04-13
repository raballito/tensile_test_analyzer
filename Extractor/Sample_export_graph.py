# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 10:46:13 2026

@author: quentin.raball
"""
import os
import matplotlib.pyplot as plt
import pandas as pd

class DataExport: 
    def __init__(self, sample):
        """
        Constructeur de la classe DataExport.
        :param sample: Instance de la classe Sample contenant les données à exporter.
        """
        self.sample = sample
        # Récupérer les données nécessaires de l'instance Sample
        self.displacement_values = self.sample.displacement_values
        self.force_values = self.sample.force_values
        self.time_values = self.sample.time_values
        self.deformation_values = self.sample.deformation_values
        self.stress_values = self.sample.stress_values
        self.sample_name = self.sample.sample_name
        self.file_path = self.sample.file_path
        self.Allong = self.sample.Allong
        self.Defo = self.sample.Defo
        self.F_max = self.sample.F_max
        self.Rm = self.sample.Rm 
        self.Re = self.sample.Re
        self.E = self.sample.E
        self.t_max = self.sample.t_max
        self.round_val = self.sample.round_val
        
        self.master = self.sample.master  # Si nécessaire pour les options supplémentaires

    def export_preview(self, graph_type=None, directory='output/IMG'):
        """
        Fonction pour exporter les graphiques.
        :param graph_type: Type de graphique à exporter (Force-Déplacement, Force-Temps, etc.)
        :param directory: Répertoire où enregistrer les images.
        :return: Chemin du fichier exporté.
        """
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
        """
        Fonction d'exportation d'un graphique.
        :param directory: Répertoire où enregistrer l'image.
        :param subfolder: Sous-dossier pour l'export.
        :param x_label: L'étiquette de l'axe des x.
        :param y_label: L'étiquette de l'axe des y.
        :param x_values: Valeurs de l'axe des x.
        :param y_values: Valeurs de l'axe des y.
        :param file_name: Nom du fichier à enregistrer.
        :param max_x_label: L'étiquette pour la valeur maximale de x.
        :param max_y_label: L'étiquette pour la valeur maximale de y.
        :return: Chemin du fichier exporté.
        """
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
        
        if self.show_rp02 and y_label == 'Contrainte [MPa]' and x_label == 'Déformation [%]' and float(self.sample.Defo) > float(self.sample.coef_re):
            self.add_elastic_limit_line(data_plot, x_label)
    
    def add_elastic_limit_line(self, data_plot, x_label):
        print(f"Etat de defo_percent (Export) : {self.sample.defo_percent}")
        print(f"Coef_re (Export) : {self.sample.coef_re}")
        if self.sample.defo_percent:
            E = self.E*10
            x_start = self.sample.coef_re
        else:
            E = self.E*1000
            x_start = self.sample.coef_re /100
        
        y_start = 0
        x_end = data_plot[x_label].max()
        y_end = E * (x_end - x_start)
        
        plt.plot([x_start, x_end], [y_start, y_end], label='Limite élastique', linestyle='--', color='orange')
        self.show_legend = self.master.get_option_show_legend()
        if self.show_legend :
            plt.legend()
    
    def add_table_to_plot(self, data_plot, x_label, y_label, max_x_label, max_y_label):
        if max_x_label == 'ε_max':
            max_x_unit = '[%]' if self.sample.defo_percent else '[-]'
            max_x_value = self.Defo if self.sample.defo_percent else self.Defo/100
        elif max_x_label == 'A_max':
            max_x_unit = '[mm]'
            max_x_value = self.Allong
        elif max_x_label == 't_max':
            max_x_unit = '[s]'
            max_x_value = self.t_max
        
        if max_y_label == 'F_max':
            max_y_unit = '[kN]' if self.master.get_option_scale_kN() else '[N]'
            max_y_value = self.F_max /1000 if self.master.get_option_scale_kN() else self.F_max
        elif max_y_label == 'Rm':
            max_y_unit = '[MPa]'
            max_y_value = self.Rm
        
        if self.round_val != 0:
            max_y_value = self.sample.format_sign(max_y_value, self.master.get_round_val())
            max_x_value = self.sample.format_sign(max_x_value, self.master.get_round_val())
            
        table_data = [[max_y_label, max_x_label],
                      [max_y_unit, max_x_unit],
                      [max_y_value, max_x_value]]
        
        if x_label == 'Déformation [%]' and y_label == 'Contrainte [MPa]':
            if self.Defo > self.sample.coef_re:
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