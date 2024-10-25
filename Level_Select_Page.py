import pygame
import json
import Buttons
import Draw_Text

class Page:
	def __init__(self, page_name, images, filename, display, page_height):
		#basic data
		self.page_name = page_name
		self.image_dict = images
		self.display = display
		self.page_height = page_height
		self.filename = filename
		
		#set up level dict
		self.level_dict = {}
		self.level_order = []

		#screen colours
		self.colours = {'Black': (0,0,0), 'Purple': (193,0,167)}

		#set up font
		self.title_font = pygame.font.SysFont('Cascadio Mono', 72)
		self.subtitle_font = pygame.font.SysFont('Cascadio Mono', 48)
		self.level_font = pygame.font.SysFont('Cascadia Mono', 36)

		#get data about page
		with open(self.filename) as file:
			self.page_data = json.load(file)

		#create buttons
		for item in self.page_data['levels'].items():
			level = item[0]
			data = item[1]
			new_button = Buttons.Button(name=data['name'], image=self.image_dict[f'{data['completion']}_completion_level'], x=data['start_x'], y=data['start_y'], y_offset=180)
			self.level_dict[f'{level}_button'] = new_button
			self.level_order.append(level)

		#create scroll bar
		self.scroll_bar = Buttons.Scroll_Bar(display=self.display, colour=(255, 84, 246), page_height=self.page_height, x=1260, y=180, width=20)

	def update_level_icons(self):
		with open(self.filename) as file:
			self.page_data = json.load(file)

		for level in self.page_data['levels']:
			completion = self.page_data['levels'][level]['completion']
			self.level_dict[f'{level}_button'].image = self.image_dict[f'{completion}_completion_level']

	def draw_text_boxes(self):
		for text_box in self.page_data['text_boxes']:
			underline=0
			if text_box['type'] == 'title':
				font=self.title_font
				underline=5
			elif text_box['type'] == 'subtitle':
				font=self.subtitle_font
			elif text_box['type'] == 'level':
				font=self.level_font
			Draw_Text.draw_text(surface=self.display, font=font, text=text_box["name"], text_colour=text_box["colour"], align=text_box["align"], underline=underline, x=text_box["start_x"], y=text_box["start_y"]-self.scroll_amount)

	def draw_levels(self):
		#draw levels
		for item in self.level_dict.items():
			level_title = item[0][0:-7]
			level = item[1]
			#draw level and check if clicked
			if level.draw(self.display, self.scroll_amount) == True:
				return(level_title)
			x, y = level.get_pos('midleft')
			Draw_Text.draw_text(surface=self.display, font=self.level_font, text=level.name, text_colour=self.colours['Black'], align='midleft', underline=False, x=x+90, y=y-180)

	def run(self):
		#fill in background
		self.display.fill(self.colours['Purple'])
		#draw scroll bar
		self.scroll_amount = self.scroll_bar.draw()
		#write text (not level text)
		self.draw_text_boxes()
		#draw level buttons and button text
		return(self.draw_levels())
		
		