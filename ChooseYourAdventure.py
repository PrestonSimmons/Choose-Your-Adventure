import random


class Pokemon:
    def __init__(self, name, level, type):
        self.name = name
        self.level = level
        self.type = type
        self.hp = level * 5
        self.moves = {
            "Tackle": {"type": "Normal", "power": 10},
            "Ember": {"type": "Fire", "power": 20},
            "Water Gun": {"type": "Water", "power": 20}
        }

    def __str__(self):
        return "{} (Level {}), Type: {}".format(self.name, self.level, self.type)

    def attack(self, move, opponent):
        if move in self.moves:
            damage = self.moves[move]["power"] * (self.level / 5)
            effectiveness = self.calculate_effectiveness(self.moves[move]["type"], opponent.type)
            damage *= effectiveness
            opponent.hp -= damage
            print("{} used {}! It's super effective!".format(self.name,
                                                             move) if effectiveness > 1 else "{} used {}!".format(
                self.name, move))
            print("{} dealt {} damage to {}.".format(self.name, damage, opponent.name))
            if opponent.hp <= 0:
                print("{} fainted!".format(opponent.name))
        else:
            print("{} doesn't know {}!".format(self.name, move))

    def calculate_effectiveness(self, move_type, opponent_type):
        effectiveness_chart = {
            "Normal": {"Normal": 1, "Fire": 1, "Water": 1},
            "Fire": {"Normal": 1, "Fire": 0.5, "Water": 2},
            "Water": {"Normal": 1, "Fire": 0.5, "Water": 0.5}
        }

        if move_type not in effectiveness_chart:
            print("Warning: Move type '{}' not found in effectiveness chart.".format(move_type))
            return 1

        if opponent_type not in effectiveness_chart[move_type]:
            print(
                "Warning: Opponent type '{}' not found in effectiveness chart for move type '{}'.".format(opponent_type,
                                                                                                          move_type))
            return 1

        return effectiveness_chart[move_type][opponent_type]


class Player:
    def __init__(self, name):
        self.name = name
        self.pokemon = []
        self.money = 100
        self.current_location = "Pallet Town"
        self.badges = []

    def move(self, direction):
        if direction in locations[self.current_location]["exits"]:
            self.current_location = locations[self.current_location]["exits"][direction]
            print("You move to", self.current_location)
            self.explore_location()
        else:
            print("You can't go that way.")

    def explore_location(self):
        location = locations[self.current_location]
        print("\n---")
        print("You are now in", self.current_location)
        print(location["description"])

        if "wild_pokemon" in location:
            wild_pokemon = location["wild_pokemon"]
            print("A wild", wild_pokemon.name, "appears!")
            self.battle(wild_pokemon)

    def battle(self, opponent):
        print("\n---")
        print("Battle begins!")
        print("Wild Pokémon", opponent.name, "appears!")

        if not self.pokemon:
            print("You have no Pokémon to battle with!")
            return

        player_pokemon = self.pokemon[0]
        opponent_pokemon = opponent
        print("Go, {}!".format(player_pokemon.name))

        while player_pokemon.hp > 0 and opponent_pokemon.hp > 0:
            print("\n---")
            print("Your Pokémon's HP:", player_pokemon.hp)
            print("Opponent's Pokémon's HP:", opponent_pokemon.hp)

            player_choice = input("Enter your move (Tackle/Ember/Water Gun): ").capitalize()
            if player_choice in ["Tackle", "Ember", "Water Gun"]:
                player_pokemon.attack(player_choice, opponent_pokemon)
                if opponent_pokemon.hp <= 0:
                    print("You defeated", opponent_pokemon.name + "!")
                    self.catch_pokemon(opponent_pokemon)
                    break
                opponent_choice = random.choice(list(opponent_pokemon.moves.keys()))
                opponent_pokemon.attack(opponent_choice, player_pokemon)
                if player_pokemon.hp <= 0:
                    print("Your Pokémon fainted.")
                    print("Game Over.")
                    break
            else:
                print("Invalid move. Choose Tackle, Ember, or Water Gun.")

    def catch_pokemon(self, pokemon):
        print("You threw a Pokéball!")
        wiggles = 0
        while wiggles < 3:
            if random.random() < 0.5:  # 50% chance of wiggling
                wiggles += 1
                print("The Pokéball wiggles...")
            else:
                print("The Pokémon broke free!")
        if wiggles == 3:
            self.pokemon.append(pokemon)
            print("Congratulations! You caught", pokemon.name + "!")
        else:
            print("Oh no! The Pokémon escaped!")

    def show_pokemon(self):
        if self.pokemon:
            print("Your Pokémon:")
            for pokemon in self.pokemon:
                print("- " + str(pokemon))
        else:
            print("You have no Pokémon.")

    def show_money(self):
        print("You have", self.money, "Pokédollars.")

    def visit_pokecenter(self):
        print("Welcome to the Pokémon Center!")
        print("Your Pokémon have been healed.")
        for pokemon in self.pokemon:
            pokemon.hp = pokemon.level * 5

    def visit_mart(self):
        print("Welcome to the Poké Mart!")
        print("Here's what we have for sale:")
        # Add item sale logic here


class GymLeader(Player):
    def __init__(self, name, pokemon):
        super().__init__(name)
        self.pokemon = [pokemon]

    def __str__(self):
        return "Gym Leader {} ({}): {}".format(self.name, self.current_location, self.pokemon[0].name)


locations = {
    "Pallet Town": {
        "description": "Your hometown.",
        "exits": {"north": "Route 1"}
    },
    "Route 1": {
        "description": "A quiet path winding through tall grass.",
        "exits": {"south": "Pallet Town"},
        "wild_pokemon": Pokemon("Pidgey", 3, "Flying")
    },
    "Pewter City Gym": {
        "description": "The Pewter City Gym, where Rock-type Pokémon trainers compete.",
        "exits": {"south": "Pewter City"},
        "gym_leader": GymLeader("Brock", Pokemon("Geodude", 10, "Rock"))
    }
}


def choose_starter():
    print("Welcome to the world of Pokémon!")
    print("I am Professor Oak. Before you embark on your journey, you need to choose your starter Pokémon.")
    print("You have three choices: Squirtle, Charmander, and Bulbasaur.")

    while True:
        choice = input("Enter the name of the Pokémon you want to choose: ").capitalize()
        if choice in ["Squirtle", "Charmander", "Bulbasaur"]:
            return choice
        else:
            print("Invalid choice. Please choose Squirtle, Charmander, or Bulbasaur.")


def main():
    starter_choice = choose_starter()
    player_name = input("Enter your name: ")
    player = Player(player_name)
    player.pokemon.append(Pokemon(starter_choice, 5,
                                  "Grass" if starter_choice == "Bulbasaur" else "Fire" if starter_choice == "Charmander" else "Water"))

    print("\nHello, {}! Your adventure begins in {} with your new {}.".format(player.name, player.current_location,
                                                                              starter_choice))

    while True:
        print("\n---")
        print("What would you like to do?")
        print("1. Move")
        print("2. Show Pokémon")
        print("3. Show money")
        print("4. Visit Pokémon Center")
        print("5. Visit Poké Mart")
        print("6. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            direction = input("Enter direction (north/south/east/west): ").lower()
            player.move(direction)
        elif choice == "2":
            player.show_pokemon()
        elif choice == "3":
            player.show_money()
        elif choice == "4":
            player.visit_pokecenter()
        elif choice == "5":
            player.visit_mart()
        elif choice == "6":
            print("Thanks for playing!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
