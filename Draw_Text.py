import pygame

pygame.font.init()

def draw_text(surface, font, text, text_colour, align, underline, x, y):
		img = font.render(text, True, text_colour)
		text_rect = img.get_rect()
		#alignment
		if align == 'centre':
			text_rect.center = (x, y)
		elif align == 'midleft':
			text_rect.midleft = (x, y)
		elif align == 'topleft':
			text_rect.topleft = (x, y)
		#underline
		if underline > 0:
			underline_width = text_rect.width * 1.2
			underline_rect = pygame.Rect(0, 0, underline_width, underline)
			underline_rect.center = (x, y+text_rect.height/2+underline)
			pygame.draw.rect(surface, (0,0,0), underline_rect)
		surface.blit(img, (text_rect.x, text_rect.y))
