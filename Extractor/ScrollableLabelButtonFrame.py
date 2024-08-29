# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 11:15:29 2024

- Scrollable File List + Checkbox + Buttons structure
- Highlighting correct line in the list on click
- Sync with Sample structure
- Add/remove file functions
- Get selected checkbox and sample vars functions from mainwindow
- Get Export Options functions

Version: Beta 1.9
Last Update: 26.08.24

@author: quentin.raball

"""
import os
import customtkinter
from Extractor.Functions_GUI import InterfaceFunctions
from Extractor.Sample import Sample
from Extractor.TestBench import TestBench


class ScrollableLabelButtonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, label_text="Liste des fichiers", **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.master = master
        self.checkbox_variable_list = []  # Liste des variables des cases à cocher
        self.switch_list = []  # Liste des cases à cocher
        self.button_list = []  # Liste des boutons
        self.sample_list = []  # Liste des samples, utilisé pour sauvegarder les infos
        self.frame_list = []  # Liste des cadres pour chaque ligne
        self.interface_functions = InterfaceFunctions(self.master)
        self.selected_frame = None
        self.selected_sample = None
        
        
        self.bind_all("<MouseWheel>", self.on_mouse_wheel)
        self.bind_all("<Button-4>", self.on_mouse_wheel)
        self.bind_all("<Button-5>", self.on_mouse_wheel)
    
    def on_mouse_wheel(self, event):
        if event.num == 4 or event.delta > 0:
            self._parent_canvas.yview_scroll(-10, "units")
        elif event.num == 5 or event.delta < 0:
            self._parent_canvas.yview_scroll(10, "units")
    
    def check_empty_list(self):
        if len(self.sample_list) != 0:
            self.master.hide_instruction_message()
        else:
            self.master.show_instruction_message()

    def add_item(self, file_path):
        test_bench_struct = TestBench(self)  # Créer une instance de TestBench pour chaque échantillon
        sample_and_channel = test_bench_struct.identify_file(file_path)
        try:
            file_path_rel = self.interface_functions.create_short_list([file_path])[0]
        except ValueError as e:
            # Si une erreur se produit lors de la création du chemin relatif, utilisez le chemin complet
            print(f"Erreur lors de la création du chemin relatif pour {file_path}. Utilisation du chemin complet.\nErreur: {e}")
            file_path_rel = file_path
        # Identification du fichier
        test_bench = TestBench.identify_test_bench(file_path)
    
        for available_sample_name, time_channel, force_channel, stroke_channel in zip(*sample_and_channel):
            sample_struct = Sample(self)  # Crée l'échantillon avec un identifiant unique
            checkbox_var = customtkinter.IntVar()
            self.checkbox_variable_list.append(checkbox_var)
            # Assignation des valeurs
            sample_struct.file_name = os.path.basename(file_path)
            sample_struct.file_path = file_path
            sample_struct.sample_name = available_sample_name
            sample_struct.test_bench = test_bench
            sample_struct.separator = test_bench_struct.separator
            sample_struct.header_index = test_bench_struct.header_index
            sample_struct.force_unit = test_bench_struct.force_unit
            sample_struct.repeat_every = test_bench_struct.repeat_every
            sample_struct.time_channel = time_channel
            sample_struct.force_channel = force_channel
            sample_struct.stroke_channel = stroke_channel
            imported = sample_struct.import_data()
            if imported == None:
                print(f"Erreur d'importation du fichier {file_path_rel}.\nFichier ignoré.\n")
                self.checkbox_variable_list.remove(checkbox_var)
                break
            # Création des lignes du tableau
            frame = customtkinter.CTkFrame(self)  # Nouveau cadre pour chaque ligne de fichier
            frame.configure(fg_color=("gray85", "gray25"))
            
            switch = customtkinter.CTkCheckBox(frame, text=f"{sample_struct.sample_name}", variable=checkbox_var)
            switch.sample_id = sample_struct.sample_id 
            label = customtkinter.CTkLabel(frame, text=f"{file_path_rel}")
            frame.bind("<Button-1>", lambda event, frame=frame, sample=sample_struct: self.highlight_row(event, frame, sample))
            label.bind("<Button-1>", lambda event, frame=frame, sample=sample_struct: self.highlight_row(event, frame, sample))
            button = customtkinter.CTkButton(frame, text="Propriétés", width=100, height=24, command=lambda sample=sample_struct, item=switch: self.interface_functions.config_button_frame_event(sample, self.master, item))
            button.bind("<Button-1>", lambda event, frame=frame, sample=sample_struct: self.highlight_row(event, frame, sample))
            switch.bind("<Button-1>", lambda event, frame=frame, sample=sample_struct: self.highlight_row(event, frame, sample))
            
            switch.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="w")  
            label.grid(row=0, column=1, padx=10, pady=(10, 10), sticky="e")  
            button.grid(row=0, column=2, padx=5, pady=(10, 10), sticky="e")
            frame.grid_columnconfigure(1, weight=1)  
            frame.grid(row=len(self.switch_list), column=0, sticky="ew")  
            self.switch_list.append(switch)
            self.button_list.append(button)
            self.sample_list.append(sample_struct)
            self.frame_list.append(frame)

    def remove_item(self, item):
        for switch, button, check, frame, sample in zip(self.switch_list, self.button_list, self.checkbox_variable_list, self.frame_list, self.sample_list):
            if switch.sample_id == item:
                button.destroy()
                switch.destroy()
                frame.destroy()
                self.switch_list.remove(switch)
                self.button_list.remove(button)
                self.checkbox_variable_list.remove(check)
                self.frame_list.remove(frame)
                self.sample_list.remove(sample)
        self.check_empty_list()    
        
    def remove_all_items(self):
        for frame in self.frame_list:
            frame.destroy()
        self.frame_list.clear()
        self.switch_list.clear()
        self.button_list.clear()
        self.sample_list.clear()
        self.checkbox_variable_list.clear()
    
    def get_selected_checkboxes(self):
        selected_checkboxes = []
        for checkbox_var, switch in zip(self.checkbox_variable_list, self.switch_list):
            if checkbox_var.get() == 1:
                selected_checkboxes.append(switch.sample_id)  # Utilisez l'ID unique plutôt que le texte
        print("Éléments sélectionnés:", selected_checkboxes)
        return selected_checkboxes
    
    def get_sample_var(self, selected_elements):
        sample_var_list = []
        for selected_element in selected_elements:
            for sample in self.sample_list:
                if sample.sample_id == selected_element:  # Correspondance via l'ID unique
                    sample_var_list.append(sample)
                    break
        return sample_var_list

    def highlight_row(self, event, frame, sample):
        for f in self.frame_list:
            if f == frame:
                f.configure(fg_color=("red", "red"))
                self.selected_frame = f
            else:
                f.configure(fg_color=("gray85", "gray25"))            
        self.interface_functions.preview_file(sample)
        frame.configure(fg_color=("red", "darkred"))
        self.selected_frame = frame
        self.selected_sample = sample
        
    def get_round_val(self):
        round_val = self.master.option_chiffre_sign.get()
        return round_val
    
    def get_coef_rp(self):
        coef_rp = self.master.option_lim_elast.get()
        return coef_rp
    
    def get_option_file_path(self):
        value_file_path = self.master.checkbox_6.get()
        if value_file_path == 0:
            option_file_path = False
        elif value_file_path ==1:
            option_file_path = True
        return option_file_path
    
    def get_option_sample_name(self):
        value_sample_name = self.master.checkbox_1.get()
        if value_sample_name == 0:
            option_sample_name = False
        elif value_sample_name ==1:
            option_sample_name = True
        return option_sample_name
    
    def get_option_scale_kN(self):
        value_scale_kN = self.master.checkbox_7.get()
        if value_scale_kN == 0:
            option_scale_kN = False
        elif value_scale_kN ==1:
            option_scale_kN = True
        return option_scale_kN
    
    def get_option_show_force_stroke(self):
        value_show_force_stroke = self.master.checkbox_5.get()
        if value_show_force_stroke == 0:
            option_show_force_stroke = False
        elif value_show_force_stroke ==1:
            option_show_force_stroke = True
        return option_show_force_stroke
    
    def get_option_defo_percent(self):
        value_defo_percent = self.master.checkbox_3.get()
        if value_defo_percent == 0:
            option_value_defo_percent = False
        elif value_defo_percent ==1:
            option_value_defo_percent = True
        return option_value_defo_percent
    
    def get_option_show_rp(self):
        value_show_rp = self.master.checkbox_4.get()
        if value_show_rp == 0:
            option_value_show_rp = False
        elif value_show_rp ==1:
            option_value_show_rp = True
        return option_value_show_rp
    
    def get_option_show_legend(self):
        value_show_legend = self.master.checkbox_2.get()
        if value_show_legend == 0:
            option_show_legend = False
        elif value_show_legend == 1:
            option_show_legend = True
        return option_show_legend
