#Thats my SoftServe Project

TBD:
1)Menu:
	1-1)Save\Load Feature upd: later using db

	1-2)Make Statistics count something and not just show unconnected graph upd: Stats must interconnect with points for each player, and show the top 10 runs

	1-3)Options:
		1-3-1)Add some more options?
		1-3-2)Create Apply button for Resolution upd: Done
		1-3-3)Do so that options window resolution btn would change the real window size (global for the get() function)

	1-4)Create_char:
		1-4-1)FILLER label under racial menu must get data from db according to the chosen race
		1-4-2)Stats labels must take right values (needs tinkering)
		1-4-3)Base Stats are 0, possible alteration points = 30
			1-4-3-1)Do so that 30 points would automatically count down when altering stats

2)Game:
	2-1)Prescribe stat modificators to Races in player creation screen:
		2-1-1)Main stats:
					Strength, Perception, Endurance, Charisma, Intelligence, Agility, Luck, Hpmodificator
					S - for your dmg multiplier
					P - for Hit chance
					E - for how many times you can Hit
					C - for eny debuff on stats (for now)
					I - hp multiplier (for now)
					A - your chance of block
					L - crit chance (crit is static 100% of your dmg)
					Hpmod - base hp + racial bonus (cannot be altered via stats screen)

	2-2)Add permanent stats upd:Idea done, needs realization

	2-3)Create hp\dmg attributes upd: base hp is 100, base dmg is 20
		2-3-1)Hp reduced by eny and replenished only 20% each round (needs realization)

	2-4)Add imagery and fluff stuff upd: later, needs a base first

	2-5)Create an enemy randomizer with similar rules

	2-6)Create battle calculations

	2-7)Reward player (points for now, calculated by how many eny`s will be killed ny run)

	*Future upd

	Armor\weapon modifiers
	Create some graphical fidelity on battles\monsters\items
	Create chance of drop for eny
	Create multiple against one battles
