# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 09:18:49 2024

Configuration Window

- Handling the individual configuration for sample
- Geometry configuration
- Analysis mode configuration
- Changing the name of the sample
- Configuration of sample class through GUI


Version: Beta 1.2
Last Update: 07.08.24


@author: quentin.raball
"""

import os
import tkinter
import customtkinter
from PIL import Image



class ConfigWindow(customtkinter.CTkToplevel):
    def __init__(self, sample, master, item, *args, **kwargs):
        super().__init__(master,*args, **kwargs)
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.title("Configuration de l'échantillon")
        self.geometry("400x860")
        
        # Definition variables
        self.master = master
        self.sample = sample
        self.item = item
        
        if not hasattr(self.sample, 'last_mode_chosen'):
            self.sample.last_mode_chosen = 0
            
        if not hasattr(self.sample, 'last_geometry_chosen'):
            self.sample.last_geometry_chosen = "Section Ronde"
            
        sample_name = self.sample.sample_name
        file_path = self.sample.file_path
        test_bench = self.sample.test_bench
        
        # Valeurs de champs par défaut
        if not self.sample.D0 == None:
            D0_default = tkinter.StringVar(self, self.sample.D0)
        else:
            D0_default = tkinter.StringVar(self, 1)
        if not self.sample.L0 == None:
            L0_default = tkinter.StringVar(self, self.sample.L0)
        else:
            L0_default = tkinter.StringVar(self, 100)
        if not self.sample.L1 == None:
            L1_default = tkinter.StringVar(self, self.sample.L1)
        else: 
            L1_default = tkinter.StringVar(self, 20)
        if not self.sample.W0 == None:
            W0_default = tkinter.StringVar(self, self.sample.W0)
        else:
            W0_default = tkinter.StringVar(self, 3)
        if not self.sample.H0 == None:
            H0_default = tkinter.StringVar(self, self.sample.H0)
        else:
            H0_default = tkinter.StringVar(self, 2)
        
        F_min_default = tkinter.StringVar(self, self.sample.lin_range[0])
        F_max_default = tkinter.StringVar(self, self.sample.lin_range[1])
        

        self.top_frame = customtkinter.CTkFrame(self)
        self.top_frame.grid(row=0, column=0, padx=20, pady=(20,0), sticky="nsew")
        
        # Champ "Fichier édité:"
        self.label_edited_file = customtkinter.CTkLabel(self.top_frame, text="Fichier édité:", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label_edited_file.grid(row=0, column=0, padx=20, pady=(5,0), sticky="nswe")
        
        # Chemin du fichier
        self.label_file_path = customtkinter.CTkLabel(self.top_frame, text=file_path)
        self.label_file_path.grid(row=1, column=0, padx=20, pady=0, sticky="nswe")
        
        # Champ "Nom de l'échantillon:"
        self.label_sample_name = customtkinter.CTkLabel(self.top_frame, text="Nom de l'échantillon:", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label_sample_name.grid(row=2, column=0, padx=20, pady=0, sticky="nswe")
        
        # Nom de l'échantillon
        self.sample_name = customtkinter.CTkLabel(self.top_frame, text=sample_name)
        self.sample_name.grid(row=3, column=0, padx=20, pady=0, sticky="nswe")
        self.top_frame.grid_columnconfigure(0, weight=1)
        self.top_frame.grid_rowconfigure(0, weight=1)
        
        # Option type de sample et caractéristiques géométriques
        # Créer la tabview avec deux onglets
        self.tabview = customtkinter.CTkTabview(self)
        self.tabview.grid(row=4, column=0, padx=(20, 20), pady=(10,0), sticky="nsew")        
        self.columnconfigure(0, weight=1)
        self.tabview.add("Section Ronde")
        self.tabview.tab("Section Ronde").grid_columnconfigure(0, weight=0)
        self.tabview.tab("Section Ronde").grid_columnconfigure(1, weight=1)
        image_rond_img_light = Image.open("static/image_traction_rond.png")
        image_rond_img_dark = Image.open("static/image_traction_rond_dark.png")
        self.image_rond = customtkinter.CTkImage(light_image=image_rond_img_light,
                                            dark_image=image_rond_img_dark,
                                            size=(100, 334))
        self.image_label_rond = customtkinter.CTkLabel(self.tabview.tab("Section Ronde"), image=self.image_rond, text="")
        self.image_label_rond.image = self.image_rond  # keep a reference to avoid garbage collection
        self.image_label_rond.grid(row=0, column=0, padx=(10, 0), pady=(10, 10), rowspan=8, sticky="nsew")
        self.tabview.add("Section Rectangulaire")
        self.tabview.tab("Section Rectangulaire").grid_columnconfigure(0, weight=0)  # configure grid of individual tabs
        self.tabview.tab("Section Rectangulaire").grid_columnconfigure(1, weight=1)
        image_rect_img_light = Image.open("static/image_traction_rect.png")
        image_rect_img_dark = Image.open("static/image_traction_rect_dark.png")
        self.image_rect = customtkinter.CTkImage(light_image=image_rect_img_light,
                                            dark_image=image_rect_img_dark,
                                            size=(100, 334))
        self.image_label_rect = customtkinter.CTkLabel(self.tabview.tab("Section Rectangulaire"), image=self.image_rect, text="")
        self.image_label_rect.image = self.image_rect  # keep a reference to avoid garbage collection
        self.image_label_rect.grid(row=0, column=0, padx=(10, 0), pady=(10, 10), rowspan=10,  sticky="nsew")
        # Section Ronde - Options
        self.label_diam_init_rond = customtkinter.CTkLabel(self.tabview.tab("Section Ronde"), text="Diamètre initial D0 [mm] :")
        self.label_diam_init_rond.grid(row=0, column=1, padx=10, pady=(10,0))
        self.option_diam_init_rond = customtkinter.CTkEntry(self.tabview.tab("Section Ronde"), textvariable = D0_default)
        self.option_diam_init_rond.grid(row=1, column=1, padx=10)
        self.label_long_init_rond = customtkinter.CTkLabel(self.tabview.tab("Section Ronde"), text="Longueur initiale L0 [mm] :")
        self.label_long_init_rond.grid(row=2, column=1, padx=10, pady=(10,0))
        self.option_long_init_rond = customtkinter.CTkEntry(self.tabview.tab("Section Ronde"), textvariable = L0_default)
        self.option_long_init_rond.grid(row=3, column=1, padx=10)
        self.label_f_max_rond = customtkinter.CTkLabel(self.tabview.tab("Section Ronde"), text="Force max régression linéaire [N] :")
        self.label_f_max_rond.grid(row=4, column=1, padx=10, pady=(10,0))
        self.option_f_max_rond = customtkinter.CTkEntry(self.tabview.tab("Section Ronde"), textvariable = F_max_default)
        self.option_f_max_rond.grid(row=5, column=1, padx=10)
        self.label_f_min_rond = customtkinter.CTkLabel(self.tabview.tab("Section Ronde"), text="Force min régression linéaire [N] :")
        self.label_f_min_rond.grid(row=6, column=1, padx=10, pady=(10,0))
        self.option_f_min_rond = customtkinter.CTkEntry(self.tabview.tab("Section Ronde"), textvariable = F_min_default)
        self.option_f_min_rond.grid(row=7, column=1, padx=10, pady=(10, 0))
        self.label_long_l1_rond = customtkinter.CTkLabel(self.tabview.tab("Section Ronde"), text="Longueur d'appui L1 [mm] :")
        self.label_long_l1_rond.grid(row=10, column=1, padx=10, pady=(10, 0))
        self.option_long_l1_rond = customtkinter.CTkEntry(self.tabview.tab("Section Ronde"), textvariable=L1_default)
        self.option_long_l1_rond.grid(row=11, column=1, padx=10, pady=(0, 10))
        self.label_long_l1_rond.grid_remove()
        self.option_long_l1_rond.grid_remove()
        
        # Section Rectangulaires - Options
        self.label_W0_init_rect = customtkinter.CTkLabel(self.tabview.tab("Section Rectangulaire"), text="Largeur initiale W0 [mm] :")
        self.label_W0_init_rect.grid(row=0, column=1, padx=10, pady=(10,0))
        self.option_W0_init_rect = customtkinter.CTkEntry(self.tabview.tab("Section Rectangulaire"), textvariable = W0_default)
        self.option_W0_init_rect.grid(row=1, column=1, padx=10)
        self.label_H0_init_rect = customtkinter.CTkLabel(self.tabview.tab("Section Rectangulaire"), text="Epaisseur initiale H0 [mm] :")
        self.label_H0_init_rect.grid(row=2, column=1, padx=10, pady=(10,0))
        self.option_H0_init_rect = customtkinter.CTkEntry(self.tabview.tab("Section Rectangulaire"), textvariable = H0_default)
        self.option_H0_init_rect.grid(row=3, column=1, padx=10)
        self.label_long_init_rect = customtkinter.CTkLabel(self.tabview.tab("Section Rectangulaire"), text="Longueur initiale L0 [mm] :")
        self.label_long_init_rect.grid(row=4, column=1, padx=10, pady=(10,0))
        self.option_long_init_rect = customtkinter.CTkEntry(self.tabview.tab("Section Rectangulaire"), textvariable = L0_default)
        self.option_long_init_rect.grid(row=5, column=1, padx=10)
        self.label_f_max_rect = customtkinter.CTkLabel(self.tabview.tab("Section Rectangulaire"), text="Force max régression linéaire [N] :")
        self.label_f_max_rect.grid(row=6, column=1, padx=10, pady=(10,0))
        self.option_f_max_rect = customtkinter.CTkEntry(self.tabview.tab("Section Rectangulaire"), textvariable = F_max_default)
        self.option_f_max_rect.grid(row=7, column=1, padx=10)
        self.label_f_min_rect = customtkinter.CTkLabel(self.tabview.tab("Section Rectangulaire"), text="Force min régression linéaire [N] :")
        self.label_f_min_rect.grid(row=8, column=1, padx=10, pady=(10,0))
        self.option_f_min_rect = customtkinter.CTkEntry(self.tabview.tab("Section Rectangulaire"), textvariable = F_min_default)
        self.option_f_min_rect.grid(row=9, column=1, padx=10, pady=(10, 0))
        self.label_long_l1_rect = customtkinter.CTkLabel(self.tabview.tab("Section Rectangulaire"), text="Longueur d'appui L1 [mm] :")
        self.label_long_l1_rect.grid(row=10, column=1, padx=10, pady=(10, 0))
        self.option_long_l1_rect = customtkinter.CTkEntry(self.tabview.tab("Section Rectangulaire"), textvariable=L1_default)
        self.option_long_l1_rect.grid(row=11, column=1, padx=10, pady=(0, 10))
        self.label_long_l1_rect.grid_remove()
        self.option_long_l1_rect.grid_remove()
        
        # Sélectionner l'onglet correct à l'ouverture de la fenêtre
        self.tabview.set(self.sample.last_geometry_chosen)

        # Options de fichiers et d'analyse (Tab1)
        self.tabview_options = customtkinter.CTkTabview(self)
        self.tabview_options.grid(row=5, column=0, padx=(20, 20), pady=(10, 0), sticky="nsew", columnspan=3)
        self.tabview_options.add("Mode de test")
        self.tabview_options.add("Options fichiers")
        self.tabview_options.tab("Mode de test").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview_options.tab("Options fichiers").grid_columnconfigure(0, weight=1)
        self.radiobutton_frame = customtkinter.CTkFrame(self.tabview_options.tab("Mode de test"))
        self.radiobutton_frame.grid(row=1, column=0, padx=(20, 0), pady=(10, 0), sticky="nsew")
        
        self.radio_var = tkinter.IntVar(value=self.sample.last_mode_chosen)
        
        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, text="Traction/Compression", variable=self.radio_var, value=0, command=lambda:self.radio_test_mode_event())
        self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="w")
        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, text="Flexion 3 points", variable=self.radio_var, value=1, command=lambda:self.radio_test_mode_event())
        self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="w")
        self.radio_button_3 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, text="Flexion 4 points", variable=self.radio_var, value=2, command=lambda:self.radio_test_mode_event())
        self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="w")
        self.radio_button_4 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, text="Module de Young", variable=self.radio_var, value=3,command=lambda:self.radio_test_mode_event())
        self.radio_button_4.grid(row=4, column=2, pady=10, padx=20, sticky="w")
        # Options de fichiers et d'analyse (Tab2)
        self.label_option_machine = customtkinter.CTkLabel(self.tabview_options.tab("Options fichiers"), text="Machine de test utilisée :")
        self.label_option_machine.grid(row=0, column=0, padx=20, pady=(10,0))
        self.option_machine = customtkinter.CTkOptionMenu(self.tabview_options.tab("Options fichiers"), dynamic_resizing=True,
                                                        values=["Shimadzu 20kN", "W+B 100kN", "W+B 400kN"])
        self.option_machine.grid(row=1, column=0, padx=20)
        self.label_option_machine = customtkinter.CTkLabel(self.tabview_options.tab("Options fichiers"), text="Canal utilisé :")
        self.label_option_machine.grid(row=2, column=0, padx=20, pady=(10,0))
        self.option_canal = customtkinter.CTkOptionMenu(self.tabview_options.tab("Options fichiers"), dynamic_resizing=True,
                                                    values=["Canal Traverse", "Canal Extensomètre"])
        self.option_canal.grid(row=3, column=0, padx=20)
        self.option_canal.set(self.sample.selected_channel)
        self.name_input_button = customtkinter.CTkButton(self.tabview_options.tab("Options fichiers"), text="Changer nom du sample",
                                                           command= lambda: self.open_input_dialog_event(self.item))
        self.name_input_button.grid(row=6, column=0, padx=20, pady=(20, 0))
        
        
        self.save_button = customtkinter.CTkButton(self, text="Sauvegarder", command=lambda: self.on_close(), font=customtkinter.CTkFont(size=15, weight="bold"))
        self.save_button.grid(row=7, column=0, pady=10, padx=20, sticky="nswe")
        
        # Comportement par défaut
        #self.radio_button_3.configure(state="disabled")
        
        relative_path = os.path.relpath(file_path)
        self.option_machine.set(test_bench)
        self.label_file_path.configure(text=relative_path)
        self.update_l1_visibility()
        
        if test_bench == "Shimadzu" or test_bench == "WB400kN":
            self.option_machine.configure(state="disabled")
            self.option_canal.set("Canal Traverse")
            self.option_canal.configure(state="disabled")
            self.radio_button_4.configure(state="disabled")
            
        elif test_bench == "WB100kN":
            self.option_machine.configure(state="disabled")
            self.option_canal.configure(state="enabled")
        else:
            self.option_machine.set("WB100kN")
            self.option_canal.configure(state="enabled")
            self.option_machine.configure(state="enabled")
            self.radio_button_4.configure(state="disabled")
            
            
        
    def radio_test_mode_event(self):
        mode_test = self.radio_var.get()
        if mode_test == 0: # Test traction
            image_rect_img_light = Image.open("static/image_traction_rect.png")
            image_rect_img_dark = Image.open("static/image_traction_rect_dark.png")
            self.image_rect = customtkinter.CTkImage(light_image=image_rect_img_light,
                                                dark_image=image_rect_img_dark,
                                                size=(100, 334))
            self.image_label_rect.configure(image=self.image_rect)
            self.image_label_rect.image = self.image_rect  # Update image reference
           
            image_rond_img_light = Image.open("static/image_traction_rond.png")
            image_rond_img_dark = Image.open("static/image_traction_rond_dark.png")
            self.image_rond = customtkinter.CTkImage(light_image=image_rond_img_light,
                                                dark_image=image_rond_img_dark,
                                                size=(100, 334))
            self.image_label_rond.configure(image=self.image_rond)
            self.image_label_rond.image = self.image_rond  # Update image reference
            self.option_canal.configure(state="enable")
            
        elif mode_test == 1: # Test flexion 3pts
            image_rect_img_light = Image.open("static/image_flexion_3pts_rect.png")
            image_rect_img_dark = Image.open("static/image_flexion_3pts_rect_dark.png")
            self.image_rect = customtkinter.CTkImage(light_image=image_rect_img_light,
                                                dark_image=image_rect_img_dark,
                                                size=(100, 334))
            self.image_label_rect.configure(image=self.image_rect)
            self.image_label_rect.image = self.image_rect  # Update image reference
            
            image_rond_img_light = Image.open("static/image_flexion_3pts_rond.png")
            image_rond_img_dark = Image.open("static/image_flexion_3pts_rond_dark.png")
            self.image_rond = customtkinter.CTkImage(light_image=image_rond_img_light,
                                                dark_image=image_rond_img_dark,
                                                size=(100, 334))
            self.image_label_rond.configure(image=self.image_rond)
            self.image_label_rond.image = self.image_rond  # Update image reference
            self.option_canal.set("Canal Traverse")
            self.option_canal.configure(state="disabled")
        
        elif mode_test == 2: # Test flexion 4pts
            image_rect_img_light = Image.open("static/image_flexion_4pts_rect.png")
            image_rect_img_dark = Image.open("static/image_flexion_4pts_rect_dark.png")
            self.image_rect = customtkinter.CTkImage(light_image=image_rect_img_light,
                                                dark_image=image_rect_img_dark,
                                                size=(100, 334))
            self.image_label_rect.configure(image=self.image_rect)
            self.image_label_rect.image = self.image_rect  # Update image reference
            
            image_rond_img_light = Image.open("static/image_flexion_4pts_rond.png")
            image_rond_img_dark = Image.open("static/image_flexion_4pts_rond_dark.png")
            self.image_rond = customtkinter.CTkImage(light_image=image_rond_img_light,
                                                dark_image=image_rond_img_dark,
                                                size=(100, 334))
            self.image_label_rond.configure(image=self.image_rond)
            self.image_label_rond.image = self.image_rond  # Update image reference
            self.option_canal.set("Canal Traverse")
            self.option_canal.configure(state="disabled")
            
        elif mode_test == 3: # Test Module de Young
            image_rect_img_light = Image.open("static/image_mod_young_rect.png")
            image_rect_img_dark = Image.open("static/image_mod_young_rect_dark.png")
            self.image_rect = customtkinter.CTkImage(light_image=image_rect_img_light,
                                                dark_image=image_rect_img_dark,
                                                size=(100, 334))
            self.image_label_rect.configure(image=self.image_rect)
            self.image_label_rect.image = self.image_rect  # Update image reference
            
            image_rond_img_light = Image.open("static/image_mod_young_rond.png")
            image_rond_img_dark = Image.open("static/image_mod_young_rond_dark.png")
            self.image_rond = customtkinter.CTkImage(light_image=image_rond_img_light,
                                                dark_image=image_rond_img_dark,
                                                size=(100, 334))
            self.image_label_rond.configure(image=self.image_rond)
            self.image_label_rond.image = self.image_rond  # Update image reference
            self.option_canal.set("Canal Extensomètre")
            self.option_canal.configure(state="disabled")
            
        self.update_l1_visibility()

    def open_input_dialog_event(self, item):
        dialog = customtkinter.CTkInputDialog(text="Veuillez saisir un nom d'échantillon:", title="Edition du nom d'échantillon")
        new_name = dialog.get_input()
        self.sample_name.configure(text=new_name)
        self.sample.sample_name = new_name
        item.configure(text=new_name)
        print("Nouveau nom de sample:", new_name)
        
    def update_l1_visibility(self):
        mode_test = self.radio_var.get()
        if mode_test == 2:  # Flexion 4 points
            self.label_long_l1_rond.grid()
            self.option_long_l1_rond.grid()
            self.label_long_l1_rect.grid()
            self.option_long_l1_rect.grid()
            self.geometry("400x940")
        else:
            self.label_long_l1_rond.grid_remove()
            self.option_long_l1_rond.grid_remove()
            self.label_long_l1_rect.grid_remove()
            self.option_long_l1_rect.grid_remove()
            self.geometry("400x860")

        
    def get_test_mode(self):
        test_number = self.radio_var.get()
        test_modes = {
            0: "Traction",
            1: "Flexion 3pts",
            2: "Flexion 4pts",
            3: "Module Young"
        }
        test_mode = test_modes.get(test_number, "Inconnu")
        self.sample.last_mode_chosen = int(test_number)
        return test_mode
    
    def get_canal(self):
        canal = self.option_canal.get()
        machine = self.option_machine.get()
        if machine == "WB100kN":
            if canal == "Canal Extensomètre":
                if self.sample.stroke_channel != 4:
                    self.sample.stroke_channel = 4
                    self.sample.selected_channel = "Canal Extensomètre"
            elif canal == "Canal Traverse":
                if self.sample.stroke_channel != 10:
                    self.sample.stroke_channel = 10
                    self.sample.selected_channel = "Canal Traverse"
        self.sample.import_data()
    
    def get_geometry(self, test_mode):
        geometry = self.tabview.get()
        self.sample.last_geometry_chosen = geometry
        if geometry == "Section Ronde":
            D0 = self.option_diam_init_rond.get()
            L0 = self.option_long_init_rond.get()
            self.sample.D0 = float(D0)
            self.sample.L0 = float(L0)
            self.sample.W0 = None
            self.sample.H0 = None
            self.sample.L1 = None            
            if test_mode == "Flexion 4pts":
                L1 = self.option_long_l1_rond.get()
                self.sample.L1 = float(L1)
        elif geometry == "Section Rectangulaire":
            W0 = self.option_W0_init_rect.get()
            H0 = self.option_H0_init_rect.get()
            L0_rect = self.option_long_init_rect.get()
            self.sample.W0 = float(W0)
            self.sample.H0 = float(H0)
            self.sample.L0 = float(L0_rect)
            self.sample.D0 = None
            self.sample.L1 = None
            if test_mode == "Flexion 4pts":
                L1_rect = self.option_long_l1_rect.get()
                self.sample.L1 = float(L1_rect)
                
        return geometry
    
    def get_linear_range(self):
        F_min = self.option_f_min_rond.get()
        F_max = self.option_f_max_rond.get()
        self.sample.lin_range = [float(F_min), float(F_max)]
    
    def get_updated_data(self):
        test_mode = self.get_test_mode()
        self.get_canal()
        geometry = self.get_geometry(test_mode)
        self.get_linear_range()
    
        self.sample.tested_mode = test_mode
        self.sample.tested_geometry = geometry
        
        return [test_mode, geometry]
    
    def save_config(self):
        # Assignation des valeurs à la classe Sample
        [test_mode, geometry] = self.get_updated_data()
        rel_file_path = os.path.relpath(self.sample.file_path)
        
        print(f"Configuration du fichier {rel_file_path} sauvegardée en mode {test_mode}.")
        
    def on_close(self):
        self.save_config()
        self.master.interface_functions.preview_file(self.sample)
        print("Fermeture de la fenêtre de configuration.")
        self.destroy()
