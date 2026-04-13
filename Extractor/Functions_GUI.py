# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 09:59:06 2024

GUI Related Functions
- Buttons Events Handeling,
- Gui Functions 
- Basically everythings related of the main window's functions
- Events throughs files managed by this file mainly

Version: Beta 1.12
Last Update: 31.03.26

@author: quentin.raball
"""

import os
import customtkinter
from Extractor.VariablesWindow import VarToplevelWindow
from Extractor.HelpWindow import HelpWindow
from Extractor.ConfigWindow import ConfigWindow
from Extractor.TestBench import TestBench
from Extractor.ExportGraphsWindow import ExportGraphsWindow
from Extractor.AnalysisSummaryWindow import AnalysisSummaryWindow
from Extractor.ExportExcelWindow import ExportExcelWindow
from tkinter import messagebox
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class InterfaceFunctions:
    def __init__(self, master):
        self.master = master # Pour tous éléments provenant de l'interface principal
        self.toplevel_window = None
        self.config_window = None
        self.file_path = None
        self.test_bench = TestBench(self)
        self.help_window = None
        self.export_window = None
        self.analysisWindow = None
        self.excel_export_window = None
    
    def show_warning(self, file):
        print(f"Fichier ignoré (déjà présent) : {file}")
        messagebox.showwarning("Fichier déjà présent", f"{os.path.basename(file)} est déjà dans la liste.")
    
    def show_warning_ignore(self, file_path):
        messagebox.showwarning("Fichier ignoré", f"Le fichier {file_path} a été ignoré car une erreur d'importation à été rencontrée.")
    
    def init_programm(self):
        data_folder = "Data"
        # Créer le dossier s'il n'existe pas
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)
        # Chercher automatiquement les fichiers dans Data
        file_list = [
            os.path.join(data_folder, f)
            for f in os.listdir(data_folder)
            if f.lower().endswith((".csv", ".lia"))
        ]
        # Conversion via ta fonction existante
        if len(file_list) > 0:
            list_csv = self.list_csv(file_list)
            return list_csv
        else:
            list_csv = None
            return list_csv
        # Important : stocker la "source"
        self.folder_ask = data_folder
        
    def ask_directory(self, folder):
        options = {
            "initialdir": folder,
            "title": "Choisissez les fichiers de données",
            "filetypes": [
                ("Fichiers de données", "*.csv *.lia"),
                ("CSV files", "*.csv"),
                ("LIA files", "*.lia"),
                ("All files", "*.*")
            ]
        }
        file_paths = filedialog.askopenfilenames(**options)
        if not file_paths:
            return None
        return list(file_paths)
    
    def save_as(titre="Enregistrer sous", defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]):
        file_path = filedialog.asksaveasfilename(
            title=titre,
            defaultextension=defaultextension,
            filetypes=filetypes
        )
        return file_path
    
    def list_csv(self, file_list):
        csv_files = []
        for filepath in file_list:
            filepath = os.path.abspath(filepath)
            if filepath.lower().endswith(".lia"):
                new_filepath = filepath[:-4] + ".csv"
                # éviter d’écraser un fichier existant
                if not os.path.exists(new_filepath):
                    os.rename(filepath, new_filepath)
                csv_files.append(new_filepath)
            elif filepath.lower().endswith(".csv"):
                csv_files.append(filepath)
    
        print("Nombre de fichiers sélectionnés :", len(csv_files))
        return csv_files

    # Fonctions supplémentaires GUI
    def open_var_window_event(self, selected_checkboxes):
        sample_names = []
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = VarToplevelWindow(selected_checkboxes, self.get_options())  # Crée une nouvelle fenêtre si elle n'existe pas ou si elle a été détruite
            self.toplevel_window.attributes("-topmost", True)
            for sample in selected_checkboxes:
                sample_names.append(sample.sample_name)
            print("Ouvre une nouvelle fenetre avec :", sample_names)
        else:
            # Vérifie si les fichiers sélectionnés ont changé
            current_files = self.toplevel_window.update_file_list(selected_checkboxes)
            self.toplevel_window.attributes("-topmost", False)
            self.toplevel_window.focus()
            if current_files != selected_checkboxes:
                # Si la liste des fichiers a changé, met à jour la fenêtre existante
                self.toplevel_window.update_file_list(selected_checkboxes)
                for sample in selected_checkboxes:
                    sample_names.append(sample.sample_name)
                print("Mise à jour de la fenetre avec :", sample_names)
            else:
                # Sinon, ramène simplement la fenêtre existante au premier plan
                self.toplevel_window.attributes("-topmost", False)
                self.toplevel_window.focus()
                print("Retourne à la fenetre existante")
            
    def open_config_window_event(self, sample, master, item, update_method=None):
        if self.config_window is None or not self.config_window.winfo_exists():
            # Si aucune fenêtre de configuration n'existe, ou si la fenêtre précédente a été détruite
            self.current_name = sample.sample_name
            self.current_item = sample.file_path
            self.current_test_bench = sample.test_bench
            file_path_rel = self.create_short_list([sample.file_path])
            self.config_window = ConfigWindow(sample, master, item)
            self.config_window.attributes("-topmost", True)
            print("Ouvre la fenetre de configuration de", sample.sample_name, " @ ", file_path_rel[0])
        else:
            # Si une fenêtre de configuration existe déjà
            if self.current_name != sample.sample_name or self.current_item != sample.file_path:
                # Vérifier si le nom ou le fichier a changé depuis la dernière fois
                self.current_name = sample.sample_name
                self.current_item = sample.file_path
                rel_file_path = os.path.relpath(self.current_item)
                self.config_window.destroy()  
                self.config_window = ConfigWindow(sample, master, self.current_item)
                self.config_window.attributes("-topmost", False)
                self.config_window.focus()
                print("Retourne à la fenetre de configuration de", sample.sample_name, " @ ", rel_file_path)
            else:
                rel_file_path = os.path.relpath(self.current_item)
                self.config_window.attributes("-topmost", False)
                self.config_window.focus()  
                print("Retourne à la fenetre de configuration de", sample.sample_name, " @ ", rel_file_path)
                
    def open_help_window_event(self):
        if self.help_window is None or not self.help_window.winfo_exists():
            self.help_window = HelpWindow()  # Crée une nouvelle fenêtre si elle n'existe pas ou si elle a été détruite
            self.help_window.attributes("-topmost", True)
            print("Ouvre une nouvelle fenetre d'aide.")
        else:
            # Sinon, ramène simplement la fenêtre existante au premier plan
            self.help_window.attributes("-topmost", False)
            self.help_window.focus()
            print("Retourne à la fenetre existante.")
    
    def open_export_window_event(self, sample_list):
        if self.export_window is None or not self.export_window.winfo_exists():
            # Si aucune fenêtre d'exportation n'existe, ou si la fenêtre précédente a été détruite
            self.export_window = ExportGraphsWindow(sample_list)
            self.current_sample_list = sample_list
            self.export_window.attributes("-topmost", True)
            self.export_window.focus()
            print("Ouvre la fenêtre d'exportation")
        else:
            self.export_window.attributes("-topmost", False)
            self.export_window.focus()
            print("Retourne à la fenêtre d'exportation")
            
    def open_summary_window_event(self, sample_list):
        if self.analysisWindow is None or not self.analysisWindow.winfo_exists():
            # Si aucune fenêtre d'exportation n'existe, ou si la fenêtre précédente a été détruite
            self.analysisWindow = AnalysisSummaryWindow(sample_list, self.get_options())
            self.analysisWindow.attributes("-topmost", True)
            self.analysisWindow.focus()
            print("Ouvre la fenêtre de résumé")
        else:
            self.analysisWindow.destroy()
            self.analysisWindow = AnalysisSummaryWindow(sample_list, self.get_options())
            self.analysisWindow.attributes("-topmost", True)
            self.analysisWindow.focus()
            print("Retourne à la fenêtre de résumé")
    
    def open_excel_export_window_event(self, sample_list):
        if self.excel_export_window is None or not self.excel_export_window.winfo_exists():
            # Si aucune fenêtre d'exportation n'existe, ou si la fenêtre précédente a été détruite
            self.excel_export_window = ExportExcelWindow(sample_list, self.get_options())
            self.excel_export_window.attributes("-topmost", True)
            self.excel_export_window.focus()
            print("Ouvre la fenêtre de résumé")
        else:
            self.excel_export_window.destroy()
            self.excel_export_window = ExportExcelWindow(sample_list, self.get_options())
            self.excel_export_window.attributes("-topmost", True)
            self.excel_export_window.focus()
            print("Retourne à la fenêtre de résumé")
            
    def get_options(self):
        return {
            'option_name': bool(self.master.checkbox_vars[0].get()),
            'option_legend': bool(self.master.checkbox_vars[1].get()),
            'option_defo_percent': bool(self.master.checkbox_vars[2].get()),
            'option_elastic_line': bool(self.master.checkbox_vars[3].get()),
            'option_show_table': bool(self.master.checkbox_vars[4].get()),
            'option_filter':bool(self.master.checkbox_vars[5].get()),
            'option_grid': bool(self.master.checkbox_vars[6].get()),
            'option_kn': bool(self.master.checkbox_vars[7].get()) 
        }
    
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
        if new_appearance_mode == "Dark" :
            self.master.ax1.set_facecolor("#5B5B5B")
            self.master.ax2.set_facecolor("#5B5B5B")
            self.master.figure_force_displacement.set_facecolor("#5B5B5B")
            self.master.figure_force_time.set_facecolor("#5B5B5B")
            self.update_preview()
            print("Changing appearence to Dark")
        else :
            self.master.ax1.set_facecolor("white")
            self.master.ax2.set_facecolor("white")
            self.master.figure_force_displacement.set_facecolor("white")
            self.master.figure_force_time.set_facecolor("white")
            self.update_preview()
            print("Changing appearence to Light")

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def directory_button_event(self, old_folder):
        print("Changement de dossier")
    
        new_files = self.ask_directory(old_folder)
        if new_files is None:
            print("Opération annulée.")
            return
        list_csv = self.list_csv(new_files)
        self.clear_plot()
        self.master.scrollable_label_button_frame.remove_all_items()
    
        for file in list_csv:
            self.master.scrollable_label_button_frame.add_item(file)
        self.master.scrollable_label_button_frame.check_empty_list()
        return new_files
            
    def remove_button_event(self, item_list):
        for item in item_list:
            self.remove_stress_graph()
            self.master.scrollable_label_button_frame.remove_item(item)
        self.clear_plot()
        print("Elements supprimés :", item_list)
    
    def clear_plot(self):
       # Effacer le graphique
       self.master.ax1.clear()
       self.master.ax2.clear()
       self.master.canvas.draw()
       self.master.canvas2.draw()
    
    def config_button_frame_event(self, sample, master, item):
        sample_name = sample.sample_name
        file_path = sample.file_path
        try:
            short_path = os.path.relpath(file_path)
        except ValueError as e:
            # Si une erreur se produit lors de la création du chemin relatif, utilisez le chemin complet
            print(f"Erreur lors de la création du chemin relatif pour {file_path}. Utilisation du chemin complet.\nErreur: {e}")
            short_path = file_path
        print("Bouton de configuration de:", sample_name, " @ ", short_path, " cliqué")
        self.open_config_window_event(sample, master, item)
    
    def preview_file(self, sample):
        self.preview_force_displacement_graph(sample)
        self.preview_force_time_graph(sample)
        if sample.analyzed_sample and sample.stress_values is not None:
            self.preview_stress_deformation_graph(sample)
            self.preview_stress_displacement_graph(sample)
        else:
            self.remove_stress_graph()
            
        print(f"Prévisualisation: {sample.sample_name}")
        
    def preview_force_displacement_graph(self, sample):
        self.master.ax1.clear()
        options = self.get_options()
        option_kn = bool(options.get('option_kn', False))
        option_grid = bool(options.get('option_grid', False))
        option_legend = bool(options.get('option_legend', True))
        disp = sample.displacement_values
        f_reg_lin_min = float(sample.lin_range[0])
        f_reg_lin_max = float(sample.lin_range[1])
       
        if option_kn:
            force = [value / 1000 for value in sample.force_values]
            f_reg_lin_min /= 1000
            f_reg_lin_max /= 1000
            ylabel = "Force [kN]"
            yunit = "kN"
        else:
            force = sample.force_values
            ylabel = "Force [N]"
            yunit = "N"
            
        self.master.ax1.set_xlim(0, 1.2 * max(disp))
        self.master.ax1.set_ylim(0, 1.3 * max(force)) 
       
        # Tracer les graphiques de base
        self.master.ax1.plot(disp, force, label=sample.sample_name)
        
        # Ajouter les lignes horizontales pour f_min et f_max
        self.master.ax1.axhline(y=f_reg_lin_max, color='b', linestyle='--', label=f'reg_lin_max = {f_reg_lin_max} {yunit}')
        self.master.ax1.axhline(y=f_reg_lin_min, color='r', linestyle='--', label=f'reg_lin_min = {f_reg_lin_min} {yunit}')
        
        # Configuration des axes et légendes
        self.master.ax1.set_xlabel("Déplacement [mm]")
        self.master.ax1.set_ylabel(ylabel)
        if option_legend:
            self.master.ax1.legend()
        if option_grid:
            self.master.ax1.grid(zorder=0, linestyle='--', alpha=0.5) 
        
        self.master.figure_force_displacement.tight_layout()
        self.master.canvas.draw()
        
    def preview_force_time_graph(self, sample):
        self.master.ax2.clear()
        options = self.get_options()
        option_kn = bool(options.get('option_kn', False))
        option_grid = bool(options.get('option_grid', False))
        option_legend = bool(options.get('option_legend', True))
        time = sample.time_values
        force = sample.force_values
        f_reg_lin_min = float(sample.lin_range[0])
        f_reg_lin_max = float(sample.lin_range[1])
        
        if option_kn:
            force = [value / 1000 for value in sample.force_values]
            f_reg_lin_min /= 1000
            f_reg_lin_max /= 1000
            ylabel = "Force [kN]"
            yunit = "kN"
        else:
            force = sample.force_values
            ylabel = "Force [N]"
            yunit = "N"
        
        self.master.ax2.set_xlim(0, 1.2 * max(time))
        self.master.ax2.set_ylim(0, 1.3 * max(force))
        
        # Tracer les graphiques de base
        self.master.ax2.plot(time, force, label=sample.sample_name)
        
        # Ajouter les lignes horizontales pour f_min et f_max
        self.master.ax2.axhline(y=f_reg_lin_max, color='b', linestyle='--', label=f'reg_lin_max = {f_reg_lin_max} {yunit}')
        self.master.ax2.axhline(y=f_reg_lin_min, color='r', linestyle='--', label=f'reg_lin_min = {f_reg_lin_min} {yunit}')
        
        # Configuration des axes et légendes
        self.master.ax2.set_xlabel("Temps [s]")
        self.master.ax2.set_ylabel(ylabel)
        if option_legend:
            self.master.ax2.legend()
        if option_grid:
            self.master.ax2.grid(zorder=0, linestyle='--', alpha=0.5) 
        
        self.master.figure_force_time.tight_layout()
        self.master.canvas2.draw()
        
    def preview_stress_deformation_graph(self, sample):
        main_window = self.master

        if not main_window.has_tab("Contrainte-Déformation"):
            main_window.tabview1.add("Contrainte-Déformation")
            main_window.tabview1.tab("Contrainte-Déformation").grid_columnconfigure(0, weight=1)
            main_window.tabview1.tab("Contrainte-Déformation").grid_rowconfigure(0, weight=1)
            main_window.frame_stress_deformation = customtkinter.CTkFrame(main_window.tabview1.tab("Contrainte-Déformation"))
            main_window.frame_stress_deformation.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
            main_window.frame_stress_deformation.grid_rowconfigure(0, weight=1)
            main_window.frame_stress_deformation.grid_columnconfigure(0, weight=1)

        # Display the graphs in the respective frames
        self.display_stress_deformation_graph(sample)
        
        
    def preview_stress_displacement_graph(self, sample):
        main_window = self.master
        if self.master.canvas3 is None:
            self.master.canvas3 = FigureCanvasTkAgg(
                self.master.figure_stress_deformation,
                master=self.master.frame_stress_deformation
            )
            self.master.canvas3.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        
        if not main_window.has_tab("Contrainte-Déplacement"):
            main_window.tabview1.add("Contrainte-Déplacement")
            main_window.tabview1.tab("Contrainte-Déplacement").grid_columnconfigure(0, weight=1)
            main_window.tabview1.tab("Contrainte-Déplacement").grid_rowconfigure(0, weight=1)
            main_window.frame_stress_displacement = customtkinter.CTkFrame(main_window.tabview1.tab("Contrainte-Déplacement"))
            main_window.frame_stress_displacement.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
            main_window.frame_stress_displacement.grid_rowconfigure(0, weight=1)
            main_window.frame_stress_displacement.grid_columnconfigure(0, weight=1)
            
        self.display_stress_displacement_graph(sample)
        
    def remove_stress_graph(self):
        main_window = self.master
        if main_window.has_tab("Contrainte-Déformation"):
            main_window.tabview1.delete("Contrainte-Déformation")
        if main_window.has_tab("Contrainte-Déplacement"):
            main_window.tabview1.delete("Contrainte-Déplacement")

    def display_stress_deformation_graph(self, sample):
        # Initialiser figure et axes
        self.master.ax3.clear()
        self.master.canvas3 = FigureCanvasTkAgg(self.master.figure_stress_deformation, master=self.master.frame_stress_deformation)
        self.master.canvas3.get_tk_widget().grid(row=0, column=0, padx=0, pady=(0, 10), sticky="nsew")
        self.master.canvas3.get_tk_widget().grid_rowconfigure(0, weight=1)
        self.master.canvas3.get_tk_widget().grid_columnconfigure(0, weight=1)
        
        # Récupérer les données
        options = self.get_options()
        option_percent = bool(options.get('option_defo_percent', False))
        option_grid = bool(options.get('option_grid', False))
        option_legend = bool(options.get('option_legend', True))
        stress = sample.stress_values
        coef_re = float(self.master.option_lim_elast.get().strip('%'))
        if option_percent:
            E = 10*float(sample.E)
            xlabel = "Déformation [%]"
            x_start = coef_re
        else: 
            E=1000*float(sample.E)
            xlabel = "Déformation [-]"
            x_start = coef_re / 100
        
        defo = sample.deformation_values       
        y_start = 0
        x_end = max(defo)
        y_end = E * (x_end - x_start)
        
        self.master.ax3.set_xlim(0, 1.2 * max(defo))
        self.master.ax3.set_ylim(0, 1.3 * max(stress))
        
        # Tracer les graphiques de base
        self.master.ax3.plot(defo, stress, label=sample.sample_name)
        show_rp02 = sample.master.get_option_show_rp()
        if show_rp02 == True and sample.Defo > sample.coef_re:
            self.master.ax3.plot([x_start, x_end], [y_start, y_end], label='Limite élastique', linestyle='--', color='orange')
        
        # Configuration des axes et légendes
        self.master.ax3.set_xlabel(xlabel)
        self.master.ax3.set_ylabel("Contrainte [MPa]")
        if option_legend:
            self.master.ax3.legend()
        if option_grid:
            self.master.ax3.grid(zorder=0, linestyle='--', alpha=0.5) 
        
        # Redessiner le graphique
        self.master.figure_stress_deformation.tight_layout()
        self.master.canvas3.draw()

    def display_stress_displacement_graph(self, sample):
        # Initialiser figure et axes
        self.master.ax4.clear()
        self.master.canvas4 = FigureCanvasTkAgg(self.master.figure_stress_displacement, master=self.master.frame_stress_displacement)
        self.master.canvas4.get_tk_widget().grid(row=0, column=0, padx=0, pady=(0, 10), sticky="nsew")
        self.master.canvas4.get_tk_widget().grid_rowconfigure(0, weight=1)
        self.master.canvas4.get_tk_widget().grid_columnconfigure(0, weight=1)
        
        # Récupérer les données
        options = self.get_options()
        option_grid = bool(options.get('option_grid', False))
        option_legend = bool(options.get('option_legend', True))
        stress = sample.stress_values
        
        # Trouver l'index où la déformation est la plus proche de zéro
        zero_deformation_index = min(range(len(sample.deformation_values)), key=lambda i: abs(sample.deformation_values[i]))
        offset_displacement = sample.displacement_values[zero_deformation_index]
        
        # Ajuster les valeurs de déplacement pour cet échantillon
        adjusted_displacement_values = [disp - offset_displacement for disp in sample.displacement_values]
        
        max_stress = max(sample.stress_values)
        max_displacement = max(adjusted_displacement_values)
        
        self.master.ax4.set_xlim(0, 1.2 * max_displacement)
        self.master.ax4.set_ylim(0, 1.3 * max_stress)
        
        # Tracer les graphiques de base
        self.master.ax4.plot(adjusted_displacement_values, stress, label=sample.sample_name)
        
        # Configuration des axes et légendes
        self.master.ax4.set_xlabel("Déplacement [mm]")
        self.master.ax4.set_ylabel("Contrainte [MPa]")
        if option_legend:
            self.master.ax4.legend()
        if option_grid:
            self.master.ax4.grid(zorder=0, linestyle='--', alpha=0.5) 
        
        # Redessiner le graphique
        self.master.figure_stress_displacement.tight_layout()
        self.master.canvas4.draw()
        
    def update_preview(self):
        # Tracer les graphiques de base
        self.master.canvas.draw()
        self.master.canvas2.draw()
    
    def export_graphics_event(self, sample_list, graphs_to_export):
        exported_sample = []
        if len(sample_list) == 0:
            message = "Exportation annulée: aucun échantillon sélectionné.\nVeuillez sélectionner un échantillon et recommencer."
            messagebox.showinfo("Exportation annulée", message)
        elif len(graphs_to_export) == 0:
            message = "Exportation annulée: aucun graphique sélectionné.\nVeuillez sélectionner un graphique et recommencer."
            messagebox.showinfo("Exportation annulée", message)
        else:
            # Demander à l'utilisateur de sélectionner un répertoire de destination
            directory = filedialog.askdirectory(title="Sélectionnez un répertoire pour enregistrer les graphiques")
        
            # Si l'utilisateur annule la sélection du répertoire
            if not directory:
                message = "Exportation annulée: aucun répertoire sélectionné.\nVeuillez sélectionner un répertoire et recommencer."
                messagebox.showinfo("Exportation annulée", message)
                return
            
            # Exportation des graphiques
            for sample in sample_list:
                for graph_type in graphs_to_export:
                    sample.export_graphs(graph_type=graph_type, directory=directory)
                exported_sample.append(sample.sample_name)
                
            message = f"Graphiques de {exported_sample} exportés sous {directory}."
            print(message)
            messagebox.showinfo("Exportation terminée", message)
            
    def end_analyze(self, sample_list):
        if len(sample_list) == 0:
            message = 'Analyse annulée. Aucun échantillon sélectionné.'
            messagebox.showinfo("Analyse Annulée", message)
        else:
            all_configured = all(sample.configured_sample for sample in sample_list)
            if not all_configured:
                message = "Les échantillons n'ont pas été correctement configurés.\n Veuillez premièrement configurer l'échantillon."
                messagebox.showinfo("Analyse annulée", message)
            else:
                analysed_sample = [sample.sample_name for sample in sample_list]
                message = f'Analyse terminée pour les samples :  {analysed_sample}'
                self.open_summary_window_event(sample_list)
        print(message)
        last_selected_element = self.master.scrollable_label_button_frame.selected_sample
        if last_selected_element is not None:
            self.preview_file(last_selected_element)      

    
    def list_themes_names(self):
        theme_files = [f for f in os.listdir("static/themes") if f.endswith(".json")]
        theme_names = [os.path.splitext(f)[0] for f in theme_files]
        return theme_names
    
    def create_short_list(self, long_list):
        short_list = []
        for file_path in long_list:
            try:
                short_path = os.path.relpath(file_path)
            except ValueError as e:
                # Si une erreur se produit lors de la création du chemin relatif, utilisez le chemin complet
                print(f"Erreur lors de la création du chemin relatif pour {file_path}. Utilisation du chemin complet.\nErreur: {e}")
                short_path = file_path
            short_list.append(short_path)
        return short_list
    

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
