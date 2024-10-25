import pygame
import Buttons
import Draw_Text

class Popup_Manager:
	def __init__(self, display, game):
		self.display = display
		self.game = game
		self.popup = None
	def run(self):
		self.popup.draw()

class Incorrect_Message:
	def __init__(self, display, game, width, height, x, y, text):
		self.display = display
		self.game = game
		
		self.rect = pygame.Rect((x, y), (width, height))
		self.rect.center = (x, y)

		self.text = text

		self.play_correct_button = Buttons.Menu_Button(display=self.display, name='play_correct_button', text='Hear Again', font=self.game.fonts['button'], colour=self.game.colours['Mid'], highlight=self.game.colours['Highlight'], width=int(width*0.4), height=int(height*0.2), x=int(self.rect.left+width*0.25), y=int(self.rect.bottom-height*0.15))
		self.next_button = Buttons.Menu_Button(display=self.display, name='next_button', text='Next', font=self.game.fonts['button'], colour=self.game.colours['Mid'], highlight=self.game.colours['Highlight'], width=int(width*0.4), height=int(height*0.2), x=int(self.rect.right-width*0.25), y=int(self.rect.bottom-height*0.15))

	def draw(self):
		#draw background box onto screen
		pygame.draw.rect(surface=self.display, color=self.game.colours['Dark'], rect=self.rect)
		#draw text onto box
		Draw_Text.draw_text(surface=self.display, font=self.game.fonts['popup'], text=self.text, text_colour=self.game.colours['Black'], align='centre', underline=0, x=self.rect.center[0], y=self.rect.center[1])
		#draw buttons
		if self.play_correct_button.draw() == True:
			self.game.Gameplay.gameplay.play_correct_sound()
		if self.next_button.draw() == True:
			if self.game.Gameplay.difficulty == 'hard' and self.game.Gameplay.lives == 0:
				self.game.Gameplay.end_game()
			else:
				self.game.Gameplay.gameplay.start_new_round()
				self.game.current_state = 'Gameplay'