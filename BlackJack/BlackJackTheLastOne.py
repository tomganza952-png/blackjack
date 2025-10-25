import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk
import ctypes
import os

ctypes.windll.shcore.SetProcessDpiAwareness(1)


#-------------------------------------------------------variabili----------------------------------------------------------

money = [500,500,500]
totoff = [0,0,0]
giocatori = ["","",""]
turno = 0
somma_carte = [0,0,0,0]
ix_carta = 0
activate_fast_cmd = False
coloreT = "green"
name = ["","",""]
carte_visualizzate = [[],[],[],[]]
lisa_carte = []
assi = [0,0,0,0]
nummazzi = 2
puntata = [0,0,0]
puntata_min = 10
puntata_max = 10000
molt = 2
difficolta = "medio"
round_n = 0
code = 0

#-------------------------------------------------------file----------------------------------------------------------


save_file_name = "sava_game.txt"
desktop_path = os.path.join(os.environ['USERPROFILE'], "OneDrive", "Desktop")
print(desktop_path)

for root, dirs, files in os.walk(desktop_path):
    print("Controllo cartella:", files)
    if save_file_name in files:
        save_game = os.path.join(root, save_file_name)
        print("File di salvataggio trovato:", save_game)
        break
else:
    print("File non trovato")


rules_file_name = "regole.txt"

for root, dirs, files in os.walk(desktop_path):
    print("Controllo cartella:", files)
    if rules_file_name in files:
        rule = os.path.join(root, rules_file_name)
        print("File di salvataggio trovato:", rule)
        with open(rule, "r", encoding="utf-8") as file:
            regole = file.read()

        break
else:
    print("File non trovato")


dorso_mazzo_roteato = "dorso_mazzo_ruotato.jpg"
for root, dirs, files in os.walk(desktop_path):
    print("Controllo cartella:", files)
    if dorso_mazzo_roteato in files:
        img1 = os.path.join(root, dorso_mazzo_roteato)
        print("File di salvataggio trovato:", dorso_mazzo_roteato)
        dorso_mazzo_roteato = Image.open(img1)
        dorso_mazzo_roteato = dorso_mazzo_roteato.resize((150, 100))
        break
else:
    print("File non trovato")



dorso_mazzo = "dorso_mazzo.jpg"
for root, dirs, files in os.walk(desktop_path):
    print("Controllo cartella:", files)
    if dorso_mazzo in files:
        img1 = os.path.join(root, dorso_mazzo)
        print("File di salvataggio trovato:", dorso_mazzo)
        dorso_mazzo = Image.open(img1)
        dorso_mazzo = dorso_mazzo.resize((100, 150))
        break
else:
    print("File non trovato")



#-------------------------------------------------------finestra principale----------------------------------------------------------

root = tk.Tk()
root.geometry("1000x800")
root.title("Blackjack")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

dorso_mazzo_roteato_tk = ImageTk.PhotoImage(dorso_mazzo_roteato)
dorso_mazzo_tk = ImageTk.PhotoImage(dorso_mazzo)

def solo_numeri(char):
    return char.isdigit() or char == ""
        
vcmd = (root.register(solo_numeri), "%P")


def massimo_char(valore):
    return len(valore) <= 12

vcmd2 = (root.register(massimo_char), "%P")


class Carta:
    def __init__(self, valore, seme):
        self.valore = valore
        self.seme = seme

    def __str__(self):
        return f"{self.valore} {self.seme}"


class Mazzo:
    def __init__(self, mazzi):
        semi = ["♤", "♡", "◇", "♧"]
        self.Nummazzi = mazzi
        self.carte = []

        for _ in range(self.Nummazzi):
            for v in range(2, 11):  
                for s in semi:
                    self.carte.append(Carta(v, s))
        figure = ["J","Q","K"]
        for _ in range(self.Nummazzi):
            for v in figure:
                for s in semi:
                    self.carte.append(Carta(v, s))
        
        for _ in range(self.Nummazzi):
            for s in semi:
                self.carte.append(Carta("A", s))
                    

        random.shuffle(self.carte)

    def __str__(self):
        return ", ".join(str(carta) for carta in self.carte)

    def pesca(self):
        if self.carte:
            carta = self.carte.pop(0)
            return carta.valore, carta.seme
        else:
            global semi 
            messagebox.showinfo("Mazzo e finito ne verrano creti nuovi")
            for _ in range(self.Nummazzi):
                for v in range(2, 11):  
                    for s in semi:
                        self.carte.append(Carta(v, s))
            figure = ["J","Q","K"]
            for _ in range(self.Nummazzi):
                for v in figure:
                    for s in semi:
                        self.carte.append(Carta(v, s))
            
            for _ in range(self.Nummazzi):
                for s in semi:
                    self.carte.append(Carta("A", s))
            random.shuffle(self.carte)
            carta = self.carte.pop(0)
            return carta.valore, carta.seme
        return None, None




