import unittest
from unittest.mock import MagicMock, patch
import customtkinter
import tkinter
from PIL import Image
from Extractor.ConfigWindow import ConfigWindow  # Assurez-vous d'importer la classe ConfigWindow correctement

class TestConfigWindow(unittest.TestCase):
    
    @patch('customtkinter.CTkToplevel')
    def setUp(self, MockCTkToplevel):
        self.mock_master = customtkinter.CTk()
        self.mock_sample = MagicMock()
        self.mock_sample.sample_name = 'Sample1'
        self.mock_sample.file_path = 'path/to/file'
        self.mock_sample.test_bench = 'Bench1'
        self.mock_sample.D0 = 2
        self.mock_sample.L0 = 50
        self.mock_sample.L1 = 20
        self.mock_sample.W0 = 12
        self.mock_sample.H0 = 1.5
        self.mock_sample.lin_range = [0, 100]
        self.mock_sample.selected_channel = 'Canal Traverse'
        self.mock_sample.last_mode_chosen = 0
        self.mock_sample.last_geometry_chosen = 'Section Ronde'
        
        self.config_window = ConfigWindow(self.mock_sample, self.mock_master, self.mock_sample.file_path)

    def test_initialization(self):
        # Teste les propriétés et éléments de l'interface utilisateur
        
        # Vérifiez que la fenêtre a été correctement configurée
        self.assertEqual(self.config_window.title(), "Configuration de l'échantillon")
        
        # Teste la création des labels
        self.assertIsInstance(self.config_window.label_edited_file, customtkinter.CTkLabel)
        self.assertIsInstance(self.config_window.label_file_path, customtkinter.CTkLabel)
        self.assertIsInstance(self.config_window.label_sample_name, customtkinter.CTkLabel)
        
        # Teste que les valeurs par défaut des variables sont correctement définies
        self.assertEqual(self.config_window.option_diam_init_rond.get(), '2')
        self.assertEqual(self.config_window.option_long_init_rond.get(), '50')
        self.assertEqual(self.config_window.option_long_l1_rond.get(), '20')
        self.assertEqual(self.config_window.option_W0_init_rect.get(), '12')
        self.assertEqual(self.config_window.option_H0_init_rect.get(), '1.5')
        self.assertEqual(self.config_window.option_f_max_rond.get(), '100')
        self.assertEqual(self.config_window.option_f_min_rond.get(), '0')
        
        # Teste que les onglets et les boutons sont correctement configurés
        self.assertIsInstance(self.config_window.tabview, customtkinter.CTkTabview)
        self.assertIsInstance(self.config_window.save_button, customtkinter.CTkButton)
        
        # Teste que les onglets sont correctement configurés
        self.assertTrue(self.config_window.tabview.tab('Section Ronde'))
        self.assertTrue(self.config_window.tabview.tab('Section Rectangulaire'))
        
        # Teste que le bon onglet est sélectionné
        self.assertEqual(self.config_window.tabview.get(), 'Section Ronde')

        # Teste que les valeurs des boutons radio sont correctement définies
        self.assertEqual(self.config_window.radio_var.get(), 0)
        
   
if __name__ == '__main__':
    unittest.main()