import pygame
import Draw_Text

class Button:
	#constructor
	def __init__(self, name, image, x, y, y_offset):
		self.name = name
		self.image = image
		self.rect = self.image.get_rect()
		self.y_offset = y_offset
		self.x = x
		self.y = y
		self.rect.topleft = (self.x, self.y + self.y_offset)
		self.clicked = False
		self.scroll_amount = 0

	def draw(self, surface, scroll_amount):
		action = False
		pos = pygame.mouse.get_pos()

		self.rect.topleft = (self.x, self.y+self.y_offset-scroll_amount)

		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == True and self.clicked == False:
				self.clicked = True
			if pygame.mouse.get_pressed()[0] == False and self.clicked == True:
				action = True

		if pygame.mouse.get_pressed()[0] == False:
			self.clicked = False
		
		surface.blit(self.image, (self.x, self.y-scroll_amount))
		
		return(action)

	def set_image(self, image):
		self.image = image

	def set_pos(self, x, y):
		self.rect.topleft = (x, y)

	def get_pos(self, align):
		if align == 'topleft':
			return(self.rect.topleft)
		elif align == 'midleft':
			return(self.rect.midleft)
		elif align == 'centre':
			return(self.rect.center)

	def get_name(self):
		return(self.name)

class Menu_Button:
	def __init__(self, display, name, text, font, colour, highlight, width, height, x, y):
		self.name = name
		self.display = display
		self.text = text
		self.font = font
		self.colour = colour
		self.highlight = highlight
		self.active_colour = self.colour
		self.width = width
		self.height = height
		self.x = x 
		self.y = y 

		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.center = (self.x, self.y)

		self.clicked = False

	def draw(self):
		pos = pygame.mouse.get_pos()
		action = False

		#get if intersected
		if self.rect.collidepoint(pos) == True:
			self.active_colour = self.highlight
			#check if mouse button is down
			if pygame.mouse.get_pressed()[0] == True and self.clicked == False:
				self.clicked = True
			if pygame.mouse.get_pressed()[0] == False and self.clicked == True:
				action = True
		else:
			self.active_colour = self.colour
		
		if pygame.mouse.get_pressed()[0] == False:
			self.clicked = False

		pygame.draw.rect(self.display, self.active_colour, self.rect)

		if self.text != None:
			Draw_Text.draw_text(surface=self.display, font=self.font, text=self.text, text_colour=(0,0,0), align='centre', underline=0, x=self.x, y=self.y)

		return(action)

	def get_name(self):
		return(self.name)

class Scroll_Bar:
	def __init__(self, display, colour, page_height, x, y, width):
		self.display = display
		self.page_height = page_height
		self.x = x
		self.y = y
		self.width = width
		self.height = 470/(page_height/470)
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
		self.display_rect = pygame.Rect(self.x, self.y-180, self.width, self.height)
		self.colour = colour
		self.clicked = False
		self.scroll_bar_distance = 470 - self.height
		self.total_scroll_distance = self.page_height - 470
	
	def draw(self):
		pos = pygame.mouse.get_pos()

		#scroll bar interaction
		if (self.rect.collidepoint(pos) == True and pygame.mouse.get_pressed()[0] == True) or self.clicked == True:
			self.clicked = True
			if pos[1] >= (180+self.height/2) and pos[1] <= (650-self.height/2):
				self.rect.centery = pos[1]
				self.display_rect.centery = pos[1]-180

			#just to make it look cleaner at the edges
			if pos[1] < (180+self.height/2):
				self.rect.top = 180
				self.display_rect.top = 0
			if pos[1] > (650-self.height/2):
				self.rect.bottom = 650
				self.display_rect.bottom = 470

		#stop following mouse if mouse click isn't being held
		if pygame.mouse.get_pressed()[0] == False:
			self.clicked = False
		
		#draw scroll bar on screen
		pygame.draw.rect(self.display, self.colour, self.display_rect)

		#get amount of pixels to scroll
		scroll_amount = self.total_scroll_distance * (self.display_rect.top/self.scroll_bar_distance)
		return(scroll_amount)

class Page_Navigator:
	def __init__(self, display, pages_list, pageManager, images, x, y):
		#important variables
		self.display = display
		self.pages_list = pages_list
		self.pageManager = pageManager
		self.num_pages = len(pages_list)
		self.current_index = self.pages_list.index(self.pageManager.page)
		self.image_dict = images
		self.x = x-6
		self.y = y-6

		#set colours
		self.active_colour = (255, 84, 246)
		self.inactive_colour = (193,0,167)

		#create buttons
		self.circle_button_dict = {}
		#circle buttons
		for i in range(self.num_pages):
			current_x = (self.x - (self.num_pages-1)/2 * 24) + 24*i
			new_circle_button = Button(name=f'{self.pages_list[i]}_button', image=self.image_dict['page_navigator_circle_inactive'], x=current_x, y=self.y, y_offset=650)
			self.circle_button_dict[f'{self.pages_list[i]}_button'] = new_circle_button
		#set active circle button
		self.circle_button_dict[f'{self.pages_list[self.current_index]}_button'].set_image(image=self.image_dict['page_navigator_circle_active'])
		
		#create left and right buttons
		distance_from_centre = (self.num_pages-1)/2*24 + 24
		self.left_button = Button(name='left_button', image=self.image_dict['page_navigator_left'], x=self.x-distance_from_centre-6, y=self.y-3, y_offset=650)
		self.right_button = Button(name='right_button', image=self.image_dict['page_navigator_right'], x=self.x+distance_from_centre, y=self.y-3, y_offset=650)

	def update_circle_buttons(self):
		#update index and set the image of new current button to active
		self.current_index = self.pages_list.index(self.pageManager.page)
		self.circle_button_dict[f'{self.pages_list[self.current_index]}_button'].set_image(image=self.image_dict['page_navigator_circle_active'])

	def draw(self):
		#draw buttons
		for button in self.circle_button_dict.values():
			if button.draw(self.display, 0) == True:
				#change the active page
				self.circle_button_dict[f'{self.pages_list[self.current_index]}_button'].set_image(image=self.image_dict['page_navigator_circle_inactive'])
				self.pageManager.page = button.get_name()[0:-7]
				self.update_circle_buttons()
		if self.left_button.draw(self.display, 0) == True:
			#change current button to inactive
			self.circle_button_dict[f'{self.pages_list[self.current_index]}_button'].set_image(image=self.image_dict['page_navigator_circle_inactive'])
			self.current_index = (self.current_index-1)%self.num_pages
			self.pageManager.page = self.pages_list[self.current_index]
			self.update_circle_buttons()
		elif self.right_button.draw(self.display, 0) == True:
			#change current button to inactive
			self.circle_button_dict[f'{self.pages_list[self.current_index]}_button'].set_image(image=self.image_dict['page_navigator_circle_inactive'])
			self.current_index = (self.current_index+1)%self.num_pages
			self.pageManager.page = self.pages_list[self.current_index]
			self.update_circle_buttons()
					