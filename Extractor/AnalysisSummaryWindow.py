# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 08:42:48 2024

End of analysis window. Print a summary of the analysis with table and graphics.
- 3 types of graphics
- Summary table with average and standard deviation

Version: Beta 1.9
Last Update: 28.08.24

@author: quentin.raball
"""

import os
import csv
import customtkinter as ctk
from tkinter import messagebox
from tkinter import filedialog
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
        self.option_name = option_list.get('option_name', False)
        self.option_path = option_list.get('option_path', False)
        self.option_legend = option_list.get('option_legend', False)
        self.option_defo_percent = option_list.get('option_defo_percent', False)
        self.option_elastic_line = option_list.get('option_elastic_line', False)
        self.option_show_table = option_list.get('option_show_table', False)
        self.option_kn = option_list.get('option_kn', False)
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        
        self.create_tabs()
        self.create_summary_table()
        self.create_buttons()

    def create_tabs(self):
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=1, column=1, padx=20, pady=(20, 0), sticky="nsew")

        self.create_tab('Graphique Contrainte-Déformation', self.plot_stress_deformation)
        self.create_tab('Graphique Force-Déplacement', self.plot_force_displacement)
        self.create_tab('Graphique Contrainte-Déplacement', self.plot_stress_displacement)

    def create_tab(self, title, plot_function):
        tab = self.tabview.add(title)
        tab.grid_rowconfigure(0, weight=1)
        tab.grid_columnconfigure(0, weight=1)

        frame = ctk.CTkFrame(tab)
        frame.grid(row=0, column=0, padx=20,  sticky="nsew")

        figure = plt.Figure()
        
        plot_function(figure)
        figure.tight_layout()

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
    
        # Initialiser des listes pour stocker les valeurs de force et de déplacement
        all_force_values = []
        all_displacement_values = []
    
        for sample in self.sample_list:
            # Trouver l'index où la déformation est la plus proche de zéro
            zero_deformation_index = min(range(len(sample.deformation_values)), key=lambda i: abs(sample.deformation_values[i]))
            offset_displacement = sample.displacement_values[zero_deformation_index]
    
            # Ajuster les valeurs de déplacement pour cet échantillon
            adjusted_displacement_values = [disp - offset_displacement for disp in sample.displacement_values]
    
            # Collecter toutes les valeurs de force et de déplacement
            all_force_values.extend(sample.force_values)
            all_displacement_values.extend(adjusted_displacement_values)
    
            # Plot only positive values
            positive_force_values = [max(0, force) for force in sample.force_values]
            if self.option_kn:
                positive_force_values = [force / 1000 for force in positive_force_values]
    
            ax.plot(adjusted_displacement_values, positive_force_values, label=self.get_label(sample))
    
        # Vérifier si les listes sont vides avant de calculer les maximums
        if all_force_values:
            max_force = max(all_force_values) / 1000 if self.option_kn else max(all_force_values)
        else:
            max_force = 0  # Valeur par défaut si aucune donnée
    
        if all_displacement_values:
            max_displacement = max(all_displacement_values)
        else:
            max_displacement = 0  # Valeur par défaut si aucune donnée
    
        # Ajuster les limites du graphique
        ax.set_xlim(0, 1.2 * max_displacement)
        ax.set_ylim(0, 1.3 * max_force)
        
        ax.set_title('Force-Déplacement')
        ax.set_xlabel('Déplacement [mm]')
        ax.set_ylabel('Force [kN]' if self.option_kn else 'Force [N]')
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
        # Créer le cadre principal avec une structure hiérarchique
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.grid(row=2, column=1, padx=20, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=0)
        main_frame.grid_rowconfigure(2, weight=1)
        
        
    
        # Cadre pour les en-têtes de colonnes (fixes)
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.grid(row=1, column=0, sticky="nsew")
    
        # Cadre avec défilement pour les données des échantillons
        scrollable_frame = ctk.CTkScrollableFrame(main_frame)
        scrollable_frame.grid(row=2, column=0, sticky="nsew")
        
        
        # Cadre pour les moyennes et écarts-types
        if len(self.sample_list) > 1:
            stats_frame = ctk.CTkFrame(main_frame)
            stats_frame.grid(row=3, column=0, padx=(0,12), sticky="nsew")
            
            

    
        # Définir les en-têtes de colonnes selon les options
        if self.option_kn == False and self.option_defo_percent:
            headers = [
                'File Name', 'Sample Name', 'F_max [N]', 'Allong [mm]', 
                'Re [MPa]', 'Rm [MPa]', 'Déformation [%]', 'E [GPa]'
            ]
        elif self.option_kn and self.option_defo_percent: 
            headers = [
                'File Name', 'Sample Name', 'F_max [kN]', 'Allong [mm]', 
                'Re [MPa]', 'Rm [MPa]', 'Déformation [%]', 'E [GPa]'
            ]
        elif self.option_kn and self.option_defo_percent == False:
            headers = [
                'File Name', 'Sample Name', 'F_max [kN]', 'Allong [mm]', 
                'Re [MPa]', 'Rm [MPa]', 'Déformation [-]', 'E [GPa]'
            ]
        else:
            headers = [
                'File Name', 'Sample Name', 'F_max [N]', 'Allong [mm]', 
                'Re [MPa]', 'Rm [MPa]', 'Déformation [-]', 'E [GPa]'
            ]
    
        # Afficher les en-têtes de colonnes
        for col, header in enumerate(headers):
            header_label = ctk.CTkLabel(header_frame, text=header, font=("Arial", 13, "bold"))
            header_label.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")
            header_frame.grid_columnconfigure(col, weight=1, uniform="columns")
    
        # Ajouter les données des échantillons dans le cadre avec défilement
        current_row = 0
        self.data = []
        for sample in self.sample_list:
            # Ajouter la ligne pour le sample principal
            values = [
                sample.file_name, sample.sample_name, sample.F_max, sample.Allong,
                sample.Re, sample.Rm, sample.Defo, sample.E
            ]
            self.data.append(values)
            for col, value in enumerate(values):
                value_label = ctk.CTkLabel(scrollable_frame, text=value)
                value_label.grid(row=current_row, column=col, padx=5, pady=5, sticky="nsew")
    
            # Ajouter les lignes pour les sous-échantillons si présents
            if sample.subsamples and sample.tested_mode == "Module Young":
                for idx, modulus in enumerate(sample.subsample_modulus):
                    row_offset = current_row + idx + 1
                    modulus_label = ctk.CTkLabel(scrollable_frame, text=modulus)
                    modulus_label.grid(row=row_offset, column=7, padx=5, pady=5, sticky="nsew")
                    description_label = ctk.CTkLabel(scrollable_frame, text=f"Sous-échantillon {idx+1}")
                    description_label.grid(row=row_offset, column=1, padx=5, pady=5, sticky="nsew")
                current_row += len(sample.subsample_modulus)
            current_row += 1
            
        # Configurer la répartition du scrollable frame et moyenne
        for col in range(len(headers)):
            scrollable_frame.grid_columnconfigure(col, weight=1, uniform="columns")
            
            
        # Calcul et affichage des statistiques si applicable
        if len(self.sample_list) > 1:
            numeric_data = np.array(self.data)[:, 2:].astype(np.float64)
            averages = self.vectorized_format_sign(np.mean(numeric_data, axis=0), 3)
            stdevs = self.vectorized_format_sign(np.std(numeric_data, axis=0), 3)
    
            avg_row = ['Moyenne', ''] + list(averages)
            std_row = ['Écart-type', ''] + list(stdevs)
    
            bold_font = ("Arial", 13, "bold")
    
            for col, value in enumerate(avg_row):
                avg_label = ctk.CTkLabel(stats_frame, text=value, font=bold_font)
                avg_label.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")
                #avg_label.grid_columnconfigure(col, weight=1, uniform="columns")
    
            for col, value in enumerate(std_row):
                std_label = ctk.CTkLabel(stats_frame, text=value)
                std_label.grid(row=1, column=col, padx=5, pady=5, sticky="nsew")
                stats_frame.grid_columnconfigure(col, weight=1, uniform="columns")
    
    
    
    def create_buttons(self):
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=3, column=1, padx=20, pady=20, sticky="nsew")
        button_frame.grid_columnconfigure((1,2), weight=1)

        close_button = ctk.CTkButton(button_frame, text="Fermer", command=lambda: self.destroy())
        close_button.grid(row=0, column=2, padx=20, sticky="w")
        close_button.grid_columnconfigure(2, weight=1)
        export_button = ctk.CTkButton(button_frame, text="Exporter", command=lambda: self.export_data())
        export_button.grid(row=0, column=1, padx=20, sticky="e")
        export_button.grid_columnconfigure(1, weight=1)
                    
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

    def export_data(self):
        # Exporter le tableau
        self.attributes("-topmost", False)
        # Export tables
        csv_filepath = self.export_table_to_csv()
        if not csv_filepath:
            messagebox.showinfo("Exportation annulée", "L'exportation a été annulée par l'utilisateur.")
            return
        # Exporter les graphiques
        self.export_graphs_to_png(csv_filepath)

        # Afficher un message de confirmation
        messagebox.showinfo("Export Réussi", "Les données ont été exportées avec succès.")
    
    def save_as(self, titre="Enregistrer sous", defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]):
        file_path = filedialog.asksaveasfilename(
            title=titre,
            defaultextension=defaultextension,
            filetypes=filetypes
        )
        return file_path

    def export_table_to_csv(self):
        
        csv_filepath = self.save_as(titre="Exporter les données", defaultextension=".csv")
        if not csv_filepath:  # L'utilisateur a annulé la sauvegarde
            return
            
        with open(csv_filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if self.option_kn == False and self.option_defo_percent:
                headers = [
                    'File Name', 'Sample Name', 'F_max [N]', 'Allong [mm]', 
                    'Re [MPa]', 'Rm [MPa]', 'Déformation [%]', 'E [GPa]'
                ]
            elif self.option_kn and self.option_defo_percent : 
                headers = [
                    'File Name', 'Sample Name', 'F_max [kN]', 'Allong [mm]', 
                    'Re [MPa]', 'Rm [MPa]', 'Déformation [%]', 'E [GPa]'
                ]
            elif self.option_kn and self.option_defo_percent == False:
                headers = [
                    'File Name', 'Sample Name', 'F_max [kN]', 'Allong [mm]', 
                    'Re [MPa]', 'Rm [MPa]', 'Déformation [-]', 'E [GPa]'
                ]
            else:
                headers = [
                    'File Name', 'Sample Name', 'F_max [N]', 'Allong [mm]', 
                    'Re [MPa]', 'Rm [MPa]', 'Déformation [-]', 'E [GPa]'
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
                
        return csv_filepath

    def export_graphs_to_png(self, csv_filepath):
        # Obtenir le répertoire du fichier CSV
        directory = os.path.dirname(csv_filepath)
        
        # Exporter le graphique Contrainte-Déformation
        figure_cd = plt.Figure(figsize=(10, 5))
        self.plot_stress_deformation(figure_cd)
        filename_cd = os.path.join(directory, "Contrainte-Déformation_export.png")
        figure_cd.savefig(filename_cd)
        plt.close(figure_cd)
    
        # Exporter le graphique Force-Déplacement
        figure_fd = plt.Figure(figsize=(10, 5))
        self.plot_force_displacement(figure_fd)
        filename_fd = os.path.join(directory, "Force-Déplacement_export.png")
        figure_fd.savefig(filename_fd)
        plt.close(figure_fd)
    
        # Exporter le graphique Contrainte-Déplacement
        figure_sd = plt.Figure(figsize=(10, 5))
        self.plot_stress_displacement(figure_sd)
        filename_sd = os.path.join(directory, "Contrainte-Déplacement_export.png")
        figure_sd.savefig(filename_sd)
        plt.close(figure_sd)