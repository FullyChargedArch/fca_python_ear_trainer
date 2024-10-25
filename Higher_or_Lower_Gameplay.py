import pygame
import random
import Buttons
import Draw_Text
import Popup_Message

class Higher_or_Lower_Gameplay:
	def __init__(self, display, images, sounds, fonts, colours, game):
		self.display = display
		self.images = images
		self.fonts = fonts
		self.colours = colours
		self.sounds = sounds
		self.channel = pygame.mixer.Channel(0)
		self.game = game 
		self.level = self.game.Gameplay.level_data
		
		#gameplay variables
		self.round = 0
		self.score = 0
		self.guesses = 0
		self.lives = 3
		self.difficulty = self.game.Gameplay.difficulty
		self.correct_options = ['higher', 'lower']
		self.notes = ['C','Db','D','Eb','E','F','Gb','G','Ab','A','Bb','B']
		self.correct = None
		self.new_round = True

		#buttons
		self.buttons = {}
		self.buttons['higher_button'] = Buttons.Menu_Button(display=self.display, name='higher_button', text='Higher', font=self.fonts['button'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=365, height=120, x=640, y=290)
		self.buttons['lower_button'] = Buttons.Menu_Button(display=self.display, name='lower_button', text='Lower', font=self.fonts['button'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=365, height=120, x=640, y=510)

	def play_correct_sound(self):
		self.channel.play(self.pitch1, 0, 1000)
		self.channel.queue(self.pitch2)

	def check_buttons(self):
		#check buttons for input
		for button in self.buttons.values():
			if button.draw() == True:
				self.guesses += 1
				if button.get_name()[0:-7] == self.correct:
					self.sounds['correct'].play()
					if self.difficulty == 'medium':
						self.lives = 3
					self.score += 1
					self.start_new_round()
				else:
					self.sounds['incorrect'].play()
					if self.difficulty == 'medium':
						self.lives -= 1
						if self.lives == 0:
							self.display_incorrect_message()
					elif self.difficulty == 'hard':
						self.lives -= 1
						self.display_incorrect_message()

	def generate_pitches(self, semitone_amount):
		#pitches
		if self.correct == 'higher':
			#generate pitch 1
			pitch1_index = random.randint(0,11)
			pitch1_octave = random.randint(1,4)
			self.pitch1 = self.sounds[f'{self.notes[pitch1_index]}{pitch1_octave}']
			
			#generate pitch 2
			pitch2_index = (pitch1_index + semitone_amount)
			pitch2_octave = pitch1_octave
			#if changed octave then add to octave and correct index
			if pitch2_index >= 12:
				pitch2_index = pitch2_index%12
				pitch2_octave += 1
			self.pitch2 = self.sounds[f'{self.notes[pitch2_index]}{pitch2_octave}']
		
		elif self.correct == 'lower':
			#generate pitch 1
			pitch1_index = random.randint(0,11)
			pitch1_octave = random.randint(2,5)
			self.pitch1 = self.sounds[f'{self.notes[pitch1_index]}{pitch1_octave}']
			
			#generate pitch 2
			pitch2_index = (pitch1_index - semitone_amount)
			pitch2_octave = pitch1_octave
			#if changed octave then add to octave and correct index
			if pitch2_index < 0:
				pitch2_index = pitch2_index%12
				pitch2_octave -= 1
			self.pitch2 = self.sounds[f'{self.notes[pitch2_index]}{pitch2_octave}']

	def start_new_round(self):
		self.round += 1
		if self.difficulty == 'medium':
			self.lives = 3
		self.correct = self.correct_options[random.randint(0, len(self.correct_options)-1)]
		
		#semitone amount
		semitone_amount = random.randint(self.level['min_semitones'], self.level['max_semitones'])

		#generate pitches
		self.generate_pitches(semitone_amount)

		#play correct sound
		self.play_correct_sound()

	def display_incorrect_message(self):
		self.game.Popup_Manager.popup = Popup_Message.Incorrect_Message(display=self.display, game=self.game, width=700, height=400, x=640, y=415, text=f'Incorrect, Correct Response: {self.correct}')
		self.game.current_state = 'Popup_Manager'

	def run(self):
		if self.new_round == True:
			self.start_new_round()
			self.new_round = False

		#write text onto screen
		Draw_Text.draw_text(surface=self.display, font=self.fonts['instructions'], text='Select the correct option.', text_colour=self.colours['Black'], align='centre', underline=0, x=640, y=400)

		#check all the gameplay related buttons
		self.check_buttons()





