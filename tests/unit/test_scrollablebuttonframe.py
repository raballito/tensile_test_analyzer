import pytest
from unittest.mock import MagicMock
from Extractor.Functions_GUI import InterfaceFunctions
from Extractor.Sample import Sample
from Extractor.TestBench import TestBench
from Extractor.ScrollableLabelButtonFrame import ScrollableLabelButtonFrame
import customtkinter

@pytest.fixture
def scrollable_frame(mocker):
    # Mock de la fenêtre principale (master)
    master = customtkinter.CTk()
    
    # Mock des méthodes spécifiques de la GUI
    mocker.patch.object(customtkinter.CTkScrollableFrame, 'grid_columnconfigure', return_value=None)
    mocker.patch.object(customtkinter.CTkScrollableFrame, 'bind_all', return_value=None)
    
    # Mock des options
    master.option_chiffre_sign = MagicMock()
    master.option_chiffre_sign.get.return_value = 2
    
    master.option_lim_elast = MagicMock()
    master.option_lim_elast.get.return_value = "0.2%"
    
    master.show_instruction_message = MagicMock()
    
    # Mock des options dans la fenêtre principale (par exemple, les options des checkboxes)
    master.checkbox_1 = MagicMock()
    master.checkbox_1.get.return_value = 1
    master.checkbox_2 = MagicMock()
    master.checkbox_2.get.return_value = 1
    master.checkbox_3 = MagicMock()
    master.checkbox_3.get.return_value = 1
    master.checkbox_4 = MagicMock()
    master.checkbox_4.get.return_value = 1
    master.checkbox_5 = MagicMock()
    master.checkbox_5.get.return_value = 1
    master.checkbox_6 = MagicMock()
    master.checkbox_6.get.return_value = 1
    master.checkbox_7 = MagicMock()
    master.checkbox_7.get.return_value = 1
    

    print("Options assignées")
    master.interface_functions = InterfaceFunctions(master)
    # Créez une instance de ScrollableLabelButtonFrame
    frame = ScrollableLabelButtonFrame(master)
    print("Frame créé")
    
    return frame

def test_add_item(mocker, scrollable_frame):
    # Mock des classes TestBench et Sample
    mocker.patch('Extractor.TestBench.TestBench.identify_file', return_value=(["Sample1"], ["Time"], ["Force"], ["Stroke"]))
    mocker.patch('Extractor.TestBench.TestBench.identify_test_bench', return_value="TestBenchMock")
    mocker.patch('Extractor.Sample.Sample.import_data', return_value=True)

    # Simuler l'ajout d'un fichier
    file_path = "test_file.csv"
    scrollable_frame.add_item(file_path)

    # Vérifier que l'élément a été ajouté correctement
    assert len(scrollable_frame.sample_list) == 1
    assert len(scrollable_frame.switch_list) == 1
    assert len(scrollable_frame.frame_list) == 1

    # Vérifier les propriétés du sample ajouté
    sample = scrollable_frame.sample_list[0]
    assert sample.file_name == "test_file.csv"
    assert sample.test_bench == "TestBenchMock"

def test_remove_item(mocker, scrollable_frame):
    # Mock des classes TestBench et Sample pour l'ajout
    mocker.patch('Extractor.TestBench.TestBench.identify_file', return_value=(["Sample1"], ["Time"], ["Force"], ["Stroke"]))
    mocker.patch('Extractor.TestBench.TestBench.identify_test_bench', return_value="TestBenchMock")
    mocker.patch('Extractor.Sample.Sample.import_data', return_value=True)
    
    # Simuler l'ajout d'un fichier
    file_path = "test_file.csv"
    scrollable_frame.add_item(file_path)

    # Suppression de l'élément ajouté
    sample_id = scrollable_frame.sample_list[0].sample_id
    scrollable_frame.remove_item(sample_id)

    # Vérifier que l'élément a été supprimé correctement
    assert len(scrollable_frame.sample_list) == 0
    assert len(scrollable_frame.switch_list) == 0
    assert len(scrollable_frame.frame_list) == 0

def test_get_selected_checkboxes(mocker, scrollable_frame):
    # Mock des classes TestBench et Sample
    mocker.patch('Extractor.TestBench.TestBench.identify_file', return_value=(["Sample1"], ["Time"], ["Force"], ["Stroke"]))
    mocker.patch('Extractor.TestBench.TestBench.identify_test_bench', return_value="TestBenchMock")
    mocker.patch('Extractor.Sample.Sample.import_data', return_value=True)

    # Simuler l'ajout de fichiers
    file_path = "test_file.csv"
    scrollable_frame.add_item(file_path)
    
    # Simuler la sélection d'une checkbox
    scrollable_frame.checkbox_variable_list[0].set(1)
    
    selected_checkboxes = scrollable_frame.get_selected_checkboxes()
    
    # Vérifier que l'élément sélectionné correspond à l'ID du sample ajouté
    assert len(selected_checkboxes) == 1
    assert selected_checkboxes[0] == scrollable_frame.sample_list[0].sample_id

def test_get_option_methods(scrollable_frame):
    # Test des méthodes d'options
    assert scrollable_frame.get_round_val() == 2
    assert scrollable_frame.get_coef_rp() == "0.2%"
    assert scrollable_frame.get_option_file_path() == True
    assert scrollable_frame.get_option_sample_name() == True
    assert scrollable_frame.get_option_scale_kN() == True
    assert scrollable_frame.get_option_show_force_stroke() == True
    assert scrollable_frame.get_option_defo_percent() == True
    assert scrollable_frame.get_option_show_rp() == True
    assert scrollable_frame.get_option_show_legend() == True