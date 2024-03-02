import tkinter.messagebox
from tkinter import *
from tkinter import messagebox
import sqlite3
import os
import subprocess
import matplotlib.pyplot as plt
from firebase_admin import *
from firebase_admin import db
import requests
import json

global name
cred = credentials.Certificate(
#veriler buraya
)
initialize_app(cred, {"databaseURL": "< url buraya >"})
ref = db.reference("calisma_gunlugu/ogrenciler")

haftalara_gore_veriler = {}
conn = sqlite3.connect("databases.db")
cursor = conn.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS veriler(hafta,gün,toplam,tr,mat,fen,ing,ink,din)"
)

cursor.execute("CREATE TABLE IF NOT EXISTS online(name,sinif)")
cursor.execute("CREATE TABLE IF NOT EXISTS name(name)")
cursor.execute("SELECT * FROM veriler ORDER BY hafta DESC LIMIT 1")
hafta = cursor.fetchone()
if hafta != None:
    cursor.execute(
        "SELECT * FROM veriler WHERE hafta = "
        + str(list(hafta)[0]).replace(".", "")
        + " ORDER BY gün DESC LIMIT 1"
    )
    gün = cursor.fetchone()
if hafta != None:
    gün = int(str(list(gün)[1]).replace(".", ""))
    hafta = int(str(list(hafta)[0]).replace(".", ""))
cursor.execute("SELECT * FROM name")
name = cursor.fetchall()
if name:
    name = list(list(name)[0])[0].replace("_"," ")
def ekle():
    global hafta
    global gün
    global ekle_window
    global türkçe_entry
    global mat_entry
    global fen_entry
    global ing_entry
    global ink_entry
    global din_entry
    ekle_window = Tk()
    ekle_window.title("Kayıt Ekle")
    ekle_window.resizable(False, False)
    # ekle_window.geometry("200x300")
    if hafta == 0:
        tarih = Label(
            ekle_window,
            text="Hafta: " + str(hafta + 1) + ", Gün: " + str(gün + 1),
            font=10,
        )
    elif gün == 7:
        tarih = Label(
            ekle_window, text="Hafta: " + str(hafta + 1) + ", Gün: 1", font=10
        )
    else:
        tarih = Label(
            ekle_window, text="Hafta: " + str(hafta) + ", Gün: " + str(gün + 1), font=10
        )
    tarih.pack()
    türkçe = Label(ekle_window, text="Türkçe Soru Sayısı: ")
    türkçe.pack()
    türkçe_entry = Entry(ekle_window)
    türkçe_entry.pack()
    matematik = Label(ekle_window, text="Matematik Soru Sayısı: ")
    matematik.pack()
    mat_entry = Entry(ekle_window)
    mat_entry.pack()
    fen = Label(ekle_window, text="Fen Bilimleri Soru Sayısı: ")
    fen.pack()
    fen_entry = Entry(ekle_window)
    fen_entry.pack()
    ing = Label(ekle_window, text="İngilizce Soru Sayısı: ")
    ing.pack()
    ing_entry = Entry(ekle_window)
    ing_entry.pack()
    ink = Label(ekle_window, text="Sosyal Bilimler Soru Sayısı: ")
    ink.pack()
    ink_entry = Entry(ekle_window)
    ink_entry.pack()
    din = Label(ekle_window, text="DKAB Soru Sayısı: ")
    din.pack()
    din_entry = Entry(ekle_window)
    din_entry.pack()
    button2 = Button(ekle_window, text="Gönder", command=gonder)
    button2.pack()
    ekle_window.mainloop()
def next_hafta():
    global info_lbl
    global cur_hafta
    if hafta != 1:
        if cur_hafta == 1:
            cur_hafta = 2
            frames[0].pack_forget()
            frames[1].pack()
        elif cur_hafta == hafta:
            frames[cur_hafta - 1].pack_forget()
            cur_hafta = 1
            frames[0].pack()
        else:
            if cur_hafta != hafta:
                cur_hafta += 1
                x = cur_hafta - 1
                y = cur_hafta - 2
                frames[x].pack()
                frames[y].pack_forget()
        info_lbl.config(text="Hafta " + str(cur_hafta))


