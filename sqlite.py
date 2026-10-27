import sqlite3
import tkinter as tk
from tkinter import messagebox

DB_NAME = "nilai_siswa.db"

def buat_tabel():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT NOT NULL,
            biologi REAL NOT NULL,
            fisika REAL NOT NULL,
            inggris REAL NOT NULL,
            prediksi_fakultas TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def simpan_data(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas) "
        "VALUES (?, ?, ?, ?, ?)",
        (nama, biologi, fisika, inggris, prediksi),
    )
    conn.commit()
    conn.close()


def tentukan_prediksi(biologi, fisika, inggris):
    if biologi >= fisika and biologi >= inggris:
        return "Kedokteran"
    elif fisika >= biologi and fisika >= inggris:
        return "Teknik"
    else:
        return "Bahasa"


def hasil_prediksi():
    nama = entries["Nama Siswa"].get().strip()
    if not nama:
        messagebox.showwarning("Peringatan", "Nama siswa harus diisi.")
        return

    try:
        biologi = float(entries["Biologi"].get())
        fisika = float(entries["Fisika"].get())
        inggris = float(entries["Inggris"].get())
    except ValueError:
        messagebox.showwarning("Peringatan", "Nilai harus berupa angka.")
        return

    for n in (biologi, fisika, inggris):
        if n < 0 or n > 100:
            messagebox.showwarning("Peringatan", "Nilai harus antara 0 - 100.")
            return

    prediksi = tentukan_prediksi(biologi, fisika, inggris)
    simpan_data(nama, biologi, fisika, inggris, prediksi)

    hasil.config(text=f"Prediksi Fakultas: {prediksi}")
    messagebox.showinfo("Berhasil", "Data berhasil disimpan ke database.")

    for e in entries.values():
        e.delete(0, tk.END)


buat_tabel()

root = tk.Tk()
root.title("Aplikasi Prediksi Prodi Pilihan")
root.geometry("400x330")

judul = tk.Label(
    root,
    text="Aplikasi Prediksi Prodi Pilihan",
    font=("Arial", 14, "bold")
)
judul.grid(row=0, column=0, columnspan=2, pady=15)

kolom = ["Nama Siswa", "Biologi", "Fisika", "Inggris"]
entries = {}

for i, nama_kolom in enumerate(kolom, start=1):
    label = tk.Label(root, text=nama_kolom)
    label.grid(row=i, column=0, padx=15, pady=6, sticky="w")

    entry = tk.Entry(root, width=25)
    entry.grid(row=i, column=1, padx=10, pady=6)
    entries[nama_kolom] = entry

button = tk.Button(
    root,
    text="Submit Nilai",
    command=hasil_prediksi
)
button.grid(row=5, column=0, columnspan=2, pady=15)

hasil = tk.Label(
    root,
    text="",
    font=("Arial", 12, "bold"),
    fg="blue"
)
hasil.grid(row=6, column=0, columnspan=2, pady=5)

root.mainloop()