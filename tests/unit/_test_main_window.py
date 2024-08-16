# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 11:57:49 2024

@author: quentin.raball
"""

import pytest
import customtkinter
from MainWindow import MainWindow
from Extractor.Functions_GUI import InterfaceFunctions
from Extractor.ScrollableLabelButtonFrame import ScrollableLabelButtonFrame
from PIL import Image
from PIL import ImageTk


@pytest.fixture
def app(mocker):
    # Mock des images pour éviter les erreurs liées aux images
    mock_image = mocker.MagicMock(spec=Image.Image)  # Utilisation de Image.Image pour la compatibilité
    mock_image_tk = mocker.MagicMock(spec=ImageTk.PhotoImage)

    # Patch de PIL.Image.open pour retourner le mock_image
    mocker.patch('PIL.Image.open', return_value=mock_image)

    # Patch de ImageTk.PhotoImage pour retourner le mock_image_tk
    mocker.patch('PIL.ImageTk.PhotoImage', return_value=mock_image_tk)
    
    # Patch de customtkinter.CTkImage pour éviter les erreurs
    mocker.patch('customtkinter.CTkImage', return_value=mock_image_tk)

    # Initialisation normale de l'application
    return MainWindow()

def test_initialization(app, mocker):
    # Mock des fonctions de InterfaceFunctions
    mocker.patch.object(app.interface_functions, 'pop_message_init')
    mocker.patch.object(app.interface_functions, 'ask_directory', return_value="dummy_directory")
    mocker.patch.object(app.interface_functions, 'list_csv', return_value=["dummy_file.csv"])
    mocker.patch.object(app.interface_functions, 'list_themes_names', return_value=["theme1", "theme2"])

    # Vérifiez que pop_message_init a été appelé
    app.interface_functions.pop_message_init.assert_called_once()


def test_on_button_add_file(app, mocker):
    mocker.patch.object(InterfaceFunctions, 'add_button_event')

    app.on_button_add_file("dummy_folder")

    app.interface_functions.add_button_event.assert_called_once_with("dummy_folder")


def test_on_remove_button_event(app, mocker):
    mocker.patch.object(ScrollableLabelButtonFrame, 'get_selected_checkboxes', return_value=["checkbox1"])
    mocker.patch.object(InterfaceFunctions, 'remove_button_event')

    app.on_remove_button_event()

    app.scrollable_label_button_frame.get_selected_checkboxes.assert_called_once()
    app.interface_functions.remove_button_event.assert_called_once_with(["checkbox1"])


def test_on_change_directory_event(app, mocker):
    mocker.patch.object(InterfaceFunctions, 'directory_button_event')

    app.on_change_directory_event()

    app.interface_functions.directory_button_event.assert_called_once()


def test_on_close(app, mocker):
    mocker.patch.object(app, 'destroy')
    mocker.patch.object(app, 'quit')

    app.on_close()

    app.destroy.assert_called_once()
    app.quit.assert_called_once()


def test_on_analyse_button_clicked(app, mocker):
    mocker.patch.object(ScrollableLabelButtonFrame, 'get_selected_checkboxes', return_value=["checkbox1"])
    mocker.patch.object(ScrollableLabelButtonFrame, 'get_sample_var', return_value=[mocker.Mock()])
    mocker.patch.object(InterfaceFunctions, 'end_analyze')

    mock_sample = mocker.Mock()
    mock_sample.configured_sample = True
    mock_sample.analyze = mocker.Mock()
    app.scrollable_label_button_frame.get_sample_var.return_value = [mock_sample]

    app.on_analyse_button_clicked()

    app.scrollable_label_button_frame.get_selected_checkboxes.assert_called_once()
    app.scrollable_label_button_frame.get_sample_var.assert_called_once_with(["checkbox1"])
    mock_sample.analyze.assert_called_once()
    app.interface_functions.end_analyze.assert_called_once_with([mock_sample])


def test_on_export_excel_button_clicked(app, mocker):
    mocker.patch.object(ScrollableLabelButtonFrame, 'get_selected_checkboxes', return_value=["checkbox1"])
    mocker.patch.object(ScrollableLabelButtonFrame, 'get_sample_var', return_value=[mocker.Mock()])
    mocker.patch.object(InterfaceFunctions, 'open_excel_export_window_event')

    app.on_export_excel_button_clicked()

    app.scrollable_label_button_frame.get_selected_checkboxes.assert_called_once()
    app.scrollable_label_button_frame.get_sample_var.assert_called_once_with(["checkbox1"])
    app.interface_functions.open_excel_export_window_event.assert_called_once()


def test_on_var_button_clicked(app, mocker):
    mocker.patch.object(ScrollableLabelButtonFrame, 'get_selected_checkboxes', return_value=["checkbox1"])
    mocker.patch.object(ScrollableLabelButtonFrame, 'get_sample_var', return_value=[mocker.Mock()])
    mocker.patch.object(InterfaceFunctions, 'open_var_window_event')

    app.on_var_button_clicked()

    app.scrollable_label_button_frame.get_selected_checkboxes.assert_called_once()
    app.scrollable_label_button_frame.get_sample_var.assert_called_once_with(["checkbox1"])
    app.interface_functions.open_var_window_event.assert_called_once_with([mocker.Mock()])