def sonraki():
    global tr
    global buton
    global mat
    global fen
    global ink
    global ing
    global din
    global datas
    global wind
    global dect
    global toplam_lbl
    maks_ders = "Boş"
    if max(datas) == tr:
        maks_ders = "Türkçe"
    elif max(datas) == mat:
        maks_ders = "Matematik"
    elif max(datas) == fen:
        maks_ders = "Fen"
    elif max(datas) == ing:
        maks_ders = "İngilizce"
    elif max(datas) == ink:
        maks_ders = "İnkılap"
    elif max(datas) == din:
        maks_ders = "DKAB"
    min_ders = "Boş"
    if min(datas) == tr:
        min_ders = "Türkçe"
    elif min(datas) == mat:
        min_ders = "Matematik"
    elif min(datas) == fen:
        min_ders = "Fen"
    elif min(datas) == ing:
        min_ders = "İngilizce"
    elif min(datas) == ink:
        min_ders = "İnkılap"
    elif min(datas) == din:
        min_ders = "DKAB"
    if "Toplam" in toplam_lbl.cget("text"):
        toplam_lbl.config(text="En Çok " + maks_ders + " Dersinden Soru Çözdün!")
        dect.config(text="(" + str(max(datas)) + ")")
    elif "En Çok" in toplam_lbl.cget("text"):
        toplam_lbl.config(text="En Az " + min_ders + " Dersinden Soru Çözdün!")
        dect.config(text="(" + str(min(datas)) + ")")
        buton.config(text="Derslere Göre Pasta Grafiği")
    elif "En Az" in toplam_lbl.cget("text"):
        buton.config(text="Haftaya Göre Soru Sayısı")
        toplam_lbl.config(text="Şimdi Grafiklere Göz Atalım!")
        dect.pack_forget()
        # SQL sorgusu ile tüm derslerin toplam değerlerini çek
        cursor.execute("SELECT tr, mat, fen, ing, ink, din FROM veriler")
        result = cursor.fetchall()
        
        tr = []
        mat = []
        fen = []
        ink = []
        ing = []
        din = []
        for row in result:
        	tr.append(int(row[0]))
        	mat.append(int(row[1]))
        	fen.append(int(row[2]))
        	ink.append(int(row[4]))    	
        	ing.append(int(row[3]))
        	din.append(int(row[5]))
   	
        tr_total = sum(tr)
        mat_total = sum(mat)
        fen_total = sum(fen)
        ing_total = sum(ing)
        ink_total = sum(ink)
        din_total = sum(din)

        # Ders adları ve toplam değerleri
        subjects = ["Türkçe", "Matematik", "Fen", "İngilizce", "Sosyal", "DKAB"]
        totals = [tr_total, mat_total, fen_total, ing_total, ink_total, din_total]

        # Daire grafiğini çiz
        plt.pie(totals, labels=subjects, autopct="%1.1f%%", startangle=90)

        # Grafiği göster
        plt.axis("equal")  # Daire grafiğini dairenin içine sığdırmak için
        plt.title("Derslerin Dağılımı")
        plt.show()
    elif "Haftaya Göre" in buton.cget("text"):
        cursor.execute(
            "SELECT hafta, SUM(tr + mat + fen + ing + ink + din) FROM veriler GROUP BY hafta"
        )
        result = cursor.fetchall()
        hafta=[]
        toplam = []
        for row in result:
        	hafta.append(int(row[0]))
        	toplam.append(int(row[1]))
        # Çizgi grafiğini çiz
        plt.plot(hafta, toplam, label="Toplam")

        # Grafiği göster
        plt.xlabel("Hafta")
        plt.ylabel("Toplam Değerler")
        plt.title("Haftaya Göre Tüm Derslerin Toplamı")
        plt.legend()
        plt.show()
        buton.config(text="Hafta Ve Derslerin Karşılaştırması")
    elif "Hafta Ve Derslerin" in buton.cget("text"):
        cursor.execute("SELECT hafta, tr, mat, fen, ing, ink, din FROM veriler")
        result = cursor.fetchall()
        # Verileri işle
        hafta = []
        tr = []
        mat = []
        fen = []
        ink = []
        ing = []
        din = []
        for row in result:
        	hafta.append(int(row[0]))
        	tr.append(int(row[1]))
        	mat.append(int(row[2]))
        	fen.append(int(row[3]))
        	ink.append(int(row[5]))    	
        	ing.append(int(row[4]))
        	din.append(int(row[6]))
