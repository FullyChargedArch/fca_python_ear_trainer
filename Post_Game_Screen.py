import pygame
import Buttons
import Draw_Text
import json

class Post_Game_Screen:
	def __init__(self, display, game):
		self.display = display
		self.game = game

		#things
		self.fonts = self.game.fonts
		self.colours = self.game.colours

		self.level = 'None'
		self.accuracy = 0

		#set up page elements
		self.top_bar = pygame.Rect(0,0,1280,180)
		self.top_bar.topleft = (0,0)
		self.bottom_bar = pygame.Rect(0,0,1280,70)
		self.bottom_bar.bottomleft = (0,720)

		#buttons
		self.play_again_button = Buttons.Menu_Button(display=self.display, name='play_again_button', text='Play Again', font=self.fonts['button'], colour=self.colours['Dark'], highlight=self.colours['Highlight'], width=380, height=125, x=445, y=560)
		self.menu_button = Buttons.Menu_Button(display=self.display, name='menu_button', text='Back to Menu', font=self.fonts['button'], colour=self.colours['Dark'], highlight=self.colours['Highlight'], width=380, height=125, x=835, y=560)

	def set_up(self):
		#level info
		self.level = self.game.Gameplay.level
		self.level_data = self.game.Gameplay.level_data
		self.difficulty = self.game.Gameplay.difficulty
		self.score = self.game.Gameplay.gameplay.score
		self.round = self.game.Gameplay.gameplay.round
		
		#game stats
		self.accuracy = round(((self.game.Gameplay.gameplay.score/(self.game.Gameplay.gameplay.guesses))*100), 2)

		if self.game.Gameplay.gameplay.lives != 0:
			self.update_save_file()

	def update_save_file(self):
		#open file
		with open(f'./data/{self.game.Level_Menu.current_page}_Page_Data.json') as file:
			data = json.load(file)

		#calculate completion
		if self.difficulty == 'easy' and self.score == 10:
			self.completion = 1
		elif self.difficulty == 'medium':
			if self.score == 10:
				self.completion = 4
			elif self.score >= 8:
				self.completion = 3
			elif self.score >= 5:
				self.completion = 3
			else:
				self.completion = 0
		elif self.difficulty == 'hard':
			if self.accuracy == 100:
				self.completion = 6
			elif self.game.Gameplay.gameplay.guesses <= 12:
				self.completion = 5
		else:
			self.completion = 0

		#determine if completion needs to be changed
		if data['levels'][self.level]['completion'] < self.completion:
			data['levels'][self.level]['completion'] = self.completion

		#determine if higher difficulty has been completed
		if data['levels'][self.level]['highest_difficulty_completed'] == '':
			data['levels'][self.level]['highest_difficulty_completed'] = self.difficulty
			data['levels'][self.level]['high_score'] = self.score
			data['levels'][self.level]['highest_accuracy'] = self.accuracy
		elif data['levels'][self.level]['highest_difficulty_completed'] == 'easy' and (self.difficulty == 'medium' or self.difficulty == 'hard'):
			data['levels'][self.level]['highest_difficulty_completed'] = self.difficulty
			data['levels'][self.level]['high_score'] = self.score
			data['levels'][self.level]['highest_accuracy'] = self.accuracy
		elif data['levels'][self.level]['highest_difficulty_completed'] == 'medium' and self.difficulty == 'hard':
			data['levels'][self.level]['highest_difficulty_completed'] = self.difficulty
			data['levels'][self.level]['high_score'] = self.score
			data['levels'][self.level]['highest_accuracy'] = self.accuracy

		#if same difficulty but higher score/accuracy
		elif data['levels'][self.level]['highest_difficulty_completed'] == self.difficulty:
			#if same difficulty but higher score change score and accuracy
			if data['levels'][self.level]['high_score'] < self.score:
				data['levels'][self.level]['high_score'] = self.score
				data['levels'][self.level]['highest_accuracy'] = self.accuracy
			#if same difficulty and score but higher accuracy change accuracy
			if data['levels'][self.level]['high_score'] == self.score and data['levels'][self.level]['highest_accuracy'] < self.accuracy:
				data['levels'][self.level]['highest_accuracy'] = self.accuracy

		#write new data to file
		with open(f'./data/{self.game.Level_Menu.current_page}_Page_Data.json', 'w') as file:
			json.dump(data, file)


	def run(self):
		#set up background
		self.display.fill(self.colours['Light'])
		pygame.draw.rect(self.display, self.colours['Dark'], self.top_bar)
		pygame.draw.rect(self.display, self.colours['Dark'], self.bottom_bar)

		#draw title text
		Draw_Text.draw_text(surface=self.display, font=self.fonts['title'], text=f'{self.level_data['gamemode']}: {self.level}', text_colour=self.colours['Black'], align='midleft', underline=0, x=10, y=80)
		Draw_Text.draw_text(surface=self.display, font=self.fonts['subtitle'], text=f'Difficulty: {self.difficulty.capitalize()}', text_colour=self.colours['Black'], align='midleft', underline=0, x=10, y=140)

		#level complete text
		if self.game.Gameplay.gameplay.lives == 0:
			Draw_Text.draw_text(surface=self.display, font=self.fonts['large_title'], text=f'Level Incomplete', text_colour=self.colours['Black'], align='centre', underline=10, x=640, y=270)
		else:
			Draw_Text.draw_text(surface=self.display, font=self.fonts['large_title'], text=f'Level Complete!', text_colour=self.colours['Black'], align='centre', underline=10, x=640, y=270)

		#draw score and accuracy
		Draw_Text.draw_text(surface=self.display, font=self.fonts['subtitle'], text=f'Score: {self.score}/{self.round}', text_colour=self.colours['Black'], align='centre', underline=0, x=413, y=400)
		Draw_Text.draw_text(surface=self.display, font=self.fonts['subtitle'], text=f'Accuracy: {self.accuracy}%', text_colour=self.colours['Black'], align='centre', underline=0, x=827, y=400)

		#draw buttons
		if self.play_again_button.draw() == True:
			self.game.Gameplay.set_up(level=self.game.Gameplay.level, level_data=self.game.Gameplay.level_data, difficulty=self.game.Gameplay.difficulty)
			self.game.current_state = 'Gameplay'
		if self.menu_button.draw() == True:
			self.game.Level_Select.page_dict[self.game.Level_Select.page].update_level_icons()
			self.game.Level_Menu.set_current_level(self.game.Level_Menu.current_page, self.game.Level_Menu.current_level)
			self.game.current_state = 'Level_Menu'