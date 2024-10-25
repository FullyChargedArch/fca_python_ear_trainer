import pygame
import Buttons
import Draw_Text
import Level_Select_Page

class Level_Select:
	def __init__(self, display, game, Level_Menu):
		#set up screen
		self.display = display
		self.game = game
		self.page = 'Note_Recognition'
		self.Level_Menu = Level_Menu

		#colours
		self.colours = {'Black': (0,0,0), 'Purple': (193,0,167), 'DarkPurple': (153, 0, 132), 'LightPurple': (255, 84, 246)}
		
		#get fonts
		self.title_font = pygame.font.SysFont('Cascadia Mono', 144)
		self.main_menu_font = pygame.font.SysFont('Cascadia Mono', 36)
		
		#load images
		self.image_dict = {}
		#level completion images
		for i in range(0,7):
			self.image_dict[f'{i}_completion_level'] = pygame.image.load(f'./textures/{i}_completion_level.png')
			self.image_dict[f'{i}_completion_level'] = pygame.transform.scale(self.image_dict[f'{i}_completion_level'], (400, 80))
		#page navigation images
		self.image_dict['page_navigator_left'] = pygame.image.load('./textures/page_navigator_left.png')
		self.image_dict['page_navigator_right'] = pygame.image.load('./textures/page_navigator_right.png')
		self.image_dict['page_navigator_circle_inactive'] = pygame.image.load('./textures/page_navigator_circle_inactive.png')
		self.image_dict['page_navigator_circle_active'] = pygame.image.load('./textures/page_navigator_circle_active.png')

		#elements of screen
		self.title_bar = pygame.Surface((1280,180))
		self.bottom_bar = pygame.Surface((1280,70))
		self.level_screen = pygame.Surface((1280,470))

		#useful for debugging clicks
		self.bottom_bar_rect = Buttons.Menu_Button(display=self.display, name='bottom_bar', text='', font=self.title_font, colour=self.colours['DarkPurple'], highlight=self.colours['DarkPurple'], width=1280, height=70, x=640, y=685)

		#create pages
		self.Higher_or_Lower = Level_Select_Page.Page(page_name='Higher or Lower', images=self.image_dict, filename='./data/Higher_or_Lower_Page_Data.json',display=self.level_screen, page_height=500)
		self.Note_Recognition = Level_Select_Page.Page(page_name='Note Recognition', images=self.image_dict, filename='./data/Note_Recognition_Page_Data.json',display=self.level_screen, page_height=840)
		self.Pitch_Recognition = Level_Select_Page.Page(page_name='Pitch Recognition', images=self.image_dict, filename='./data/Pitch_Recognition_Page_Data.json',display=self.level_screen, page_height=840)
		self.Interval_Recognition = Level_Select_Page.Page(page_name='Interval Recognition', images=self.image_dict, filename='./data/Interval_Recognition_Page_Data.json',display=self.level_screen, page_height=1320)
		self.Chord_Recognition = Level_Select_Page.Page(page_name='Chord_Recognition', images=self.image_dict, filename='./data/Chord_Recognition_Page_Data.json', display=self.level_screen, page_height=840)
		self.page_dict = {'Higher_or_Lower': self.Higher_or_Lower, 'Note_Recognition': self.Note_Recognition, 'Pitch_Recognition': self.Pitch_Recognition, 'Interval_Recognition': self.Interval_Recognition, 'Chord_Recognition': self.Chord_Recognition}
		self.page_order = ['Higher_or_Lower', 'Note_Recognition', 'Pitch_Recognition', 'Interval_Recognition', 'Chord_Recognition']

		#page navigator setup
		self.page_navigator = Buttons.Page_Navigator(display=self.bottom_bar, pages_list=self.page_order, pageManager=self, images=self.image_dict, x=640, y=35)

		#back to main menu button
		self.main_menu_button = Buttons.Menu_Button(display=self.display, name='main_menu_button', text='Main Menu', font=self.main_menu_font, colour=self.colours['DarkPurple'], highlight=self.colours['Purple'], width=200, height=50, x=120, y=685)

	def run(self):
		#fill surfaces
		self.display.fill(self.colours['Purple'])
		self.title_bar.fill(self.colours['DarkPurple'])
		self.bottom_bar.fill(self.colours['DarkPurple'])

		#draw text onto surfaces
		Draw_Text.draw_text(surface=self.title_bar, font=self.title_font, text='Level Select', text_colour=self.colours['Black'], align='centre', underline=0, x=640, y=110)

		#bottom bar clicked
		bottom_clicked = self.bottom_bar_rect.draw()

		#draw the page navigator
		self.page_navigator.draw()

		#blit surfaces onto display
		self.display.blit(self.title_bar, (0,0))
		self.display.blit(self.bottom_bar, (0, 650))
		self.display.blit(self.level_screen, (0, 180))

		#draw main menu button
		if self.main_menu_button.draw() == True:
			self.game.current_state = 'Main_Menu'

		#run the current level screen to display
		level_selected = self.page_dict[self.page].run()
		
		#if level clicked go to level menu
		if level_selected != None and bottom_clicked == False:
			self.Level_Menu.set_current_level(self.page, level_selected)
			self.game.current_state = 'Level_Menu'

class Page_Manager:
	def __init__(self, current_page):
		self.current_page = current_page
	def get_current_page(self):
		return(self.current_page)
	def set_current_page(self, current_page):
		self.current_page = current_page
