# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 14:01:01 2024

@author: quentin.raball
"""
import pandas as pd
import numpy as np
import unittest
from unittest.mock import MagicMock

# Supposons que la classe Sample soit définie dans un fichier nommé sample.py
from Extractor.Sample import Sample

class TestSample(unittest.TestCase):

    def setUp(self):
        # Créer une instance fictive de la classe master
        self.mock_master = MagicMock()
        self.mock_master.get_round_val.return_value = 2
        self.mock_master.get_coef_rp.return_value = '0.2%'
        self.mock_master.get_option_file_path.return_value = True
        self.mock_master.get_option_sample_name.return_value = True
        self.mock_master.get_option_scale_kN.return_value = False
        self.mock_master.get_option_show_force_stroke.return_value = True
        self.mock_master.get_option_defo_percent.return_value = True
        self.mock_master.get_option_show_rp.return_value = True
        self.mock_master.get_option_show_legend.return_value = True
        
        # Instanciation de la classe Sample avec l'objet master fictif
        self.sample = Sample(self.mock_master)
        self.sample.file_path = 'test_data.csv'
        self.sample.sample_name = 'TestSample'
        self.sample.tested_geometry = "Section Ronde"
        self.sample.selected_channel = "Canal Traverse"
        self.sample.D0 = 10  # Diamètre pour Section Ronde
        self.sample.L0 = 50  # Longueur initiale
        self.sample.lin_range = [200,300]
        self.sample.force_channel = 2
        self.sample.stroke_channel = 3
        self.sample.time_channel = 1
        self.sample.repeat_every = 3

    def test_import_data(self):
        self.sample.end_filter = 0
        # Simuler le contenu d'un fichier CSV pour l'importation
        csv_content = '''"Temps [s]","Force [N]","Déplacement [mm]"
            0,100,0.1
            1,200,0.2
            2,300,0.3
            3,400,0.4
            4,500,0.5
            '''
        # Simuler l'ouverture et la lecture du fichier
        with unittest.mock.patch('builtins.open', unittest.mock.mock_open(read_data=csv_content)):
            time_values, force_values, displacement_values = self.sample.import_data()
        
        # Vérifier que les valeurs importées sont correctes
        self.assertEqual(time_values, [0, 1, 2, 3, 4])
        self.assertEqual(force_values, [100, 200, 300, 400, 500])
        self.assertEqual(displacement_values, [0.1, 0.2, 0.3, 0.4, 0.5])
    
    def test_analyze_traction(self):
        # Simuler des valeurs de force et de déplacement pour l'analyse
        self.sample.force_values = [100, 200, 300, 400, 500]
        self.sample.displacement_values = [0.1, 0.2, 0.3, 0.4, 0.5]
        self.sample.tested_mode = "Traction"
        
        # Lancer l'analyse
        self.sample.analyze()
        
        # Vérifier que les valeurs calculées sont correctes
        self.assertAlmostEqual(self.sample.F_max, 500)
        self.assertAlmostEqual(self.sample.Allong, 0.3)  # Valeur max de déplacement moins la première valeur
        self.assertAlmostEqual(self.sample.stress_values[-1], 500 / (np.pi * (self.sample.D0**2) / 4))
    
    def test_export_preview(self):
        # Simuler des valeurs de données pour le graphique
        self.sample.force_values = [100, 200, 300, 400, 500]
        self.sample.displacement_values = [0.1, 0.2, 0.3, 0.4, 0.5]
        self.sample.time_values = [0, 1, 2, 3, 4]
        
        # Vérifier l'export d'un graphique
        with unittest.mock.patch('matplotlib.pyplot.savefig'):
            path = self.sample.export_preview(graph_type='Force-Déplacement')
            self.assertIn('graphique_force_déplacement', path)

    def test_add_table_to_plot(self):
        # Simuler des valeurs pour un plot
        data_plot = pd.DataFrame({
            'Déplacement [mm]': [0.1, 0.2, 0.3, 0.4, 0.5],
            'Force [N]': [100, 200, 300, 400, 500]
        })

        # Simuler le max pour le tableau
        self.sample.F_max = 500
        self.sample.Allong = 0.4
        self.sample.round_val = 2
        
        # Tester l'ajout d'un tableau au plot
        with unittest.mock.patch('matplotlib.pyplot.table'):
            self.sample.add_table_to_plot(data_plot, 'Déplacement [mm]', 'Force [N]', 'A_max', 'F_max')

    def test_invalid_graph_type(self):
        # Test pour s'assurer qu'une ValueError est levée pour un type de graphique invalide
        with self.assertRaises(ValueError):
            self.sample.export_preview(graph_type='InvalidType')

if __name__ == '__main__':
    unittest.main()