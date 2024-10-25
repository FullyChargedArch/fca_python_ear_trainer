import pygame
import random
import Buttons
import Piano
import Draw_Text
import Popup_Message


class Pitch_Recognition_Gameplay:
	def __init__(self, display, game, level_data):
		self.display = display
		self.game = game 

		#init things
		self.fonts = self.game.fonts
		self.colours = {'White': (255,255,255), 'Black': (0,0,0), 'Light Grey': (188, 188, 188), 'Dark Grey': (68, 68, 68)}
		self.sounds = self.game.sounds
		self.channel = pygame.mixer.Channel(0)

		#get level data
		self.level_data = level_data

		#gameplay variables
		self.round = 0
		self.score = 0
		self.guesses = 0
		self.lives = 3
		self.difficulty = self.game.Gameplay.difficulty
		self.correct = None 
		self.correct_sound = None
		self.new_round = True
		self.notes = self.level_data['notes']
		self.low_octave = 1
		self.high_octave = 5

		#set up keyboard
		self.piano1 = Piano.Piano(display=self.display, colours=self.colours, sounds=self.sounds, octave=1, width=250, height=240, x=140, y=450)
		self.piano2 = Piano.Piano(display=self.display, colours=self.colours, sounds=self.sounds, octave=2, width=250, height=240, x=390, y=450)
		self.piano3 = Piano.Piano(display=self.display, colours=self.colours, sounds=self.sounds, octave=3, width=250, height=240, x=640, y=450)
		self.piano4 = Piano.Piano(display=self.display, colours=self.colours, sounds=self.sounds, octave=4, width=250, height=240, x=890, y=450)
		self.piano5 = Piano.Piano(display=self.display, colours=self.colours, sounds=self.sounds, octave=5, width=250, height=240, x=1140, y=450)

	def generate_answer(self):
		self.correct_note = self.notes[random.randint(0, len(self.notes)-1)]
		self.correct_octave = random.randint(self.low_octave, self.high_octave)
		self.correct = f'{self.correct_note}{self.correct_octave}'

		#correct sounds
		if "#" not in self.correct_note:
			self.correct_sound = self.sounds[f'{self.correct_note}{self.correct_octave}']
		elif self.correct_note == 'C#':
			self.correct_sound = self.sounds[f'Db{self.correct_octave}']
		elif self.correct_note == 'D#':
			self.correct_sound = self.sounds[f'Eb{self.correct_octave}']
		elif self.correct_note == 'F#':
			self.correct_sound = self.sounds[f'Gb{self.correct_octave}']
		elif self.correct_note == 'G#':
			self.correct_sound = self.sounds[f'Ab{self.correct_octave}']
		elif self.correct_note == 'A#':
			self.correct_sound = self.sounds[f'Bb{self.correct_octave}']

	def play_correct_sound(self):
		self.channel.play(self.correct_sound)

	def start_new_round(self):
		self.round += 1
		if self.difficulty == 'medium':
			self.lives = 3

		#generate note
		self.generate_answer()

		#queue correct sound
		self.channel.queue(self.correct_sound)

		print(self.correct)

	def check_input(self):
		#draw keyboard
		for piano in [self.piano1, self.piano2, self.piano3, self.piano4, self.piano5]:
			
			key_pressed = piano.draw()
			
			if key_pressed != None:
				self.guesses += 1

				#get the note played
				if len(key_pressed[0:-4]) != 1:
					if self.level_data['notation'] == 'flat':
						note_guess = key_pressed[3:-4]
					elif self.level_data['notation'] == 'sharp':
						note_guess = key_pressed[0:-7]
					elif self.level_data['notation'] == 'both':
						note_guess = key_pressed[0:-7]
					else:
						note_guess = key_pressed[0:-4]
					note_sound = key_pressed[3:-4]
				else:
					note_guess = key_pressed[0:-4]
					note_sound = key_pressed[0:-4]

				#add octave to the end of each
				note_guess = f'{note_guess}{piano.octave}'
				note_sound = f'{note_sound}{piano.octave}'

				#play sound of the key pressed
				self.channel.play(self.sounds[f'{note_sound}'], 0, 1000)

				#check if the note was correct
				if note_guess == self.correct:
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

	def display_incorrect_message(self):
		self.game.Popup_Manager.popup = Popup_Message.Incorrect_Message(display=self.display, game=self.game, width=700, height=400, x=640, y=415, text=f'Incorrect, Correct Note: {self.correct}')
		self.game.current_state = 'Popup_Manager'

	def run(self):
		if self.new_round == True:
			self.start_new_round()
			self.new_round = False

		#draw instruction text on screen
		Draw_Text.draw_text(surface=self.display, font=self.fonts['instructions'], text='Play the note you hear in the correct octave.', text_colour=self.colours['Black'], align='centre', underline=0, x=640, y=250)

		#check for player input
		self.check_input()
