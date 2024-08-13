# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 14:50:39 2024

Excel Export Window
- Selection of the desired options
- Availablility depends on the analysis of the sample
- Export in Output directory

Version: Beta 1.3
Last Update: 13.08.24

@author: quentin.raball
"""

import customtkinter
from tkinter import IntVar
import pandas as pd
import openpyxl
from openpyxl.drawing.image import Image
import matplotlib.pyplot as plt
import os
from tkinter import messagebox

class ExportExcelWindow(customtkinter.CTkToplevel):
    def __init__(self, sample_list, option_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Sélection des options pour exportation Excel")
        self.geometry("500x300")
        self.sample_list = sample_list

        print(f"État des options : {option_list}")
        self.option_name = option_list[0]
        self.option_path = option_list[1]
        self.option_legend = option_list[2]
        self.option_defo_percent = option_list[3]
        self.option_elastic_line = option_list[4]
        self.option_show_table = option_list[5]
        self.option_kn = option_list[6]
        
        # Variables pour suivre les choix des utilisateurs
        self.selected_options = {
            'graphics': IntVar(value=1),
            'analysis': IntVar(value=1),
            'summary': IntVar(value=1),
            'stress_values': IntVar(value=1),
            'deformation_values': IntVar(value=1)
        }
        
        self.create_widgets(sample_list)

    def create_widgets(self, sample_list):
        customtkinter.CTkLabel(self, text="Choisissez les options pour l'exportation sous Excel:", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Section des options principales
        self.check_graphics = customtkinter.CTkCheckBox(self, text="Inclure les graphiques", variable=self.selected_options['graphics'])
        self.check_analysis = customtkinter.CTkCheckBox(self, text="Inclure l'analyse", variable=self.selected_options['analysis'])
        self.check_summary = customtkinter.CTkCheckBox(self, text="Inclure le résumé", variable=self.selected_options['summary'])
        self.check_stress_values = customtkinter.CTkCheckBox(self, text="Inclure les valeurs de contrainte", variable=self.selected_options['stress_values'])
        self.check_deformation_values = customtkinter.CTkCheckBox(self, text="Inclure les valeurs de déformation", variable=self.selected_options['deformation_values'])

        self.check_graphics.pack(anchor='w', padx=20, pady=5)
        self.check_analysis.pack(anchor='w', padx=20, pady=5)
        self.check_summary.pack(anchor='w', padx=20, pady=5)
        self.check_stress_values.pack(anchor='w', padx=20, pady=5)
        self.check_deformation_values.pack(anchor='w', padx=20, pady=5)

        # Boutons Exporter et Annuler
        self.button_export = customtkinter.CTkButton(self, text="Exporter", command=lambda: self.get_options()).pack(pady=20)        
        
        # Mise à jour de l'état des cases à cocher selon les analyses
        self.update_checkbox_state(sample_list)

    def update_checkbox_state(self, sample_list):
        if len(sample_list) == 0:
            self.check_graphics.deselect()
            self.check_analysis.deselect()
            self.check_summary.deselect()
            self.check_stress_values.deselect()
            self.check_deformation_values.deselect()
            
            self.check_graphics.configure(state='disabled')
            self.check_analysis.configure(state='disabled')
            self.check_summary.configure(state='disabled')
            self.check_stress_values.configure(state='disabled')
            self.check_deformation_values.configure(state='disabled')
        else:
            # Vérifier si tous les échantillons sont analysés
            all_analyzed = all(sample.analyzed_sample for sample in self.sample_list)
    
            if not all_analyzed:
                self.check_analysis.deselect()
                self.check_summary.deselect()
                self.check_stress_values.deselect()
                self.check_deformation_values.deselect()
    
                self.check_analysis.configure(state='disabled')
                self.check_summary.configure(state='disabled')
                self.check_stress_values.configure(state='disabled')
                self.check_deformation_values.configure(state='disabled')
            else:
                self.check_analysis.configure(state='normal')
                self.check_summary.configure(state='normal')
                self.check_stress_values.configure(state='normal')
                self.check_deformation_values.configure(state='normal')
    
                if not self.selected_options['analysis'].get():
                    self.check_summary.deselect()
                    self.check_stress_values.deselect()
                    self.check_deformation_values.deselect()
    
                    self.check_summary.configure(state='disabled')
                    self.check_stress_values.configure(state='disabled')
                    self.check_deformation_values.configure(state='disabled')
                else:
                    self.check_summary.configure(state='normal')
                    self.check_stress_values.configure(state='normal')
                    self.check_deformation_values.configure(state='normal')

    def get_options(self):
        # Collecter les options sélectionnées
        include_graphics = self.selected_options['graphics'].get()
        include_analysis = self.selected_options['analysis'].get()
        include_summary = self.selected_options['summary'].get()
        include_stress_values = self.selected_options['stress_values'].get()
        include_deformation_values = self.selected_options['deformation_values'].get()

        # Appel à la fonction d'exportation avec les options
        self.export_samples_to_excel(self.sample_list, include_graphics, include_analysis, include_summary, include_stress_values, include_deformation_values)
        self.destroy()

    def export_samples_to_excel(self, sample_list, include_graphics, include_analysis, include_summary, include_stress_values, include_deformation_values):
        if len(sample_list) == 0:
            message = "Exportation annulée: aucun échantillon sélectionné.\nVeuillez sélectionner un échantillon et recommencer."
            messagebox.showinfo("Exportation annulée", message)
        else:
            # Définir le chemin d'exportation
            name = 'export_samples.xlsx'
            export_path = os.path.join('output', 'Excel')
            if not os.path.exists(export_path):
                os.makedirs(export_path)
            file_path = os.path.join(export_path, name)
            
            # Créer un fichier Excel
            writer = pd.ExcelWriter(file_path, engine='openpyxl')
        
            # Résumé
            if include_summary:
                # Insérer le résumé sur la première page
                summary_sheet = writer.book.create_sheet(title="Résumé")
                
                # Ajout des graphiques (si sélectionnés)
                if include_graphics:
                    self.generate_and_add_graphics(summary_sheet)
    
                # Ajouter le résumé des valeurs
                summary_data = {
                    "File Name": [],
                    "Sample Name": [],
                    "F_max": [],
                    "Allong": [],
                    "Re": [],
                    "Rm": [],
                    "Déformation": [],
                    "E": []
                }
                
                for sample in sample_list:
                    summary_data["File Name"].append(sample.file_name)
                    summary_data["Sample Name"].append(sample.sample_name)
                    summary_data["F_max"].append(sample.F_max)
                    summary_data["Allong"].append(sample.Allong)
                    summary_data["Re"].append(sample.Re)
                    summary_data["Rm"].append(sample.Rm)
                    summary_data["Déformation"].append(sample.Defo)
                    summary_data["E"].append(sample.E)
    
                # Création du DataFrame et insertion dans Excel
                df_summary = pd.DataFrame(summary_data)
                df_summary.to_excel(writer, sheet_name="Résumé", startrow=1, index=False)
        
                # Calcul des moyennes et écart-types si plusieurs échantillons
                if len(sample_list) > 2:
                    numeric_data = df_summary.iloc[:, 2:].astype(float)  # Sélectionner les colonnes numériques
                    averages = numeric_data.mean(axis=0).tolist()
                    stdevs = numeric_data.std(axis=0).tolist()
    
                    # Ajouter les moyennes et écart-types à la feuille Excel
                    writer.sheets["Résumé"].append(['Moyenne', ''] + averages)
                    writer.sheets["Résumé"].append(['Écart-type', ''] + stdevs)
    
            # Exporter chaque échantillon dans une nouvelle feuille
            for sample in sample_list:
                sheet_name = f'Echantillon {sample.sample_name}'
                sample_df = pd.DataFrame()
                
                # Ajout des données de bases
                sample_df["Temps [s]"] = sample.time_values
                sample_df["Déplacement [mm]"] = sample.displacement_values
                force_unit = "Force [kN]" if self.option_kn else "Force [N]"
                sample_df[force_unit] = sample.force_values
                
                # Ajouter les données choisies selon les options
                if include_analysis:
                    if include_stress_values:
                        sample_df["Contrainte [MPa]"] = sample.stress_values
                    if include_deformation_values:
                        sample_df["Déformation [%]"] = sample.deformation_values if self.option_defo_percent else "Déformation [-]"
        
                sample_df.to_excel(writer, sheet_name=sheet_name, index=False)
        
                # Ajouter les graphiques si option cochée
                if include_graphics:
                    fig, ax = plt.subplots()
                    ax.plot(sample.displacement_values, sample.force_values)  # Graphique exemple
                    plt.savefig('temp_graph.png')
                    img = openpyxl.drawing.image.Image('temp_graph.png')
                    writer.sheets[sheet_name].add_image(img, 'G1')
        
            # Sauvegarder le fichier
            writer._save()
            sample_names = ", ".join([str(sample.sample_name) for sample in sample_list])
            end_message = f'Exportation des échantillons [{sample_names}] terminée.'
            print(end_message)
            messagebox.showinfo("Exportation terminée", end_message)
            writer.close()
            
    def generate_and_add_graphics(self, summary_sheet):
        # Graphique 1: Contrainte-Déformation
        fig1, ax1 = plt.subplots()
        self.plot_stress_deformation(ax1)
        plt.savefig('graph1.png')
        img1 = Image('graph1.png')
        summary_sheet.add_image(img1, 'I1')

        # Graphique 2: Force-Déplacement
        fig2, ax2 = plt.subplots()
        self.plot_force_displacement(ax2)
        plt.savefig('graph2.png')
        img2 = Image('graph2.png')
        summary_sheet.add_image(img2, 'P1')

        # Graphique 3: Contrainte-Déplacement
        fig3, ax3 = plt.subplots()
        self.plot_stress_displacement(ax3)
        plt.savefig('graph3.png')
        img3 = Image('graph3.png')
        summary_sheet.add_image(img3, 'W1')

        plt.close(fig1)
        plt.close(fig2)
        plt.close(fig3)

    def plot_stress_deformation(self, ax):
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

    def plot_force_displacement(self, ax):
        max_force = 0
        max_displacement = 0

        for sample in self.sample_list:
            max_force = max(max_force, max(sample.force_values))
            max_displacement = max(max_displacement, max(sample.displacement_values))
            
            ax.plot(sample.displacement_values, sample.force_values, label=self.get_label(sample))
        
        ax.set_xlim(0, 1.2 * max_displacement)
        ax.set_ylim(0, 1.3 * max_force)

        ax.set_title('Force-Déplacement')
        ax.set_xlabel('Déplacement [mm]')
        ax.set_ylabel('Force [N]')
        if self.option_legend:
            ax.legend()

    def plot_stress_displacement(self, ax):
        max_stress = 0
        max_displacement = 0

        for sample in self.sample_list:
            max_stress = max(max_stress, max(sample.stress_values))
            max_displacement = max(max_displacement, max(sample.displacement_values))
            
            ax.plot(sample.displacement_values, sample.stress_values, label=self.get_label(sample))
        
        ax.set_xlim(0, 1.2 * max_displacement)
        ax.set_ylim(0, 1.3 * max_stress)

        ax.set_title('Contrainte-Déplacement')
        ax.set_xlabel('Déplacement [mm]')
        ax.set_ylabel('σ [MPa]')
        if self.option_legend:
            ax.legend()

    def get_label(self, sample):
        # Retourner l'étiquette appropriée pour un échantillon
        return f"Échantillon {sample.sample_name}"