#        hafta = [row[0] for row in result]
#        tr = [row[1] for row in result]
#        mat = [row[2] for row in result]
#        fen = [row[3] for row in result]
#        ing = [row[4] for row in result]
#        ink = [row[5] for row in result]
#        din = [row[6] for row in result]

        # Sütun grafiğini çiz
        width = 0.2  # Sütun genişliği
        fig, ax = plt.subplots()
        ax.bar([w - width * 2 for w in hafta], tr, width, label="tr")
        ax.bar([w - width for w in hafta], mat, width, label="mat")
        ax.bar(hafta, fen, width, label="fen")
        ax.bar([w + width for w in hafta], ing, width, label="ing")
        ax.bar([w + width * 2 for w in hafta], ink, width, label="ink")
        ax.bar([w + width * 3 for w in hafta], din, width, label="din")

        # Grafiği düzenle
        ax.set_xticks(hafta)
        ax.set_xlabel("Hafta")
        ax.set_ylabel("Ders Değerleri")
        ax.set_title("Haftaya Göre Ders Dağılımı")
        ax.legend()
        plt.show()
        wind.destroy()
        messagebox.showinfo(
            title="Bu Kadardı", message="Programını Buna Göre Hazırlamayı Unutma..."
        )


def wrapped():
    global tr
    global mat
    global fen
    global ink
    global ing
    global buton
    global din
    global wind
    global datas
    global dect
    global toplam_lbl
    cursor.execute("SELECT SUM(toplam) FROM veriler")
    toplam = list(list(cursor.fetchall())[0])[0]
    cursor.execute("SELECT SUM(tr) FROM veriler")
    tr = list(list(cursor.fetchall())[0])[0]
    cursor.execute("SELECT SUM(mat) FROM veriler")
    mat = list(list(cursor.fetchall())[0])[0]
    cursor.execute("SELECT SUM(fen) FROM veriler")
    fen = list(list(cursor.fetchall())[0])[0]
    cursor.execute("SELECT SUM(ing) FROM veriler")
    ing = list(list(cursor.fetchall())[0])[0]
    cursor.execute("SELECT SUM(ink) FROM veriler")
    ink = list(list(cursor.fetchall())[0])[0]
    cursor.execute("SELECT SUM(din) FROM veriler")
    din = list(list(cursor.fetchall())[0])[0]
    datas = [tr, mat, fen, ink, ing, din]
    wind = Tk()
    lab = Label(wind, text="Hadi Sorularının Analizini Yapalım!")
    lab.pack()
    toplam_lbl = Label(
        wind, text="Toplam " + str(toplam) + " Soru Çözdün!"
    )
    dect = Label(wind, text="Bu inanılmaz")
    buton = Button(wind, text="Devam Et", command=sonraki)
    toplam_lbl.pack()
    dect.pack()
    buton.pack()


