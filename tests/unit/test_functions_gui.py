import pytest
import os
import tkinter as tk
from tkinter import messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
from unittest.mock import MagicMock, patch
from Extractor.Functions_GUI import InterfaceFunctions
from Extractor.VariablesWindow import VarToplevelWindow
from Extractor.HelpWindow import HelpWindow
from Extractor.ExportGraphsWindow import ExportGraphsWindow
from Extractor.AnalysisSummaryWindow import AnalysisSummaryWindow
from Extractor.ExportExcelWindow import ExportExcelWindow
from Extractor.ConfigWindow import ConfigWindow
import tempfile
import customtkinter

# Fixtures pour le setup et teardown des tests
@pytest.fixture
def mock_master(mocker):
    master = tk.Tk()
    master.option_chiffre_sign = tk.StringVar()
    master.option_chiffre_sign.set('2')
    master.ax1 = plt.Axes(plt.figure(), [0, 0, 1, 1])
    master.ax2 = plt.Axes(plt.figure(), [0, 0, 1, 1])
    master.scrollable_label_button_frame = tk.Frame(master)
    master.scrollable_label_button_frame.selected_sample = None
    master.canvas = FigureCanvasTkAgg(plt.figure(), master=master)
    master.canvas2 = FigureCanvasTkAgg(plt.figure(), master=master)
    master.item = mocker.MagicMock()

    # Mock customtkinter widgets
    master.checkbox_1 = mocker.MagicMock()
    master.checkbox_1.get.return_value = True
    master.checkbox_2 = mocker.MagicMock()
    master.checkbox_2.get.return_value = True
    master.checkbox_3 = mocker.MagicMock()
    master.checkbox_3.get.return_value = True
    master.checkbox_4 = mocker.MagicMock()
    master.checkbox_4.get.return_value = True
    master.checkbox_5 = mocker.MagicMock()
    master.checkbox_5.get.return_value = True
    master.checkbox_6 = mocker.MagicMock()
    master.checkbox_6.get.return_value = True
    master.checkbox_7 = mocker.MagicMock()
    master.checkbox_7.get.return_value = True

    # Mock tabview1
    master.tabview1 = mocker.MagicMock()
    master.tabview1.add = MagicMock()
    master.tabview1.tab = MagicMock(return_value=tk.Frame(master))

    # Simuler que tabview1._tab_dict est vide
    master.tabview1._tab_dict = {}

    # Mock has_tab method
    master.has_tab = MagicMock(return_value=False)

    return master

@pytest.fixture
def interface_functions(mock_master, mocker):
    mocker.patch('tkinter.filedialog.askdirectory', return_value=tempfile.gettempdir())
    mocker.patch('tkinter.messagebox.showinfo')
    mock_master.tabview1 = customtkinter.CTkTabview(mock_master)
    mock_master.tabview1.add("Force-Déplacement")

    return InterfaceFunctions(mock_master)

def test_open_var_window_event(interface_functions, mocker):
    selected_checkboxes = []
    interface_functions.master.interface_functions = interface_functions  # Assurez-vous que l'attribut est défini

    # Test avec des checkboxes vides
    interface_functions.open_var_window_event(selected_checkboxes)
    assert isinstance(interface_functions.toplevel_window, VarToplevelWindow)
    
    # Mock d'un sample avec les attributs nécessaires
    mock_sample = MagicMock()
    mock_sample.analyzed_sample = True
    mock_sample.stress_values = [0,1,2,3]
    mock_sample.deformation_values = [0,1,2,3]
    mock_sample.displacement_values = [0,1,2,3]
    mock_sample.force_values = [0,1,2,3]
    
    sample_list = [mock_sample]
    
    # Test avec un sample valide
    interface_functions.open_var_window_event(sample_list)
    assert isinstance(interface_functions.toplevel_window, VarToplevelWindow)

def test_open_help_window_event(interface_functions):
    interface_functions.open_help_window_event()
    assert isinstance(interface_functions.help_window, HelpWindow)
    interface_functions.open_help_window_event()
    assert isinstance(interface_functions.help_window, HelpWindow)

def test_open_export_window_event(interface_functions):
    mock_sample = MagicMock()
    mock_sample.force_values = [1, 2, 3]
    mock_sample.displacement_values = [0.1, 0.2, 0.3]
    mock_sample.time_values = [1,2,3]
    mock_sample.lin_range = [0.5, 1.5]
    mock_sample.sample_name = "Sample 1"
    mock_sample.analyzed_sample = True
    sample_list = []
    interface_functions.open_export_window_event(sample_list)
    assert isinstance(interface_functions.export_window, ExportGraphsWindow)
    sample_list = [mock_sample]
    interface_functions.open_export_window_event(sample_list)
    assert isinstance(interface_functions.export_window, ExportGraphsWindow)
    
