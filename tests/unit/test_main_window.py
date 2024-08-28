import unittest
from unittest.mock import MagicMock, patch
from PIL import Image
import customtkinter
from MainWindow import MainWindow

class TestMainWindow(unittest.TestCase):

    @patch('MainWindow.customtkinter.CTk')  # Assurez-vous que le chemin d'importation est correct
    @patch('MainWindow.customtkinter.CTkButton')
    @patch('MainWindow.customtkinter.CTkLabel')
    @patch('MainWindow.customtkinter.CTkImage')  # Mock des images avec des attributs d'image
    @patch('MainWindow.InterfaceFunctions')  # Corriger le chemin d'importation
    @patch('MainWindow.ScrollableLabelButtonFrame')  # Corriger le chemin d'importation
    @patch('tkinter.messagebox')  # Mock des fenêtres de messagebox
    @patch('tkinter.filedialog.askdirectory')  # Mock de askdirectory pour les dialogues de répertoires
    def setUp(self, MockAskDirectory, MockMessageBox, MockScrollableLabelButtonFrame, MockInterfaceFunctions, MockCTkImage, MockCTkLabel, MockCTkButton, MockCTk):
        # Initialiser les mocks
        self.mock_ctk = MockCTk
        self.mock_ctk_button = MockCTkButton
        self.mock_ctk_label = MockCTkLabel

        # Créer un mock pour CTkImage
        self.mock_ctk_image = MagicMock()
        self.mock_ctk_image.light_image = MagicMock()
        self.mock_ctk_image.dark_image = MagicMock()

        self.mock_interface_functions = MockInterfaceFunctions
        self.mock_scrollable_label_button_frame = MockScrollableLabelButtonFrame
        self.mock_ask_directory = MockAskDirectory
        self.mock_messagebox = MockMessageBox

        # Simuler askdirectory
        self.mock_ask_directory.return_value = 'test_folder'

        # Patch Image.open pour éviter l'ouverture réelle du fichier image
        with patch('PIL.Image.open', return_value=MagicMock(spec=Image.Image)) as MockImageOpen:
            # Assigner le mock à CTkImage
            MockCTkImage.return_value = self.mock_ctk_image

            # Créer une instance de MainWindow
            self.window = MainWindow()

            # Patch le logo_label pour éviter les problèmes d'image
            with patch('MainWindow.customtkinter.CTkLabel') as MockCTkLabel:
                self.mock_ctk_label_instance = MagicMock()
                MockCTkLabel.return_value = self.mock_ctk_label_instance
                self.window.logo_label = MockCTkLabel(self.window.sidebar_frame, image=self.mock_ctk_image, text="")

    def test_initialization(self):
        self.assertEqual(self.window.title(), "Tensile Test Analyzer")
        self.assertIsNotNone(self.window.interface_functions)
        self.assertIsNotNone(self.window.scrollable_label_button_frame)

    def test_folder_initialization(self):
        self.window.interface_functions.ask_directory = MagicMock(return_value='test_folder')
        self.window.folder_ask = self.window.interface_functions.ask_directory()
        self.assertEqual(self.window.folder_ask, 'test_folder')

    def test_sidebar_buttons(self):
        self.mock_ctk_button.assert_any_call(self.window.sidebar_frame, text="Ajouter un fichier", command=unittest.mock.ANY)
        self.mock_ctk_button.assert_any_call(self.window.sidebar_frame, text="Supprimer les fichiers", command=unittest.mock.ANY)
        self.mock_ctk_button.assert_any_call(self.window.sidebar_frame, text="Changer de répertoire", command=unittest.mock.ANY)
        self.mock_ctk_button.assert_any_call(self.window.sidebar_frame, text="Aide", command=self.window.interface_functions.open_help_window_event)

    def test_add_item(self):
        mock_scrollable_label_button_frame = self.mock_scrollable_label_button_frame.return_value
        self.window.scrollable_label_button_frame = mock_scrollable_label_button_frame

        self.window.add_item('test_file.csv')
        mock_scrollable_label_button_frame.add_item.assert_called_with('test_file.csv')

    def test_on_var_button_clicked(self):
        self.window.scrollable_label_button_frame.get_selected_checkboxes = MagicMock(return_value=['checkbox1'])
        self.window.scrollable_label_button_frame.get_sample_var = MagicMock(return_value=['sample1'])

        self.window.on_var_button_clicked()
        self.window.interface_functions.open_var_window_event.assert_called_with(['sample1'])

    def test_on_export_graphics_button_clicked(self):
        self.window.scrollable_label_button_frame.get_selected_checkboxes = MagicMock(return_value=['checkbox1'])
        self.window.scrollable_label_button_frame.get_sample_var = MagicMock(return_value=['sample1'])

        self.window.on_export_graphics_button_clicked()
        self.window.interface_functions.open_export_window_event.assert_called_with(['sample1'])

    def test_on_export_excel_button_clicked(self):
        self.window.scrollable_label_button_frame.get_selected_checkboxes = MagicMock(return_value=['checkbox1'])
        self.window.scrollable_label_button_frame.get_sample_var = MagicMock(return_value=['sample1'])

        self.window.on_export_excel_button_clicked()
        self.window.interface_functions.open_excel_export_window_event.assert_called_with(['sample1'])

    def test_on_close(self):
        self.window.destroy = MagicMock()
        self.window.quit = MagicMock()

        self.window.on_close()
        self.window.destroy.assert_called_once()
        self.window.quit.assert_called_once()

if __name__ == '__main__':
    unittest.main()