import pygame
import Buttons

class Piano:
	def __init__(self, display, colours, sounds, octave, width, height, x, y):
		#passed variables
		self.display = display
		self.colours = colours
		self.sounds = sounds
		self.octave = octave
		self.width = width
		self.height = height
		self.x = x
		self.y = y

		#key width and height
		self.key_border =int((0.1*self.width/7)/2)
		self.white_key_width = int(self.width/7)
		self.white_key_height = int(self.height)
		self.black_key_width = int(self.white_key_width * 2/3)
		self.black_key_height = int(self.height * 2/3)

		#set up black background
		self.keyboard_background = pygame.Rect((0,0), (self.width, self.height),)
		self.keyboard_background.center = (self.x, self.y)

		#set up white keys
		self.C_key = Key(display=self.display, name='C_key', key_type='left_white', border=self.key_border, colour=self.colours['White'], hightlight=self.colours['Light Grey'], width=self.white_key_width, height=self.white_key_height, x=self.x-3*self.white_key_width, y=self.y)
		self.D_key = Key(display=self.display, name='D_key', key_type='mid_white', border=self.key_border, colour=self.colours['White'], hightlight=self.colours['Light Grey'], width=self.white_key_width, height=self.white_key_height, x=self.x-2*self.white_key_width, y=self.y)
		self.E_key = Key(display=self.display, name='E_key', key_type='right_white', border=self.key_border, colour=self.colours['White'], hightlight=self.colours['Light Grey'], width=self.white_key_width, height=self.white_key_height, x=self.x-1*self.white_key_width, y=self.y)
		self.F_key = Key(display=self.display, name='F_key', key_type='left_white', border=self.key_border, colour=self.colours['White'], hightlight=self.colours['Light Grey'], width=self.white_key_width, height=self.white_key_height, x=self.x, y=self.y)
		self.G_key = Key(display=self.display, name='G_key', key_type='mid_white', border=self.key_border, colour=self.colours['White'], hightlight=self.colours['Light Grey'], width=self.white_key_width, height=self.white_key_height, x=self.x+1*self.white_key_width, y=self.y)
		self.A_key = Key(display=self.display, name='A_key', key_type='mid_white', border=self.key_border, colour=self.colours['White'], hightlight=self.colours['Light Grey'], width=self.white_key_width, height=self.white_key_height, x=self.x+2*self.white_key_width, y=self.y)
		self.B_key = Key(display=self.display, name='B_key', key_type='right_white', border=self.key_border, colour=self.colours['White'], hightlight=self.colours['Light Grey'], width=self.white_key_width, height=self.white_key_height, x=self.x+3*self.white_key_width, y=self.y)

		#set up black keys
		self.Db_key = Key(display=self.display, name='C#/Db_key', key_type='black', border=self.key_border, colour=self.colours['Black'], hightlight=self.colours['Dark Grey'], width=self.black_key_width, height=self.black_key_height, x=self.x-2.5*self.white_key_width, y=self.y)
		self.Eb_key = Key(display=self.display, name='D#/Eb_key', key_type='black', border=self.key_border, colour=self.colours['Black'], hightlight=self.colours['Dark Grey'], width=self.black_key_width, height=self.black_key_height, x=self.x-1.5*self.white_key_width, y=self.y)
		self.Gb_key = Key(display=self.display, name='F#/Gb_key', key_type='black', border=self.key_border, colour=self.colours['Black'], hightlight=self.colours['Dark Grey'], width=self.black_key_width, height=self.black_key_height, x=self.x+0.5*self.white_key_width, y=self.y)
		self.Ab_key = Key(display=self.display, name='G#/Ab_key', key_type='black', border=self.key_border, colour=self.colours['Black'], hightlight=self.colours['Dark Grey'], width=self.black_key_width, height=self.black_key_height, x=self.x+1.5*self.white_key_width, y=self.y)
		self.Bb_key = Key(display=self.display, name='A#/Bb_key', key_type='black', border=self.key_border, colour=self.colours['Black'], hightlight=self.colours['Dark Grey'], width=self.black_key_width, height=self.black_key_height, x=self.x+2.5*self.white_key_width, y=self.y)

		#all keys
		self.key_list = [self.C_key, self.Db_key, self.D_key, self.Eb_key, self.E_key, self.F_key, self.Gb_key, self.G_key, self.Ab_key, self.A_key, self.Bb_key, self.B_key]

	def draw(self):
		#draw black background
		pygame.draw.rect(surface=self.display, color=self.colours['Black'], rect=self.keyboard_background)

		#draw keys
		key_pressed = None
		for key in self.key_list:
			if key.draw() == True:
				key_pressed = key.name
		return(key_pressed)