def info(event):
    cursor.execute("SELECT * FROM veriler WHERE hafta = " + str(cur_hafta) + ".")
    data = cursor.fetchall()
    data = list(data[event.widget.cget("text") - 1])
    root = Tk()
    #root.geometry("200x250")
    root.title("Detaylı Bilgi")
    root.resizable(False, False)
    hafta_lbl = Label(root, text="Hafta: " + str(data[0]))
    gün_lbl = Label(root, text="Gün: " + str(event.widget.cget("text")))
    toplam_lbl = Label(root, text="Toplam: " + str(data[2]))
    tr_lbl = Label(root, text="Türkçe: " + str(data[3]))
    mat_lbl = Label(root, text="Matematik: " + str(data[4]))
    fen_lbl = Label(root, text="Fen Bilmleri " + str(data[5]))
    ing_lbl = Label(root, text="İngilizce: " + str(data[6]))
    ink_lbl = Label(root, text="İnkılap: " + str(data[7]))
    dkab_lbl = Label(root, text="DKAB: " + str(data[8]))
    hafta_lbl.pack()
    gün_lbl.pack()
    toplam_lbl.pack()
    tr_lbl.pack()
    mat_lbl.pack()
    fen_lbl.pack()
    ing_lbl.pack()
    ink_lbl.pack()
    dkab_lbl.pack()


def gonder():
    global ekle_window
    global hafta
    global gün
    global türkçe_entry
    global mat_entry
    global fen_entry
    global ing_entry
    global ink_entry
    global din_entry
    if türkçe_entry.get() == "":
        tr_data = 0
    else:
        tr_data = int(türkçe_entry.get())
    if mat_entry.get() == "":
        mat_data = 0
    else:
        mat_data = int(mat_entry.get())
    if fen_entry.get() == "":
        fen_data = 0
    else:
        fen_data = int(fen_entry.get())
    if ing_entry.get() == "":
        ing_data = 0
    else:
        ing_data = int(ing_entry.get())
    if ink_entry.get() == "":
        ink_data = 0
    else:
        ink_data = int(ink_entry.get())
    if din_entry.get() == "":
        din_data = 0
    else:
        din_data = int(din_entry.get())
    toplam = tr_data + mat_data + fen_data + ing_data + ink_data + din_data
    if hafta == 0:
        hafta = 1
        gün = 1
    elif gün == 7:
        hafta += 1
        gün = 1
    else:
        gün += 1
    xd = str(hafta)
    cursor.execute(
        f"INSERT INTO veriler VALUES({xd}, {gün}, {toplam}, {tr_data}, {mat_data}, {fen_data}, {ing_data}, {ink_data}, {din_data})"
    )
    conn.commit()
    messagebox.showinfo(title="Başarılı!", message="Kayıt Başarılı!")
    ekle_window.destroy()
    conn.close()
    window.destroy()
    subprocess.run(["python", os.getcwd() + "\main.py"])


def post():
    global name
    global hafta
    global cur_hafta
    cursor.execute("SELECT * FROM veriler WHERE hafta=" + str(cur_hafta))
    veri = cursor.fetchall()

    def step2():
        name = enryxd.get().replace(" ", "_")
        ref = db.reference("calisma_gunlugu/ogrenciler/" + enryxd.get())
        toplam = 0
        tr = 0
        mat = 0
        fen = 0
        ing = 0
        sos  = 0
        din = 0
        for i in range(len(veri)):
            toplam += int(veri[i][2])
            tr += int(veri[i][3])
            mat += int(veri[i][4])
            fen += int(veri[i][5])
            ing += int(veri[i][6])
            sos += int(veri[i][7])
            din += int(veri[i][8])

        ref.push(veri)
        tk.destroy()
        cursor.execute("CREATE TABLE IF NOT EXISTS name(name)")
        cursor.execute("SELECT * FROM name")
        data = cursor.fetchall()
        cursor.execute("SELECT * FROM online")
        deger = cursor.fetchall()
        if deger:
            ref2 = db.reference(f"calisma_gunlugu/siniflar/{list(deger[0])[1]}/haftalar")
            ref2.push(veri)
            ref2 = db.reference(f"calisma_gunlugu/siniflar/{list(deger[0])[1]}/info")
            data = {
                "toplam": ref2.get()["toplam"] + toplam,
                "tr": ref2.get()["tr"] + tr,
                "mat": ref2.get()["mat"] + mat,
                "fen": ref2.get()["fen"] + fen,
                "ing": ref2.get()["ing"] + ing,
                "sos": ref2.get()["sos"] + sos,
                "din": ref2.get()["din"] + din,
                "toplam_haftalar": ref2.get()["toplam_haftalar"] + 1,
            }
            url = f"< url buraya >/calisma_gunlugu/siniflar/{list(deger[0])[1]}/info.json?auth=AIzaSyBV1mk2oq5kn3wuZHti44sjJoKSq6nvAbQ"
            response = requests.patch(url, data=json.dumps(data))
            url2 = f"< url buraya >/calisma_gunlugu/siniflar/{list(deger[0])[1]}/ogrenci/{list(deger[0])[0]}/info.json?auth=AIzaSyBV1mk2oq5kn3wuZHti44sjJoKSq6nvAbQ"
            response2 = requests.patch(url2, data=json.dumps(data))
        if data == []:
            cursor.execute(f"INSERT INTO name (name) VALUES (?)", (name,))
        else:
            cursor.execute(f"UPDATE name SET name='{name}'")
        conn.commit()
        messagebox.showinfo(
            title="İşlem Başarılı", message="Hafta sınıf gurubu(kayıtlıysa) ve admine gönderildi."
        )

    tk = Tk()
    lbl = Label(tk, text="Adınız Soyadınız: ")
    enryxd = Entry(tk)
    if name:
        enryxd.insert(0,name)
    button = Button(tk, text="Gönder", command=step2)
    lbl.pack()
    enryxd.pack()
    button.pack()
