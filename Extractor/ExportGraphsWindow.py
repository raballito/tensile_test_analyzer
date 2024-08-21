# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 12:37:41 2024

Graphics Export Window
- Selection of the desired Graphics
- Availablility depends on the analysis of the sample
- Export in Output directory

Version: Beta 1.8
Last Update: 21.08.24

@author: quentin.raball
"""

import customtkinter as ctk
from tkinter import IntVar

class ExportGraphsWindow(ctk.CTkToplevel):
    def __init__(self, sample_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Sélection des graphiques à exporter")
        self.geometry("500x300")
        self.sample_list = sample_list
        
        # Variable pour suivre les choix des utilisateurs
        self.selected_options = {
            'force_displacement': IntVar(value=1),
            'force_time': IntVar(value=1),
            'stress_deformation': IntVar(value=0),
            'stress_displacement': IntVar(value=0)
        }
        
        self.create_widgets(sample_list)

    def create_widgets(self, sample_list):
        ctk.CTkLabel(self, text="Choisissez les graphiques à exporter :", font=("Arial", 12, "bold")).pack(pady=10)
        
        self.strenght_displacement_cb = ctk.CTkCheckBox(self, text="Force-Déplacement", variable=self.selected_options['force_displacement'])
        self.strenght_displacement_cb.pack(anchor='w', padx=20, pady=5)
        
        self.strenght_time_cb = ctk.CTkCheckBox(self, text="Force-Temps", variable=self.selected_options['force_time'])
        self.strenght_time_cb.pack(anchor='w', padx=20, pady=5)
        
        self.stress_deformation_cb = ctk.CTkCheckBox(self, text="Contrainte-Déformation", variable=self.selected_options['stress_deformation'])
        self.stress_deformation_cb.pack(anchor='w', padx=20, pady=5)
        
        self.stress_displacement_cb = ctk.CTkCheckBox(self, text="Contrainte-Déplacement", variable=self.selected_options['stress_displacement'])
        self.stress_displacement_cb.pack(anchor='w', padx=20, pady=5)
        
        ctk.CTkButton(self, text="Exporter", command=lambda: self.export_selected(sample_list)).pack(pady=20)

        self.update_checkbox_state(sample_list)

    def update_checkbox_state(self, sample_list):
        # Vérifier si tous les échantillons sont analysés
        if len(sample_list) == 0:
            self.strenght_displacement_cb.deselect()
            self.strenght_time_cb.deselect()
            self.stress_deformation_cb.deselect()
            self.stress_displacement_cb.deselect()
            self.stress_deformation_cb.configure(state='disabled')
            self.stress_displacement_cb.configure(state='disabled')
            self.strenght_displacement_cb.configure(state='disabled')
            self.strenght_time_cb.configure(state='disabled')
        else:
            all_analyzed = all(sample.analyzed_sample for sample in sample_list)
            if not all_analyzed:
                self.stress_deformation_cb.deselect()
                self.stress_displacement_cb.deselect()
                self.stress_deformation_cb.configure(state='disabled')
                self.stress_displacement_cb.configure(state='disabled')
            else:
                self.stress_deformation_cb.select()
                self.stress_displacement_cb.select()
                self.stress_deformation_cb.configure(state='normal')
                self.stress_displacement_cb.configure(state='normal')

    def export_selected(self, sample_list):
        self.attributes("-topmost", False)
        selected_graphs = {
            'force_displacement': self.selected_options['force_displacement'].get(),
            'force_time': self.selected_options['force_time'].get(),
            'stress_deformation': self.selected_options['stress_deformation'].get(),
            'stress_displacement': self.selected_options['stress_displacement'].get()
        }
        
        graphs_to_export = []
        
        if selected_graphs['force_displacement']:
            graphs_to_export.append('Force-Déplacement')
        
        if selected_graphs['force_time']:
            graphs_to_export.append('Force-Temps')
        
        if selected_graphs['stress_deformation']:
            graphs_to_export.append('Contrainte-Déformation')
        
        if selected_graphs['stress_displacement']:
            graphs_to_export.append('Contrainte-Déplacement')
        
        
        self.master.interface_functions.export_graphics_event(sample_list, graphs_to_export)
        self.destroy()
