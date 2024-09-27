import tkinter as tk
from tkinter import messagebox

class Player:
    def __init__(self, name, total_invested, final_amount):
        self.name = name
        self.total_invested = total_invested
        self.final_amount = final_amount
        self.balance = final_amount - self.total_invested

def calculate_movements(players):
    debtors = []
    creditors = []

    # Calculate total balance
    total_balance = sum(player.balance for player in players)
    total_invested = sum(player.total_invested for player in players)
    total_final = sum(player.final_amount for player in players)

    print("Total balance:")
    print(total_balance)
    print("Total invested:")
    print(total_invested)
    print("Total final:")
    print(total_final)

    messagebox.showinfo("Resumen de Inversiones", f"Total invertido: ${total_invested:.2f}\nTotal final: ${total_final:.2f}\nBalance total: ${total_balance:.2f}")


    if abs(total_balance) > 0.01:  # Allowing a small epsilon for floating point errors
        messagebox.showerror("Error", "La suma de los balances no es cero. Verifica las inversiones y los montos finales.")
        return []

    # Separate players into debtors and creditors
    for player in players:
        if player.balance < -0.01:
            debtors.append(player)
        elif player.balance > 0.01:
            creditors.append(player)

    movements = []

    # Make movements between debtors and creditors
    while debtors and creditors:
        debtor = debtors[0]
        creditor = creditors[0]

        amount_to_transfer = min(-debtor.balance, creditor.balance)
        movements.append(f"{debtor.name} paga a {creditor.name} ${amount_to_transfer:.2f}")

        debtor.balance += amount_to_transfer
        creditor.balance -= amount_to_transfer

        if abs(debtor.balance) < 0.01:
            debtors.pop(0)
        if abs(creditor.balance) < 0.01:
            creditors.pop(0)

    return movements

# GUI Application
class PokerSettlementApp:
    def __init__(self, master):
        self.master = master
        master.title("Distribución de Ganancias del Poker")



        self.players = [
           
        ]

     

    

        # Player Input Frame
        self.input_frame = tk.Frame(master)
        self.input_frame.pack(pady=10)

        tk.Label(self.input_frame, text="Nombre:").grid(row=0, column=0, padx=5)
        tk.Label(self.input_frame, text="Total Invertido:").grid(row=0, column=1, padx=5)
        tk.Label(self.input_frame, text="Monto Final:").grid(row=0, column=2, padx=5)

        self.name_entry = tk.Entry(self.input_frame)
        self.name_entry.grid(row=1, column=0, padx=5)
        self.invested_entry = tk.Entry(self.input_frame)
        self.invested_entry.grid(row=1, column=1, padx=5)
        self.final_entry = tk.Entry(self.input_frame)
        self.final_entry.grid(row=1, column=2, padx=5)

        self.add_player_button = tk.Button(self.input_frame, text="Agregar Jugador", command=self.add_player)
        self.add_player_button.grid(row=1, column=3, padx=5)

        # Players List
        self.players_frame = tk.Frame(master)
        self.players_frame.pack(pady=10)

        self.players_listbox = tk.Listbox(self.players_frame, width=50)
        self.players_listbox.pack()

        # Calculate Movements Button
        self.calculate_button = tk.Button(master, text="Calcular Movimientos", command=self.calculate)
        self.calculate_button.pack(pady=10)

        # Results Frame
        self.results_frame = tk.Frame(master)
        self.results_frame.pack(pady=10)

        self.results_text = tk.Text(self.results_frame, width=60, height=15)
        self.results_text.pack()

        red = Player("Red", 16525, 23650)
        diego = Player("Diego", 16525, 10700)
        nou = Player("Nou", 16525, 57700)
        facu = Player("Facu", 48525, 10600)
        lolo = Player("Lolo", 16525, 13000)
        juanpa = Player("Juanpa", 16525, 22500)
        franco = Player("Franco", 32525, 7950)
        ivancho = Player("Ivancho", 16525, 67150)
        agus = Player("Agus", 16525, 0)
        chenzo = Player("Chenzo", 16525, 0)

        self.add_player(diego)
        self.add_player(red)
        self.add_player(nou)
        self.add_player(facu)
        self.add_player(lolo)
        self.add_player(juanpa)
        self.add_player(franco)
        self.add_player(ivancho)
        self.add_player(agus)
        self.add_player(chenzo)

        # red = Player("Red", 10000, 15000)
        # facu = Player("Facu", 10000, 5000)
        # self.add_player(red)
        # self.add_player(facu)



    def add_player(self):
        name = self.name_entry.get().strip()
        total_invested = self.invested_entry.get().strip()
        final_amount = self.final_entry.get().strip()

        if not name or not total_invested or not final_amount:
            messagebox.showwarning("Advertencia", "Por favor, completa todos los campos.")
            return

        try:
            total_invested = float(total_invested)
            final_amount = float(final_amount)
        except ValueError:
            messagebox.showerror("Error", "Los montos deben ser números.")
            return

        player = Player(name, total_invested, final_amount)
    
        self.players.append(player)

        self.players_listbox.insert(tk.END, f"{name}: Invertido ${total_invested:.2f}, Final ${final_amount:.2f}")

        # Clear input fields
        self.name_entry.delete(0, tk.END)
        self.invested_entry.delete(0, tk.END)
        self.final_entry.delete(0, tk.END)

    def add_player(self, player):
        self.players.append(player)
        self.players_listbox.insert(tk.END, f"{player.name}: Invertido ${player.total_invested:.2f}, Final ${player.final_amount:.2f}")

    def calculate(self):
        if not self.players:
            messagebox.showwarning("Advertencia", "No hay jugadores para calcular.")
            return

        movements = calculate_movements(self.players)

        self.results_text.delete(1.0, tk.END)

        total_invested = sum(player.total_invested for player in self.players)
        self.results_text.insert(tk.END, "Resumen de Inversiones:\n")
        for player in self.players:
            self.results_text.insert(tk.END, f"{player.name}: ${player.total_invested:.2f}\n")
        self.results_text.insert(tk.END, f"Total invertido: ${total_invested:.2f}\n\n")

        if movements:
            self.results_text.insert(tk.END, "Movimientos para balancear las cuentas:\n")
            for movement in movements:
                self.results_text.insert(tk.END, movement + "\n")
        else:
            self.results_text.insert(tk.END, "No se requieren movimientos.")

        # Reset players for next calculation
        self.players = []
        self.players_listbox.delete(0, tk.END)

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = PokerSettlementApp(root)
    root.mainloop()