def degerlendir(event):
    global name
    global cur_hafta
    list = []
    text = ""
    ref = db.reference(f"calisma_gunlugu/degerlendirmeler/{name}/{cur_hafta}")
    for i,j in ref.get().items():
        wind2 = Tk()
        for k in j.split("."):
        	list.append(k+".\n")
        for l in list:
        	text = text + l
        lbl = Label(wind2,text=str(text))
        lbl.pack()
window = Tk()
window.title("Dersmatik")
window.resizable(False, False)
label = Label(window, text="Dersmatik", font=("Halventica", 15))
label.pack()
global dataz
dataz = {}
if hafta is None:
    hafta = 0
    gün = 0
    label2 = Label(window, text="Kayıt bulamadım, kayıt eklemeye ne dersin?")
    button = Button(window, text="Kayıt ekle", command=ekle)
    label2.pack()
    button.pack()
else:
    window.geometry("250x500")
    global info_lbl
    info_lbl = Label(window, text="Hafta 1", font=("Halventica", 12))
    button5 = Button(window, text="Sonraki Hafta", command=next_hafta)
    button7 = Button(window, text="Haftayı Gönder", command=post)
    button6 = Button(window, text="Wrapped", command=wrapped)
    button = Button(window, text="Kayıt ekle", command=ekle)
    button.pack()
    button6.pack(side=BOTTOM)
    button5.pack()
    button7.pack(side=BOTTOM)
    info_lbl.pack()
    global cur_hafta
    cur_hafta = 1
    buttons = {}
    frames = {}
    buttons_deg = {}
    for i in range(hafta):
        cursor.execute("SELECT * FROM veriler WHERE hafta = " + str(i + 1) + ".")
        rows = cursor.fetchall()
        frames[i] = Frame(window)
        frames[i].pack()
        if name:
            ref = db.reference(f"calisma_gunlugu/degerlendirmeler/{name}/{i + 1}")
            if ref.get() != None:
                for k,j in ref.get().items():
                    dataz[i] = j
                buttons_deg[i] = Button(frames[i],text="Değerlendirmeyi Gör")
                buttons_deg[i].bind("<Button-1>", degerlendir)
                buttons_deg[i].pack()
        if i != 0:
            frames[i].pack_forget()
        for j in range(len(rows)):
            day_number = j + 1
            buttons[j + 1] = Button(frames[i], text=day_number, width=5, height=2)
            buttons[j + 1].pack()
            buttons[j + 1].bind("<Button-1>", info)

window.mainloop()
