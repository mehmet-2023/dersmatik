import sqlite3
import os
import tkinter.messagebox
from tkinter import *
from tkinter import messagebox, Tk
import subprocess
import matplotlib.pyplot as plt
from firebase_admin import *
from firebase_admin import db

cred = credentials.Certificate(
#Veriler buraya
)
initialize_app(cred, {"databaseURL": "< url buraya >"})
ref = db.reference("calisma_gunlugu/ogrenciler")

conn = sqlite3.connect("databases.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS online(name,sinif)")
cursor.execute("SELECT * FROM name")
name = cursor.fetchall()
name = list(list(name)[0])[0].replace("_"," ")
cursor.execute("SELECT * FROM online")
veri = cursor.fetchall()

def onebyone():
    global room_id
    global name
    tkk = Tk()
    label = Label(tkk,text="Sorgulamak İstediğiniz Öğrenciyi Girin:")
    entry = Entry(tkk)
    def pie():
        global hedef
        ref = db.reference("calisma_gunlugu/siniflar/" + room_id + "/ogrenci/" + hedef + "/info")
        veriler = ref.get()
        veriler.pop('toplam_haftalar', None)
        veriler.pop('toplam', None)
        plt.pie(veriler.values(), labels=veriler.keys(), autopct='%1.1f%%', startangle=90)
        plt.title('Ders Dağılımı')

        # Grafiği göster
        plt.show()
    def comment():
        ref = db.reference("calisma_gunlugu/genel_degerlendirmeler/" + hedef)
        def step3():
            ref.push(entry2.get("1.0", "end-1c"))
            messagebox.showinfo(title="Başarılı",message="Değerlendirme Gönderildi")
            wind.destroy()
        wind = Tk()
        lbl = Label(wind,text=hedef+" için bir değerlendirme yaz")
        entry2 = Text(wind)
        buttton = Button(wind,text="Gönder",command=step3)
        lbl.pack()
        entry2.pack()
        buttton.pack()
    def step2():
        global hedef
        hedef = entry.get()
        ref = db.reference("calisma_gunlugu/siniflar/" + room_id + "/ogrenci/"+entry.get()+"/info")
        win =Tk()
        lbl = Label(win, text=entry.get()+" Adlı Öğrencinin Durumu:")
        lbl.pack()
        blnk = Label(win)
        blnk.pack()
        toplam = ref.get()["toplam"]
        toplam_haftalar = ref.get()["toplam_haftalar"]
        tr = ref.get()["tr"]
        mat = ref.get()["mat"]
        fen = ref.get()["fen"]
        ing = ref.get()["ing"]
        sos = ref.get()["sos"]
        din = ref.get()["din"]
        lbl2 = Label(win,text=f"Çözdüğü Toplam Soru: {toplam}\nTürkçeden Çözdüğü Soru: {tr}\nMatematikten Çözdüğü Soru: {mat}\nFenden Çözdüğü Soru: {fen}\nİngilizceden Çözdüğü Soru: {ing}\n Sosyal Bilimlerden Çözdüğü Soru: {sos}\nDKAB'den Çözdüğü Soru: {din}\n")
        lbl2.pack()
        but = Button(win,text="Ders Dağlımı",command = pie)
        but2 = Button(win,text="Genel Değerlendirme Yaz", command=comment)
        but.pack()
        but2.pack()
        tkk.destroy()
    button = Button(tkk,text="Gönder",command=step2)
    label.grid(row=0,column=0)
    entry.grid(row=1, column=0)
    button.grid(row=2,column=0)
def line():
    global room_id
    global name
    ref = db.reference("calisma_gunlugu/siniflar/" + room_id + "/haftalar")
    toplam_degerler = {}
    for key, value in ref.get().items():
        for sublist in value:
            index_key = sublist[0]
            if index_key not in toplam_degerler:
                toplam_degerler[index_key] = 0
            toplam_degerler[index_key] += sublist[3]
    x = list(toplam_degerler.keys())
    y = list(toplam_degerler.values())

    plt.plot(x, y, marker='o')
    plt.title('Haftalık İlerleme Raporu')
    plt.xlabel('Hafta')
    plt.ylabel('Soru Sayısı')
    plt.show()
def graph():
    global name
    global room_id
    ref = db.reference("calisma_gunlugu/siniflar/" + room_id + "/info")
    veriler = ref.get()
    veriler.pop('toplam', None)
    veriler.pop('toplam_haftalar', None)
    etiketler = veriler.keys()
    degerler = list(veriler.values())
    plt.pie(degerler, labels=etiketler, autopct='%1.1f%%', startangle=90)
    plt.title('Sınıf Geneli Ders Dağılımı')
    plt.show()