def test_export_graphics_event(interface_functions, mocker):
    # Créer un mock pour les objets Sample
    mock_sample = MagicMock()
    mock_sample.sample_name = 'Sample1'
    mock_sample.export_preview = mocker.MagicMock()
    
    # Liste des échantillons et des graphiques à exporter
    sample_list = [mock_sample]
    graphs_to_export = ['Contrainte-Déformation', 'Force-Déplacement']

    # Obtenir le chemin du répertoire temporaire utilisé pour le test
    temp_directory = tempfile.gettempdir()

    # Appeler la méthode à tester
    interface_functions.export_graphics_event(sample_list, graphs_to_export)

    # Vérifier les appels aux méthodes de boîtes de dialogue
    filedialog.askdirectory.assert_called_once_with(title="Sélectionnez un répertoire pour enregistrer les graphiques")
    
    # Vérifier que les messages sont correctement affichés pour la fin de l'exportation
    messagebox.showinfo.assert_called_with(
        "Exportation terminée",
        f"Graphiques de ['Sample1'] exportés sous {temp_directory}."
    )
    
    # Vérifier que les graphiques sont exportés pour chaque échantillon et type de graphique
    for graph_type in graphs_to_export:
        mock_sample.export_preview.assert_any_call(graph_type=graph_type, directory=temp_directory)
    
    # Tests pour lorsque sample_list est vide
    with patch('tkinter.filedialog.askdirectory', return_value=temp_directory):
        interface_functions.export_graphics_event([], graphs_to_export)
        messagebox.showinfo.assert_called_with(
            "Exportation annulée",
            "Exportation annulée: aucun échantillon sélectionné.\nVeuillez sélectionner un échantillon et recommencer."
        )

    # Tests pour lorsque graphs_to_export est vide
    with patch('tkinter.filedialog.askdirectory', return_value=temp_directory):
        interface_functions.export_graphics_event(sample_list, [])
        messagebox.showinfo.assert_called_with(
            "Exportation annulée",
            "Exportation annulée: aucun graphique sélectionné.\nVeuillez sélectionner un graphique et recommencer."
        )
    
    # Tests pour lorsque le répertoire est annulé
    with patch('tkinter.filedialog.askdirectory', return_value=''):
        interface_functions.export_graphics_event(sample_list, graphs_to_export)
        messagebox.showinfo.assert_called_with(
            "Exportation annulée",
            "Exportation annulée: aucun répertoire sélectionné.\nVeuillez sélectionner un répertoire et recommencer.")

def test_open_summary_window_event(interface_functions, mocker):
    sample_list = []
    mocker.patch('Extractor.Functions_GUI.InterfaceFunctions.get_options', return_value={'option_name': True})
    interface_functions.open_summary_window_event(sample_list)
    assert isinstance(interface_functions.analysisWindow, AnalysisSummaryWindow)
    # Mock d'un sample avec l'attribut 'analyzed_sample'
    mock_sample = mocker.MagicMock()
    mock_sample.analyzed_sample = True
    mock_sample.stress_values = [0,1,2,3]
    mock_sample.deformation_values = [0,1,2,3]
    mock_sample.displacement_values = [0,1,2,3]
    mock_sample.force_values = [0,1,2,3]
    sample_list = [mock_sample]
    interface_functions.open_summary_window_event(sample_list)
    assert isinstance(interface_functions.analysisWindow, AnalysisSummaryWindow)

def test_open_excel_export_window_event(interface_functions, mocker):
    sample_list = []
    mocker.patch('Extractor.Functions_GUI.InterfaceFunctions.get_options', return_value={'option_name': True})
    interface_functions.open_excel_export_window_event(sample_list)
    assert isinstance(interface_functions.excel_export_window, ExportExcelWindow)
    # Mock d'un sample avec l'attribut 'analyzed_sample'
    mock_sample = mocker.MagicMock()
    mock_sample.analyzed_sample = True
    sample_list = [mock_sample]
    interface_functions.open_excel_export_window_event(sample_list)
    assert isinstance(interface_functions.excel_export_window, ExportExcelWindow)

