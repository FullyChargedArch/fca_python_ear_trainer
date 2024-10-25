import pygame
import random
import Buttons
import Draw_Text
import Popup_Message

class Chord_Recognition_Gameplay:
	def __init__(self, display, game, level_data):
		self.display = display
		self.game = game

		#init things
		self.fonts = self.game.fonts
		self.colours = self.game.colours
		self.sounds = self.game.sounds
		self.channel_0 = pygame.mixer.Channel(0)
		self.channel_1 = pygame.mixer.Channel(1)
		self.channel_2 = pygame.mixer.Channel(2)
		self.channels = [self.channel_0, self.channel_1, self.channel_2]

		#get level data
		self.level_data = level_data


		#gameplay variables
		self.round = 0
		self.score = 0
		self.guesses = 0
		self.lives = 3
		self.difficulty = self.game.Gaemplay.diffictuly
		self.correct = None
		self.new_round = True
		self.notes = ['C','Db','D','Eb','E','F','Gb','G','Ab','A','Bb','B']
		self.chords = self.level_data['chords']
		self.chord_tones = []
		self.pitches = []

		#set up buttons
		self.buttons = []
		for i in range(7):
			button = Buttons.Menu_Button(display=self.display, name=self.chords[i], text=self.chords[i], font=self.fonts['Button'], colour=self.colours['Mid'], highlight=self.colours['highlight'], width=150, height=150, x=160+160*i, y=415)
			self.buttons.append(button)

		for i in range(len(self.chords1)-1):
			self.chords[i].replace('C#','Db')
			self.chords[i].replace('D#', 'Eb')
			self.chords[i].replace('F#', 'Gb')
			self.chords[i].replace('G#', 'Ab')
			self.chords[i].replace('A#','Bb')


	def generate_answer(self):
		#pick a random chord from the key
		self.correct = self.chords[random.randint(0,len(self.chords)-1)]

		#generate pitches to play
		self.chord_tones = []
		self.pitches = []

		#get root note
		root_note = self.correct[0:-3]
		chord_type = self.correct.replace(root_note, '')

		#add to chord_tones
		self.chord_tones.append(root_note)
		root_index = self.notes.index(root_note)

		if chord_type == 'maj':
			self.chord_tones.append(self.notes[(root_index+4)//12])
			self.chord_tones.append(self.notes[(root_index+7)//12])
		elif chord_type == 'min':
			self.chord_tones.append(self.notes[(root_index+3)//12])
			self.chord_tones.append(self.notes[(root_index+7)//12])
		elif chord_type == 'dim':
			self.chord_tones.append(self.notes[(root_index+3)//12])
			self.chord_tones.append(self.notes[(root_index+6)//12])

		#add octaves to notes
		self.octave = random.randint(2,4)
		self.pitches.append(f'{self.chord_tones[0]}{self.octave}')

		for i in range(1, len(self.chord_tones)):
			if self.notes.index(self.chord_tones[i]) < self.notes.index(self.chord_tones[i-1]):
				self.octave += 1
			self.pitches.append(f'{self.chord_tones[i]}{self.octave}')


	def play_correct_sound(self):
		for i in range(len(self.pitches)):
			self.channels[i].play(self.sounds[self.pitches[i]])

	def start_new_round(self):
		self.round += 1
		if self.difficulty == 'medium':
			self.lives = 3

		#generate note
		self.generate_answer()

		#queue correct sound
		self.play_correct_sound()

		print(self.correct)

	def check_input(self):
		for button in self.buttons:
			if button.draw() == True:
				self.guesses += 1
				if button.name == self.correct_interval:
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
		self.game.Popup_Manager.popup = Popup_Message.Incorrect_Message(display=self.display, game=self.game, width=700, height=400, x=640, y=415, text=f'Incorrect, Correct Chord: {self.correct}')
		self.game.current_state = 'Popup_Manager'

	def run(self):
		if self.new_round == True:
			self.start_new_round()
			self.new_round = False

		#draw instruction text on screen
		Draw_Text.draw_text(surface=self.display, font=self.fonts['instructions'], text='Choose the chord you hear.', text_colour=self.colours['Black'], align='centre', underline=0, x=640, y=300)

		#check for player input
		self.check_input()