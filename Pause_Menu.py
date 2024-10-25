import pygame
import Buttons
import Draw_Text

class Pause_Menu:
	def __init__(self, display, game):
		self.display = display
		self.game = game

		#fonts and colours
		self.fonts = self.game.fonts
		self.colours = self.game.colours

		#create buttons
		self.resume_button = Buttons.Menu_Button(display=self.display, name='resume_button', text='Resume', font=self.fonts['button'], colour=self.colours['Dark'], highlight=self.colours['Highlight'], width=500, height=100, x=640, y=310)
		self.retry_button = Buttons.Menu_Button(display=self.display, name='retry_button', text='Retry', font=self.fonts['button'], colour=self.colours['Dark'], highlight=self.colours['Highlight'], width=500, height=100, x=640, y=425)
		self.menu_button = Buttons.Menu_Button(display=self.display, name='menu_button', text='Quit Game', font=self.fonts['button'], colour=self.colours['Dark'], highlight=self.colours['Highlight'], width=500, height=100, x=640, y=540)

	def run(self):
		self.display.fill(self.colours['Mid'])
		Draw_Text.draw_text(surface=self.display, font=self.fonts['large_title'], text=f'Game Paused', text_colour=self.colours['Black'], align='centre', underline=10, x=640, y=180)
		if self.resume_button.draw() == True:
			self.game.current_state = 'Gameplay'
		if self.retry_button.draw() == True:
			self.game.Gameplay.set_up(level=self.game.Gameplay.level, level_data=self.game.Gameplay.level_data, difficulty=self.game.Gameplay.difficulty)
			self.game.current_state = 'Gameplay'
		if self.menu_button.draw() == True:
			self.game.current_state = 'Level_Menu'