def distribuisci_carta_coord(x, y, girarsi, seme, realvalore, plrCarta):
    
    carta_duplicata = tk.Label(canvas, width=14, height=8, bg="white", bd=2, relief="solid", text=f"{realvalore} {seme}")
    carta_id = canvas.create_window(800, 150, window=carta_duplicata)

    dorso_duplicato = tk.Label(canvas, image=dorso_mazzo_tk, bd=0)
    dorso_id = canvas.create_window(800, 150, window=dorso_duplicato)
    
    carta_duplicata.dorso_id = dorso_id
    carta_duplicata.girarsi = girarsi

    carte_visualizzate[plrCarta].append({
        "id": carta_id,
        "widget": carta_duplicata,
        "dorso": dorso_id
    })

    # Avvia animazione
    anima_diagonale(800, 150, carta_id, dorso_id, carta_duplicata, x, y, 0)

def anima_diagonale(start_x, start_y, carta_id, dorso_id, carta_label, target_x, target_y, passo):
    passi_totali = 20
    if passo <= passi_totali:
        # Calcola posizione interpolata in base al passo
        progress = passo / passi_totali
        x = start_x + (target_x - start_x) * progress
        y = start_y + (target_y - start_y) * progress

        # Ottieni posizione corrente della carta
        current_coords = canvas.coords(carta_id)
        if current_coords:
            dx = x - current_coords[0]
            dy = y - current_coords[1]
            canvas.move(carta_id, dx, dy)
            canvas.move(dorso_id, dx, dy)

        root.after(20, lambda: anima_diagonale(start_x, start_y, carta_id, dorso_id, carta_label, target_x, target_y, passo + 1))
    else:
        # Alla fine dell'animazione
        if carta_label.girarsi:
            canvas.delete(dorso_id)






def realV (valore):
    if valore == "J" or valore == "Q" or valore == "K" :
        realvalore = 10
    elif valore == "A" :
        realvalore = 11
    else:
        realvalore = valore
    return realvalore



def dare_carte():
    global lista_carte
    try:
        for i in range(4):
            somma_carte[i] = 0
            assi[i] = 0
        for z in carte_visualizzate:
            for carta in z:
                canvas.delete(carta["id"])
        for z in carte_visualizzate:
            z.clear()

        x_base = [175, 1075, 1575, 1100]
        y_base = [700, 800, 800, 175]

        lista_carte = []


        for turno in range(2):
            for e in range (4):
                girarsi = not (e == 3 and turno == 0)
                valore, seme = mazzo.pesca()
                if valore == "A":
                    assi[e] += 1
                realvalore = realV(valore)
                x = x_base[e] + turno * 140
                y = y_base[e]
                lista_carte.append((x, y, girarsi, seme, valore, realvalore, e))
        print (lista_carte)


        def distribuisci_sequenza(index=0):
            if index < len(lista_carte):
                x, y, girarsi, seme, realvalore, valore, e = lista_carte[index]
                distribuisci_carta_coord(x, y, girarsi, seme, realvalore, e)
                somma_carte[e] += valore
                root.after(500, lambda: distribuisci_sequenza(index + 1))
                canvas.itemconfig(count_id, text = f"{somma_carte[0]}")

        distribuisci_sequenza()
    except TypeError:
        pass


def stai():
    global giocatori, turno, somma_carte, puntata
    if somma_carte[turno] > 21:
        fine_turno(giocatori[turno], f"sballato, {giocatori[turno]} ha perso: {puntata[turno]}")
    elif somma_carte[turno] == 21:
        fine_turno(giocatori[turno], f"BlackJack!!, {giocatori[turno]} ha vinto: {puntata[turno]}")
    else:
        fine_turno(giocatori[turno], f", se il banco fa meno di: {somma_carte[turno]} allora {giocatori[turno]} vince: {puntata[turno]}")



def mostra_c_banco():
    carta = carte_visualizzate[3][0]
    canvas.delete(carta["dorso"])
    carta["dorso"] = None

def fine_round ():
    global bt_chiedi_id, bt_stai_id, bt_raddoppia_id, turno, somma_carte, activate_fast_cmd, round_n
    activate_fast_cmd = False
    mostra_c_banco()
    if somma_carte[3] > 21 and assi[3] >= 1:
        somma_carte[3] -= 10
        assi[3] -= 1
    x = somma_carte[3]
    if somma_carte[3] < 17:
        while x < 17:
            print (f"carta banco {x}")
            x = carta_banco()
            canvas.itemconfigure(count_id_banco, state="normal", text = x)
        messagebox.showinfo("banco", f"il banco ha fatto: {x}")
        dopo_fineR()
    else:
        messagebox.showinfo("banco", f"il banco ha fatto: {somma_carte[3]}")
        dopo_fineR()
    
    