def chat():
    global room_id
    global name
    chat_ref = db.reference("calisma_gunlugu/siniflar/" + room_id + "/chat")
    name = name.replace("_"," ")
    def gonder():
        chat_ref.push(f"{name}: {entry.get()}")
        entry.delete(0, END)
    chat = Tk()
    msg = Text(chat,width=50,height=30)
    msg.pack()
    msg.config(state=DISABLED)
    entry = Entry(chat,width=30)
    entry.pack(side=LEFT, padx=(100,5))
    button = Button(chat, text="Gönder",command=gonder)
    button.pack(side=LEFT, padx=5)
    def add(event):
        if type(event.data) == dict:
            for i, j in event.data.items():
                win.after(0,lambda:msg.config(state=NORMAL))
                win.after(0, lambda value=j: msg.insert(END, f"{value}\n"))
        elif type(event.data) == str:
            win.after(0, lambda: msg.config(state=NORMAL))
            win.after(0, lambda value=event.data: msg.insert(END, f"{value}\n"))
        else:
            for i in event.data:
                if i != None:
                    win.after(0,lambda:msg.config(state=NORMAL))
                    win.after(0, lambda value=i: msg.insert(END, f"{value}\n"))

        win.after(0,lambda:msg.config(state=DISABLED))
    chat_ref.listen(add)

def join():
    global room_id
    global name
    ref = db.reference("calisma_gunlugu/siniflar/"+ent.get()+"/chat")
    if not ref.get():
        messagebox.showerror(title="Hata",message="Bu sınıf hiç kurulmamış")
    else:
        name = ent2.get()
        room_id = ent.get()
        ref2 = db.reference("calisma_gunlugu/siniflar/"+ent.get()+"/name")
        ref3 = db.reference("calisma_gunlugu/siniflar/"+ent.get()+"/uyeler")
        ref4 = db.reference("calisma_gunlugu/siniflar/"+ent.get()+"/info")
        cursor.execute("SELECT * FROM online")
        veri = cursor.fetchall()
        if veri:
            cursor.execute(f"UPDATE online SET name = '{ent2.get()}'")
            cursor.execute(f"UPDATE online SET sinif = '{ent.get()}'")
        else:
            cursor.execute("INSERT INTO online VALUES (?,?)", (ent2.get(), ent.get(),))
            conn.commit()
            ref.push(f"Sınıf: {ent2.get()} Odaya Katıldı!")
            ref3.push(ent2.get())
        for key,liste in ref2.get().items():
            deger = liste
        if ref3.get():
            degerler = []
            for key,liste in ref3.get().items():
                degerler.append(liste)
        else:
            degerler = []
        if ref4.get():
            haftalar = ref4.get()["toplam_haftalar"]
            toplam = ref4.get()["toplam"]
            tr = ref4.get()["tr"]
            mat = ref4.get()["mat"]
            fen = ref4.get()["fen"]
            sos = ref4.get()["sos"]
            ing = ref4.get()["ing"]
            din = ref4.get()["din"]
        win.destroy()
        tk = Tk()
        label = Label(tk,text=deger,font=("bold",15))
        label.grid(row=0,column=0,columnspan=2)
        labels = {}
        for i in range(len(degerler)):
            labels[i] = Label(tk,text=degerler[i],font=("Arial",9),bg="light grey")
            labels[i].grid(row =12+i,column=0)
        label2 = Label(tk,text="Sınıf Durumu:", font = ("arial",10),width=30)
        label2.grid(row=1,column=0,columnspan=2)
        label3 = Label(tk,text=f"Çözülen toplam soru: {toplam} \nÇözülen toplam türkçe: {tr} \nÇözülen toplam matematik: {mat} \nÇözülen toplam fen: {fen} \nÇözülen toplam ingilizce: {ing} \nÇözülen toplam sosyal: {sos} \nÇözülen toplam din: {din} \nGönderilen toplam hafta: {haftalar}",font=("arial",9))
        label3.grid(row = 2,column=0,rowspan = 6,columnspan=2)
        button2 = Button(tk,text="Soru Dağlımı",width=15,command=graph)
        button2.grid(row=8,column=0)
        button3 = Button(tk,text="Haftalık İlerleme",width=15,command=line)
        button3.grid(row=8,column=1)
        button4 = Button(tk,text="Öğrenci Analizi",width=15,command=onebyone)
        button4.grid(row=9,column=0)
        button5 = Button(tk,text="Sınıf Sohbeti",width=15,command=chat)
        button5.grid(row=9,column=1)
        lbl5 = Label(tk,text="Kayıt Eklemek İçin Ana Uygulamaya Geç")
        lbl5.grid(row=10,column=0,columnspan=2)
        lbl6 = Label(tk,text="Sınıf Üyeleri:")
        lbl6.grid(row=11,column=0,columnspan=2)

win = Tk()
win.title("Sınıflar")
win.resizable(False,False)

lab = Label(win,text="Dersmatik - Online",font=("Arial",15,"bold"))
lab.grid(row=0,column=0)

blank = Label(win)
blank.grid(row=1,column=0)

lab2 = Label(win,text="Adminin Verdiği Sınıf Kodunu Girin:")
lab2.grid(row=2,column=0)

ent = Entry(win)
ent.grid(row=3,column=0)

lab3 = Label(win,text="Adınız Soyadınız:")
lab3.grid(row=4,column=0)

ent2 = Entry(win)
ent2.grid(row=5,column=0)
if name:
    ent2.insert(0,name)
buton = Button(win,text="Partiye Katıl!")
buton.grid(row=6,column=0)
if len(veri) != 0:
    ent2.delete(0,END)
    ent2.insert(0, list(veri[0])[0])
    ent.insert(0, list(veri[0])[1])
    join()
else:
    buton.bind("<Button-1>", lambda event: join())

win.mainloop()
