import pygame
import csv
import random
from pygame.locals import *
from singleton import Singleton
from champion_factory import ChampionFactory
from weapon_factory import WeaponFactory
from player import Player
from computer import Computer

SCREENRECT    		= Rect(0, 0, 640, 480)
USE_PYGAME_CLOCK	= True
PYGAME_FPS			= 50
WEAPONS_FILE		= "weapons.txt"

class GameManager(metaclass=Singleton):
	def __init__(self):
		self._running				= True
		self._display_surf			= None
		self._surface				= None
		self._player				= None
		self._computer				= None
		self._random_weapon			= None
		self._weapons				= []
		self._updates				= []
		self._event					= False
		self.size					= self.weight, self.height = 800, 600
		self._ground				= [[450,600,-30,705],[365,400,-15,97],[300,330,155,265],[365,400,315,462],[375,400,565,675]]
		self._random_weapon_rect	= Rect(((self._ground[0][0]/2)+150, self._ground[0][0]+60), (40, 40))
		self._player_weapon_rect	= Rect((0, 30), (40, 40))
		self._comp_weapon_rect		= Rect((self.size[0]-45,30), (40, 40))
		self._player_rect			= Rect((0,self._ground[0][0]),(120, 100))
		self._comp_rect				= Rect((self._ground[0][1],self._ground[0][0]),(120, 100))

	def init_weapons(self):
		self._weapons = []
		weapfactory = WeaponFactory()
		try:
			with open(WEAPONS_FILE) as f:
				reader = csv.reader(f)
				self._weapons = [weapfactory.create_weapon(col1, int(col2), int(col3), [champion.capitalize() for champion in col4.split()]) for col1, col2, col3, col4 in reader]
		except Exception as exp:
			print(exp)

	def randomWeapon(self):
		if self._random_weapon is None:
			rand = random.randint(0,1000)
			if rand <= 10:
				rand = random.randint(0,len(self._weapons)-1)
				self._random_weapon = self._weapons[rand]
				self._random_weapon.setPosition(self._random_weapon_rect)
				self._updates.append(self._random_weapon.update())
		else:
			rand = random.randint(0,5000)
			if rand <= 10:
				self._random_weapon=None
			else:
				self._updates.append(self._random_weapon.update())

	def checkWeaponColission(self):
		if self._random_weapon is not None:
			if self._player.getChampion().checkColission(self._random_weapon.getPosition()):
				if self._player.getChampion().setWeapon(self._random_weapon):
					self._player.getChampion().getWeapon().setPosition(self._player_weapon_rect)
				return True
			elif self._computer.getChampion().checkColission(self._random_weapon.getPosition()):
				if self._computer.getChampion().setWeapon(self._random_weapon):
					self._computer.getChampion().getWeapon().setPosition(self._comp_weapon_rect)
				return True
		return False

	def on_init(self):
		pygame.init()
		pygame.display.set_caption('Samurai VS. Viking')
		pygame.mouse.set_visible(0)

		infoObject = pygame.display.Info()
		# self.size = infoObject.current_w, infoObject.current_h
		SCREENRECT = Rect(0,0,self.weight,self.height)
		self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)## | pygame.FULLSCREEN)
		self._surface = pygame.image.load('background.jpg')
		self._surface = pygame.transform.scale(self._surface, self.size).convert()
		self._running = True

	def on_event(self, event):
		if (event.type == pygame.KEYDOWN) or (event.type == pygame.QUIT):
			if (event.type == pygame.QUIT) or (event.key == pygame.K_ESCAPE):
				self._running = False

		keystate = pygame.key.get_pressed()
		self._updates.append(self._player.update(keystate=keystate))


	def on_loop(self):
		self.randomWeapon()
		if self.checkWeaponColission():
			self._random_weapon = None
		if not self._computer.getChampion().isAlive() or self._player.getChampion().isAlive():
			self._updates.append(self._computer.update())
		self._updates.append(self._player.update())
		if self._computer.getChampion().isAlive() and not self._player.getChampion().isAlive():
			self._updates.append(self._computer.update())

		#Update collected weapons locations
		if self._player.getChampion().getWeapon() is not None:
			self._updates.append(self._player.getChampion().getWeapon().update())
		if self._computer.getChampion().getWeapon() is not None:
			self._updates.append(self._computer.getChampion().getWeapon().update())

	def on_render(self):
		self._display_surf.blit(self._surface,(0,0))
		for update in self._updates:
			self._display_surf.blit(update[0], update[1])
		self._updates = []
		pygame.draw.rect(self._display_surf,(255,0,0),(10,10,100,15))
		if self._player.getChampion().getLife()>0:
			pygame.draw.rect(self._display_surf,(0,255,0),(10,10,100-((100/self._player.getChampion().getHealth())*(self._player.getChampion().getHealth() - self._player.getChampion().getLife())),15))
		pygame.draw.rect(self._display_surf,(255,0,0),(self.size[0]-110,10,100,15))
		if self._computer.getChampion().getLife()>0:
			pygame.draw.rect(self._display_surf,(0,255,0),(self.size[0]-110,10,100-((100/self._computer.getChampion().getHealth())*(self._computer.getChampion().getHealth() - self._computer.getChampion().getLife())),15))
		pygame.display.update()

	def on_cleanup(self):
		pygame.quit()

	def on_execute(self):
		if self.on_init() == False:
			self._running = False

		self.init_weapons()
		# player_rect = Rect((0,self._ground[0][0]),(120, 100))
		# comp_rect = Rect((self._ground[0][1],self._ground[0][0]),(120, 100))

		champfactory = ChampionFactory()
		weapfactory = WeaponFactory()

		viking = champfactory.create_champion('viking', self._comp_rect, self._ground)
		samurai = champfactory.create_champion('samurai', self._player_rect, self._ground)

		self._computer = Computer(champion=viking)
		self._player = Player(name="Player1", champion=samurai)
		self._computer.setRival(self._player.getChampion())
		self._player.setRival(self._computer.getChampion())
		# self._computer.setWeapon(Sword("Basic Sword", 1, 10))

		clock = pygame.time.Clock()
		while(self._running):
			if USE_PYGAME_CLOCK:
				clock.tick(PYGAME_FPS)
			else:
				clock.tick()
			self.on_loop()
			self.on_render()

			self._event  = False
			for event in pygame.event.get():
				self.on_event(event)

		self.on_cleanup()

if __name__ == "__main__" :
	gameManager = GameManager()
	gameManager.on_execute()
