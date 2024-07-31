# Tensile Test Analyzer

Ce programme a été créer pour l'école HEIG-VD, afin de traiter les résultats des machines de tractions.

Le projet est basé sur le plugin CustomTkInter : https://github.com/TomSchimansky/CustomTkinter


## Installation de python sur windows
Pour installer python:

- Start+S
- Taper "CMD" et executer (il faut peut-être les accès administrateurs)
- Taper "python --version" et vérifier la version (min 3.11). Si python n'est pas installé, une fenêtre Windows Store devrait s'ouvrir permettant son installation.
- Taper la commande "pip3 install customtkinter" dans l'invite de commande.
- Installer le plugin en acceptant l'installation (appuyer sur la touche "Y" pour valider) des autres plugins.
- Si besoins (erreur ou autre), il faut probablement installer les plugins matplotlib, numpy, pandas et PIL

Si tout a été installé correctement, il suffit de lancer le programme principal en double-cliquant sur le fichier "MainWindow.py". Le programme devrait s'exécuter normalement.




## F.A.Q

1) Problèmes d'installation du plugin customtkinter

Pour résoudre ces problèmes (notamment si lors de l'execution du programme, celui-ci dit que le plugin est introuvable):
- Installer Miniconda, un gestionnaire de packages pour python.
- Ouvrir miniconda, et créer un nouvel environnement : conda create -n <env-name> avec <env-name>: le nom de l'environnement voulu/choisi
- Installer le package customtkinter avec la commande suivante: conda install -n <env-name> bioconda::customtkinter
- Activer le nouvel environnement python avec la commande : conda activate <env-name>
- Toujours dans l'interface conda, aller dans le répertoire du projet. cd ./<dir> pour ce déplacer dans le dossier <dir>. cd .. pour revenir en arrière.
- Trouver le fichier MainWindow.py et l'executer dans le nouvel environnement.

S'il manque des autres plugins, utiliser la commande : conda install -n <env-name> <package> avec <package> le nom du package voulu. Ils sont disponibles ici : https://anaconda.org/