def dopo_fineR():
    global turno, round_n, giocatori
    cosa1, cosa2, cosa3 = conteggi_vincite()
    turno = 0
    round_n += 1
    aggiorna_gui1()
    canvas2.itemconfigure(lb_scritta7, state="normal", text = f"{giocatori[0]} ha {cosa1}")
    canvas2.itemconfigure(lb_scritta8, state="normal", text = f"{giocatori[1]} ha {cosa2}")
    canvas2.itemconfigure(lb_scritta9, state="normal", text = f"{giocatori[2]} ha {cosa3}")
    canvas2.itemconfigure(btn_salvataggio_id, state="normal")
    show_frame(frame_punt)
    




def conteggi_vincite():
    global puntata, money, molt
    cosa = [0,0,0]
    for i in range(3):
        if  (somma_carte[3] > 21 and somma_carte[i] > 21) or somma_carte[i] == somma_carte[3]:
            cosa[i] = f"pareggiato: riprende la puntata"
        elif (somma_carte[i] > 21 and somma_carte[3] <= 21) or (somma_carte[3] > somma_carte[i] and somma_carte[3] <= 21):
            cosa[i] = f"perso: {puntata[i]}"
            money[i] -= puntata[i]
        elif (somma_carte[3] > 21 and somma_carte[i] <= 21) or (somma_carte[i] > somma_carte[3] and somma_carte[i] <= 21):
            cosa[i] = f"vinto: {puntata[i]}"
            money[i] -= puntata[i]
            money[i] += puntata[i]*molt
        else :
            cosa[i] = f"pareggiato: riprende la puntata"

    return cosa[0],cosa[1],cosa[2]
            


    

def ruota_posizioni_giocatori():
    posizioni = [[1145, 800],[1645, 800],[245, 700]]


    ordine_giocatori = [[2, 1, 0], [0, 2, 1], [1, 0, 2]]
    ordine = ordine_giocatori[(turno+1) % 3]
    
    
    for i in range (3):
        plr_index = ordine[i]
        x_base, y_base = posizioni[i]
        carte_ids = carte_visualizzate[plr_index]

        passo_x = 140
        offset_x = -(len(carte_ids) - 1) * passo_x / 2

        for j, carta_id in enumerate(carte_ids):
            x = x_base + offset_x + j * passo_x
            y = y_base
            canvas.coords(carta_id["id"], x, y)




def fine_turno(plr, cosa):
    global turno, count_id, ix_carta
    messagebox.showinfo(f"fine turno {plr}", cosa)
    ix_carta = 0
    if turno < 2:
        print (f"fine turno {turno} somma: {somma_carte[turno]}")
        ruota_posizioni_giocatori()
        turno += 1
        lb_turno.config(text=f"deve giocare  :{giocatori[turno]}")
        canvas.itemconfig(count_id, text = f"{somma_carte[turno]}")
    else:
        lb_turno.config(text=f"deve giocare  : banco")
        fine_round()




def carta_banco():
    global ix_carta, mazzo, somma_carte, assi
    try:
        valore, seme = mazzo.pesca()
        realvalore = realV(valore)
        somma_carte[3] += realvalore
        if valore == "A":
            assi[3] += 1
        if somma_carte[3] > 21 and assi[3] >= 1:
            somma_carte[3] -= 10
            assi[3] -= 1
        print(valore, seme, somma_carte[3])
        distribuisci_carta_coord(1380 + ix_carta, 175, True, seme, valore, 3)
        ix_carta += 140
        
        root.after(900)
        return somma_carte[3]
    except TypeError:
        pass




def carta1 ():
    global ix_carta, giocatori, turno, puntata
    if somma_carte[turno] < 21:
        try:
            girarsi = True
            valore, seme = mazzo.pesca()
            if valore == "A":
                assi[turno] += 1
            realvalore = realV(valore)
            somma_carte[turno] += realvalore
            canvas.itemconfig(count_id, text = f"{somma_carte[turno]}")
            print(f"cliccato chiedi carta: Turno {turno}, carta: {valore}, somma:{somma_carte}, assi: {assi[turno]}")
            distribuisci_carta_coord(455+ix_carta, 700, girarsi, seme, valore, turno)
            ix_carta += 140
            if somma_carte[turno] > 21 and assi[turno]>=1:
                somma_carte[turno] -= 10
                canvas.itemconfig(count_id, text = f"{somma_carte[turno]}")
                assi[turno] -= 1
            if somma_carte[turno] > 21:
                fine_turno(giocatori[turno], f"sballato, f{giocatori[turno]} ha perso: {puntata[turno]}")
            elif somma_carte[turno] == 21:
                fine_turno(giocatori[turno], f"BlackJack!!, f{giocatori[turno]} potrebbe vincere: {puntata[turno]} se il banco fa meno di: {somma_carte[turno]}")
        except TypeError:
            pass