def test_change_appearance_mode_event(interface_functions, mocker):
    mock_event = "dark"  # ou "light" selon le test
    mock_figure = mocker.MagicMock()
    
    # Mock the attributes of master
    interface_functions.master = customtkinter.CTk()
    interface_functions.master.figure_force_displacement = mock_figure
    interface_functions.master.ax1 = mocker.MagicMock()
    interface_functions.master.ax1.set_facecolor = mocker.MagicMock()
    interface_functions.master.ax2 = mocker.MagicMock()
    interface_functions.master.ax2.set_facecolor = mocker.MagicMock()
    interface_functions.master.figure_force_displacement = mocker.MagicMock()
    interface_functions.master.figure_force_displacement.set_facecolor = mocker.MagicMock()
    interface_functions.master.figure_force_time = mocker.MagicMock()
    interface_functions.master.figure_force_time.set_facecolor = mocker.MagicMock()
    interface_functions.master.canvas = mocker.MagicMock()
    interface_functions.master.canvas2 = mocker.MagicMock()

    # Mock the set_appearance_mode function
    mock_set_appearance_mode = mocker.patch('customtkinter.set_appearance_mode')

    # Call the function to be tested
    interface_functions.change_appearance_mode_event(mock_event)
    
    # Assert that set_appearance_mode was called correctly
    mock_set_appearance_mode.assert_called_once_with(mock_event)
    
def test_directory_button_event(interface_functions, mocker):
    # Mocks
    mock_dir = "mock_directory_path"
    mock_old_folder = "mock_old_folder"
    mock_csv_files = ["file1.csv", "file2.csv", "file3.csv"]
    mocker.patch('tkinter.filedialog.askdirectory', return_value=mock_dir)
    mocker.patch('os.listdir', return_value=mock_csv_files)

    # Créer un mock pour scrollable_label_button_frame avec une méthode remove_all_items
    mock_scrollable_frame = mocker.MagicMock()
    interface_functions.master.scrollable_label_button_frame = mock_scrollable_frame

    # Appeler la fonction à tester
    interface_functions.directory_button_event(mock_old_folder)

    mock_scrollable_frame.remove_all_items.assert_called_once()
    mock_scrollable_frame.check_empty_list.assert_called_once()
    
def test_add_button_event(interface_functions, mocker):
    # Chemin simulé pour le fichier sélectionné
    mock_file_path = "mock_directory/mock_file.csv"

    # Simuler tkinter.filedialog.askopenfilename pour retourner un chemin de fichier simulé
    mocker.patch('tkinter.filedialog.askopenfilename', return_value=mock_file_path)

    # Créer un mock pour selected_sample et le définir sur l'objet master
    mock_sample = mocker.MagicMock()
    interface_functions.master.selected_sample = mock_sample

    # Créer un mock pour master avec une méthode add_item
    mock_master = mocker.MagicMock()
    interface_functions.master = mock_master

    # Appeler la fonction à tester avec le folder simulé
    mock_folder = "mock_folder_path"
    interface_functions.add_button_event(mock_folder)

    # Normaliser les chemins pour la comparaison
    expected_path = os.path.normpath(mock_file_path)
    actual_path = os.path.normpath(mock_master.add_item.call_args[0][0])
    
    # Vérifier que add_item a été appelée avec le chemin de fichier simulé
    assert actual_path == expected_path
    
def test_remove_button_event(interface_functions, mocker):
    mock_sample = mocker.MagicMock()
    mock_item_list = ["item1", "item2"]  # Liste d'exemple
    mocker.patch.object(interface_functions, 'update_preview')  # Mock pour éviter des effets de bord
    interface_functions.master.selected_sample = mock_sample

    # Créer un mock pour scrollable_label_button_frame avec une méthode remove_item
    mock_scrollable_frame = mocker.MagicMock()
    interface_functions.master.scrollable_label_button_frame = mock_scrollable_frame

    # Appeler la fonction à tester
    interface_functions.remove_button_event(mock_item_list)

    # Vérifier que remove_item a été appelée avec les bons paramètres
    for item in mock_item_list:
        mock_scrollable_frame.remove_item.assert_any_call(item)

    
