import pygame
import Buttons
import Draw_Text
import Higher_or_Lower_Gameplay
import Note_Recognition_Gameplay
import Pitch_Recognition_Gameplay
import Interval_Recognition_Gameplay

class Gameplay:
	def __init__(self, display, game):
		self.display = display
		self.game = game

		#set up fonts
		self.fonts = self.game.fonts

		#set up colours
		self.colours = {'Black': (0,0,0), 'Dark': (128,128,128), 'Mid': (160,160,160), 'Light': (188,188,188), 'Highlight': (226,226,226)}

		#set up page elements
		self.top_bar = pygame.Rect(0,0,1280,180)
		self.top_bar.topleft = (0,0)
		self.bottom_bar = pygame.Rect(0,0,1280,70)
		self.bottom_bar.bottomleft = (0,720)

		#load images used for gameplay
		self.images = self.game.images

		#load sounds
		self.sounds = self.game.sounds

		#set up lives counter
		self.lives = 3
		self.lives_counter = Lives_Counter(self.display)

		#gameplay variables
		self.round = 0

		#buttons
		self.settings_button = Buttons.Button(name='settings_button', image=self.images['settings'], x=1230-30, y=685-30, y_offset=0)
		self.play_button = Buttons.Button(name='play_button', image=self.images['play'], x=1150-30, y=685-30, y_offset=0)

	def set_up(self, level, level_data, difficulty):
		#set up personal variables
		self.level = level
		self.level_data = level_data
		self.difficulty = difficulty

		if self.level_data['gamemode'] == 'Higher or Lower':
			self.gameplay = Higher_or_Lower_Gameplay.Higher_or_Lower_Gameplay(display=self.display, images=self.images, sounds=self.sounds, fonts=self.fonts, colours=self.colours, game=self.game)
		if self.level_data['gamemode'] == 'Note Recognition':
			self.gameplay = Note_Recognition_Gameplay.Note_Recognition_Gameplay(display=self.display, game=self.game, level_data=self.level_data)
		if self.level_data['gamemode'] == 'Pitch Recognition':
			self.gameplay = Pitch_Recognition_Gameplay.Pitch_Recognition_Gameplay(display=self.display, game=self.game, level_data=self.level_data)
		if self.level_data['gamemode'] == 'Interval Recognition':
			self.gameplay = Interval_Recognition_Gameplay.Interval_Recognition_Gameplay(display=self.display, game=self.game, level_data=self.level_data)
		if self.level_data['gamemode'] == 'Chord Recognition':
			self.gameplay = Chord_Recognition_Gameplay.Chord_Recognition_Gameplay(display=self.display, game=self.game, level_data=self.level_data)

	def end_game(self):
		pygame.mixer.stop()
		if self.round == 11 or self.difficulty == 'hard':
			self.round -= 1
			self.gameplay.round -= 1
		self.game.Post_Game_Screen.set_up()
		self.game.current_state = 'Post_Game_Screen'

	def run(self):
		#set up background
		self.display.fill(self.colours['Light'])
		pygame.draw.rect(self.display, self.colours['Dark'], self.top_bar)
		pygame.draw.rect(self.display, self.colours['Dark'], self.bottom_bar)

		#draw title text
		Draw_Text.draw_text(surface=self.display, font=self.fonts['title'], text=f'{self.level_data['gamemode']}: {self.level}', text_colour=self.colours['Black'], align='midleft', underline=0, x=10, y=80)
		Draw_Text.draw_text(surface=self.display, font=self.fonts['subtitle'], text=f'Difficulty: {self.difficulty.capitalize()}', text_colour=self.colours['Black'], align='midleft', underline=0, x=10, y=140)

		#round counter
		Draw_Text.draw_text(surface=self.display, font=self.fonts['round_counter'], text=f'Round: {self.round}/10', text_colour=self.colours['Black'], align='midleft', underline=0, x=10, y=685)

		#lives counter
		self.lives_counter.draw(self.lives)

		#options and play button
		if self.settings_button.draw(self.display, 0) == True:
			pygame.mixer.stop()
			self.game.current_state = 'Pause_Menu'
		if self.play_button.draw(self.display, 0) == True:
			self.gameplay.play_correct_sound()

		#draw gameplay page
		self.gameplay.run()
		self.round = self.gameplay.round 
		self.lives = self.gameplay.lives

		#end game after 10 rounds
		if self.round == 11:
			self.end_game()
		#if on hard end game when out of lives
		if self.lives == 0 and self.gameplay.difficulty == 'hard':
			self.gameplay.display_incorrect_message()
			self.gameplay.round += 1
			self.round += 1





class Lives_Counter:
	def __init__(self, display):
		self.display = display
		self.images = {}
		self.images['full_heart'] = pygame.image.load('./textures/heart_full.png')
		self.images['full_heart'] = pygame.transform.scale(self.images['full_heart'], (60, 60))
		self.images['empty_heart'] = pygame.image.load('./textures/heart_empty.png')
		self.images['empty_heart'] = pygame.transform.scale(self.images['empty_heart'], (60, 60))

	def draw(self, current_lives):
		#draw full hearts then empty hearts
		for i in range(0,current_lives):
			self.display.blit(self.images['full_heart'], (640-120+i*90, 655))
		for i in range(0,3-current_lives):
			self.display.blit(self.images['empty_heart'], (640+60-i*90, 655))
