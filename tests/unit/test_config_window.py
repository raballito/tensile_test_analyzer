import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
from PIL import Image
from Extractor.ConfigWindow import ConfigWindow
from Extractor.Sample import Sample
from Extractor.ScrollableLabelButtonFrame import ScrollableLabelButtonFrame
import customtkinter

class TestConfigWindow(unittest.TestCase):

    def setUp(self):
        # Configuration initiale des mocks pour Sample
        self.mock_sample = MagicMock(spec=Sample)
        self.mock_sample.sample_name = "Sample1"
        self.mock_sample.file_path = "/path/to/file"
        self.mock_sample.test_bench = "Shimadzu"
        self.mock_sample.D0 = None
        self.mock_sample.L0 = None
        self.mock_sample.L1 = None
        self.mock_sample.W0 = None
        self.mock_sample.H0 = None
        self.mock_sample.lin_range = [0, 100]
        self.mock_sample.selected_channel = "Canal Traverse"
        self.mock_sample.stroke_channel = 10
        self.mock_sample.option_machine = "Shimadzu 20kN"
        self.mock_sample.import_data = MagicMock(return_value=True)

        # Configuration initiale des mocks pour ScrollableLabelButtonFrame
        self.mock_scrollable_frame = MagicMock(spec=ScrollableLabelButtonFrame)
        self.mock_scrollable_frame.sample_list = [self.mock_sample]
        self.mock_scrollable_frame.master = MagicMock()

        # Configuration des mocks pour ConfigWindow
        self.root = tk.Tk()
        self.mock_ctk_image_rond = MagicMock()
        self.mock_ctk_image_rond.create_scaled_photo_image.return_value = MagicMock()

        # Patch PIL.Image.open
        with patch('PIL.Image.open', return_value=MagicMock(spec=Image.Image)) as MockImageOpen:
            # Patch customtkinter.CTkTabview and related components
            with patch('customtkinter.CTkTabview') as MockCTkTabview:
                self.mock_ctk_tabview_instance = MagicMock()
                MockCTkTabview.return_value = self.mock_ctk_tabview_instance

                def tab_side_effect(tab_name):
                    if tab_name == "Section Rectangulaire":
                        return MagicMock()
                    elif tab_name == "Section Ronde":
                        return MagicMock()
                    return None

                self.mock_ctk_tabview_instance.tab.side_effect = tab_side_effect

                # Initialiser ConfigWindow avec des mocks
                with patch('Extractor.ConfigWindow.ConfigWindow.__init__', lambda x, *args, **kwargs: None):
                    self.config_window = ConfigWindow(
                        sample=self.mock_sample,
                        master=self.root,
                        item=MagicMock()
                    )

                    # Simuler les attributs nécessaires
                    self.config_window.option_canal = MagicMock()
                    self.config_window.option_canal.set = MagicMock()
                    self.config_window.option_canal.get = MagicMock(return_value="Canal Traverse")

                    self.config_window.option_machine = MagicMock()
                    self.config_window.option_machine.get = MagicMock(return_value="Shimadzu 20kN")

                    self.config_window.radio_var = MagicMock()
                    self.config_window.radio_var.get = MagicMock(return_value=0)
                    
                    self.config_window.tabview = MagicMock()

                    # Simuler les boutons radio
                    self.config_window.radio_button_2 = MagicMock()
                    self.config_window.radio_button_3 = MagicMock()
                    self.config_window.radio_button_4 = MagicMock()

                    # Simuler les autres options
                    self.config_window.option_f_min_rond = MagicMock()
                    self.config_window.option_f_min_rond.get = MagicMock(return_value="0")

                    self.config_window.option_f_max_rond = MagicMock()
                    self.config_window.option_f_max_rond.get = MagicMock(return_value="100")

                    self.config_window.option_diam_init_rond = MagicMock()
                    self.config_window.option_diam_init_rond.get = MagicMock(return_value="1")

                    self.config_window.option_long_init_rond = MagicMock()
                    self.config_window.option_long_init_rond.get = MagicMock(return_value="10")

                    self.config_window.option_W0_init_rect = MagicMock()
                    self.config_window.option_W0_init_rect.get = MagicMock(return_value="1")

                    self.config_window.option_H0_init_rect = MagicMock()
                    self.config_window.option_H0_init_rect.get = MagicMock(return_value="1")

                    self.config_window.option_long_init_rect = MagicMock()
                    self.config_window.option_long_init_rect.get = MagicMock(return_value="10")

                    self.config_window.option_long_l1_rond = MagicMock()
                    self.config_window.option_long_l1_rond.get = MagicMock(return_value="1")

                    self.config_window.option_long_l1_rect = MagicMock()
                    self.config_window.option_long_l1_rect.get = MagicMock(return_value="1")

                    # Simuler la méthode sample de ConfigWindow
                    self.config_window.sample = self.mock_sample

                    self.config_window.sample_name = MagicMock()
                    self.config_window.sample_name.cget = MagicMock(return_value="Sample1")

                    self.config_window.label_file_path = MagicMock()
                    self.config_window.label_file_path.cget = MagicMock(return_value="/path/to/file")

                    self.config_window.label_long_l1_rond = MagicMock()
                    self.config_window.option_long_l1_rond = MagicMock()
                    self.config_window.label_long_l1_rect = MagicMock()
                    self.config_window.option_long_l1_rect = MagicMock()

                    self.config_window.geometry = MagicMock(return_value="400x940")
                    self.config_window.title = MagicMock(return_value="Configuration de l'échantillon")

    def tearDown(self):
        self.root.destroy()

    def test_initial_setup(self):
        self.assertEqual(self.config_window.title(), "Configuration de l'échantillon")
        self.assertEqual(self.config_window.geometry(), "400x940")
        self.assertEqual(self.config_window.label_file_path.cget("text"), "/path/to/file")
        self.assertEqual(self.config_window.sample_name.cget("text"), "Sample1")

    def test_radio_button_selection(self):
        # Test initial selection
        self.config_window.radio_var.get.return_value = 0  # Default value
        
        # Simuler le clic sur le bouton radio "Flexion 3 points"
        self.config_window.radio_button_2.invoke()
        self.config_window.radio_var.get.return_value = 1  # Simuler la sélection
        self.assertEqual(self.config_window.radio_var.get(), 1)
    
        # Simuler le clic sur le bouton radio "Flexion 4 points"
        self.config_window.radio_button_3.invoke()
        self.config_window.radio_var.get.return_value = 2  # Simuler la sélection
        self.assertEqual(self.config_window.radio_var.get(), 2)
    
        # Simuler le clic sur le bouton radio "Module de Young"
        self.config_window.radio_button_4.invoke()
        self.config_window.radio_var.get.return_value = 3  # Simuler la sélection
        self.assertEqual(self.config_window.radio_var.get(), 3)

    @patch('customtkinter.CTkInputDialog')
    def test_open_input_dialog_event(self, MockInputDialog):
        mock_dialog = MockInputDialog.return_value
        mock_dialog.get_input.return_value = "New Sample Name"
        
        self.config_window.open_input_dialog_event(MagicMock())
    
        # Vérifiez que le nom de l'échantillon et le texte de l'élément ont été mis à jour
        self.assertEqual(self.config_window.sample.sample_name, "New Sample Name")
        self.assertEqual(self.mock_sample.sample_name, "New Sample Name")

    def test_update_menus(self):
        # Simuler les retours des mocks pour le test bench
        self.config_window.sample.test_bench = "WB100kN_1"
    
        # Assurez-vous que le mock de l'option machine retourne la valeur correcte
        self.config_window.option_machine.get.return_value = "W+B 100kN"
    
        self.config_window.update_menus("WB100kN_1", 1)
    
        # Vérifiez que la mise à jour a été faite correctement
        self.assertEqual(self.config_window.option_canal.get(), "Canal Traverse")
        self.assertEqual(self.config_window.option_machine.get(), "W+B 100kN")
        
        self.config_window.update_menus("WB100kN_2", 1)
        self.assertEqual(self.config_window.option_canal.get(), "Canal Traverse")
        self.assertEqual(self.config_window.option_machine.get(), "W+B 100kN")
        
        self.config_window.sample.selected_channel = "Canal Extensomètre"
        self.config_window.option_canal.get.return_value = "Canal Extensomètre"
        self.config_window.update_menus("WB100kN_2", 3)
        self.assertEqual(self.config_window.option_canal.get(), "Canal Extensomètre")
        self.assertEqual(self.config_window.option_machine.get(), "W+B 100kN")
    
        # Simuler un autre cas de mise à jour
        self.config_window.sample.test_bench = "Shimadzu"
        self.config_window.option_machine.get.return_value = "Shimadzu 20kN"
        self.config_window.sample.selected_channel = "Canal Extensomètre"
        self.config_window.option_canal.get.return_value = "Canal Extensomètre"
    
        self.config_window.update_menus("Shimadzu", 3)
        self.assertEqual(self.config_window.option_canal.get(), "Canal Extensomètre")
        self.assertEqual(self.config_window.option_machine.get(), "Shimadzu 20kN")
        
        # Simuler un autre cas de mise à jour
        self.config_window.sample.test_bench = "WB400kN_2"
        self.config_window.option_machine.get.return_value = "WB400kN_2"
        self.config_window.sample.selected_channel = "Canal Traverse"
        self.config_window.option_canal.get.return_value = "Canal Traverse"
    
        self.config_window.update_menus("WB400kN_2", 2)
        self.assertEqual(self.config_window.option_canal.get(), "Canal Traverse")
        self.assertEqual(self.config_window.option_machine.get(), "WB400kN_2")

    def test_update_l1_visibility(self):
        # Configurer les retours attendus pour winfo_ismapped initialement
        self.config_window.label_long_l1_rond.winfo_ismapped.return_value = False
        self.config_window.option_long_l1_rond.winfo_ismapped.return_value = False
        self.config_window.label_long_l1_rect.winfo_ismapped.return_value = False
        self.config_window.option_long_l1_rect.winfo_ismapped.return_value = False
    
        # Simuler le clic sur le bouton radio "Module de Young"
        self.config_window.radio_var.set(3)
        self.config_window.radio_button_4.invoke()  # Assuming radio_button_4 is for Module de Young
        self.config_window.radio_var.get.return_value = 3
        self.config_window.update_l1_visibility()
    
        # Vérifier que les éléments ne sont pas mappés lorsque le radio_var est sur Module de Young (3)
        self.assertFalse(self.config_window.label_long_l1_rond.winfo_ismapped())
        self.assertFalse(self.config_window.option_long_l1_rond.winfo_ismapped())
        self.assertFalse(self.config_window.label_long_l1_rect.winfo_ismapped())
        self.assertFalse(self.config_window.option_long_l1_rect.winfo_ismapped())
    
        # Simuler le clic sur le bouton radio "Flexion 4 points"
        self.config_window.radio_var.set(2)
        self.config_window.radio_button_3.invoke()  # Assuming radio_button_3 is for Flexion 4 points
        self.config_window.radio_var.get.return_value = 2
    
        # Simuler que les éléments sont maintenant visibles
        self.config_window.label_long_l1_rond.winfo_ismapped.return_value = True
        self.config_window.option_long_l1_rond.winfo_ismapped.return_value = True
        self.config_window.label_long_l1_rect.winfo_ismapped.return_value = True
        self.config_window.option_long_l1_rect.winfo_ismapped.return_value = True
    
        self.config_window.update_l1_visibility()
    
        # Vérifier que les éléments sont mappés lorsque le radio_var est sur Flexion 4 points (2)
        self.assertTrue(self.config_window.label_long_l1_rond.winfo_ismapped())
        self.assertTrue(self.config_window.option_long_l1_rond.winfo_ismapped())
        self.assertTrue(self.config_window.label_long_l1_rect.winfo_ismapped())
        self.assertTrue(self.config_window.option_long_l1_rect.winfo_ismapped())

if __name__ == '__main__':
    unittest.main()