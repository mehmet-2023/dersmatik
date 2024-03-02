from tkinter import *
from tkinter import messagebox
from firebase_admin import *
from firebase_admin import db
import sqlite3
from random import randint
import requests
import json
import subprocess

cred = credentials.Certificate(
#Veriler buraya
)
initialize_app(cred, {"databaseURL": "< url buraya >"})
ref = db.reference("calisma_gunlugu/ogrenciler")
conn = sqlite3.connect("databases.db")
cursor = conn.cursor()
window = Tk()
window.resizable(False, False)
label = Label(window, text="Merhaba Admin!")
label.pack()
label2 = Label(window, text="İstek Bekleyen Öğrenciler:")
label2.pack()
blank = Label(window)
blank.pack()
buttons = {}

def send():
    global name
    global ref
    global gunler
    global tk
    tk2 = Tk()
    labx = Label(tk2, text="Haftayı Değerlendir")
    labxx = Label(tk2, text="Bunu Öğrenci Görecek")
    msg = Text(tk2)

    def command2():
        ref = db.reference("calisma_gunlugu/ogrenciler/" + name)
        ref.set({})
        ref = db.reference(f"calisma_gunlugu/degerlendirmeler/{name}/{gunler[0][0]}")
        ref.push(msg.get("1.0", "end-1c"))
        messagebox.showinfo(title="Başarılı", message="İşlem Başarılı!")
        tk2.destroy()
        tk.destroy()
        window.destroy()
        subprocess.run(["python", os.getcwd()+"/admin.py"])

    btn = Button(tk2, text="Gönder", command=command2)
    labx.pack()
    labxx.pack()
    msg.pack()
    btn.pack()

def create():
    cursor.execute("""SELECT * FROM online""")
    value = cursor.fetchall()
    if value:
        messagebox.showerror(title="Hata", message="Zaten Bir Sınıfa Katılmışsınız.")
    else:
        sinif = Tk()
        label_sinif = Label(sinif, text="Sınıf Oluştur")
        label_sinif.pack()
        blank = Label(sinif)
        blank.pack()
        label2_sinif = Label(sinif, text="Sınıf Adı:")
        label2_sinif.pack()
        entry_sinif = Entry(sinif)
        entry_sinif.pack()

        def step2():
            room_id = randint(100000, 999999)
            name = "Admin"
            cursor.execute("""INSERT INTO online VALUES (?,?)""", (name, room_id,))
            conn.commit()
            ref = db.reference(f"calisma_gunlugu/siniflar/{room_id}/chat")
            ref.push("Sınıf: Sınıf Kuruldu")
            ref = db.reference(f"calisma_gunlugu/siniflar/{room_id}/uyeler")
            ref.push("Admin")
            ref = db.reference(f"calisma_gunlugu/siniflar/{room_id}/name")
            ref.push(entry_sinif.get())
            data = {
                "toplam": 0,
                "tr": 0,
                "mat": 0,
                "fen": 0,
                "ing": 0,
                "sos": 0,
                "din": 0,
                "toplam_haftalar": 0,
            }
            url = f"< url buraya >/calisma_gunlugu/siniflar/{room_id}/info.json?auth=AIzaSyBV1mk2oq5kn3wuZHti44sjJoKSq6nvAbQ"
            response = requests.patch(url, data=json.dumps(data))
            messagebox.showinfo(title="Sınıf Kuruldu!", message=f"Sınıf Kodu: {room_id} bu kodu asla unutmayın!")
            messagebox.showinfo(title="Sınıf Kuruldu!", message="Online.py dosyasını açın, sınıf kuruldu.")
            sinif.destroy()
            window.destroy()
        send_sinif = Button(sinif, command=step2, text="Sınıf Oluştur")
        send_sinif.pack()
        sinif.mainloop()

def nextday():
    global ref
    global gunler
    global lab_info
    global lab_day
    global name
    global curday
    global nextbutton2
    curday += 1
    if curday != 7:
        lab_info.config(
            text=f"Türkçe: {gunler[curday][3]} \nMatematik: {gunler[curday][4]} \nFen: {gunler[curday][5]}\nİngilizce: {gunler[curday][6]}\nSosyal: {gunler[curday][7]}\nDKAB: {gunler[curday][8]}"
        )
        lab_day.config(text="Gün " + str(curday + 1))
    else:
        curday = 0
        lab_info.config(
            text=f"Türkçe: {gunler[curday][3]} \nMatematik: {gunler[curday][4]} \nFen: {gunler[curday][5]}\nİngilizce: {gunler[curday][6]}\nSosyal: {gunler[curday][7]}\nDKAB: {gunler[curday][8]}"
        )
        lab_day.config(text="Gün " + str(curday + 1))


def check(event):
    global name
    global ref
    global lab_info
    global lab_day
    global tk
    global curday
    global nextbutton2
    global gunler
    tk = Tk()
    gunler = {}
    name = event.widget.cget("text")
    lab = Label(tk, text=name)
    lab.pack()
    ref = db.reference("calisma_gunlugu/ogrenciler/" + name)
    for gun, liste in ref.get().items():
        for i in range(len(liste)):
            gunler[i] = liste[i]
    lab_day = Label(tk, text="Gün 1")
    lab_info = Label(
        tk,
        text=f"Türkçe: {gunler[0][3]} \nMatematik: {gunler[0][4]} \nFen: {gunler[0][5]}\nİngilizce: {gunler[0][6]}\nSosyal: {gunler[0][7]}\nDKAB: {gunler[0][8]}",
    )
    nextbutton = Button(tk, text="Sonraki Gün", command=nextday)
    nextbutton2 = Button(tk, text="Değerlendirme Yaz", command=send)
    curday = 0
    lab_day.pack()
    lab_info.pack()
    nextbutton.pack()
    nextbutton2.pack()


if ref.get() != None:
    for i in range(len(ref.get())):
        name = list(ref.get())[i]
        buttons[i] = Button(window, text=name, width=15)
        buttons[i].pack()
        buttons[i].bind("<Button-1>", check)
else:
    labxd = Label(window, text="Bekleyen Öğrenci Yok.")
    labxd.pack()
blank2 = Label(window)
blank2.pack()
button = Button(window,text="Sınıf Oluştur",command=create)
button.pack(side=BOTTOM)
window.mainloop()