def cartaR ():
    global ix_carta, turno, puntata, giocatori
    if somma_carte[turno] < 21:
        try:
            puntata[turno] = puntata[turno]*2
            girarsi = True
            valore, seme = mazzo.pesca()
            realvalore = realV(valore)
            somma_carte[turno] += realvalore
            if valore == "A":
                assi[turno] += 1
            print(f"cliccato raddoppia: Turno {turno}, carta: {valore}, somma: {somma_carte[turno]}, assi: {assi[turno]}")
            canvas.itemconfig(count_id, text = f"{somma_carte[turno]}")
            distribuisci_carta_coord(455+ix_carta, 700, girarsi, seme, valore, turno)
            ix_carta += 140
            if somma_carte[turno] > 21 and assi[turno]>=1:
                somma_carte[turno] -= 10
                canvas.itemconfig(count_id, text = f"{somma_carte[turno]}")
                assi[turno] -= 1
            if somma_carte[turno] > 21:
                fine_turno(giocatori[turno], f"sballato , {giocatori[turno]} ha perso: {puntata[turno]}")
            elif somma_carte[turno] == 21:
                fine_turno(giocatori[turno], f"BlackJack!!, {giocatori[turno]} ha vinto: {puntata[turno]}")
            else:
                fine_turno(giocatori[turno], f"{somma_carte[turno]}, se il banco fa meno di: {somma_carte[turno]} allora {giocatori[turno]} vince: {puntata[turno]}")
        except TypeError:
            pass



def raddoppia ():
    cartaR()
    



def inizio_round():
    global bt_chiedi_id, bt_stai_id, bt_raddoppia_id
    global mazzo, nummazzi, money, activate_fast_cmd, puntata, round_n
    try:
        name1 = int(entry1_puntata.get())
        name2 = int(entry2_puntata.get())
        name3 = int(entry3_puntata.get())
        if name1<=money[0] and name2<=money[1] and name3<=money[2] and name1<=puntata_max and name2<=puntata_max and name3<=puntata_max and name1>=puntata_min and name2>=puntata_min and name3>=puntata_min:
            puntata[0] = (name2)
            puntata[1] = (name1)
            puntata[2] = (name3)
            show_frame(frame_gioco)
            lb_turno.config(text=f"deve giocare  :{giocatori[turno]}")
            activate_fast_cmd = True
            if round_n <= 0:
                mazzo = Mazzo(nummazzi)
            dare_carte()
        elif puntata_min>money[0] or puntata_min>money[1] or puntata_min>money[2]:
            messagebox.showinfo("Errore", "non si hanno abbastanza soldi da poter puntare gioco finito")
        else:
            messagebox.showinfo("Errore", "Inserisci le puntate correttamente")
    except ValueError:
        messagebox.showinfo("Errore", "Inserisci le puntate correttamente")



def play():
    name1 = entryName1.get()
    name2 = entryName2.get()
    name3 = entryName3.get()
    if name1 and name2 and name3:
        giocatori[0] = (name1)
        giocatori[1] = (name2)
        giocatori[2] = (name3)
        lb_turno.config(text=f"deve giocare  :{giocatori[turno]}")
        aggiorna_gui1()
        show_frame(frame_punt)
    else:
        messagebox.showinfo("Errore", "Inserisci i nomi dei giocatori")


def show_frame(frame):
    frame.tkraise()


def return_menu():
    show_frame(frame_menu)


def pressed(event):
    global activate_fast_cmd
    if activate_fast_cmd == True:
        print(event.char)
        if event.char == "1":
            stai()
        elif event.char == "2":
            carta1()
        elif event.char == "3":
            raddoppia()


def aggiorna_gui1 ():
    lb_scritta3.config(text = f"soldi: {money[0]}")
    lb_scritta4.config(text = f"soldi: {money[1]}")
    lb_scritta5.config(text = f"soldi: {money[2]}")
    lb_scritta6.config(text = f"puntata massima: {puntata_max},   puntata minima: {puntata_min}")




