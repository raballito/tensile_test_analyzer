# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 14:50:39 2024

Excel Export Window
- Selection of the desired options
- Availablility depends on the analysis of the sample
- Export in Output directory
- Export everything in Excel file

Version: Beta 1.4
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
import shutil
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
        self.option_graphics = customtkinter.CTkCheckBox(self, text="Inclure les graphiques", variable=self.selected_options['graphics'])
        self.option_analysis = customtkinter.CTkCheckBox(self, text="Inclure l'analyse", variable=self.selected_options['analysis'], command=lambda:self.update_checkbox_state(sample_list))
        self.option_summary = customtkinter.CTkCheckBox(self, text="Inclure le résumé", variable=self.selected_options['summary'])
        self.option_stress_values = customtkinter.CTkCheckBox(self, text="Inclure les valeurs de contrainte", variable=self.selected_options['stress_values'])
        self.option_deformation_values = customtkinter.CTkCheckBox(self, text="Inclure les valeurs de déformation", variable=self.selected_options['deformation_values'])

        self.option_graphics.pack(anchor='w', padx=20, pady=5)
        self.option_analysis.pack(anchor='w', padx=20, pady=5)
        self.option_summary.pack(anchor='w', padx=20, pady=5)
        self.option_stress_values.pack(anchor='w', padx=20, pady=5)
        self.option_deformation_values.pack(anchor='w', padx=20, pady=5)

        # Boutons Exporter et Annuler
        self.button_export = customtkinter.CTkButton(self, text="Exporter", command=lambda: self.get_options()).pack(pady=20)        
        
        # Mise à jour de l'état des cases à cocher selon les analyses
        self.update_checkbox_state(sample_list)

    def update_checkbox_state(self, sample_list):
        if len(sample_list) == 0:
            self.option_graphics.deselect()
            self.option_analysis.deselect()
            self.option_summary.deselect()
            self.option_stress_values.deselect()
            self.option_deformation_values.deselect()
            
            self.option_graphics.configure(state='disabled')
            self.option_analysis.configure(state='disabled')
            self.option_summary.configure(state='disabled')
            self.option_stress_values.configure(state='disabled')
            self.option_deformation_values.configure(state='disabled')
        else:
            # Vérifier si tous les échantillons sont analysés
            all_analyzed = all(sample.analyzed_sample for sample in self.sample_list)
    
            if not all_analyzed:
                self.option_analysis.deselect()
                self.option_summary.deselect()
                self.option_stress_values.deselect()
                self.option_deformation_values.deselect()
    
                self.option_analysis.configure(state='disabled')
                self.option_summary.configure(state='disabled')
                self.option_stress_values.configure(state='disabled')
                self.option_deformation_values.configure(state='disabled')
            else:
                self.option_analysis.configure(state='normal')
                self.option_summary.configure(state='normal')
                self.option_stress_values.configure(state='normal')
                self.option_deformation_values.configure(state='normal')
    
                if not self.selected_options['analysis'].get():
                    self.option_summary.deselect()
                    self.option_stress_values.deselect()
                    self.option_deformation_values.deselect()
    
                    self.option_summary.configure(state='disabled')
                    self.option_stress_values.configure(state='disabled')
                    self.option_deformation_values.configure(state='disabled')
                else:
                    self.option_summary.configure(state='normal')
                    self.option_stress_values.configure(state='normal')
                    self.option_deformation_values.configure(state='normal')

    def get_options(self):
        # Collecter les options sélectionnées
        include_graphics = self.selected_options['graphics'].get()
        include_summary = self.selected_options['summary'].get()
        include_analysis = self.selected_options['analysis'].get()        
        include_stress_values = self.selected_options['stress_values'].get()
        include_deformation_values = self.selected_options['deformation_values'].get()

        # Appel à la fonction d'exportation avec les options
        self.export_samples_to_excel(self.sample_list, include_graphics, include_analysis, include_summary, include_stress_values, include_deformation_values)
        self.destroy()

    def export_samples_to_excel(self, sample_list, include_graphics, include_analysis, include_summary, include_stress_values, include_deformation_values):
        if len(sample_list) == 0:
            messagebox.showinfo("Exportation annulée", "Aucun échantillon sélectionné.\nVeuillez sélectionner un échantillon et recommencer.")
            return
    
        # Définir le chemin d'exportation
        file_path = self.prepare_export_path('export_samples.xlsx')
        
        # Créer un fichier Excel
        writer = pd.ExcelWriter(file_path, engine='openpyxl')
        
        # Créer un dossier temporaire pour les graphiques
        self.temp_dir = 'temp'
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
    
        # Ajouter le résumé
        if include_summary:
            self.add_summary_sheet(writer, sample_list, include_graphics, include_analysis)
    
        # Exporter chaque échantillon
        for sample in sample_list:
            self.export_sample(writer, sample, include_graphics, include_analysis, include_stress_values, include_deformation_values)
            self.add_sample_details_table(writer, sample, include_analysis)
            
        # Sauvegarder le fichier
        self.finalize_export(writer, sample_list)
    
    
    def prepare_export_path(self, filename):
        #Prépare le chemin de sauvegarde pour le fichier Excel.
        export_path = os.path.join('output', 'Excel')
        if not os.path.exists(export_path):
            os.makedirs(export_path)
        return os.path.join(export_path, filename)
    
    
    def add_summary_sheet(self, writer, sample_list, include_graphics, include_analysis):
        #Ajoute une feuille de résumé avec les données des échantillons et éventuellement des graphiques.
        summary_sheet = writer.book.create_sheet(title="Résumé")
    
        # Ajout des graphiques (si sélectionnés)
        if include_graphics:
            self.generate_and_add_graphics(summary_sheet, sample_list)
        if include_analysis:
            # Collecte des données pour le résumé
            summary_data = {
                "File Name": [sample.file_name for sample in sample_list],
                "Sample Name": [sample.sample_name for sample in sample_list],
                "F_max [N]": [sample.F_max for sample in sample_list],
                "Allong [mm]": [sample.Allong for sample in sample_list],
                "Re [MPa]": [sample.Re for sample in sample_list],
                "Rm [MPa]": [sample.Rm for sample in sample_list],
                "Déformation [%]": [sample.Defo for sample in sample_list],
                "E [GPa]": [sample.E for sample in sample_list]
            }
        else: 
            # Collecte des données pour le résumé
            summary_data = {
                "File Name": [sample.file_name for sample in sample_list],
                "Sample Name": [sample.sample_name for sample in sample_list],
            }
    
        # Création du DataFrame et insertion dans Excel
        df_summary = pd.DataFrame(summary_data)
        df_summary.to_excel(writer, sheet_name="Résumé", startrow=1, index=False)
    
        # Calcul des moyennes et écart-types si plusieurs échantillons
        if len(sample_list) > 2 and include_analysis:
            self.add_summary_statistics(writer, df_summary)
    
    
    def add_summary_statistics(self, writer, df_summary):
        #Ajoute les moyennes et écart-types au résumé.
        numeric_data = df_summary.iloc[:, 2:].astype(float)  # Colonnes numériques
        averages = numeric_data.mean(axis=0).tolist()
        stdevs = numeric_data.std(axis=0).tolist()
    
        # Ajouter les moyennes et écart-types à la feuille Excel
        summary_sheet = writer.sheets["Résumé"]
        summary_sheet.append(['Moyenne', ''] + averages)
        summary_sheet.append(['Écart-type', ''] + stdevs)
    
    
    def export_sample(self, writer, sample, include_graphics, include_analysis, include_stress_values, include_deformation_values):
        #Exporte les données d'un échantillon dans une nouvelle feuille du fichier Excel.
        sheet_name = f'Echantillon {sample.sample_name}'
        sample_df = pd.DataFrame()
    
        # Ajout des données de bases
        sample_df["Temps [s]"] = sample.time_values
        sample_df["Déplacement [mm]"] = sample.displacement_values
        force_unit = "Force [kN]" if self.option_kn else "Force [N]"
        sample_df[force_unit] = sample.force_values
    
        # Ajouter les données d'analyse si sélectionnées
        if include_analysis:
            if include_stress_values:
                sample_df["Contrainte [MPa]"] = sample.stress_values
            if include_deformation_values:
                sample_df["Déformation [%]"] = sample.deformation_values if self.option_defo_percent else sample.deformation_values
    
        # Écrire les données de l'échantillon dans le fichier Excel
        sample_df.to_excel(writer, sheet_name=sheet_name, index=False)
    
        # Ajouter les graphiques si option cochée
        if include_graphics:
            self.add_sample_graph(writer, sample)
    
    
    def add_sample_graph(self, writer, sample):
        # Graphique force-déplacement
        fig1, ax1 = plt.subplots()
        self.plot_force_displacement(ax1, [sample])
        
        # Utiliser un nom unique pour chaque fichier d'image
        graph1_filename = os.path.join(self.temp_dir, f'sample_graph1_{sample.sample_name}.png')
        plt.savefig(graph1_filename)
        
        # Ajouter l'image au fichier Excel
        img1 = openpyxl.drawing.image.Image(graph1_filename)
        writer.sheets[f'Echantillon {sample.sample_name}'].add_image(img1, 'J1')
        plt.close(fig1)
        
        if sample.analyzed_sample:
            # Graphique contrainte-déformation
            fig2, ax2 = plt.subplots()
            self.plot_stress_deformation(ax2, [sample], True)
            
            # Utiliser un nom unique pour chaque fichier d'image
            graph2_filename = os.path.join(self.temp_dir, f'sample_graph2_{sample.sample_name}.png')
            plt.savefig(graph2_filename)
            
            # Ajouter l'image au fichier Excel
            img2 = openpyxl.drawing.image.Image(graph2_filename)
            writer.sheets[f'Echantillon {sample.sample_name}'].add_image(img2, 'Q1')
            plt.close(fig2)
    
    def add_sample_details_table(self, writer, sample, include_analysis):        
        # Extraire les données géométriques en fonction de la forme de l'échantillon
        if sample.tested_geometry == "Section Ronde" and sample.tested_geometry is not None and include_analysis:
            if include_analysis:
                details_data = {
                    "Caractéristique": ["D0 [mm]", "L0 [mm]", "F_Max [N]", "Allong [mm]", "Re [MPa]", "Rm [MPa]", "Déformation [%]", "E [GPa]", "Reg F_min [N]", "Reg F_max [N]", "Mode de test", "Banc de Test"],
                    "Valeur": [sample.D0, sample.L0, sample.F_max, sample.Allong, sample.Re, sample.Rm, sample.Defo, sample.E, sample.lin_range[0], sample.lin_range[1], sample.tested_mode, sample.test_bench]
                }
            else: 
                details_data = {
                    "Caractéristique": ["D0 [mm]", "L0 [mm]", "Reg F_min [N]", "Reg F_max [N]", "Mode de test", "Banc de Test"],
                    "Valeur": [sample.D0, sample.L0, sample.lin_range[0], sample.lin_range[1], sample.tested_mode, sample.test_bench]
                }
        elif sample.tested_geometry == "Section Rectangulaire" and sample.tested_geometry is not None :
            if include_analysis:
                details_data = {
                    "Caractéristique": ["W0 [mm]", "H0 [mm]", "L0 [mm]", "F_Max [N]", "Allong [mm]", "Re [MPa]", "Rm [MPa]", "Déformation [%]", "E [GPa]", "Reg F_min [N]", "Reg F_max [N]", "Mode de test", "Banc de Test"],
                    "Valeur": [sample.W0, sample.H0, sample.L0, sample.F_max, sample.Allong, sample.Re, sample.Rm, sample.Defo, sample.E, sample.lin_range[0], sample.lin_range[1], sample.tested_mode, sample.test_bench]
                }
            else:
                details_data = {
                    "Caractéristique": ["W0 [mm]", "H0 [mm]", "L0 [mm]", "Reg F_min [N]", "Reg F_max [N]", "Mode de test", "Banc de Test"],
                    "Valeur": [sample.W0, sample.H0, sample.L0, sample.lin_range[0], sample.lin_range[1], sample.tested_mode, sample.test_bench]
                }
        
        else:
            # Ajouter d'autres formes si nécessaire
            details_data = {
                "Caractéristique": ["Reg F_min [N]", "Reg F_max [N]", "Mode de test", "Banc de Test"],
                "Valeur": ["Non défini", "Non défini", "Non défini", "Non défini"]
            }
        
        # Créer un DataFrame pour la table
        df_details = pd.DataFrame(details_data)
        
        # Trouver la feuille associée à l'échantillon
        sheet_name = f'Echantillon {sample.sample_name}'
        
        # Insérer la table à l'indice G16
        df_details.to_excel(writer, sheet_name=sheet_name, startrow=1, startcol=6, index=False)
            
    def generate_and_add_graphics(self, summary_sheet, sample_list):
        # Graphique 1: Force-Déplacement
        fig1, ax1 = plt.subplots()
        self.plot_force_displacement(ax1, sample_list)
        graph1_filename = os.path.join(self.temp_dir, 'summary_graph1.png')
        plt.savefig(graph1_filename)
        img1 = Image(graph1_filename)
        summary_sheet.add_image(img1, 'J1')

        # Graphique 2: Contrainte Déformation
        fig2, ax2 = plt.subplots()
        option_elastic_line = False
        self.plot_stress_deformation(ax2, sample_list, option_elastic_line)
        graph2_filename = os.path.join(self.temp_dir, 'summary_graph2.png')
        plt.savefig(graph2_filename)
        img2 = Image(graph2_filename)
        summary_sheet.add_image(img2, 'Q1')

        # Graphique 3: Contrainte-Déplacement
        fig3, ax3 = plt.subplots()
        self.plot_stress_displacement(ax3, sample_list)
        graph3_filename = os.path.join(self.temp_dir, 'summary_graph3.png')
        plt.savefig(graph3_filename)
        img3 = Image(graph3_filename)
        summary_sheet.add_image(img3, 'X1')

        plt.close(fig1)
        plt.close(fig2)
        plt.close(fig3)

    def plot_stress_deformation(self, ax, sample_list, option_elastic_line):
        max_stress = 0
        max_deformation = 0
        
        for sample in sample_list:
            max_stress = max(max_stress, max(sample.stress_values))
            max_deformation = max(max_deformation, max(sample.deformation_values))
            
            # Plot only positive values
            positive_stress_values = [max(0, stress) for stress in sample.stress_values]
            ax.plot(sample.deformation_values, positive_stress_values, label=self.get_label(sample))
            
            if len(sample_list) == 1 and self.option_elastic_line and option_elastic_line:
                data_plot = pd.DataFrame({'Déformation': sample.deformation_values, 'Contrainte': sample.stress_values})
                x_label = 'Déformation'
                self.add_elastic_limit_line(data_plot, x_label, sample.E, sample.coef_rp)
            
        
        # Adjust the plot limits based on the maximum positive values
        ax.set_xlim(0, 1.2 * max_deformation)
        ax.set_ylim(0, 1.3 * max_stress)

        ax.set_title('Contrainte-Déformation')
        ax.set_xlabel('Déformation [%]') if self.option_defo_percent else ax.set_xlabel('Déformation [-]')
        ax.set_ylabel('σ [MPa]')
        if self.option_legend:
            ax.legend()

    def plot_force_displacement(self, ax, sample_list):
        max_force = 0
        max_displacement = 0

        for sample in sample_list:
            max_force = max(max_force, max(sample.force_values))
            max_displacement = max(max_displacement, max(sample.displacement_values))
            
            ax.plot(sample.displacement_values, sample.force_values, label=self.get_label(sample))
        
        ax.set_xlim(0, 1.2 * max_displacement)
        ax.set_ylim(0, 1.3 * max_force)

        ax.set_title('Force-Déplacement')
        ax.set_xlabel('Déplacement [mm]')
        ax.set_ylabel('Force [N]') if not self.option_kn else ax.set_xlabel('Force [kN]')
        if self.option_legend:
            ax.legend()

    def plot_stress_displacement(self, ax, sample_list):
        max_stress = 0
        max_displacement = 0

        for sample in sample_list:
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
            
    def add_elastic_limit_line(self, data_plot, x_label, mod_young, coef_rp):
        if self.option_defo_percent:
            E = mod_young*10
        else:
            E = mod_young*1000
        x_start = coef_rp
        y_start = 0
        x_end = data_plot[x_label].max()
        y_end = E * (x_end - x_start)
        
        plt.plot([x_start, x_end], [y_start, y_end], label='Limite élastique', linestyle='--', color='orange')
        

    def get_label(self, sample):
        # Retourner l'étiquette appropriée pour un échantillon
        return f"Échantillon {sample.sample_name}"
    
    def finalize_export(self, writer, sample_list):
        #Sauvegarde et ferme le fichier Excel.
        writer._save()
        sample_names = ", ".join([str(sample.sample_name) for sample in sample_list])
        end_message = f'Exportation des échantillons [{sample_names}] terminée.'
        print(end_message)
        messagebox.showinfo("Exportation terminée", end_message)
        writer.close()
        shutil.rmtree(self.temp_dir)