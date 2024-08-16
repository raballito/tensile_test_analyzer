# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 08:41:16 2024

Test Bench related Class

Saving all informations about current sample's Testbench.

Available functions:
    -identify_test_bench(file_path) for identify the test machine with headers of the csv
    -identify_file(file_path) to config the sample with the correct columns number in the csv


Version: Beta 1.1
Last Update: 06.08.24

@author: quentin.raball
"""


import pandas as pd

class TestBench:
    
    @staticmethod
    def identify_test_bench(file_path):
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
            test_bench = 'Shimadzu'
            
        elif 'Déplacement [ mm ]' in first_lines[0] or 'Force [ kN ]' in first_lines[0]:
            if 'Force [ kN ]' in first_lines[0]:
                test_bench = 'WB400kN_1'
            elif 'Force [ N ]' in first_lines[0]:
                test_bench = 'WB400kN_2'
                
        elif 'C_1_Temps[s]' in first_lines[0] or 'C_1_Force[kN]' in first_lines[0] or 'C_1_Déform1[mm]' in first_lines[0]:
            if 'C_1_Valeur de commande[%]' in first_lines[0] or 'C_1_Valeur de consigne[]' in first_lines[0]:
                test_bench = 'WB100kN_1'
            else: 
                test_bench = 'WB100kN_2' 
        else:
            test_bench = "Unknown"        
        return test_bench
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.FileName = None
        self.test_bench = None
        self.number_of_test = None
        self.available_sample_names = None
        self.extensometer_choice_value = "Course Traverse"
        self.sample_name = None
        self.separator = ','
        self.header_index = 2
        self.force_channel = 2
        self.stroke_channel = 3
        self.time_channel = 1
        self.force_unit = 1
        self.repeat_every = 3
        self.samples_and_channels = []
        
         
    #Fonction d'identification du banc de test
    def identify_file(self, file_path):
        test_bench = self.identify_test_bench(file_path)
        # Identifier la machine de traction en fonction des informations et configure les valeurs pour importation.
        if test_bench=="Shimadzu":
            self.separator = ','
            self.header_index = 2
            self.force_channel = 2
            self.stroke_channel = 3
            self.time_channel = 1
            self.force_unit = 1 #Unité canal force en N
            self.repeat_every = 3
            with open(file_path, 'r', encoding='latin-1') as file: 
                first_line = file.readline().strip()
                self.available_sample_names = list(filter(None, first_line.split(self.separator)))
                self.available_sample_names = [name.strip('\"') for name in self.available_sample_names if name.strip('\"')]
                list_time_channel = [self.time_channel + self.repeat_every * idx for idx, _ in enumerate(self.available_sample_names)]
                list_force_channel = [self.force_channel + self.repeat_every * idx for idx, _ in enumerate(self.available_sample_names)]
                list_stroke_channel = [self.stroke_channel + self.repeat_every * idx for idx, _ in enumerate(self.available_sample_names)]
                self.number_of_test = len(first_line[1]) // 3
                self.samples_and_channels = [self.available_sample_names, list_time_channel, list_force_channel, list_stroke_channel]
        
        elif test_bench == 'WB400kN_1':
            self.separator = ','
            self.header_index = 1
            self.force_channel = 3
            self.stroke_channel = 2
            self.time_channel = 1
            self.force_unit = 1000 #Unités du canal force en kN
            self.repeat_every = 3
            with open(file_path, 'r', encoding='latin-1') as file: 
                first_line = file.readline().strip()
                self.available_sample_names = ['Default W+B 400 kN']
                list_time_channel = [self.time_channel + self.repeat_every * idx for idx, _ in enumerate(self.available_sample_names)]
                list_force_channel = [self.force_channel + self.repeat_every * idx for idx, _ in enumerate(self.available_sample_names)]
                list_stroke_channel = [self.stroke_channel + self.repeat_every * idx for idx, _ in enumerate(self.available_sample_names)]
                self.number_of_test = len(first_line[1]) // 3
                self.samples_and_channels = [self.available_sample_names, list_time_channel, list_force_channel, list_stroke_channel]
        
        elif test_bench == 'WB400kN_2':
            self.separator = ','
            self.header_index = 1
            self.force_channel = 3
            self.stroke_channel = 2
            self.time_channel = 1
            self.force_unit = 1 #Unités du canal force en kN
            self.repeat_every = 3
            with open(file_path, 'r', encoding='latin-1') as file: 
                first_line = file.readline().strip()
                self.available_sample_names = ['Default W+B 400 kN']
                list_time_channel = [self.time_channel + self.repeat_every * idx for idx, _ in enumerate(self.available_sample_names)]
                list_force_channel = [self.force_channel + self.repeat_every * idx for idx, _ in enumerate(self.available_sample_names)]
                list_stroke_channel = [self.stroke_channel + self.repeat_every * idx for idx, _ in enumerate(self.available_sample_names)]
                self.number_of_test = len(first_line[1]) // 3
                self.samples_and_channels = [self.available_sample_names, list_time_channel, list_force_channel, list_stroke_channel]
        
        elif test_bench == 'WB100kN_1': #Version avec canaux virtuel
            self.separator = ';'
            self.header_index = 1
            self.force_channel = 3
            self.time_channel = 2
            self.stroke_channel = 10
            self.force_unit = 1000 #Unité canal force en kN
            self.repeat_every = 10
            with open(file_path, 'r', encoding='latin-1') as file: 
                first_line = file.readline().strip()
                self.available_sample_names = ['Default W+B 100 kN']
                list_time_channel = [self.time_channel + self.repeat_every * idx for idx, _ in enumerate(self.available_sample_names)]
                list_force_channel = [self.force_channel + self.repeat_every * idx for idx, _ in enumerate(self.available_sample_names)]
                list_stroke_channel = [self.stroke_channel + self.repeat_every * idx for idx, _ in enumerate(self.available_sample_names)]
                self.number_of_test = len(first_line[1]) // 10
                self.samples_and_channels = [self.available_sample_names, list_time_channel, list_force_channel, list_stroke_channel]
            
        elif test_bench == 'WB100kN_2': #Version sans les virtual channel
            self.separator = ';'
            self.header_index = 1
            self.force_channel = 3
            self.time_channel = 2
            self.stroke_channel = 5
            self.force_unit = 1000 #Unité canal force en kN
            self.repeat_every = 5
            with open(file_path, 'r', encoding='latin-1') as file: 
                first_line = file.readline().strip()
                self.available_sample_names = ['Default W+B 100 kN']
                list_time_channel = [self.time_channel + self.repeat_every * idx for idx, _ in enumerate(self.available_sample_names)]
                list_force_channel = [self.force_channel + self.repeat_every * idx for idx, _ in enumerate(self.available_sample_names)]
                list_stroke_channel = [self.stroke_channel + self.repeat_every * idx for idx, _ in enumerate(self.available_sample_names)]
                self.number_of_test = len(first_line[1]) // 5
                self.samples_and_channels = [self.available_sample_names, list_time_channel, list_force_channel, list_stroke_channel]
        
        else:
           self.separator = ';'
           self.header_index = 1
           self.force_channel = 3
           self.stroke_channel = 2
           self.time_channel = 1
           self.force_unit = 1000 #Unités du canal force en kN
           self.repeat_every = 3

        self.default_sample_names = self.available_sample_names.copy()
        
        #print("Sample and channels:", self.samples_and_channels)
        return self.samples_and_channels
