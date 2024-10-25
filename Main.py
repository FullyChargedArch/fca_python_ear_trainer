#import built in modules
import pygame
import sys
import random

#import custom modules
import Buttons
import Main_Menu
import Level_Select
import Level_Menu
import Gameplay
import Post_Game_Screen
import Pause_Menu
import Popup_Message

#allow sound to be played through pygame
pygame.mixer.init()

#set constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

class Main:
	def __init__(self):
		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		self.clock = pygame.time.Clock()

		#load things

		#set up fonts
		self.fonts = {}
		self.fonts['title'] = pygame.font.SysFont('Cascadia Mono', 80)
		self.fonts['subtitle'] = pygame.font.SysFont('Cascadia Mono', 48)
		self.fonts['round_counter'] = pygame.font.SysFont('Cascadia Mono', 60)
		self.fonts['instructions'] = pygame.font.SysFont('Cascadia Mono', 48)
		self.fonts['button'] =  pygame.font.SysFont('Cascadia Mono', 48)
		self.fonts['button_small'] = pygame.font.SysFont('Cascadia Mono', 30)
		self.fonts['large_title'] = pygame.font.SysFont('Cascadia Mono', 100)
		self.fonts['popup'] = pygame.font.SysFont('Cascadia Mono', 48)

		#load sounds
		self.sounds = {}
		for octave in range(1,6):
			for note in ['C','Db','D','Eb','E','F','Gb','G','Ab','A','Bb','B']:
				self.sounds[f'{note}{octave}'] = pygame.mixer.Sound(file=f'./sound_effects/{note}{octave}.mp3')
		self.sounds['correct'] = pygame.mixer.Sound(file=f'./sound_effects/correct.mp3')
		self.sounds['incorrect'] = pygame.mixer.Sound(file='./sound_effects/incorrect.mp3')

		#load images
		self.images = {}
		self.images['settings'] = pygame.image.load('./textures/settings.png')
		self.images['settings'] = pygame.transform.scale(self.images['settings'], (60, 60))
		self.images['play'] = pygame.image.load('./textures/play_button.png')
		self.images['play'] = pygame.transform.scale(self.images['play'], (60, 60))

		#colours
		self.colours = {'Black': (0,0,0), 'Dark': (128,128,128), 'Mid': (160,160,160), 'Light': (188,188,188), 'Highlight': (226,226,226)}

		#place gamestates here
		self.Main_Menu = Main_Menu.Main_Menu(self.screen, self)
		self.Level_Menu = Level_Menu.Level_Menu(self.screen, self)
		self.Level_Select = Level_Select.Level_Select(self.screen, self, self.Level_Menu)
		self.Gameplay = Gameplay.Gameplay(self.screen, self)
		self.Post_Game_Screen = Post_Game_Screen.Post_Game_Screen(self.screen, self)
		self.Pause_Menu = Pause_Menu.Pause_Menu(self.screen, self)
		self.Popup_Manager = Popup_Message.Popup_Manager(self.screen, self)

		#place states in a dictionary here
		self.current_state = 'Main_Menu'
		self.states = {'Main_Menu': self.Main_Menu,'Level_Select': self.Level_Select, 'Level_Menu': self.Level_Menu, 'Gameplay': self.Gameplay, 'Post_Game_Screen': self.Post_Game_Screen, 'Pause_Menu': self.Pause_Menu, 'Popup_Manager': self.Popup_Manager}

	def run(self):
		while True:
			#event handler
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			self.states[self.current_state].run()

			pygame.display.update()
			self.clock.tick(FPS)

Main = Main()
Main.run()