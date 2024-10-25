import pygame
import random
import Buttons
import Draw_Text
import Popup_Message


#
#
#
#
#
#
# intervals seem to be correct now
#
#
#
#

class Interval_Recognition_Gameplay:
	def __init__(self, display, game, level_data):
		self.display = display
		self.game = game

		#init things
		self.fonts = self.game.fonts
		self.colours = self.game.colours
		self.sounds = self.game.sounds
		self.channel_0 = pygame.mixer.Channel(0)
		self.channel_1 = pygame.mixer.Channel(1)

		#get level data
		self.level_data = level_data

		#gameplay variables
		self.round = 0
		self.score = 0
		self.guesses = 0
		self.lives = 3
		self.difficulty = self.game.Gameplay.difficulty
		self.correct = None 
		self.new_round = True
		self.notes = ['C','Db','D','Eb','E','F','Gb','G','Ab','A','Bb','B']
		self.interval_dict = {'unison': 0, 'min2': 1, 'maj2': 2, 'min3': 3, 'maj3': 4, 'p4': 5, '#4/b5': 6, 'p5': 7, 'min6': 8, 'maj6': 9, 'min7': 10, 'maj7': 11, 'oct': 12, 'min9': 13, 'maj9': 14, 'min10': 15, 'maj10': 16, 'p11': 17, '#11/b12': 18, 'p12': 19, 'min13': 20, 'maj13': 21, 'min14': 22, 'maj14': 23, '2oct': 24}
		self.intervals = self.level_data['intervals']

		if self.level_data['buttons'] == '1st oct':
			self.set_up_1st_oct_buttons()
		elif self.level_data['buttons'] == '2nd oct':
			self.set_up_2nd_oct_buttons()
		elif self.level_data['buttons'] == 'both oct':
			self.set_up_both_oct_buttons()
		

	def set_up_1st_oct_buttons(self):
		#create buttons
		self.unison = Buttons.Menu_Button(display=self.display, name='unison', text='unison', font=self.fonts['button'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=120, height=120, x=185, y=360)
		self.maj2 = Buttons.Menu_Button(display=self.display, name='maj2', text='maj2', font=self.fonts['button'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=120, height=120, x=315, y=360)
		self.maj3 = Buttons.Menu_Button(display=self.display, name='maj3', text='maj3', font=self.fonts['button'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=120, height=120, x=445, y=360)
		self.p4 = Buttons.Menu_Button(display=self.display, name='p4', text='p4', font=self.fonts['button'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=120, height=120, x=575, y=360)
		self.p5 = Buttons.Menu_Button(display=self.display, name='p5', text='p5', font=self.fonts['button'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=120, height=120, x=705, y=360)
		self.maj6 = Buttons.Menu_Button(display=self.display, name='maj6', text='maj6', font=self.fonts['button'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=120, height=120, x=835, y=360)
		self.maj7 = Buttons.Menu_Button(display=self.display, name='maj7', text='maj7', font=self.fonts['button'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=120, height=120, x=965, y=360)
		self.oct = Buttons.Menu_Button(display=self.display, name='oct', text='oct', font=self.fonts['button'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=120, height=120, x=1095, y=360)

		self.min2 = Buttons.Menu_Button(display=self.display, name='min2', text='min2', font=self.fonts['button'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=120, height=120, x=250, y=490)
		self.min3 = Buttons.Menu_Button(display=self.display, name='min3', text='min3', font=self.fonts['button'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=120, height=120, x=380, y=490)
		self.tritone = Buttons.Menu_Button(display=self.display, name='#4/b5', text='#4/b5', font=self.fonts['button'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=120, height=120, x=640, y=490)
		self.min6 = Buttons.Menu_Button(display=self.display, name='min6', text='min6', font=self.fonts['button'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=120, height=120, x=770, y=490)
		self.min7 = Buttons.Menu_Button(display=self.display, name='min7', text='min7', font=self.fonts['button'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=120, height=120, x=900, y=490)

		self.buttons = [self.unison, self.min2, self.maj2, self.min3, self.maj3, self.p4, self.tritone, self.p5, self.min6, self.maj6, self.min7, self.maj7, self.oct]

	def set_up_2nd_oct_buttons(self):
		#create buttons
		self.oct = Buttons.Menu_Button(display=self.display, name='oct', text='oct', font=self.fonts['button'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=120, height=120, x=185, y=360)
		self.maj9 = Buttons.Menu_Button(display=self.display, name='maj9', text='maj9', font=self.fonts['button'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=120, height=120, x=315, y=360)
		self.maj10 = Buttons.Menu_Button(display=self.display, name='maj10', text='maj10', font=self.fonts['button'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=120, height=120, x=445, y=360)
		self.p11 = Buttons.Menu_Button(display=self.display, name='p11', text='p11', font=self.fonts['button'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=120, height=120, x=575, y=360)
		self.p12 = Buttons.Menu_Button(display=self.display, name='p12', text='p12', font=self.fonts['button'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=120, height=120, x=705, y=360)
		self.maj13 = Buttons.Menu_Button(display=self.display, name='maj13', text='maj13', font=self.fonts['button'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=120, height=120, x=835, y=360)
		self.maj14 = Buttons.Menu_Button(display=self.display, name='maj14', text='maj14', font=self.fonts['button'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=120, height=120, x=965, y=360)
		self.oct2 = Buttons.Menu_Button(display=self.display, name='2oct', text='2oct', font=self.fonts['button'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=120, height=120, x=1095, y=360)

		self.min9 = Buttons.Menu_Button(display=self.display, name='min9', text='min9', font=self.fonts['button'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=120, height=120, x=250, y=490)
		self.min10 = Buttons.Menu_Button(display=self.display, name='min10', text='min10', font=self.fonts['button'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=120, height=120, x=380, y=490)
		self.tritone2 = Buttons.Menu_Button(display=self.display, name='#11/b12', text='#11/b12', font=self.fonts['button'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=120, height=120, x=640, y=490)
		self.min13 = Buttons.Menu_Button(display=self.display, name='min13', text='min13', font=self.fonts['button'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=120, height=120, x=770, y=490)
		self.min14 = Buttons.Menu_Button(display=self.display, name='min14', text='min14', font=self.fonts['button'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=120, height=120, x=900, y=490)

		self.buttons = [self.oct, self.min9, self.maj9, self.min10, self.maj10, self.p11, self.tritone2, self.p12, self.min13, self.maj13, self.min14, self.maj14, self.oct2]

	def set_up_both_oct_buttons(self):
		#1st oct
		self.unison = Buttons.Menu_Button(display=self.display, name='unison', text='unison', font=self.fonts['button_small'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=70, height=70, x=80, y=400)
		self.maj2 = Buttons.Menu_Button(display=self.display, name='maj2', text='maj2', font=self.fonts['button_small'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=70, height=70, x=160, y=400)
		self.maj3 = Buttons.Menu_Button(display=self.display, name='maj3', text='maj3', font=self.fonts['button_small'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=70, height=70, x=240, y=400)
		self.p4 = Buttons.Menu_Button(display=self.display, name='p4', text='p4', font=self.fonts['button_small'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=70, height=70, x=320, y=400)
		self.p5 = Buttons.Menu_Button(display=self.display, name='p5', text='p5', font=self.fonts['button_small'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=70, height=70, x=400, y=400)
		self.maj6 = Buttons.Menu_Button(display=self.display, name='maj6', text='maj6', font=self.fonts['button_small'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=70, height=70, x=480, y=400)
		self.maj7 = Buttons.Menu_Button(display=self.display, name='maj7', text='maj7', font=self.fonts['button_small'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=70, height=70, x=560, y=400)
		self.oct = Buttons.Menu_Button(display=self.display, name='oct', text='oct', font=self.fonts['button_small'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=70, height=70, x=640, y=400)

		self.min2 = Buttons.Menu_Button(display=self.display, name='min2', text='min2', font=self.fonts['button_small'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=70, height=70, x=120, y=480)
		self.min3 = Buttons.Menu_Button(display=self.display, name='min3', text='min3', font=self.fonts['button_small'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=70, height=70, x=200, y=480)
		self.tritone = Buttons.Menu_Button(display=self.display, name='#4/b5', text='#4/b5', font=self.fonts['button_small'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=70, height=70, x=360, y=480)
		self.min6 = Buttons.Menu_Button(display=self.display, name='min6', text='min6', font=self.fonts['button_small'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=70, height=70, x=440, y=480)
		self.min7 = Buttons.Menu_Button(display=self.display, name='min7', text='min7', font=self.fonts['button_small'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=70, height=70, x=520, y=480)

		#2nd oct
		self.maj9 = Buttons.Menu_Button(display=self.display, name='maj9', text='maj9', font=self.fonts['button_small'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=70, height=70, x=720, y=400)
		self.maj10 = Buttons.Menu_Button(display=self.display, name='maj10', text='maj10', font=self.fonts['button_small'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=70, height=70, x=800, y=400)
		self.p11 = Buttons.Menu_Button(display=self.display, name='p11', text='p11', font=self.fonts['button_small'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=70, height=70, x=880, y=400)
		self.p12 = Buttons.Menu_Button(display=self.display, name='p12', text='p12', font=self.fonts['button_small'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=70, height=70, x=960, y=400)
		self.maj13 = Buttons.Menu_Button(display=self.display, name='maj13', text='maj13', font=self.fonts['button_small'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=70, height=70, x=1040, y=400)
		self.maj14 = Buttons.Menu_Button(display=self.display, name='maj14', text='maj14', font=self.fonts['button_small'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=70, height=70, x=1120, y=400)
		self.oct2 = Buttons.Menu_Button(display=self.display, name='2oct', text='2oct', font=self.fonts['button_small'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=70, height=70, x=1200, y=400)

		self.min9 = Buttons.Menu_Button(display=self.display, name='min9', text='min9', font=self.fonts['button_small'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=70, height=70, x=680, y=480)
		self.min10 = Buttons.Menu_Button(display=self.display, name='min10', text='min10', font=self.fonts['button_small'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=70, height=70, x=760, y=480)
		self.tritone2 = Buttons.Menu_Button(display=self.display, name='#11/b12', text='#11/b12', font=self.fonts['button_small'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=70, height=70, x=920, y=480)
		self.min13 = Buttons.Menu_Button(display=self.display, name='min13', text='min13', font=self.fonts['button_small'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=70, height=70, x=1000, y=480)
		self.min14 = Buttons.Menu_Button(display=self.display, name='min14', text='min14', font=self.fonts['button_small'], colour=self.colours['Mid'], highlight=self.colours['Highlight'], width=70, height=70, x=1080, y=480)

		self.buttons = [self.unison, self.min2, self.maj2, self.min3, self.maj3, self.p4, self.tritone, self.p5, self.min6, self.maj6, self.min7, self.maj7, self.oct, self.min9, self.maj9, self.min10, self.maj10, self.p11, self.tritone2, self.p12, self.min13, self.maj13, self.min14, self.maj14, self.oct2]


	def generate_answer(self):
		self.correct_interval = self.intervals[random.randint(0, len(self.intervals)-1)]
		self.semitone_difference = self.interval_dict[self.correct_interval]

		#generate notes
		note_index = random.randint(0,11)
		
		note1 = self.notes[note_index]
		octave1 = random.randint(2,4)

		note2 = self.notes[(note_index+self.semitone_difference)%12]
		octave2 = octave1 + self.semitone_difference//12
		
		if self.notes.index(note2) < self.notes.index(note1):
			octave2 += 1

		if octave2 == 6:
			octave1 -= 1
			octave2 -= 1

		self.pitch1 = f'{note1}{octave1}'
		self.pitch2 = f'{note2}{octave2}'

	def play_correct_sound(self):
		if self.level_data['type'] == 'jump':
			self.channel_0.play(self.sounds[self.pitch1], 0, 500)
			self.channel_0.queue(self.sounds[self.pitch2])
		elif self.level_data['type'] == 'together':
			self.channel_0.play(self.sounds[self.pitch1])
			self.channel_1.play(self.sounds[self.pitch2])

	def start_new_round(self):
		self.round += 1
		if self.difficulty == 'medium':
			self.lives = 3

		#generate note
		self.generate_answer()

		#queue correct sound
		self.play_correct_sound()

		print(self.pitch1, self.pitch2, self.correct_interval)
	
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
		self.game.Popup_Manager.popup = Popup_Message.Incorrect_Message(display=self.display, game=self.game, width=700, height=400, x=640, y=415, text=f'Incorrect, Correct Note: {self.correct_interval}')
		self.game.current_state = 'Popup_Manager'
	
	def run(self):
		if self.new_round == True:
			self.start_new_round()
			self.new_round = False

		#draw instruction text on screen
		if self.level_data['buttons'] == 'both oct':
			Draw_Text.draw_text(surface=self.display, font=self.fonts['instructions'], text='Choose the interval you hear.', text_colour=self.colours['Black'], align='centre', underline=0, x=640, y=300)
		else:
			Draw_Text.draw_text(surface=self.display, font=self.fonts['instructions'], text='Choose the interval you hear.', text_colour=self.colours['Black'], align='centre', underline=0, x=640, y=250)

		#check for player input
		self.check_input()