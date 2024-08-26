# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 09:59:06 2024

Help window
- Print images in the window
- One menu for each mode of analysis

Version: Beta 1.0
Last Update: 05.08.24

@author: quentin.raball
"""

import customtkinter
import os
from PIL import Image


class HelpWindow(customtkinter.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        self.title("Formules utiles")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        self.logo_image = customtkinter.CTkImage(Image.open("static/COMATEC_HEIG-VD_logotype_rouge-rvb.png"), size=(120, 40))
        self.image_icon_image = customtkinter.CTkImage(Image.open("static/Logo_Traction.png"), size=(30, 30))
        self.traction_image = customtkinter.CTkImage(light_image=Image.open("static/Logo_Traction.png"),
                                                     dark_image=Image.open("static/Logo_Traction.png"), size=(40, 30))
        self.flex_3pts_image = customtkinter.CTkImage(light_image=Image.open("static/Logo_flex_3Pts.png"),
                                                      dark_image=Image.open("static/Logo_flex_3Pts.png"), size=(40, 30))
        self.flex_4pts_image = customtkinter.CTkImage(light_image=Image.open("static/Logo_flex_4Pts.png"),
                                                      dark_image=Image.open("static/Logo_flex_4Pts.png"), size=(40, 30))

        # Store image references
        self.images = {
            'logo_image': self.logo_image,
            'image_icon_image': self.image_icon_image,
            'traction_image': self.traction_image,
            'flex_3pts_image': self.flex_3pts_image,
            'flex_4pts_image': self.flex_4pts_image
        }

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.traction_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Traction",
                                                       fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                       image=self.traction_image, anchor="w", command=self.traction_button_event)
        self.traction_button.grid(row=1, column=0, sticky="ew")

        self.flex_3pts_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Flexion 3pts",
                                                        fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                        image=self.flex_3pts_image, anchor="w", command=self.flex_3pts_button_event)
        self.flex_3pts_button.grid(row=2, column=0, sticky="ew")

        self.flex_4pts_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Flexion 4pts",
                                                        fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                        image=self.flex_4pts_image, anchor="w", command=self.flex_4pts_button_event)
        self.flex_4pts_button.grid(row=3, column=0, sticky="ew")

        # Add a spacer row before the close button
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.close_button = customtkinter.CTkButton(self.navigation_frame, text="Fermer", command=self.close_window)
        self.close_button.grid(row=5, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.traction_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.traction_frame.grid_columnconfigure(0, weight=1)
        image_tract_light = Image.open("static/Formule_Traction.png")
        image_tract_dark = Image.open("static/Formule_Traction_dark.png")
        self.traction_formula_image = customtkinter.CTkImage(light_image=image_tract_light,
                                            dark_image=image_tract_dark,
                                            size=(650, 450))
        self.traction_image_label = customtkinter.CTkLabel(self.traction_frame, text="", image=self.traction_formula_image)
        self.traction_image_label.grid(row=0, column=0, padx=20, pady=20)
        self.images['traction_formula_image'] = self.traction_formula_image

        # create second frame
        self.flex_3pts_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.flex_3pts_frame.grid_columnconfigure(0, weight=1)
        image_flex_3pts_light = Image.open("static/Formule_Flex3pts.png")
        image_flex_3pts_dark = Image.open("static/Formule_Flex3pts_dark.png")
        self.flex_3pts_formula_image = customtkinter.CTkImage(light_image=image_flex_3pts_light,
                                            dark_image=image_flex_3pts_dark,
                                            size=(650, 450))
        self.flex_3pts_image_label = customtkinter.CTkLabel(self.flex_3pts_frame, text="", image=self.flex_3pts_formula_image)
        self.flex_3pts_image_label.grid(row=0, column=0, padx=20, pady=20)
        self.images['flex_3pts_formula_image'] = self.flex_3pts_formula_image

        # create third frame
        self.flex_4pts_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.flex_4pts_frame.grid_columnconfigure(0, weight=1)
        image_flex_4pts_light = Image.open("static/Formule_Flex4pts.png")
        image_flex_4pts_dark = Image.open("static/Formule_Flex4pts_dark.png")
        self.flex_4pts_formula_image = customtkinter.CTkImage(light_image=image_flex_4pts_light,
                                            dark_image=image_flex_4pts_dark,
                                            size=(650, 450))
        self.flex_4pts_image_label = customtkinter.CTkLabel(self.flex_4pts_frame, text="", image=self.flex_4pts_formula_image)
        self.flex_4pts_image_label.grid(row=0, column=0, padx=20, pady=20)
        self.images['flex_4pts_formula_image'] = self.flex_4pts_formula_image

        # select default frame
        self.select_frame_by_name("Traction")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.traction_button.configure(fg_color=("gray75", "gray25") if name == "Traction" else "transparent")
        self.flex_3pts_button.configure(fg_color=("gray75", "gray25") if name == "Flexion 3pts" else "transparent")
        self.flex_4pts_button.configure(fg_color=("gray75", "gray25") if name == "Flexion 4pts" else "transparent")

        # show selected frame
        if name == "Traction":
            self.traction_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.traction_frame.grid_forget()
        if name == "Flexion 3pts":
            self.flex_3pts_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.flex_3pts_frame.grid_forget()
        if name == "Flexion 4pts":
            self.flex_4pts_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.flex_4pts_frame.grid_forget()

    def traction_button_event(self):
        self.select_frame_by_name("Traction")

    def flex_3pts_button_event(self):
        self.select_frame_by_name("Flexion 3pts")

    def flex_4pts_button_event(self):
        self.select_frame_by_name("Flexion 4pts")

    def close_window(self):
        print("Fermeture de la fenêtre d'aide.")
        self.destroy()
