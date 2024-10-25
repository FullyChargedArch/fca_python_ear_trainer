import pygame
import json
import Buttons
import Draw_Text

class Level_Menu:
	def __init__(self, display, game):
		self.display = display
		self.game = game
		self.current_page = None
		self.current_level = None

		#set up boxes
		self.title_background = pygame.Rect(0,0, 1280, 180)

		#set up fonts
		self.title_font = pygame.font.SysFont('Cascadia Mono', 144)
		self.level_font = pygame.font.SysFont('Cascadio Mono', 72)
		self.high_score_font = pygame.font.SysFont('Cascadio Mono', 48)
		self.button_font = pygame.font.SysFont('Cascadio Mono', 48)

		#set up colours
		self.colours = {'Black': (0,0,0), 'Purple': (193,0,167), 'DarkPurple': (153, 0, 132), 'LightPurple': (255, 84, 246)}

		#set up buttons
		self.easy_button = Buttons.Menu_Button(display=self.display, name='easy_button', text='Easy', font=self.button_font, colour=self.colours['DarkPurple'], highlight=self.colours['LightPurple'], width=430, height=75, x=640, y=395)
		self.medium_button = Buttons.Menu_Button(display=self.display, name='medium_button', text='Medium', font=self.button_font, colour=self.colours['DarkPurple'], highlight=self.colours['LightPurple'], width=430, height=75, x=640, y=480)
		self.hard_button = Buttons.Menu_Button(display=self.display, name='hard_button', text='Hard', font=self.button_font, colour=self.colours['DarkPurple'], highlight=self.colours['LightPurple'], width=430, height=75, x=640, y=565)
		self.back_button = Buttons.Menu_Button(display=self.display, name='back_button', text='Back', font=self.button_font, colour=self.colours['DarkPurple'], highlight=self.colours['LightPurple'], width=430, height=75, x=640, y=650)

		#navigation buttons
		self.left_button = Buttons.Menu_Button(display=self.display, name='left_button', text='<', font=self.button_font, colour=self.colours['DarkPurple'], highlight=self.colours['LightPurple'], width=50, height=450, x=25, y=450)
		self.right_button = Buttons.Menu_Button(display=self.display, name='right_button', text='>', font=self.button_font, colour=self.colours['DarkPurple'], highlight=self.colours['LightPurple'], width=50, height=450, x=1255, y=450)

	def set_current_level(self, current_page, current_level):
		#get page info
		self.current_page = current_page
		with open(f'./data/{current_page}_Page_Data.json') as file:
			self.page_data = json.load(file)
		#get level info
		self.current_level = current_level
		self.level_data = self.page_data['levels'][current_level]
		self.level_order = self.game.Level_Select.page_dict[self.current_page].level_order
	
	def run(self):
		#background
		self.display.fill(self.colours['Purple'])
		pygame.draw.rect(self.display, self.colours['DarkPurple'], self.title_background)

		#draw text on screen
		Draw_Text.draw_text(surface=self.display, font=self.title_font, text=self.current_page.replace('_',' '), text_colour=self.colours['Black'], align='centre', underline=0, x=640, y=110)
		Draw_Text.draw_text(surface=self.display, font=self.level_font, text=self.current_level.replace('_',' '), text_colour=self.colours['Black'], align='centre', underline=5, x=640, y=255)
		Draw_Text.draw_text(surface=self.display, font=self.high_score_font, text=f'Best: {self.level_data['highest_difficulty_completed'].capitalize()} {self.level_data['high_score']}/10, {self.level_data['highest_accuracy']}% Accuracy', text_colour=self.colours['Black'], align='centre', underline=0, x=640, y=325)

		#draw buttons on screen
		for button in [self.easy_button, self.medium_button, self.hard_button]:
			if button.draw() == True:
				self.game.Gameplay.set_up(level=self.current_level, level_data=self.level_data, difficulty=button.name[0:-7])
				self.game.current_state = 'Gameplay'
		if self.back_button.draw() == True:
			self.game.current_state = 'Level_Select'
		if self.left_button.draw() == True:
			current_index = self.level_order.index(self.current_level)
			current_index = (current_index-1)%(len(self.level_order))
			self.set_current_level(self.current_page, self.level_order[current_index])
		if self.right_button.draw() == True:
			current_index = self.level_order.index(self.current_level)
			current_index = (current_index+1)%(len(self.level_order))
			self.set_current_level(self.current_page, self.level_order[current_index])