def test_preview_file(interface_functions, mocker):
    # Créer un mock pour l'échantillon avec des valeurs simulées
    mock_sample = mocker.MagicMock()
    mock_sample.force_values = [1, 2, 3]
    mock_sample.displacement_values = [0.1, 0.2, 0.3]
    mock_sample.time_values = [1,2,3]
    mock_sample.lin_range = [0.5, 1.5]
    mock_sample.sample_name = "Sample 1"
    
    # Créer un mock pour ax1 et canvas
    mock_ax1 = mocker.MagicMock()
    mock_canvas = mocker.MagicMock()

    # Patch self.master.ax1 et self.master.canvas
    interface_functions.master.ax1 = mock_ax1
    interface_functions.master.canvas = mock_canvas
    
    # Créer un mock pour ax2 et canvas
    mock_ax2 = mocker.MagicMock()
    mock_canvas2 = mocker.MagicMock()

    # Patch self.master.ax2 et self.master.canvas
    interface_functions.master.ax2 = mock_ax2
    interface_functions.master.canvas2 = mock_canvas2
    
    # Appeler la méthode à tester
    interface_functions.preview_file(mock_sample)

    # Vérifier que les méthodes attendues ont été appelées sur mock_ax1
    mock_ax1.clear.assert_called_once()
    mock_ax1.set_xlim.assert_called_once_with(0, 1.2 * max(mock_sample.displacement_values))
    mock_ax1.set_ylim.assert_called_once_with(0, 1.3 * max(mock_sample.force_values))
    mock_ax1.plot.assert_called_once_with(mock_sample.displacement_values, mock_sample.force_values, label=mock_sample.sample_name)
    mock_ax1.axhline.assert_any_call(y=float(mock_sample.lin_range[1]), color='b', linestyle='--', label=f'reg_lin_max = {float(mock_sample.lin_range[1])} N')
    mock_ax1.axhline.assert_any_call(y=float(mock_sample.lin_range[0]), color='r', linestyle='--', label=f'reg_lin_min = {float(mock_sample.lin_range[0])} N')
    mock_ax1.set_xlabel.assert_called_once_with("Déplacement [mm]")
    mock_ax1.set_ylabel.assert_called_once_with("Force [N]")
    mock_ax1.legend.assert_called_once()
    mock_canvas.draw.assert_called_once()

def test_preview_stress_deformation_graph(interface_functions):
    # Créer un mock pour l'échantillon avec des valeurs simulées
    mock_sample = MagicMock()
    mock_sample.stress_values = [1, 2, 3]
    mock_sample.deformation_values = [0.1, 0.2, 0.3]

    # Configurer le mock pour has_tab pour renvoyer False au début
    interface_functions.master.has_tab.return_value = False

    # Appeler la méthode à tester
    interface_functions.preview_stress_deformation_graph(mock_sample)

    # Vérifier que frame_stress_deformation a été créé et configuré
    assert isinstance(interface_functions.master.frame_stress_deformation, customtkinter.CTkFrame)
    
def test_preview_stress_displacement_graph(interface_functions):
    # Créer un mock pour l'échantillon avec des valeurs simulées
    mock_sample = MagicMock()
    mock_sample.stress_values = [1, 2, 3]
    mock_sample.deformation_values = [0.1, 0.2, 0.3]
    mock_sample.displacement_values = [1,2,3]

    # Configurer le mock pour has_tab pour renvoyer False au début
    interface_functions.master.has_tab.return_value = False

    # Appeler la méthode à tester
    interface_functions.preview_stress_displacement_graph(mock_sample)

    # Vérifier que frame_stress_deformation a été créé et configuré
    assert isinstance(interface_functions.master.frame_stress_displacement, customtkinter.CTkFrame)
    

# Test des méthodes d'exportation et d'analyse
def test_export_preview_event(interface_functions):
    sample_list = []
    graphs_to_export = ['Force-Déplacement']
    interface_functions.export_graphics_event(sample_list, graphs_to_export)

def test_end_analyze(interface_functions):
    sample_list = []
    interface_functions.end_analyze(sample_list)
    assert True  # Remplacez par des assertions spécifiques si nécessaire

# Test des méthodes de gestion des fichiers
def test_list_csv(interface_functions):
    with tempfile.TemporaryDirectory() as temp_dir:
        with open(os.path.join(temp_dir, "test.lia"), 'w') as f:
            f.write("test")
        csv_files = interface_functions.list_csv(temp_dir)
        assert len(csv_files) > 0

def test_list_themes_names(interface_functions):
    theme_names = interface_functions.list_themes_names()
    assert isinstance(theme_names, list)

def test_create_short_list(interface_functions):
    long_list = ["path/to/file1.csv", "path/to/file2.csv"]
    short_list = interface_functions.create_short_list(long_list)
    # Normaliser les chemins de fichiers pour la comparaison
    short_list = [os.path.normpath(path) for path in short_list]
    expected_list = ["path/to/file1.csv", "path/to/file2.csv"]
    expected_list = [os.path.normpath(path) for path in expected_list]
    assert short_list == expected_list

def test_format_sign(interface_functions):
    formatted_num = interface_functions.format_sign(1234.56789, 3)
    assert formatted_num == 1230.0