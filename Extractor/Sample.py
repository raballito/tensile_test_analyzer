# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 12:27:44 2024

Sample related Class

Saving all informations about current sample.
Available functions:
-import_data() to import datas from the file to the structure
-analyze() to analyze the samples with mode and geometry
-export_preview() to export graphics and tables

Version: Beta 1.13
Last Update: 10.04.26

@author: quentin.raball
"""

# Importation des modules
import uuid
from Extractor.DataManipulation import DataManipulation
from Extractor.DataFilter import FilterData
from Extractor.DataAnalyzer import DataAnalyzer
from Extractor.Sample_export_graph import DataExport

class Sample:    
    def __init__(self, master):
        self.master = master
        self.file_name = None
        self.file_path = None
        self.test_bench = None
        self.number_of_test = None
        self.available_sample_names = None
        self.extensometer_choice_value = None
        self.sample_name = "Default"
        self.separator = ','
        self.header_index = 2
        self.base_time_channel = 1
        self.time_channel = 1
        self.base_force_channel = 2
        self.force_channel = 2
        self.base_stroke_channel = 3
        self.stroke_channel = 3
        self.force_unit = 1
        self.repeat_every = None
        self.tested_mode = None
        self.tested_geometry = None
        self.time_values = []
        self.force_values = []
        self.displacement_values = []
        self.stress_values = []
        self.original_deformation_values = []
        self.deformation_values = []
        self.samples_and_channels = []
        self.subsamples = []
        self.L0 = None
        self.L1 = None
        self.S0 = None
        self.D0 = None
        self.W0 = None
        self.H0 = None
        self.lin_range = []
        self.F_max = None
        self.Allong = None
        self.t_max = None
        self.elastic_retreat = None
        self.Re = None
        self.Rm = None
        self.Defo = None
        self.E = None
        self.Y_Offset = None
        self.X_Offset = None
        self.idx0 = None
        self.selected_channel = "Canal Traverse"
        self.round_val = self.master.get_round_val()
        self.coef_re_unformatted = self.master.get_coef_re()
        self.coef_re = float(self.coef_re_unformatted.strip('%'))
        self.end_filter = 0
        self.show_sample_name = self.master.get_option_sample_name()
        self.scale_kN = self.master.get_option_scale_kN()
        self.show_Fmax_Allong_value = self.master.get_option_show_force_stroke()
        self.defo_percent = self.master.get_option_defo_percent()
        self.show_rp02 = self.master.get_option_show_rp()
        self.show_legend = self.master.get_option_show_legend()
        self.show_grid = self.master.get_option_grid()
        self.clean_end = self.master.get_option_filter()
        self.filter_pipeline = FilterData(normalize=True, method="mixed")
        self.DataManipulation = DataManipulation(self)
        self.analyzed_sample = False
        self.configured_sample = False
        self.last_mode_chosen = 0
        self.last_geometry_chosen = "Section Ronde"
        self.sample_id = uuid.uuid4()
      
    def import_data(self):
        return self.DataManipulation.import_data()
    
    # Fonction d'analyse. Conversion vers contrainte-déformation
    def analyze(self):
        analysis = DataAnalyzer(self).analyze()
        self.update_results(analysis)
        self.print_results()
        return analysis
    
    def update_results(self, analysis):
        """Mettre à jour les résultats dans Sample à partir des résultats de DataAnalyzer."""
        data_manipulation = DataManipulation(self)
        self.F_max = analysis[0]
        self.Rm = analysis[1]
        self.Re = analysis[2]
        self.E = analysis[3]
        self.Allong = analysis[4]
        self.Defo = analysis[5]
        self.elastic_retreat = analysis[6]
        self.stress_values = analysis[7]
        self.original_deformation_values = analysis[8]
        self.deformation_values = data_manipulation.convert_deformation(self.original_deformation_values)

        
    def print_results(self):
        print("\nDonnées Individuelles Extraites :\n\nForce Max = ", self.F_max, " [N]\nRm = ", self.Rm, " [MPa]\nRe = ", self.Re, " [MPa]\nE = ", self.E, " [GPa]\nAllongement max = ", self.Allong, " [mm]\nDéformation Max = ", self.Defo, " [%]\nRetour élastique: ", self.elastic_retreat, " [%]\n")
        
    def export_graphs(self, graph_type=None, directory='output/IMG'):
        # Crée une instance de DataExport et utilise la pour exporter les graphiques
        data_export = DataExport(self)
        self.defo_percent = self.master.get_option_defo_percent()
        self.coef_re = float(self.master.get_coef_re().strip('%'))
        return data_export.export_preview(graph_type, directory)
    
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