class Key:
	def __init__(self, display, name, key_type, border, colour, hightlight, width, height, x, y):
		self.display = display
		self.name = name
		self.type = key_type
		self.border = border
		self.colour = colour
		self.highlight = hightlight
		self.width = width 
		self.height = height 
		self.x = x
		self.y = y
		self.rects = []
		self.active_colour = self.colour

		if self.type == 'left_white':
			self.bottom_rect = pygame.Rect((0,0), (self.width-self.border, int(self.height*1/3-self.border)))
			self.bottom_rect.midbottom = (self.x, int(self.y+self.height/2-self.border))
			self.top_rect = pygame.Rect((0,0), (int(self.width*2/3-self.border), int(self.height*2/3-self.border)))
			#self.top_rect.topleft = (int(self.x-self.width/2+self.border/2), int(self.y-self.height/2+self.border))
			self.top_rect.bottomleft = self.bottom_rect.topleft
			self.rects = [self.top_rect, self.bottom_rect]
		elif self.type == 'mid_white':
			self.top_rect = pygame.Rect((0,0), (int(self.width*1/3-self.border), int(self.height*2/3-self.border)))
			self.top_rect.midtop = (self.x, int(self.y-self.height/2+self.border))
			self.bottom_rect = pygame.Rect((0,0), (self.width-self.border, int(self.height*1/3-self.border)))
			self.bottom_rect.midbottom = (self.x, int(self.y+self.height/2-self.border))
			self.rects = [self.top_rect, self.bottom_rect]
		elif self.type == 'right_white':
			self.bottom_rect = pygame.Rect((0,0), (self.width-self.border, int(self.height*1/3-self.border)))
			self.bottom_rect.midbottom = (self.x, int(self.y+self.height/2-self.border))
			self.top_rect = pygame.Rect((0,0), (int(self.width*2/3-self.border), int(self.height*2/3-self.border)))
			#self.top_rect.topright = (int(self.x+self.width/2-self.border/2), int(self.y-self.height/2+self.border))
			self.top_rect.bottomright = self.bottom_rect.topright
			self.rects = [self.top_rect, self.bottom_rect]
		elif self.type == 'black':
			self.rect = pygame.Rect((0,0), (self.width+self.border, self.height-self.border))
			self.rect.midtop = (self.x, int(self.y-(self.height*0.75)+self.border))
			self.rects = [self.rect]

		self.clicked = False
	
	def draw(self):
		pos = pygame.mouse.get_pos()
		action = False

		#get if intersected
		for rect in self.rects:
			if rect.collidepoint(pos) == True:
				self.active_colour = self.highlight
				#check if mouse button is down
				if pygame.mouse.get_pressed()[0] == True and self.clicked == False:
					self.clicked = True
				if pygame.mouse.get_pressed()[0] == False and self.clicked == True:
					action = True
		
		#unhighlight if needed
		if len(self.rects) == 2:
			if self.top_rect.collidepoint(pos) == False and self.bottom_rect.collidepoint(pos) == False:
				self.active_colour = self.colour
		else:
			if self.rect.collidepoint(pos) == False:
				self.active_colour = self.colour

		#reset clicked
		if pygame.mouse.get_pressed()[0] == False:
			self.clicked = False

		for rect in self.rects:
			pygame.draw.rect(self.display, self.active_colour, rect)

		return(action)

		

