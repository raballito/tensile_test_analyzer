# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 08:42:48 2024

End of analysis window. Print a summary of the analysis with table and graphics.
- 3 types of graphics
- Summary table with average and standard deviation

Version: Beta 1.2
Last Update: 07.08.24

@author: quentin.raball
"""

import os
import csv
import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class AnalysisSummaryWindow(ctk.CTkToplevel):
    def __init__(self, sample_list, option_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Résumé de l'Analyse")
        self.geometry("1280x800")

        self.sample_list = [sample for sample in sample_list if sample.analyzed_sample]
        
        print(f"Etat des options : {option_list}")
        self.option_name = option_list[0]
        self.option_path = option_list[1]
        self.option_legend = option_list[2]
        self.option_defo_percent = option_list[3]
        self.option_elastic_line = option_list[4]
        self.option_show_table = option_list[5]
        
        self.create_tabs()
        self.create_summary_table()
        self.create_buttons()

    def create_tabs(self):
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(expand=True, fill='both')

        self.create_tab('Graphique Contrainte-Déformation', self.plot_stress_deformation)
        self.create_tab('Graphique Force-Déplacement', self.plot_force_displacement)
        self.create_tab('Graphique Contrainte-Déplacement', self.plot_stress_displacement)

    def create_tab(self, title, plot_function):
        tab = self.tabview.add(title)
        tab.grid_rowconfigure(0, weight=1)
        tab.grid_columnconfigure(0, weight=1)

        frame = ctk.CTkFrame(tab)
        frame.grid(row=0, column=0, padx=20, pady=(10, 10), sticky="nsew")

        figure = plt.Figure()
        plot_function(figure)

        canvas = FigureCanvasTkAgg(figure, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill='both')

    def plot_stress_deformation(self, figure):
        ax = figure.add_subplot(111)
        max_stress = 0
        max_deformation = 0
        
        for sample in self.sample_list:
            max_stress = max(max_stress, max(sample.stress_values))
            max_deformation = max(max_deformation, max(sample.deformation_values))
            
            # Plot only positive values
            positive_stress_values = [max(0, stress) for stress in sample.stress_values]
            ax.plot(sample.deformation_values, positive_stress_values, label=self.get_label(sample))
        
        # Adjust the plot limits based on the maximum positive values
        ax.set_xlim(0, 1.2 * max_deformation)
        ax.set_ylim(0, 1.3 * max_stress)

        ax.set_title('Contrainte-Déformation')
        ax.set_xlabel('Déformation [%]') if self.option_defo_percent else ax.set_xlabel('Déformation [-]')
        ax.set_ylabel('σ [MPa]')
        if self.option_legend:
            ax.legend()

    def plot_force_displacement(self, figure):
        ax = figure.add_subplot(111)
        max_force = 0
        max_displacement = 0
        
        for sample in self.sample_list:
            # Trouver l'index où la déformation est la plus proche de zéro
            zero_deformation_index = min(range(len(sample.deformation_values)), key=lambda i: abs(sample.deformation_values[i]))
            offset_displacement = sample.displacement_values[zero_deformation_index]
            
            # Ajuster les valeurs de déplacement pour cet échantillon
            adjusted_displacement_values = [disp - offset_displacement for disp in sample.displacement_values]
            
            max_force = max(max_force, max(sample.force_values))
            max_displacement = max(max_displacement, max(adjusted_displacement_values))
            
            # Plot only positive values
            positive_force_values = [max(0, force) for force in sample.force_values]
            ax.plot(adjusted_displacement_values, positive_force_values, label=self.get_label(sample))
        
        # Adjust the plot limits based on the maximum positive values
        ax.set_xlim(0, 1.2 * max_displacement)
        ax.set_ylim(0, 1.3 * max_force)
        ax.set_title('Force-Déplacement')
        ax.set_xlabel('Déplacement [mm]')
        ax.set_ylabel('Force [N]')
        if self.option_legend:
            ax.legend()

    def plot_stress_displacement(self, figure):
        ax = figure.add_subplot(111)
        max_stress = 0
        max_displacement = 0
        
        for sample in self.sample_list:
            # Trouver l'index où la déformation est la plus proche de zéro
            zero_deformation_index = min(range(len(sample.deformation_values)), key=lambda i: abs(sample.deformation_values[i]))
            offset_displacement = sample.displacement_values[zero_deformation_index]
            
            # Ajuster les valeurs de déplacement pour cet échantillon
            adjusted_displacement_values = [disp - offset_displacement for disp in sample.displacement_values]
            
            max_stress = max(max_stress, max(sample.stress_values))
            max_displacement = max(max_displacement, max(adjusted_displacement_values))
            
            # Plot only positive values
            positive_stress_values = [max(0, stress) for stress in sample.stress_values]
            ax.plot(adjusted_displacement_values, positive_stress_values, label=self.get_label(sample))
    
        
        # Adjust the plot limits based on the maximum positive values
        ax.set_xlim(0, 1.2 * max_displacement)
        ax.set_ylim(0, 1.3 * max_stress)
        ax.set_title('Contrainte-Déplacement')
        ax.set_xlabel('Déplacement [mm]')
        ax.set_ylabel('σ [MPa]')
        if self.option_legend:
            ax.legend()
            
            
    def get_label(self, sample):
        if self.option_name and self.option_path:
            label = f'{sample.sample_name} - {os.path.relpath(sample.file_path)}'
        elif self.option_name and not self.option_path:
            label = f'{sample.sample_name}'
        elif self.option_path and not self.option_name:
            label = f'{os.path.relpath(sample.file_path)}'
        else:
            label = ''
        return label

    def create_summary_table(self):
        frame = ctk.CTkFrame(self)
        frame.pack(expand=True, fill='both', padx=20, pady=20)

        headers = [
            'File Name', 'Sample Name', 'F_max [N]', 'Allong [mm]', 
            'Re [MPa]', 'Rm [MPa]', 'Déformation [%]', 'E [GPa]'
        ]

        # Ajouter une configuration pour les colonnes
        for col, header in enumerate(headers):
            header_label = ctk.CTkLabel(frame, text=header, font=("Arial", 13, "bold"))
            header_label.grid(row=0, column=col, padx=5, pady=5, sticky='w')

            # Configurer le poids des colonnes
            if col == 0:
                frame.grid_columnconfigure(col, weight=3, uniform="columns")  # Poids plus élevé pour la première colonne
            elif col == 1:
                frame.grid_columnconfigure(col, weight=2, uniform="columns")  # Poids plus élevé pour la deuxième colonne
            else:
                frame.grid_columnconfigure(col, weight=1, uniform="columns")

        self.data = []
        for row, sample in enumerate(self.sample_list, start=1):
            values = [
                sample.file_name, sample.sample_name, sample.F_max, sample.Allong,
                sample.Re, sample.Rm, sample.Defo, sample.E
            ]
            self.data.append(values)
            for col, value in enumerate(values):
                value_label = ctk.CTkLabel(frame, text=value)
                value_label.grid(row=row, column=col, padx=5, pady=5, sticky='w')

        if len(self.sample_list) > 2:
            numeric_data = np.array(self.data)[:, 2:].astype(np.float64)  # Convertir uniquement les valeurs numériques
            averages = self.vectorized_format_sign(np.mean(numeric_data, axis=0), 3)
            stdevs = self.vectorized_format_sign(np.std(numeric_data, axis=0), 3)

            avg_row = ['Moyenne', ''] + list(averages)
            std_row = ['Écart-type', ''] + list(stdevs)

            bold_font = ("Arial", 13, "bold")

            for col, value in enumerate(avg_row):
                avg_label = ctk.CTkLabel(frame, text=value, font=bold_font)
                avg_label.grid(row=len(self.sample_list) + 1, column=col, padx=5, pady=5, sticky='w')

                # Ajuster la largeur minimale des colonnes de données numériques
                if col > 1:
                    frame.grid_columnconfigure(col, minsize=100, uniform="columns")

            for col, value in enumerate(std_row):
                std_label = ctk.CTkLabel(frame, text=value)
                std_label.grid(row=len(self.sample_list) + 2, column=col, padx=5, pady=5, sticky='w')

                # Ajuster la largeur minimale des colonnes de données numériques
                if col > 1:
                    frame.grid_columnconfigure(col, minsize=100, uniform="columns")
                    
    def vectorized_format_sign(self, nums, sig_figs):
        return [self.format_sign(num, sig_figs) for num in nums]

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

    def create_buttons(self):
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=20)

        close_button = ctk.CTkButton(button_frame, text="Fermer", command=lambda: self.destroy())
        close_button.pack(side='left', padx=10)
        export_button = ctk.CTkButton(button_frame, text="Exporter", command=lambda: self.export_data())
        export_button.pack(side='left', padx=10)

    def export_data(self):
        # Exporter le tableau
        self.attributes("-topmost", False)
        self.export_table_to_csv()

        # Exporter les graphiques
        self.export_graphs_to_png()

        # Afficher un message de confirmation
        messagebox.showinfo("Export Réussi", "Les données ont été exportées avec succès.")

    def export_table_to_csv(self):
        output_dir = "output"
        filename  = "table_export.csv"
        csv_filepath = os.path.join(output_dir, filename)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
            
        with open(csv_filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            
            # Écrire les en-têtes
            headers = [
                'File Name', 'Sample Name', 'F_max [N]', 'Allong [mm]', 
                'Re [MPa]', 'Rm [MPa]', 'Déformation [%]', 'E [GPa]'
            ]
            writer.writerow(headers)
            
            # Écrire les données
            for sample in self.sample_list:
                writer.writerow([
                    sample.file_name, sample.sample_name, sample.F_max, sample.Allong,
                    sample.Re, sample.Rm, sample.Defo, sample.E
                ])
            
            # Écrire les lignes de moyennes et écart-types si disponibles
            if len(self.sample_list) > 2:
                numeric_data = np.array(self.data)[:, 2:].astype(np.float64)
                averages = np.mean(numeric_data, axis=0)
                stdevs = np.std(numeric_data, axis=0)
                
                writer.writerow(['Moyenne', ''] + list(self.vectorized_format_sign(averages, 3)))
                writer.writerow(['Écart-type', ''] + list(self.vectorized_format_sign(stdevs, 3)))

    def export_graphs_to_png(self):
        # Exporter le graphique Contrainte-Déformation
        figure_cd = plt.Figure(figsize=(10, 5))
        self.plot_stress_deformation(figure_cd)
        filename_cd = "output/Contrainte-Déformation_export.png"
        figure_cd.savefig(filename_cd)
        plt.close(figure_cd)

        # Exporter le graphique Force-Déplacement
        figure_fd = plt.Figure(figsize=(10, 5))
        self.plot_force_displacement(figure_fd)
        filename_fd = "output/Force-Déplacement_export.png"
        figure_fd.savefig(filename_fd)
        plt.close(figure_fd)

        # Exporter le graphique Contrainte-Déplacement
        figure_sd = plt.Figure(figsize=(10, 5))
        self.plot_stress_displacement(figure_sd)
        filename_sd = "output/Contrainte-Déplacement_export.png"
        figure_sd.savefig(filename_sd)
        plt.close(figure_sd)

    
        
