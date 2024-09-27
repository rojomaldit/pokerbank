class Player:
    def __init__(self, name, total_invested, final_amount):
        self.name = name
        self.total_invested = total_invested
        self.final_amount = final_amount
        self.balance = final_amount - self.total_invested 

def calculate_movements(players):
    debtors = []
    creditors = []

    # Separate players into debtors and creditors
    for player in players:
        if player.balance < 0:
            debtors.append(player)
        elif player.balance > 0:
            creditors.append(player)

    movements = []

    # Make movements between debtors and creditors
    while debtors and creditors:
        debtor = debtors[0]
        creditor = creditors[0]

        amount_to_transfer = min(-debtor.balance, creditor.balance)
        movements.append(f"{debtor.name} pays {creditor.name} ${amount_to_transfer:.2f}")

        debtor.balance += amount_to_transfer
        creditor.balance -= amount_to_transfer

        if debtor.balance == 0:
            debtors.pop(0)
        if creditor.balance == 0:
            creditors.pop(0)

    return movements

# Example usage
players = []

while True:
    name = input("Player's name (or 'end' to finish): ")
    if name.lower() == 'end':
        break
    total_invested = float(input(f"Total invested for {name}: "))
    final_amount = float(input(f"Final amount of {name}: "))

    players.append(Player(name, total_invested, final_amount))

movements = calculate_movements(players)

total_invested = 0
for player in players:
    print(f"{player.name}: ${player.total_invested:.2f}")
    total_invested += player.total_invested
print(f"Total invested: ${total_invested:.2f}")
print("\nMinimum movements to balance the accounts:")
for movement in movements:
    print(movement)