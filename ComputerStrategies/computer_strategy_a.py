from .computer_strategy import ComputerStrategy
import random

class ComputerStrategyA(ComputerStrategy):
	"""
	Implement the algorithm using the ComputerStrategy interface.
	"""

	def algorithm_execution(self, computer):
		render = computer.getRender()
		if computer.getRival().isAlive():
			rand = random.randint(0,100)
			if computer.getChampion().checkRadius(computer.getRival().getRect()):
				if rand<=computer.getHitChanges():
					computer.getRival()._onHit(computer.getChampion()._tryAttack())
				else:
					computer.getChampion()._tryAttack()
			if computer.getRival().getRect().left < computer.getChampion().getRect().left:
				rand2 = 1
			elif computer.getRival().getRect().left > computer.getChampion().getRect().left:
				rand2 = 2
			else:
				rand2 = 0

			if rand<=10:
				if rand2 == 1:
					computer.setDirection(-1)
					render = computer.getChampion()._tryMove(computer.getDirection())
				elif rand2 == 2:
					computer.setDirection(1)
					render = computer.getChampion()._tryMove(computer.getDirection())
				else:
					computer.setDirection(0)
					render = computer.getChampion()._onStand()
			else:
				if computer.getDirection() == 0:
					render = computer.getChampion()._onStand()
				else:
					render = computer.getChampion()._tryMove(computer.getDirection())

				render = computer.getChampion()._onAttack()
				render = computer.getChampion()._onHit()
				render = computer.getChampion()._onDie()
		else:
			render = computer.getChampion()._onStand()

		return render