def salva_partita():
    try:
        global code, save_game, giocatori, money
        canvas2.itemconfigure(btn_salvataggio_id, state = "hidden" )
        with open(save_game, 'r', encoding='utf-8') as file:
            if file:
                l = [line.strip() for line in file.readlines()]
                print ("lista righe salva:", l)
                if len(l) < 5:
                    code = 1
                else:
                    code = int(l[-7]) + 1
                file.close()
        with open(save_game, 'a', encoding='utf-8') as file:
            file.write(f"{code if code != 0 else 1}\n")
            for i in range(3):
                file.write(f"{giocatori[i]}\n")
                file.write(f"{money[i]}\n")
            file.close()
            messagebox.showinfo("salvataggio in corso", f"i dati sono stati salvati correttamente, col codice: {code if code != 0 else 1}\n")
    except IndexError:
        messagebox.showinfo("Errore", "non sono stati salvati i dati")
        canvas2.itemconfigure(btn_salvataggio_id, state = "normal" )






#---------------------------------------  frame gioco  ---------------------------------------------

# Frame contenitore del gioco
frame_gioco = tk.Frame(root)
frame_gioco.grid(row=0, column=0, sticky="nsew")


# Sfondo (verde sotto il canvas)
lb = tk.Label(frame_gioco, bg = coloreT, width=145, height=35)
lb.grid(row=0, column=0, rowspan=41, columnspan=41)

# Canvas da disegno
canvas = tk.Canvas(frame_gioco, width=2000, height=1050, bg=coloreT)
canvas.grid(row=0, column=0, columnspan=40, rowspan=40)




root.bind("<KeyPress>", pressed)





label_dorso = tk.Label(canvas, image = dorso_mazzo_roteato_tk, bd = 7)
label_dorso.place(relx=0.357, rely=0.085)


frame = tk.Frame(frame_gioco, bg="red")
frame.grid(row=41, column=0, columnspan=40, pady=10)



btn_chiedi = tk.Button(canvas, text="[2] Chiedi carta", command=carta1, width=15)
btn_stai = tk.Button(canvas, text="[1] Stai", command=stai, width=15)
btn_raddoppia = tk.Button(canvas, text="[3] raddoppia", command=raddoppia, width=15)

lb_turno = tk.Label(canvas, text = f"deve giocare  :{giocatori[turno]}")
lb_turno_id = canvas.create_window(105, 550, window=lb_turno)


count_id = canvas.create_text(200, 875, text="0", fill="yellow", font=("Helvetica", 20, "bold"))
canvas.itemconfigure(count_id, state="hidden")

canvas.itemconfigure(count_id, state="normal")
bt_chiedi_id = canvas.create_window(300, 950, window=btn_chiedi)
bt_stai_id = canvas.create_window(100, 950, window=btn_stai)
bt_raddoppia_id = canvas.create_window(500, 950, window=btn_raddoppia)

count_id_banco = canvas.create_text(1000, 100, text="0", fill="yellow", font=("Helvetica", 20, "bold"))
canvas.itemconfigure(count_id_banco, state="hidden")




#---------------------------------------  frame puntate  ---------------------------------------------

frame_punt = tk.Frame(root)
frame_punt.grid(row=0, column=0, sticky="nsew")

canvas2 = tk.Canvas(frame_punt, width=2000, height=1050, bg = "lightblue")
canvas2.grid(row=0, column=0, columnspan=40, rowspan=40)

entry1_puntata = tk.Entry(frame_punt, width=18, validate="key", validatecommand=vcmd)
entry1_puntata_id = canvas2.create_window(1000, 700, window=entry1_puntata)

entry2_puntata = tk.Entry(frame_punt, width=18, validate="key", validatecommand=vcmd)
entry2_puntata_id = canvas2.create_window(300, 700, window=entry2_puntata)

entry3_puntata = tk.Entry(frame_punt, width=18, validate="key", validatecommand=vcmd)
entry3_puntata_id = canvas2.create_window(1700, 700, window=entry3_puntata)
    
lb_scritta = tk.Label(frame_punt, text = f"puntata player 1:", bg = "lightblue")
lb_scritta_id = canvas2.create_window(140, 700, window=lb_scritta)
    
lb_scritta1 = tk.Label(frame_punt, text = f"puntata player 2:", bg = "lightblue")
lb_scritta_id1 = canvas2.create_window(840, 700, window=lb_scritta1)
    
lb_scritta2 = tk.Label(frame_punt, text = f"puntata player3:", bg = "lightblue")
lb_scritta_id2 = canvas2.create_window(1540, 700, window=lb_scritta2)
    
btn_distribuisci = tk.Button(frame_punt, text="inizia round", command=inizio_round, width=18)
btn_distribuisci_id = canvas2.create_window(1000, 900, window=btn_distribuisci)

