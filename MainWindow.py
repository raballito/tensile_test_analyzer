# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 09:59:06 2024

Tensile Test Analyzer - Main Window

- Easy and updated GUI
- Updated Events and Events Handling
- List all files available
- Separate sample configuration
- Separate files for classes
- Multisampling handling
- Export graphics and sample summary

Version: Beta 1.4
Last Update: 13.08.24

@author: quentin.raball
"""

import customtkinter
from Extractor.Functions_GUI import InterfaceFunctions
from Extractor.ScrollableLabelButtonFrame import ScrollableLabelButtonFrame
from PIL import Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt



customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("static/themes/red.json") # Themes: "blue", "green", "dark-blue", 


class MainWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        # Charger les fonctions supplémentaires du GUI
        self.interface_functions = InterfaceFunctions(self)
        self.scrollable_label_button_frame = ScrollableLabelButtonFrame(self)

        # Configuration de la fenêtre
        self.title("Tensile Test Analyzer")
        self.geometry(f"{1200}x{800}")

        # Initialisation du dossier de travail
        self.interface_functions.pop_message_init()
        folder_ask = self.interface_functions.ask_directory()
        list_csv = self.interface_functions.list_csv(folder_ask)
        theme_names = self.interface_functions.list_themes_names()

        # Configuration  de la grille principale
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Barre latérale et widget associés
        logo_img = Image.open("static\\COMATEC_HEIG-VD_logotype_rouge-rvb.png")
        logo = customtkinter.CTkImage(light_image=logo_img,
                                  dark_image=logo_img,
                                  size=(140,43))
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=7, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(7, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, image=logo, text="")
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.title_label = customtkinter.CTkLabel(self.sidebar_frame, text="Tensile Test Analyzer", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.title_label.grid(row=1, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Ajouter un fichier", command=lambda: self.on_button_add_file(folder_ask))
        self.sidebar_button_1.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Supprimer les fichiers", command=lambda: self.on_remove_button_event())
        self.sidebar_button_2.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Changer de répertoire", command=lambda: self.on_change_directory_event())
        self.sidebar_button_3.grid(row=4, column=0, padx=20, pady=10)
        #self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame, text="TestButton", command=lambda: self.on_test_button_clicked())
        #self.sidebar_button_4.grid(row=5, column=0, padx=20, pady=10)
        self.sidebar_button_5 = customtkinter.CTkButton(self.sidebar_frame, text="Aide", command=self.interface_functions.open_help_window_event)
        self.sidebar_button_5.grid(row=6, column=0, padx=20, pady=10)
        #self.theme_label = customtkinter.CTkLabel(self.sidebar_frame, text="Couleur Theme :", anchor="w")
        #self.theme_label.grid(row=8, column=0, padx=20, pady=(10, 0))
        #self.theme_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=theme_names,
        #                                                     command=self.interface_functions.change_theme_event)
        #self.theme_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 10))
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Mode d'apparence :", anchor="w")
        self.appearance_mode_label.grid(row=10, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark"],
                                                                       command=self.interface_functions.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=11, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=12, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.interface_functions.change_scaling_event)
        self.scaling_optionemenu.grid(row=13, column=0, padx=20, pady=(10, 20))


        # Bouton principal et champ supplémentaire
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Options/Commandes supplémentaires")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.bouton_analyse = customtkinter.CTkButton(master=self,  text="Analyser la sélection", font=customtkinter.CTkFont(size=15, weight="bold"), command=lambda: self.on_analyse_button_clicked())
        self.bouton_analyse.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")


        # Affichage graphique prévisualisation
        self.tabview1 = customtkinter.CTkTabview(self)
        self.tabview1.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        
        self.tabview1.add("Force-Déplacement")
        self.tabview1.tab("Force-Déplacement").grid_columnconfigure(0, weight=1)
        self.tabview1.tab("Force-Déplacement").grid_rowconfigure(0, weight=1)
        
        self.tabview1.add("Force-Temps")
        self.tabview1.tab("Force-Temps").grid_columnconfigure(0, weight=1)
        self.tabview1.tab("Force-Temps").grid_rowconfigure(0, weight=1)
        
        self.frame_force_displacement = customtkinter.CTkFrame(self.tabview1.tab("Force-Déplacement"))
        self.frame_force_displacement.grid(row=0, column=0, padx=20, pady=(10, 10), sticky="nsew")
        self.frame_force_displacement.grid_rowconfigure(0, weight=1)
        self.frame_force_displacement.grid_columnconfigure(0, weight=1)
        
        self.frame_force_time = customtkinter.CTkFrame(self.tabview1.tab("Force-Temps"))
        self.frame_force_time.grid(row=0, column=0, padx=20, pady=(10, 10), sticky="nsew")
        self.frame_force_time.grid_rowconfigure(0, weight=1)
        self.frame_force_time.grid_columnconfigure(0, weight=1)

        # Intégration de Matplotlib dans les cadres intermédiaires
        self.figure_force_displacement, self.ax1 = plt.subplots()
        self.figure_force_time, self.ax2 = plt.subplots()

        self.canvas = FigureCanvasTkAgg(self.figure_force_displacement, master=self.frame_force_displacement)
        self.canvas.get_tk_widget().grid(row=0, column=0, padx=0, pady=(0, 10), sticky="nsew")
        self.canvas.get_tk_widget().grid_rowconfigure(0, weight=1)
        self.canvas.get_tk_widget().grid_columnconfigure(0, weight=1)

        self.canvas2 = FigureCanvasTkAgg(self.figure_force_time, master=self.frame_force_time)
        self.canvas2.get_tk_widget().grid(row=0, column=0, padx=0, pady=(0, 10), sticky="nsew")
        self.canvas2.get_tk_widget().grid_rowconfigure(0, weight=1)
        self.canvas2.get_tk_widget().grid_columnconfigure(0, weight=1)

        # Options de fichiers et d'analyse
        self.tabview2 = customtkinter.CTkTabview(self, width=200)
        self.tabview2.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.tabview2.add("Options d'analyse")
        self.tabview2.tab("Options d'analyse").grid_columnconfigure(0, weight=1)
        self.label_chiffre_sign = customtkinter.CTkLabel(self.tabview2.tab("Options d'analyse"), text="Nombre de chiffres significatifs :")
        self.label_chiffre_sign.grid(row=0, column=0, padx=20, pady=(20, 0))
        self.option_chiffre_sign = customtkinter.CTkOptionMenu(self.tabview2.tab("Options d'analyse"), dynamic_resizing=True,
                                                    values=["1", "2", "3", "4", "5"])
        self.option_chiffre_sign.grid(row=1, column=0, padx=20)
        
        self.label_lim_elast = customtkinter.CTkLabel(self.tabview2.tab("Options d'analyse"), text="Définition de la limite élastique :")
        self.label_lim_elast.grid(row=2, column=0, padx=20, pady=(10,0))
        self.option_lim_elast = customtkinter.CTkOptionMenu(self.tabview2.tab("Options d'analyse"), dynamic_resizing=True,
                                                    values=["0.1%", "0.2%", "0.3%", "0.4%", "0.5%"])
        self.option_lim_elast.grid(row=3, column=0, padx=20)
        
        self.file_var_button = customtkinter.CTkButton(self.tabview2.tab("Options d'analyse"), text="Afficher données des fichiers",
                                              command=lambda: self.on_var_button_clicked())
        self.file_var_button.grid(row=4, column=0, padx=20, pady=(40, 20))
        self.export_graphics_button = customtkinter.CTkButton(self.tabview2.tab("Options d'analyse"), text="Exportation des graphiques",
                                              command=lambda: self.on_export_graphics_button_clicked())
        self.export_graphics_button.grid(row=5, column=0, padx=20, pady=(20, 20))
        self.export_excel_button = customtkinter.CTkButton(self.tabview2.tab("Options d'analyse"), text="Exportation sous Excel",
                                              command=lambda: self.on_export_excel_button_clicked())
        self.export_excel_button.grid(row=6, column=0, padx=20, pady=(20, 20))

        # Options d'exportations
        self.checkbox_slider_frame = customtkinter.CTkScrollableFrame(self, label_text="Options d'exportation")
        self.checkbox_slider_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame, text="Nom du sample")
        self.checkbox_1.grid(row=1, column=0, pady=(0, 0), padx=10, sticky="nw")
        self.checkbox_2 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame, text="Nom du fichier")
        self.checkbox_2.grid(row=2, column=0, pady=(20, 0), padx=10, sticky="nw")
        self.checkbox_3 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame, text="Légendes")
        self.checkbox_3.grid(row=3, column=0, pady=(20, 0), padx=10, sticky="nw")
        self.checkbox_4 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame, text="Déformation en [%]")
        self.checkbox_4.grid(row=4, column=0, pady=(20, 0), padx=10, sticky="nw")
        self.checkbox_5 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame, text="Droite limite élastique")
        self.checkbox_5.grid(row=5, column=0, pady=(20, 0), padx=10, sticky="nw")
        self.checkbox_6 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame, text="Montrer résultats calculés")
        self.checkbox_6.grid(row=6, column=0, pady=(20, 0), padx=10, sticky="nw")
        self.checkbox_7 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame, text="Utilisation des [kN]")
        self.checkbox_7.grid(row=7, column=0, pady=20, padx=10, sticky="nw")

        # Assignation des valeurs et comportements par défaut
        self.checkbox_1.select()
        self.checkbox_2.select()
        self.checkbox_3.select()
        self.checkbox_4.select()
        self.checkbox_5.select()
        self.checkbox_6.select()
        self.appearance_mode_optionemenu.set("Light")
        self.scaling_optionemenu.set("100%")
        self.option_chiffre_sign.set("3")
        self.option_lim_elast.set("0.2%")
        #self.theme_optionemenu.set("red")
                
        # Création liste de fichiers
        self.scrollable_label_button_frame = ScrollableLabelButtonFrame(master=self, label_text="Liste des fichiers")
        self.scrollable_label_button_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_label_button_frame.grid_rowconfigure(0, weight=1) # A régler pour agrandir la zone vers le bas
        self.instruction_frame = None
        self.instruction_label = None
        for i in range(len(list_csv)):
            self.scrollable_label_button_frame.add_item(list_csv[i])
        if len(list_csv) == 0:
            self.show_instruction_message()
        self.focus()
    
    def has_tab(self, tab_name):
        return tab_name in self.tabview1._tab_dict

    def show_instruction_message(self):
        self.instruction_frame = customtkinter.CTkFrame(master=self.master)
        self.instruction_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # Configurez la grille pour centrer le texte
        self.instruction_frame.grid_columnconfigure(0, weight=1)
        self.instruction_frame.grid_rowconfigure(0, weight=1)

        self.instruction_label = customtkinter.CTkLabel(
            master=self.instruction_frame,
            text="Veuillez ajouter un fichier manuellement ou placez vos fichiers dans le répertoire 'Data'",
            anchor="center"
        )
        self.instruction_label.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")

    def hide_instruction_message(self):
        if self.instruction_frame:
            self.instruction_frame.grid_forget()
            self.instruction_frame = None

    def add_item(self, file_path):
        self.hide_instruction_message()
        self.scrollable_label_button_frame.add_item(file_path)
        
    def on_var_button_clicked(self):
        selected_checkboxes = self.scrollable_label_button_frame.get_selected_checkboxes()    
        sample_list = self.scrollable_label_button_frame.get_sample_var(selected_checkboxes)
        self.interface_functions.open_var_window_event(sample_list)
        
    def on_export_graphics_button_clicked(self):
        selected_checkboxes = self.scrollable_label_button_frame.get_selected_checkboxes()    
        sample_list = self.scrollable_label_button_frame.get_sample_var(selected_checkboxes)
        self.interface_functions.open_export_window_event(sample_list)
         
    def on_test_button_clicked(self):
        selected_checkboxes = self.scrollable_label_button_frame.get_selected_checkboxes()
        sample_list = self.scrollable_label_button_frame.get_sample_var(selected_checkboxes)
        for sample in sample_list:
            sample.show_var()
            
    def on_analyse_button_clicked(self):
        selected_checkboxes = self.scrollable_label_button_frame.get_selected_checkboxes()
        sample_list = self.scrollable_label_button_frame.get_sample_var(selected_checkboxes)
        if not len(sample_list) == 0:
            all_configured = all(sample.configured_sample for sample in sample_list)
            if all_configured:
                for sample in sample_list:
                    sample.analyze()
        self.interface_functions.end_analyze(sample_list)
        
    def on_export_excel_button_clicked(self):
        selected_checkboxes = self.scrollable_label_button_frame.get_selected_checkboxes()
        sample_list = self.scrollable_label_button_frame.get_sample_var(selected_checkboxes)
        self.interface_functions.open_excel_export_window_event(sample_list)
        
    def on_button_add_file(self, folder):
        self.interface_functions.add_button_event(folder)

    def on_remove_button_event(self):
        selected_checkboxes = self.scrollable_label_button_frame.get_selected_checkboxes()
        self.interface_functions.remove_button_event(selected_checkboxes)
        
    def on_change_directory_event(self):
        self.interface_functions.directory_button_event()
        
    def on_close(self):
        print("Fermeture de la fenêtre principale.")
        self.destroy()
        self.quit()
            
# Lancement de l'app
if __name__ == "__main__":
    app = MainWindow()
    #app._state_before_windows_set_titlebar_color = 'zoomed'
    app.mainloop()
    
    
