# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 09:18:49 2024

Variables window
Used to get main values from the sample structure

Print tables with all values. Export possible

Version: Beta 1.9
Last Update: 26.08.24

@author: quentin.raball
"""

import csv
import customtkinter
from tkinter import messagebox
from tkinter import filedialog

class VarToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, sample_list, option_list,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Liste des variables des fichiers sélectionnés")
        self.geometry("900x400")  # Taille initiale de la fenêtre
        
        print(f"Etat des options : {option_list}")
        self.option_name = option_list.get('option_name', False)
        self.option_path = option_list.get('option_path', False)
        self.option_legend = option_list.get('option_legend', False)
        self.option_defo_percent = option_list.get('option_defo_percent', False)
        self.option_elastic_line = option_list.get('option_elastic_line', False)
        self.option_show_table = option_list.get('option_show_table', False)
        self.option_kn = option_list.get('option_kn', False)
        
        # Conteneur principal pour l'organisation verticale
        container = customtkinter.CTkFrame(self)
        container.pack(fill="both", expand=True)

        # Ajout du titre
        self.label = customtkinter.CTkLabel(container, text="Liste des variables des fichiers sélectionnés :", font=("Arial", 15, "bold"))
        self.label.pack(padx=20, pady=20)

        # Conteneur pour le canevas et les barres de défilement
        canvas_frame = customtkinter.CTkFrame(container, fg_color="transparent")
        canvas_frame.pack(fill="both", expand=True)

        self.canvas = customtkinter.CTkCanvas(canvas_frame, bg="gray85")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar_y = customtkinter.CTkScrollbar(canvas_frame, orientation="vertical", command=self.canvas.yview)
        self.scrollbar_y.pack(side="right", fill="y")

        self.scrollbar_x = customtkinter.CTkScrollbar(container, orientation="horizontal", command=self.canvas.xview)
        self.scrollbar_x.pack(side="top", fill="x")

        self.canvas.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)

        self.scrollable_frame = customtkinter.CTkFrame(self.canvas, fg_color=("gray85", "gray25"))
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Affichage des en-têtes du tableau
        if self.option_defo_percent and self.option_kn == False:
            headers = [
                "Nom Sample", "Banc de Test", 
                "Mode Testé", "Géométrie Testée", 
                "L0 [mm]", "L1 [mm]", "D0 [mm]", "W0 [mm]", "H0 [mm]", "Zone Lin. [N]", 
                "Taille des données", "Max Force [N]", "Max Dépl. [mm]",
                "Rp [MPa]", "Rm [MPa]", "Max Deform. [%]", "E [GPa]"
            ]
        elif self.option_defo_percent and self.option_kn:
            headers = [
                "Nom Sample", "Banc de Test", 
                "Mode Testé", "Géométrie Testée", 
                "L0 [mm]", "L1 [mm]", "D0 [mm]", "W0 [mm]", "H0 [mm]", "Zone Lin. [N]", 
                "Taille des données", "Max Force [kN]", "Max Dépl. [mm]",
                "Rp [MPa]", "Rm [MPa]", "Max Deform. [%]", "E [GPa]"
            ]
        elif self.option_defo_percent == False and self.option_kn:
            headers = [
                "Nom Sample", "Banc de Test", 
                "Mode Testé", "Géométrie Testée", 
                "L0 [mm]", "L1 [mm]", "D0 [mm]", "W0 [mm]", "H0 [mm]", "Zone Lin. [N]", 
                "Taille des données", "Max Force [kN]", "Max Dépl. [mm]",
                "Rp [MPa]", "Rm [MPa]", "Max Deform. [-]", "E [GPa]"
            ]
        else:
            headers = [
                "Nom Sample", "Banc de Test", 
                "Mode Testé", "Géométrie Testée", 
                "L0 [mm]", "L1 [mm]", "D0 [mm]", "W0 [mm]", "H0 [mm]", "Zone Lin. [N]", 
                "Taille des données", "Max Force [N]", "Max Dépl. [mm]",
                "Rp [MPa]", "Rm [MPa]", "Max Deform. [-]", "E [GPa]"
            ]
            

        for col, header in enumerate(headers):
            header_label = customtkinter.CTkLabel(self.scrollable_frame, text=header, font=("Arial", 10, "bold"))
            header_label.grid(row=0, column=col, padx=5, pady=5, sticky='w')

        # Affichage des valeurs des fichiers
        self.sample_list = sample_list
        self.display_sample_list()

        # Boutons en bas de la fenêtre
        button_frame = customtkinter.CTkFrame(container, fg_color="transparent")
        button_frame.pack(side="bottom", padx=20, pady=10)

        # Bouton Fermer
        self.close_button = customtkinter.CTkButton(button_frame, text="Fermer", command=self.destroy)
        self.close_button.pack(side="left", padx=10)

        # Bouton Export CSV
        self.export_csv_button = customtkinter.CTkButton(button_frame, text="Exporter", command=self.export_to_csv)
        self.export_csv_button.pack(side="left", padx=10)
        

    def display_sample_list(self):
        # Efface les éléments précédents
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Affichage des en-têtes du tableau
        if self.option_defo_percent and self.option_kn == False:
            headers = [
                "Nom Sample", "Banc de Test", 
                "Mode Testé", "Géométrie Testée", 
                "L0 [mm]", "L1 [mm]", "D0 [mm]", "W0 [mm]", "H0 [mm]", "Zone Lin. [N]", 
                "Taille des données", "Max Force [N]", "Max Dépl. [mm]",
                "Rp [MPa]", "Rm [MPa]", "Max Deform. [%]", "E [GPa]"
            ]
        elif self.option_defo_percent and self.option_kn:
            headers = [
                "Nom Sample", "Banc de Test", 
                "Mode Testé", "Géométrie Testée", 
                "L0 [mm]", "L1 [mm]", "D0 [mm]", "W0 [mm]", "H0 [mm]", "Zone Lin. [N]", 
                "Taille des données", "Max Force [kN]", "Max Dépl. [mm]",
                "Rp [MPa]", "Rm [MPa]", "Max Deform. [%]", "E [GPa]"
            ]
        elif self.option_defo_percent == False and self.option_kn:
            headers = [
                "Nom Sample", "Banc de Test", 
                "Mode Testé", "Géométrie Testée", 
                "L0 [mm]", "L1 [mm]", "D0 [mm]", "W0 [mm]", "H0 [mm]", "Zone Lin. [N]", 
                "Taille des données", "Max Force [kN]", "Max Dépl. [mm]",
                "Rp [MPa]", "Rm [MPa]", "Max Deform. [-]", "E [GPa]"
            ]
        else:
            headers = [
                "Nom Sample", "Banc de Test", 
                "Mode Testé", "Géométrie Testée", 
                "L0 [mm]", "L1 [mm]", "D0 [mm]", "W0 [mm]", "H0 [mm]", "Zone Lin. [N]", 
                "Taille des données", "Max Force [N]", "Max Dépl. [mm]",
                "Rp [MPa]", "Rm [MPa]", "Max Deform. [-]", "E [GPa]"
            ]

        for col, header in enumerate(headers):
            header_label = customtkinter.CTkLabel(self.scrollable_frame, text=header, font=("Arial", 10, "bold"))
            header_label.grid(row=0, column=col, padx=5, pady=5, sticky='w')

        # Affichage des valeurs des fichiers
        for row, sample in enumerate(self.sample_list, start=1):
            values = [
                sample.sample_name, sample.test_bench,
                sample.tested_mode, sample.tested_geometry, sample.L0, sample.L1, sample.D0, 
                sample.W0, sample.H0, f"({sample.lin_range})", f"({len(sample.time_values)},3)", 
                sample.F_max, sample.Allong, 
                sample.Re, sample.Rm, 
                sample.Defo, sample.E
            ]

            for col, value in enumerate(values):
                value_label = customtkinter.CTkLabel(self.scrollable_frame, text=value)
                value_label.grid(row=row, column=col, padx=5, pady=5, sticky='w')

    def save_as(self, titre="Enregistrer sous", defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]):
        file_path = filedialog.asksaveasfilename(
            title=titre,
            defaultextension=defaultextension,
            filetypes=filetypes
        )
        return file_path

    def export_to_csv(self):
        if not self.sample_list:
            message = "Aucun échantillon à exporter.\nVeuillez sélectionner un échantillon et recommencer."
            print(message)
            messagebox.showinfo("Exportation annulée", message)
            self.destroy()
            return
        
        self.attributes("-topmost", False)
        csv_filepath = self.save_as(titre="Exporter les données", defaultextension=".csv")
        
        if not csv_filepath:  # L'utilisateur a annulé la sauvegarde
            return
        
            
        # Écriture des données dans le fichier CSV
        with open(csv_filepath, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Écriture de l'en-tête
            
            if self.option_defo_percent and self.option_kn == False:
                headers = [
                    "Nom Sample", "Banc de Test", 
                    "Mode Testé", "Géométrie Testée", 
                    "L0 [mm]", "L1 [mm]", "D0 [mm]", "W0 [mm]", "H0 [mm]", "Zone Lin. [N]", 
                    "Taille des données", "Max Force [N]", "Max Dépl. [mm]",
                    "Rp [MPa]", "Rm [MPa]", "Max Deform. [%]", "E [GPa]"
                ]
            elif self.option_defo_percent and self.option_kn:
                headers = [
                    "Nom Sample", "Banc de Test", 
                    "Mode Testé", "Géométrie Testée", 
                    "L0 [mm]", "L1 [mm]", "D0 [mm]", "W0 [mm]", "H0 [mm]", "Zone Lin. [N]", 
                    "Taille des données", "Max Force [kN]", "Max Dépl. [mm]",
                    "Rp [MPa]", "Rm [MPa]", "Max Deform. [%]", "E [GPa]"
                ]
            elif self.option_defo_percent == False and self.option_kn:
                headers = [
                    "Nom Sample", "Banc de Test", 
                    "Mode Testé", "Géométrie Testée", 
                    "L0 [mm]", "L1 [mm]", "D0 [mm]", "W0 [mm]", "H0 [mm]", "Zone Lin. [N]", 
                    "Taille des données", "Max Force [kN]", "Max Dépl. [mm]",
                    "Rp [MPa]", "Rm [MPa]", "Max Deform. [-]", "E [GPa]"
                ]
            else:
                headers = [
                    "Nom Sample", "Banc de Test", 
                    "Mode Testé", "Géométrie Testée", 
                    "L0 [mm]", "L1 [mm]", "D0 [mm]", "W0 [mm]", "H0 [mm]", "Zone Lin. [N]", 
                    "Taille des données", "Max Force [N]", "Max Dépl. [mm]",
                    "Rp [MPa]", "Rm [MPa]", "Max Deform. [-]", "E [GPa]"
                ]
            writer.writerow(headers)
            # Écriture des lignes de données
            for sample in self.sample_list:
                writer.writerow([
                    sample.sample_name, sample.test_bench,
                    sample.tested_mode, sample.tested_geometry, sample.L0, sample.L1, sample.D0, 
                    sample.W0, sample.H0, f"({sample.lin_range})", f"({len(sample.time_values)},3)", 
                    sample.F_max, sample.Allong, 
                    sample.Re, sample.Rm, 
                    sample.Defo, sample.E
                ])
                
        message = f"Données exportées vers : {csv_filepath}"
        print(message)
        messagebox.showinfo("Exportation terminée", message)
        self.destroy()
        return
    
    
    def update_file_list(self, sample_list):
        option_list = self.master.interface_functions.get_options()
        self.option_defo_percent = option_list.get('option_defo_percent', False)
        self.option_kn = option_list.get('option_kn', False)
        self.sample_list = sample_list
        self.display_sample_list()
        return
        
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