lb_scritta3 = tk.Label(frame_punt, text = f"soldi: {money[0]}", bg = "lightblue")
lb_scritta_id3 = canvas2.create_window(140, 675, window=lb_scritta3)

lb_scritta4 = tk.Label(frame_punt, text = f"soldi: {money[1]}", bg = "lightblue")
lb_scritta_id4 = canvas2.create_window(840, 675, window=lb_scritta4)

lb_scritta5 = tk.Label(frame_punt, text = f"soldi: {money[2]}", bg = "lightblue")
lb_scritta_id5 = canvas2.create_window(1540, 675, window=lb_scritta5)

lb_scritta6 = tk.Label(frame_punt, text = f"puntata massima: {puntata_max},   puntata minima: {puntata_min}", bg = "lightblue")
lb_scritta_id6 = canvas2.create_window(1000, 400, window=lb_scritta6)

btn_menu = tk.Button(frame_punt, text="🔙 home", command= return_menu)
btn_menu_id = canvas2.create_window(35, 20, window=btn_menu)

btn_salvataggio = tk.Button(frame_punt, text="salva partita", command=salva_partita)
btn_salvataggio_id = canvas2.create_window(50, 80, window=btn_salvataggio, state = "hidden" )

lb_scritta7 = canvas2.create_text(500, 200, text="vittoria player 1", fill="yellow", font=("Helvetica", 25, "bold"))
canvas2.itemconfigure(lb_scritta7, state="hidden")

lb_scritta8 = canvas2.create_text(1000, 300, text="vittoria player 2", fill="yellow", font=("Helvetica", 25, "bold"))
canvas2.itemconfigure(lb_scritta8, state="hidden")

lb_scritta9 = canvas2.create_text(1500, 200, text="vittoria player 3", fill="yellow", font=("Helvetica", 25, "bold"))
canvas2.itemconfigure(lb_scritta9, state="hidden")




#---------------------------------------  frame menu  ---------------------------------------------

frame_menu = tk.Frame(root, bg="blue")
frame_menu.grid(row=0, column=0, sticky="nsew")

lbSfondo = tk.Label(frame_menu, bg="blue", width=240, height=50)
lbSfondo.grid(row=0, column=0, rowspan=41, columnspan=41)

bt_play = tk.Button(frame_menu, text="Play", width=11, height=2, font=("arial", 20), command=play)
bt_play.grid(row=10, column=20)


lbtitle = tk.Label(frame_menu, text="blackjack", font=("Times New Roman", 36, "bold"), bg="blue", fg="white")
lbtitle.grid(row=5, column=20)

entryName2 = tk.Entry(frame_menu, validate="key", validatecommand=vcmd2)
entryName2.grid(row=15, column=20)

lbName2 = tk.Label(frame_menu, text="player 2:", bg="blue", fg="white")
lbName2.grid(row=14, column=20)

entryName1 = tk.Entry(frame_menu, validate="key", validatecommand=vcmd2)
entryName1.grid(row=15, column=12)

lbName1 = tk.Label(frame_menu, text="player 1:", bg="blue", fg="white")
lbName1.grid(row=14, column=12)

entryName3 = tk.Entry(frame_menu, validate="key", validatecommand=vcmd2)
entryName3.grid(row=15, column=28)

lbName3 = tk.Label(frame_menu, text="player 3:", bg="blue", fg="white")
lbName3.grid(row=14, column=28)

lbMyName = tk.Label(frame_menu, text="created by: tommaso ganzaroli", bg="blue", fg="white", width=25, height=2)
lbMyName.grid(row=40, column=0, sticky="w", columnspan=10)












def esci():
    root.quit()


def mostra_regole():
    finestra = tk.Toplevel()
    finestra.title("Regole del Black Jack")

    frame_regole = tk.Frame(finestra, width=1000, height=600)
    frame_regole.grid(row=2, column=20, sticky="nsew")

    scrollbar = tk.Scrollbar(frame_regole)
    scrollbar.pack(side="right", fill="y")

    # Text widget con wrapping e scrollbar
    text = tk.Text(frame_regole, wrap="word", yscrollcommand=scrollbar.set, font=("Arial", 12), height=60, width=120)
    text.insert("1.0", regole)
    text.config(state="disabled")
    text.pack(side="left", fill="both", expand=True)

    scrollbar.config(command=text.yview)


    

