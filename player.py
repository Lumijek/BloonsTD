class Player:
    def __init__(self, health, money, eco):
        self.health = health
        self.money = money
        self.eco = eco

    def change_eco(self, ech_change):
        self.eco += eco_increase

    def change_money(self, money_change):
        self.money += money_change

    def change_health(self, health_change):
        self.health += health_change

    def get_eco(self):
        return self.eco

    def get_money(self):
        return self.money

    def get_health(self):
        return self.health
