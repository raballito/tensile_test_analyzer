# Tensile Test Analyzer

Ce programme a été créer pour le département COMATEC de la Haute Ecole d'Ingénierie et de Gestion du Canton de Vaud (HEIG-VD).

https://heig-vd.ch/recherche/instituts/comatec/

Il permet de traiter les résultats de tests obtenus par les machines de tractions à disposition du département.
Les fichiers analysés doivent être en format '.csv'. 

Le projet est basé sur Python et sur le plugin CustomTkInter : https://github.com/TomSchimansky/CustomTkinter

Projet en français réalisé par Quentin Raball

N° Version : Beta 1.10

## Fonctionnalités
- Gestion des fichiers dans le programme.
- Traitement des fichiers csv obtenus par les machines de traction.
- Traitement de fichiers comprenant plusieurs échantillons en un seul fichier.
- Traitement des fichiers selon les 4 modes suivants : "Traction/Compression", "Flexion 3pts", "Flexion 4pts" et "Module de Young".
- Traitement des échantillons selon deux géométries possibles : "Ronde" et "Rectangulaires".
- Paramétrage individuels des échantillons avant leur analyse.
- Générer les graphiques suivants: "Force-Déplacement", "Force-Temps", "Contrainte-Déformation" et "Contrainte-Déplacement", groupés et individuels.
- Optention des valeurs intéressante d'une courbe de traction telles que Re, Rm, A%, E, etc...
- Exportation des résultats obtenus sous forme graphique et sous forme de tableau.
- Exportation de tous les samples et leurs valeurs dans un fichier Excel.
- Bien d'autre à découvrir !
- Bien d'autre à venir (Voir plus loin) !


## Machine Utilisées
Le département COMATEC utilise actuellement les machines suivantes:
- Shimadzu - 20 [kN] maximum - Sans Extensomètre
- Walter & Bai - 100 [kN] maximum - Avec et sans extensomètres
- Walter & Bai - 400 [kN] maximum - Sans extensomètre


## A venir (Work in Progress)
- Meilleure gestion des fenêtres
- Meilleure gestion du Dark Mode et réglage des derniers problèmes avec le mode sombre.
- Sauvegarde + Chargements sessions/résultats d'analyses.
- Nouveaux modes de test.
- Nouvelles géométries d'échantillons.
- Nouvelles machines supportées.
- Gestion de l'extensomètre pour les machines Shimadzu 20kN et W+B 400kN.
- Batch processing

## Utilisation
Ajoutez les fichiers csv directement obtenus par les machines de tractions dans le dossier Data du programme.
Vous pouvez aussi ajouter les fichiers depuis l'interface en cliquant sur le bouton approprié.
Configurez les échantillons en éditant leurs propriétés à partir du bouton correspondant.
Sélectionnez les fichiers que vous voulez analyser et cliquer sur le bouton "Analyser" en bas de la fenêtre.
Vous pouvez ensuite exporter les résultats en cliquant sur les boutons appropriés.


## F.A.Q
1) Les résultats n'apparaissent pas sur la fenêtre.

Agrandissez la fenêtre ou utilisez l'option de "scalling" afin de diminuer la taille des caractères.

2) Problèmes d'installation du plugin customtkinter

Pour résoudre ces problèmes (notamment si lors de l'execution du programme, celui-ci dit que le plugin est introuvable):
- Installer Miniconda, un gestionnaire de packages pour python.
- Ouvrir miniconda, et créer un nouvel environnement : "conda create -n [env-name]" avec [env-name]: le nom de l'environnement voulu/choisi
- Activer le nouvel environnement python avec la commande : "conda activate [env-name]"
- Installer le package customtkinter avec la commande suivante: "conda install -n [env-name] bioconda::customtkinter"
- Toujours dans l'interface conda, aller dans le répertoire du projet. "cd ./[dir]" pour ce déplacer dans le dossier [dir]. cd .. pour revenir en arrière.
- Trouver le fichier MainWindow.py et l'executer dans le nouvel environnement.

S'il manque des autres plugins, utiliser la commande : "conda install -n [env-name] [package]" avec [package] le nom du package voulu. Ils sont disponibles ici : https://anaconda.org/

3) Problèmes d'installation de Python

Pour installer python:

- Start+S
- Taper "CMD" et executer (il faut peut-être les accès administrateurs)
- Taper "python --version" et vérifier la version (min 3.11). Si python n'est pas installé, une fenêtre Windows Store devrait s'ouvrir permettant son installation.
- Si besoins (erreur ou autre), il faut probablement installer les plugins matplotlib, numpy, pandas et PIL

Si tout a été installé correctement, il suffit de lancer le programme principal en double-cliquant sur le fichier "MainWindow.py". Le programme devrait s'exécuter normalement.
