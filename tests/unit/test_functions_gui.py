import pytest
import os
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Extractor.Functions_GUI import InterfaceFunctions
from Extractor.VariablesWindow import VarToplevelWindow
from Extractor.ConfigWindow import ConfigWindow
from Extractor.HelpWindow import HelpWindow
from Extractor.ExportGraphsWindow import ExportGraphsWindow
from Extractor.AnalysisSummaryWindow import AnalysisSummaryWindow
from Extractor.ExportExcelWindow import ExportExcelWindow
import tempfile

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

    # Mock customtkinter widgets
    master.checkbox_1 = mocker.MagicMock()
    master.checkbox_1.get.return_value = True  # Default value for tests

    master.tabview = mocker.MagicMock()
    master.tabview.tab.return_value = tk.Frame(master)

    return master

@pytest.fixture
def interface_functions(mock_master):
    return InterfaceFunctions(mock_master)

# Test des méthodes d'ouverture des fenêtres
def test_open_var_window_event(interface_functions, mock_master):
    selected_checkboxes = []
    interface_functions.open_var_window_event(selected_checkboxes)
    assert isinstance(interface_functions.toplevel_window, VarToplevelWindow)

def test_open_help_window_event(interface_functions):
    interface_functions.open_help_window_event()
    assert isinstance(interface_functions.help_window, HelpWindow)

def test_open_export_window_event(interface_functions):
    sample_list = []
    interface_functions.open_export_window_event(sample_list)
    assert isinstance(interface_functions.export_window, ExportGraphsWindow)

def test_open_summary_window_event(interface_functions, mocker):
    sample_list = []
    mocker.patch('Extractor.Functions_GUI.InterfaceFunctions.get_options', return_value={'option_name': True})
    interface_functions.open_summary_window_event(sample_list)
    assert isinstance(interface_functions.analysisWindow, AnalysisSummaryWindow)

def test_open_excel_export_window_event(interface_functions, mocker):
    sample_list = []
    mocker.patch('Extractor.Functions_GUI.InterfaceFunctions.get_options', return_value={'option_name': True})
    interface_functions.open_excel_export_window_event(sample_list)
    assert isinstance(interface_functions.excel_export_window, ExportExcelWindow)


def test_update_preview(interface_functions):
    interface_functions.update_preview()
    assert interface_functions.master.canvas is not None
    assert interface_functions.master.canvas2 is not None

# Test des méthodes d'exportation et d'analyse
def test_export_preview_event(interface_functions):
    sample_list = []
    graphs_to_export = ['Force-Déplacement']
    interface_functions.export_preview_event(sample_list, graphs_to_export)

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