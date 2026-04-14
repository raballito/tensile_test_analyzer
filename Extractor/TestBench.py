# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 08:41:16 2024

Test Bench related Class

Saving all informations about current sample's Testbench.

Available functions:
    -identify_test_bench(file_path) for identify the test machine with headers of the csv
    -identify_file(file_path) to config the sample with the correct columns number in the csv


Version: Beta 1.12
Last Update: 31.03.26

@author: quentin.raball
"""

import os
import pandas as pd

class TestBenchConfig:
    def __init__(self, separator, header_index, force_channel, stroke_channel, ext_channel, time_channel, force_unit, repeat_every):
        self.separator = separator
        self.header_index = header_index
        self.force_channel = force_channel
        self.stroke_channel = stroke_channel
        self.ext_channel = ext_channel
        self.time_channel = time_channel
        self.force_unit = force_unit
        self.repeat_every = repeat_every
        self.samples_and_channels = None  # Cela sera défini après lecture du fichier

    def configure_channels(self, available_sample_names, repeat_every):
        list_time_channel = [self.time_channel + repeat_every * idx for idx, _ in enumerate(available_sample_names)]
        list_force_channel = [self.force_channel + repeat_every * idx for idx, _ in enumerate(available_sample_names)]
        list_stroke_channel = [self.stroke_channel + repeat_every * idx for idx, _ in enumerate(available_sample_names)]
        list_ext_channel = [self.ext_channel + repeat_every * idx for idx, _ in enumerate(available_sample_names)] if self.ext_channel else [None] * len(available_sample_names)
        
        return [available_sample_names, list_time_channel, list_force_channel, list_stroke_channel, list_ext_channel]


class TestBench:
    def __init__(self, file_path):
        # separator, header_index, force_channel, stroke_channel, ext_channel, time_channel, force_unit, repeat_every
        self.configurations = {
            "Shimadzu_1": TestBenchConfig(',', 2, 2, 3, None, 1, 1, 3),
            "Shimadzu_2": TestBenchConfig(',', 2, 2, 3, 4, 1, 1, 4),
            "WB100kN_1": TestBenchConfig(';', 1, 3, 10, 4, 2, 1000, 10),
            "WB100kN_2" : TestBenchConfig(';', 1, 3, 5, 4, 2, 1000, 5),
            "WB400kN_1" : TestBenchConfig(',', 1, 3, 2, None, 1, 1000, 3),
            "WB400kN_2" : TestBenchConfig(',', 1, 3, 2, None, 1, 1, 3),
            "Unknown" : TestBenchConfig(',', 1, 3, 2, None, 1, 1, 3),
            # Ajoute d'autres machines ici si nécessaire
        }
        self.file_path = file_path
        self.test_bench = None

    def identify_test_bench(self, file_path):
        potential_separators = [',', ';', '\t']  # Ajoutez d'autres séparateurs si nécessaire
        best_separator = None
        best_parts_count = 0
        for separator in potential_separators:
            df = pd.read_csv(file_path, sep=separator, nrows=3, header=None, encoding='latin-1')
            first_lines = df.values.tolist()
            parts_count = len(first_lines[1])
            if parts_count > best_parts_count:
                best_separator = separator
                best_parts_count = parts_count
        separator = best_separator
        with open(file_path, 'r', encoding='latin-1') as file:
            # Lire les trois premières lignes
            first_lines = [file.readline().strip() for _ in range(3)]
        first_lines = [[item.strip('"') for item in line.split(separator)] for line in first_lines]
        if 'Temps' in first_lines[1] or 'Force' in first_lines[1] or 'Stroke' in first_lines[1] or 'Course_Traverse' in first_lines[1]:
            if 'Ext.1' in first_lines[1]:
                self.test_bench = 'Shimadzu_2'
            else: 
                self.test_bench = 'Shimadzu_1'
            
        elif 'Déplacement [ mm ]' in first_lines[0] or 'Force [ kN ]' in first_lines[0]:
            if 'Force [ kN ]' in first_lines[0]:
                self.test_bench = 'WB400kN_1'
            elif 'Force [ N ]' in first_lines[0]:
                self.test_bench = 'WB400kN_2'
                
        elif 'C_1_Temps[s]' in first_lines[0] or 'C_1_Force[kN]' in first_lines[0] or 'C_1_Déform1[mm]' in first_lines[0]:
            if 'C_1_Valeur de commande[%]' in first_lines[0] or 'C_1_Valeur de consigne[]' in first_lines[0]:
                self.test_bench = 'WB100kN_1'
            else: 
                self.test_bench = 'WB100kN_2' 
        else:
            self.test_bench = "Unknown"        
        return self.test_bench

    def identify_file(self, file_path):
        test_bench = self.identify_test_bench(file_path)
        test_bench_config = self.configurations.get(test_bench)
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        print(f"Identification du fichier. Veuillez patienter.\nNom de la machine utilisée : {test_bench}.\nNom du fichier : {file_name}")
        if not test_bench_config:
            raise ValueError(f"Machine {test_bench} inconnue")

        with open(file_path, 'r', encoding='latin-1') as file:
            first_line = file.readline().strip()
            # Pour certaines machines (comme Shimadzu), récupérer les noms d'échantillons depuis la première ligne
            if test_bench == "Shimadzu_1" or test_bench == "Shimadzu_2":
                available_sample_names = [name.strip('\"') for name in first_line.split(test_bench_config.separator) if name.strip('\"')]
            else:
                # Pour d'autres machines (comme WB100kN), utiliser le nom du fichier comme nom d'échantillon
                available_sample_names = [file_name]
        
        test_bench_config.samples_and_channels = test_bench_config.configure_channels(available_sample_names, test_bench_config.repeat_every)
        
        return test_bench_config.samples_and_channels
