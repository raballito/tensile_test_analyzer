# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 09:18:49 2024

Version: 1.0
Last Update: 15.05.24

@author: quentin.raball
"""

import os
import csv
import customtkinter
from tkinter import messagebox

class VarToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, sample_list, master, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Liste des variables des fichiers sélectionnés")
        self.geometry("900x400")  # Taille initiale de la fenêtre
        self.master = master

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
        headers = [
            "Sample Name", "Test Bench", 
            "Tested Mode", "Tested Geometry", 
            "L0 [mm]", "L1 [mm]", "D0 [mm]", "W0 [mm]", "H0 [mm]", "Lin Range [N]", 
            "Size of Data Values", "Max Force [N]", "Max Stroke [mm]",
            "Rp [MPa]", "Rm [MPa]", "Max Deform [%]", "E [GPa]"
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
        chiffres_sign = int(self.master.option_chiffre_sign.get())
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Affichage des en-têtes du tableau
        headers = [
            "Sample Name", "Test Bench", 
            "Tested Mode", "Tested Geometry", 
            "L0 [mm]", "L1 [mm]", "D0 [mm]", "W0 [mm]", "H0 [mm]", "Lin Range [N]", 
            "Size of Data Values", "Max Force [N]", "Max Stroke [mm]",
            "Re [MPa]", "Rm [MPa]", "Max Deform [%]", "E [GPa]"
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
                self.format_sign(sample.F_max, chiffres_sign), self.format_sign(sample.Allong, chiffres_sign), 
                self.format_sign(sample.Re, chiffres_sign), self.format_sign(sample.Rm, chiffres_sign), 
                self.format_sign(sample.Defo, chiffres_sign), self.format_sign(sample.E, chiffres_sign)
            ]

            for col, value in enumerate(values):
                value_label = customtkinter.CTkLabel(self.scrollable_frame, text=value)
                value_label.grid(row=row, column=col, padx=5, pady=5, sticky='w')

    def export_to_csv(self):
        if not self.sample_list:
            message = "Aucun échantillon à exporter.\nVeuillez sélectionner un échantillon et recommencer."
            print(message)
            messagebox.showinfo("Exportation annulée", message)
            self.destroy()
            return

        csv_filename = "samples_summary.csv"
        output_dir = "output"
        csv_filepath = os.path.join(output_dir, csv_filename)
        chiffres_sign = int(self.master.option_chiffre_sign.get())
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
            
        # Écriture des données dans le fichier CSV
        with open(csv_filepath, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Écriture de l'en-tête
            writer.writerow([
                "Sample Name", "Test Bench", 
                "Tested Mode", "Tested Geometry", 
                "L0 [mm]", "L1 [mm]", "D0 [mm]", "W0 [mm]", "H0 [mm]", "Lin Range [N]", 
                "Size of Data Values", "Max Force [N]", "Max Stroke [mm]",
                "Re [MPa]", "Rm [MPa]", "Max Deform [%]", "E [GPa]"
            ])
            # Écriture des lignes de données
            for sample in self.sample_list:
                writer.writerow([
                    sample.sample_name, sample.test_bench,
                    sample.tested_mode, sample.tested_geometry, sample.L0, sample.L1, sample.D0, 
                    sample.W0, sample.H0, f"({sample.lin_range})", f"({len(sample.time_values)},3)", 
                    self.format_sign(sample.F_max, chiffres_sign), self.format_sign(sample.Allong, chiffres_sign), 
                    self.format_sign(sample.Re, chiffres_sign), self.format_sign(sample.Rm, chiffres_sign), 
                    self.format_sign(sample.Defo, chiffres_sign), self.format_sign(sample.E, chiffres_sign)
                ])
                
        message = f"Données exportées vers : {csv_filepath}"
        print(message)
        messagebox.showinfo("Exportation terminée", message)
        self.destroy()
        return
    
    def update_file_list(self, sample_list):
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