def impostazioni_p():
    global nummazzi, puntata_max, puntata_min, money, coloreT, molt
    def piunummazzi():
        global nummazzi
        if nummazzi<8:
            nummazzi += 1
            lb_nummazzi.config(text =f"{nummazzi}")
            
    def menonummazzi():
        global nummazzi
        if nummazzi>1:
            nummazzi -= 1
            lb_nummazzi.config(text =f"{nummazzi}")
    
    def menosoldi():
        global money
        if money[0]>100:
            money[0] -= 100
            money[1] -= 100
            money[2] -= 100
            lb_mn.config(text =f"{money[0]}")
    
    def piusoldi():
        global money
        if money[0]<50000:
            money[0] += 100
            money[1] += 100
            money[2] += 100
            lb_mn.config(text =f"{money[0]}")
    
    def menosoldiS():
        global money
        if money[0]>1000:
            money[0] -= 1000
            money[1] -= 1000
            money[2] -= 1000
            lb_mn.config(text =f"{money[0]}")
    
    def piusoldiS():
        global money
        if money[0]<50000:
            money[0] += 1000
            money[1] += 1000
            money[2] += 1000
            lb_mn.config(text =f"{money[0]}")
    
    def piu_pt_max():
        global puntata_max
        if puntata_max<100000:
            puntata_max += 10000
            lb_max_pt.config(text =f"{puntata_max}")
    
    def meno_pt_max():
        global puntata_max
        if puntata_max>10000:
            puntata_max -= 10000
            lb_max_pt.config(text =f"{puntata_max}")
            
    def piu_pt_min():
        global puntata_min
        if puntata_min<1000:
            puntata_min += 10
            lb_min_pt.config(text =f"{puntata_min}")
    
    def meno_pt_min():
        global puntata_min
        if puntata_min>20:
            puntata_min -= 10
            lb_min_pt.config(text =f"{puntata_min}")
    
    
    def loadP():
        loaded_ = False
        global save_game, code
        with open(save_game, "r") as f:
            l = [r.strip() for r in f.readlines()]
        code_plr = lb_saveP.get()
        for e in range (0,len(l), 7):
            if l[e] == code_plr:
                code = l[e]
                lb_tasto_load
                name [0] = l[e+1]
                name [1] = l[e+3]
                name [2] = l[e+5]
                money [0] = int(l[e+2])
                money [1] = int(l[e+4])
                money [2] = int(l[e+6])
                entryName1.delete(0, tk.END)
                entryName1.insert(0, f"{name [0]}")
                
                entryName2.delete(0, tk.END)
                entryName2.insert(0, f"{name [1]}")
                
                entryName3.delete(0, tk.END)
                entryName3.insert(0, f"{name [2]}")
                lb_tasto_load.configure(text = "loaded")
                messagebox.showinfo("ti preghiamo di:", "inserirti nuovamente le impostazioni della vecchia partita. grazie e buon divertimanto (forse)")
                loaded_ = True
        if loaded_ == False:
            lb_tasto_load.configure(text = "failed load")
        print (l)

    
    
    def cambio_colore():
        global coloreT
        stop = False
        colori = ["green","red","orange","yellow", "lightgreen", "lightblue", "blue", "violet", "gray"]
        if coloreT != "gray":
            for e in colori:
                if stop == True:
                    coloreT = e
                    lb_colore.config(fg = coloreT)
                    canvas.config(bg = coloreT)
                    lb.config(bg = coloreT)
                    break
                if coloreT == e:
                    stop = True
        else:
            coloreT = "green"
            lb_colore.config(fg = coloreT)
            canvas.config(bg = coloreT)
            lb.config(bg = coloreT)
    
    
    def piu_molt():
        global molt, difficolta
        it = 0
        stop = False
        difficolta_poss = ["facilissimo","facile","medio","difficile", "difficilissimo"]
        diffN = [10,5,2,1.7, 1.5]
        if difficolta != "difficilissimo":
            for e in difficolta_poss:
                if stop == True:
                    molt = diffN[it]
                    difficolta = e
                    lb_diff.config(text = f"{difficolta}{molt}")
                    break
                if difficolta == e:
                    stop = True
                it = it+1
        else:
            difficolta = "facilissimo"
            molt = 10
            lb_diff.config(text = f"{difficolta}{molt}")

    
    finestra2 = tk.Toplevel()
    finestra2.title("impostazioni partita")

    frame_imp = tk.Frame(finestra2, width=1000, height=600)
    frame_imp.grid()
    
    lb_titolo= tk.Label(frame_imp, text ="impostazioni partita" )
    lb_titolo.grid(row=4, column=21, sticky="nsew")
    
    lb_num_mazzi= tk.Label(frame_imp, text ="numero di mazzi: " )
    lb_num_mazzi.grid(row=8, column=5, sticky="nsw")
    
    lb_nummazzi= tk.Label(frame_imp, text =f"{nummazzi}" )
    lb_nummazzi.grid(row=8, column=30, sticky="nswe")
    
    lb_num_piu= tk.Button(frame_imp, text =">", command=piunummazzi )
    lb_num_piu.grid(row=8, column=36, sticky="nws")
    
    lb_num_meno= tk.Button(frame_imp, text ="<", command=menonummazzi )
    lb_num_meno.grid(row=8, column=24, sticky="nswe")
    
    lb_saveP= tk.Label(frame_imp, text ="riprendi partita codice:" )
    lb_saveP.grid(row=10, column=5, sticky="nsw")
    
    lb_saveP= tk.Entry(frame_imp, validate="key", validatecommand=vcmd)
    lb_saveP.grid(row=10, column=21, columnspan=4, sticky="nsew")
    
    lb_tasto_load= tk.Button(frame_imp, text ="load", command=loadP)
    lb_tasto_load.grid(row=10, column=30, sticky="nswe")
    
    lb_saldo= tk.Label(frame_imp, text ="saldo iniziale:" )
    lb_saldo.grid(row=12, column=5, sticky="nsw")
    
    lb_mn= tk.Label(frame_imp, text =f"{money[0]}" )
    lb_mn.grid(row=12, column=30, sticky="nswe")
    
    lb_num_piu= tk.Button(frame_imp, text =">", command=piusoldi )
    lb_num_piu.grid(row=12, column=36, sticky="nws")
    
    lb_num_meno= tk.Button(frame_imp, text ="<", command=menosoldi )
    lb_num_meno.grid(row=12, column=24, sticky="nswe")
    
    lb_num_piu= tk.Button(frame_imp, text ="》", command=piusoldiS, width=1 )
    lb_num_piu.grid(row=12, column=38, sticky="nws")
    
    lb_num_meno= tk.Button(frame_imp, text ="《", command=menosoldiS, width=1 )
    lb_num_meno.grid(row=12, column=22, sticky="nswe")
    
    lb_color= tk.Label(frame_imp, text ="colore banco: " )
    lb_color.grid(row=14, column=5, sticky="nsw")
    
    lb_colore= tk.Label(frame_imp, text ="■", fg = coloreT )
    lb_colore.grid(row=14, column=30, sticky="nswe")
    
    lb_num_piu= tk.Button(frame_imp, text =">", command=cambio_colore )
    lb_num_piu.grid(row=14, column=36, sticky="nws")
    
    lb_max= tk.Label(frame_imp, text ="puntata massima:" )
    lb_max.grid(row=16, column=5, sticky="nsw")
    
    lb_max_pt= tk.Label(frame_imp, text =f"{puntata_max}" )
    lb_max_pt.grid(row=16, column=30, sticky="nswe")
    
    lb_max_piu= tk.Button(frame_imp, text =">", command=piu_pt_max )
    lb_max_piu.grid(row=16, column=36, sticky="nws")
    
    lb_max_meno= tk.Button(frame_imp, text ="<", command=meno_pt_max )
    lb_max_meno.grid(row=16, column=24, sticky="nswe")
    
    lb_min= tk.Label(frame_imp, text ="puntata minima:" )
    lb_min.grid(row=18, column=5, sticky="nsw")
    
    lb_min_pt= tk.Label(frame_imp, text =f"{puntata_min}" )
    lb_min_pt.grid(row=18, column=30, sticky="nswe")
    
    lb_min_piu= tk.Button(frame_imp, text =">", command=piu_pt_min )
    lb_min_piu.grid(row=18, column=36, sticky="nws")
    
    lb_min_meno= tk.Button(frame_imp, text ="<", command=meno_pt_min )
    lb_min_meno.grid(row=18, column=24, sticky="nswe")

    lb_min= tk.Label(frame_imp, text ="difficolta (moltiplicatore vincite):" )
    lb_min.grid(row=20, column=5, sticky="nsw")
    
    lb_diff= tk.Label(frame_imp, text =f"medio{molt}", width=17 )
    lb_diff.grid(row=20, column=30, sticky="nswe")
    
    lb_diff_piu= tk.Button(frame_imp, text =">", command=piu_molt )
    lb_diff_piu.grid(row=20, column=36, sticky="nws")
    


menu_button = tk.Menubutton(frame_menu, text="☰ Menu", relief=tk.RAISED, direction='below')
menu_button.grid(row=0, column=0, sticky="nw")  

# Menu associato al Menubutton
menu = tk.Menu(menu_button, tearoff=0)
menu.add_command(label="impostazioni partita", command=impostazioni_p)
menu.add_command(label="Regole", command=mostra_regole)
menu.add_command(label="chiusura forzata", command=esci)

menu_button.config(menu=menu)





show_frame(frame_menu)
root.mainloop()
