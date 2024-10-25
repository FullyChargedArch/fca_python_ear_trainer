import pygame
import sys
import json
import Buttons
import Draw_Text

class Main_Menu:
	def __init__(self, display, game):
		self.display = display
		self.game = game
		self.colours = {'Black': (0,0,0), 'Purple': (193,0,167), 'DarkPurple': (153, 0, 132), 'LightPurple': (255, 84, 246)}
		self.title = 'Main Menu'
		self.title_font = pygame.font.SysFont('Cascadia Mono', 172)
		self.button_font = pygame.font.SysFont('Cascadia Mono', 72)
		self.level_select_button = Buttons.Menu_Button(display=self.display, name='level_select_button', text='Level Select', font=self.button_font, colour=self.colours['DarkPurple'], highlight=self.colours['LightPurple'], width=500, height= 110, x=640, y=350)
		self.options_button = Buttons.Menu_Button(display=self.display, name='options_button', text='Options', font=self.button_font, colour=self.colours['DarkPurple'], highlight=self.colours['LightPurple'], width=500, height= 110, x=640, y=480)
		self.quit_button = Buttons.Menu_Button(display=self.display, name='quit_button', text='Quit', font=self.button_font, colour=self.colours['DarkPurple'], highlight=self.colours['LightPurple'], width=500, height= 110, x=640, y=610)

	def run(self):
		self.display.fill(self.colours['Purple'])

		#draw title
		Draw_Text.draw_text(surface=self.display, font=self.title_font, text=self.title, text_colour=(0,0,0), align='centre', underline=10, x=640, y=180)

		if self.level_select_button.draw() == True:
			self.game.current_state = 'Level_Select'
		if self.options_button.draw() == True:
			pass
		if self.quit_button.draw() == True:
			pygame.quit()
			sys.exit()

