"""
Dijital Kutuphane Sistemi - Modern Grafik Arayuz (customtkinter)
Dark mode, yuvarlatilmis koseli, modern bir GUI.
siniflar.py icindeki Kitap, Uye ve Odunc siniflarini kullanir.
"""

import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk
from siniflar import Kitap, Uye


# Global tema ayarlari
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Tema renkleri (Treeview gibi sayfaya uyacak sekilde manuel ayarlanir)
BG = "#1a1a1a"
CARD_BG = "#212121"
ROW_BG = "#2b2b2b"
ROW_ALT = "#262626"
TEXT = "#e6e6e6"
SUBTEXT = "#9a9a9a"
ACCENT = "#3b82f6"
SUCCESS = "#22c55e"
WARNING = "#f59e0b"


class KutuphaneArayuz(ctk.CTk):
    """Modern dark-themed kutuphane arayuzu."""

    def __init__(self):
        super().__init__()
        self.title("Dijital Kutuphane")
        self.geometry("980x640")
        self.minsize(900, 600)

        # Veri depolari
        self.kitaplar = []
        self.uyeler = []
        self.oduncler = []

        self._tema_treeview()
        self._ust_bar()
        self._tab_view()

        self._ornek_veri_yukle()
        self._tablolari_yenile()

    # -------- Treeview icin dark stil --------
    def _tema_treeview(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Modern.Treeview",
            background=ROW_BG,
            foreground=TEXT,
            fieldbackground=ROW_BG,
            rowheight=30,
            borderwidth=0,
            font=("SF Pro Display", 12),
        )
        style.configure(
            "Modern.Treeview.Heading",
            background=CARD_BG,
            foreground=SUBTEXT,
            relief="flat",
            font=("SF Pro Display", 11, "bold"),
        )
        style.map(
            "Modern.Treeview",
            background=[("selected", ACCENT)],
            foreground=[("selected", "white")],
        )
        style.map("Modern.Treeview.Heading", background=[("active", CARD_BG)])

    # -------- Ust bar (header) --------
    def _ust_bar(self):
        header = ctk.CTkFrame(self, height=70, corner_radius=0, fg_color=CARD_BG)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        ic = ctk.CTkFrame(header, fg_color="transparent")
        ic.pack(side="left", padx=24, fill="y")

        ctk.CTkLabel(
            ic,
            text="📚  Dijital Kütüphane",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=TEXT,
        ).pack(side="left", pady=18)

        ctk.CTkLabel(
            ic,
            text="  •  OOP Ödev Projesi",
            font=ctk.CTkFont(size=13),
            text_color=SUBTEXT,
        ).pack(side="left", pady=18)

        # Sag taraf: istatistik rozetleri
        sag = ctk.CTkFrame(header, fg_color="transparent")
        sag.pack(side="right", padx=24, fill="y")

        self.rozet_kitap = self._rozet_olustur(sag, "📖", "0", "Kitap")
        self.rozet_kitap.pack(side="left", padx=6, pady=12)

        self.rozet_uye = self._rozet_olustur(sag, "👤", "0", "Üye")
        self.rozet_uye.pack(side="left", padx=6, pady=12)

        self.rozet_aktif = self._rozet_olustur(sag, "⏱", "0", "Aktif Ödünç")
        self.rozet_aktif.pack(side="left", padx=6, pady=12)

    def _rozet_olustur(self, parent, ikon, deger, baslik):
        kart = ctk.CTkFrame(parent, fg_color=BG, corner_radius=10, width=110, height=46)
        kart.pack_propagate(False)
        ic = ctk.CTkFrame(kart, fg_color="transparent")
        ic.pack(expand=True)
        ctk.CTkLabel(
            ic, text=f"{ikon} ", font=ctk.CTkFont(size=14)
        ).grid(row=0, column=0, rowspan=2, padx=(6, 2))
        lbl_deger = ctk.CTkLabel(
            ic, text=deger, font=ctk.CTkFont(size=16, weight="bold"), text_color=TEXT
        )
        lbl_deger.grid(row=0, column=1, sticky="w")
        ctk.CTkLabel(
            ic, text=baslik, font=ctk.CTkFont(size=10), text_color=SUBTEXT
        ).grid(row=1, column=1, sticky="w")
        kart.deger_label = lbl_deger
        return kart

    # -------- Sekmeli icerik --------
    def _tab_view(self):
        self.tabs = ctk.CTkTabview(self, fg_color=BG, segmented_button_selected_color=ACCENT)
        self.tabs.pack(fill="both", expand=True, padx=20, pady=(12, 20))

        self.tabs.add("Kitaplar")
        self.tabs.add("Üyeler")
        self.tabs.add("Ödünç / İade")
        self.tabs.add("Geçmiş")

        self._sayfa_kitaplar(self.tabs.tab("Kitaplar"))
        self._sayfa_uyeler(self.tabs.tab("Üyeler"))
        self._sayfa_islemler(self.tabs.tab("Ödünç / İade"))
        self._sayfa_gecmis(self.tabs.tab("Geçmiş"))

    # -------- Sayfa: Kitaplar --------
    def _sayfa_kitaplar(self, parent):
        # Sol: tablo
        sol = ctk.CTkFrame(parent, fg_color=CARD_BG, corner_radius=12)
        sol.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=8)

        ctk.CTkLabel(
            sol, text="Kitap Listesi", font=ctk.CTkFont(size=15, weight="bold"),
            text_color=TEXT
        ).pack(anchor="w", padx=16, pady=(14, 6))

        tablo_cer = ctk.CTkFrame(sol, fg_color=ROW_BG, corner_radius=8)
        tablo_cer.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        sutunlar = ("id", "ad", "yazar", "kategori", "durum")
        self.tablo_kitap = ttk.Treeview(
            tablo_cer, columns=sutunlar, show="headings",
            style="Modern.Treeview", height=18
        )
        for s, baslik, gen in [
            ("id", "ID", 50), ("ad", "Ad", 220), ("yazar", "Yazar", 150),
            ("kategori", "Kategori", 110), ("durum", "Durum", 100)
        ]:
            self.tablo_kitap.heading(s, text=baslik)
            self.tablo_kitap.column(s, width=gen, anchor="w")
        self.tablo_kitap.pack(fill="both", expand=True, padx=2, pady=2)

        # Sag: form karti
        sag = ctk.CTkFrame(parent, fg_color=CARD_BG, corner_radius=12, width=290)
        sag.pack(side="right", fill="y", pady=8)
        sag.pack_propagate(False)

        ctk.CTkLabel(
            sag, text="Yeni Kitap Ekle", font=ctk.CTkFont(size=15, weight="bold"),
            text_color=TEXT
        ).pack(anchor="w", padx=18, pady=(18, 12))

        self.giris_kitap_ad = self._form_alani(sag, "Kitap Adı")
        self.giris_kitap_yazar = self._form_alani(sag, "Yazar")
        self.giris_kitap_kategori = self._form_alani(sag, "Kategori")

        ctk.CTkButton(
            sag, text="＋  Kitap Ekle", height=42, corner_radius=10,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=ACCENT, hover_color="#2563eb",
            command=self._kitap_ekle
        ).pack(fill="x", padx=18, pady=(8, 18))

    def _form_alani(self, parent, label):
        ctk.CTkLabel(
            parent, text=label, font=ctk.CTkFont(size=11),
            text_color=SUBTEXT, anchor="w"
        ).pack(fill="x", padx=18, pady=(6, 2))
        e = ctk.CTkEntry(
            parent, height=36, corner_radius=8,
            fg_color=BG, border_color="#333", text_color=TEXT
        )
        e.pack(fill="x", padx=18, pady=(0, 4))
        return e

    def _kitap_ekle(self):
        ad = self.giris_kitap_ad.get().strip()
        yazar = self.giris_kitap_yazar.get().strip()
        kategori = self.giris_kitap_kategori.get().strip()
        if not (ad and yazar and kategori):
            messagebox.showwarning("Eksik bilgi", "Tüm alanları doldurun.")
            return
        kitap_id = len(self.kitaplar) + 1
        self.kitaplar.append(Kitap(kitap_id, ad, yazar, kategori))
        self.giris_kitap_ad.delete(0, "end")
        self.giris_kitap_yazar.delete(0, "end")
        self.giris_kitap_kategori.delete(0, "end")
        self._tablolari_yenile()

    # -------- Sayfa: Uyeler --------
    def _sayfa_uyeler(self, parent):
        sol = ctk.CTkFrame(parent, fg_color=CARD_BG, corner_radius=12)
        sol.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=8)

        ctk.CTkLabel(
            sol, text="Üye Listesi", font=ctk.CTkFont(size=15, weight="bold"),
            text_color=TEXT
        ).pack(anchor="w", padx=16, pady=(14, 6))

        tablo_cer = ctk.CTkFrame(sol, fg_color=ROW_BG, corner_radius=8)
        tablo_cer.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        sutunlar = ("id", "ad", "email", "aktif")
        self.tablo_uye = ttk.Treeview(
            tablo_cer, columns=sutunlar, show="headings",
            style="Modern.Treeview", height=18
        )
        for s, baslik, gen in [
            ("id", "ID", 50), ("ad", "Ad Soyad", 220),
            ("email", "Email", 260), ("aktif", "Aktif Ödünç", 100)
        ]:
            self.tablo_uye.heading(s, text=baslik)
            self.tablo_uye.column(s, width=gen, anchor="w")
        self.tablo_uye.pack(fill="both", expand=True, padx=2, pady=2)

        sag = ctk.CTkFrame(parent, fg_color=CARD_BG, corner_radius=12, width=290)
        sag.pack(side="right", fill="y", pady=8)
        sag.pack_propagate(False)

        ctk.CTkLabel(
            sag, text="Yeni Üye Ekle", font=ctk.CTkFont(size=15, weight="bold"),
            text_color=TEXT
        ).pack(anchor="w", padx=18, pady=(18, 12))

        self.giris_uye_ad = self._form_alani(sag, "Ad Soyad")
        self.giris_uye_email = self._form_alani(sag, "Email")

        ctk.CTkButton(
            sag, text="＋  Üye Ekle", height=42, corner_radius=10,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=ACCENT, hover_color="#2563eb",
            command=self._uye_ekle
        ).pack(fill="x", padx=18, pady=(8, 18))

    def _uye_ekle(self):
        ad = self.giris_uye_ad.get().strip()
        email = self.giris_uye_email.get().strip()
        if not (ad and email):
            messagebox.showwarning("Eksik bilgi", "Ad ve email gerekli.")
            return
        uye_id = len(self.uyeler) + 1
        self.uyeler.append(Uye(uye_id, ad, email))
        self.giris_uye_ad.delete(0, "end")
        self.giris_uye_email.delete(0, "end")
        self._tablolari_yenile()

    # -------- Sayfa: Odunc / Iade --------
    def _sayfa_islemler(self, parent):
        # Iki kart yan yana
        sol = ctk.CTkFrame(parent, fg_color=CARD_BG, corner_radius=12)
        sol.pack(side="left", fill="both", expand=True, padx=(0, 8), pady=8)

        ctk.CTkLabel(
            sol, text="📤  Ödünç Ver", font=ctk.CTkFont(size=15, weight="bold"),
            text_color=TEXT
        ).pack(anchor="w", padx=18, pady=(18, 12))

        ctk.CTkLabel(sol, text="Kitap", font=ctk.CTkFont(size=11),
                     text_color=SUBTEXT, anchor="w").pack(fill="x", padx=18, pady=(4, 2))
        self.combo_kitap = ctk.CTkComboBox(
            sol, height=38, state="readonly",
            fg_color=BG, border_color="#333", button_color=ACCENT,
            dropdown_fg_color=CARD_BG
        )
        self.combo_kitap.pack(fill="x", padx=18, pady=2)
        self.combo_kitap.set("")

        ctk.CTkLabel(sol, text="Üye", font=ctk.CTkFont(size=11),
                     text_color=SUBTEXT, anchor="w").pack(fill="x", padx=18, pady=(10, 2))
        self.combo_uye = ctk.CTkComboBox(
            sol, height=38, state="readonly",
            fg_color=BG, border_color="#333", button_color=ACCENT,
            dropdown_fg_color=CARD_BG
        )
        self.combo_uye.pack(fill="x", padx=18, pady=2)
        self.combo_uye.set("")

        ctk.CTkButton(
            sol, text="📤  Ödünç Ver", height=44, corner_radius=10,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=SUCCESS, hover_color="#16a34a",
            command=self._odunc_ver
        ).pack(fill="x", padx=18, pady=(20, 18))

        # Sag: iade
        sag = ctk.CTkFrame(parent, fg_color=CARD_BG, corner_radius=12)
        sag.pack(side="right", fill="both", expand=True, padx=(8, 0), pady=8)

        ctk.CTkLabel(
            sag, text="📥  İade Al", font=ctk.CTkFont(size=15, weight="bold"),
            text_color=TEXT
        ).pack(anchor="w", padx=18, pady=(18, 12))

        ctk.CTkLabel(sag, text="Aktif Ödünç", font=ctk.CTkFont(size=11),
                     text_color=SUBTEXT, anchor="w").pack(fill="x", padx=18, pady=(4, 2))
        self.combo_aktif = ctk.CTkComboBox(
            sag, height=38, state="readonly",
            fg_color=BG, border_color="#333", button_color=ACCENT,
            dropdown_fg_color=CARD_BG
        )
        self.combo_aktif.pack(fill="x", padx=18, pady=2)
        self.combo_aktif.set("")

        ctk.CTkButton(
            sag, text="📥  İade Al", height=44, corner_radius=10,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=WARNING, hover_color="#d97706",
            command=self._iade_al
        ).pack(fill="x", padx=18, pady=(20, 18))

    def _odunc_ver(self):
        k_idx = self.combo_kitap.cget("values").index(self.combo_kitap.get()) \
            if self.combo_kitap.get() in self.combo_kitap.cget("values") else -1
        u_idx = self.combo_uye.cget("values").index(self.combo_uye.get()) \
            if self.combo_uye.get() in self.combo_uye.cget("values") else -1
        if k_idx < 0 or u_idx < 0:
            messagebox.showwarning("Eksik seçim", "Kitap ve üye seçin.")
            return
        kitap = self._musait_kitaplar[k_idx]
        uye = self.uyeler[u_idx]
        odunc = uye.kitap_odunc_al(kitap, self.oduncler)
        if odunc:
            messagebox.showinfo("Tamam", f"'{kitap.ad}' {uye.ad} adına ödünç verildi.")
        self._tablolari_yenile()

    def _iade_al(self):
        secim = self.combo_aktif.get()
        degerler = self.combo_aktif.cget("values")
        if secim not in degerler:
            messagebox.showwarning("Eksik seçim", "İade edilecek ödünç seçin.")
            return
        idx = degerler.index(secim)
        odunc = self._aktif_oduncler[idx]
        odunc.uye.kitap_iade_et(odunc)
        messagebox.showinfo("Tamam", f"'{odunc.kitap.ad}' iade edildi.")
        self._tablolari_yenile()

    # -------- Sayfa: Gecmis --------
    def _sayfa_gecmis(self, parent):
        kart = ctk.CTkFrame(parent, fg_color=CARD_BG, corner_radius=12)
        kart.pack(fill="both", expand=True, pady=8)

        ctk.CTkLabel(
            kart, text="Tüm Ödünç İşlemleri",
            font=ctk.CTkFont(size=15, weight="bold"), text_color=TEXT
        ).pack(anchor="w", padx=18, pady=(18, 8))

        tablo_cer = ctk.CTkFrame(kart, fg_color=ROW_BG, corner_radius=8)
        tablo_cer.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        sutunlar = ("id", "kitap", "uye", "tarih", "durum")
        self.tablo_gecmis = ttk.Treeview(
            tablo_cer, columns=sutunlar, show="headings",
            style="Modern.Treeview", height=20
        )
        for s, baslik, gen in [
            ("id", "ID", 50), ("kitap", "Kitap", 240), ("uye", "Üye", 180),
            ("tarih", "Ödünç Tarihi", 130), ("durum", "Durum", 140)
        ]:
            self.tablo_gecmis.heading(s, text=baslik)
            self.tablo_gecmis.column(s, width=gen, anchor="w")
        self.tablo_gecmis.pack(fill="both", expand=True, padx=2, pady=2)

    # -------- Yenileme --------
    def _ornek_veri_yukle(self):
        self.kitaplar.append(Kitap(1, "Suç ve Ceza", "Dostoyevski", "Roman"))
        self.kitaplar.append(Kitap(2, "1984", "George Orwell", "Distopya"))
        self.kitaplar.append(Kitap(3, "Sefiller", "Victor Hugo", "Roman"))
        self.kitaplar.append(Kitap(4, "Olasılıksız", "Adam Fawer", "Bilim Kurgu"))
        self.kitaplar.append(Kitap(5, "Simyacı", "Paulo Coelho", "Roman"))
        self.uyeler.append(Uye(1, "Ahmet Yılmaz", "ahmet@mail.com"))
        self.uyeler.append(Uye(2, "Ayşe Demir", "ayse@mail.com"))
        self.uyeler.append(Uye(3, "Mehmet Kaya", "mehmet@mail.com"))

    def _tablolari_yenile(self):
        # Kitap tablosu
        self.tablo_kitap.delete(*self.tablo_kitap.get_children())
        for i, k in enumerate(self.kitaplar):
            tag = "evn" if i % 2 == 0 else "odd"
            self.tablo_kitap.insert(
                "", "end", values=(k.kitap_id, k.ad, k.yazar, k.kategori, k.durum.upper()),
                tags=(tag,)
            )
        self.tablo_kitap.tag_configure("evn", background=ROW_BG)
        self.tablo_kitap.tag_configure("odd", background=ROW_ALT)

        # Uye tablosu
        self.tablo_uye.delete(*self.tablo_uye.get_children())
        for i, u in enumerate(self.uyeler):
            tag = "evn" if i % 2 == 0 else "odd"
            self.tablo_uye.insert(
                "", "end", values=(u.uye_id, u.ad, u.email, len(u.aktif_oduncler)),
                tags=(tag,)
            )
        self.tablo_uye.tag_configure("evn", background=ROW_BG)
        self.tablo_uye.tag_configure("odd", background=ROW_ALT)

        # Gecmis tablosu
        self.tablo_gecmis.delete(*self.tablo_gecmis.get_children())
        for i, o in enumerate(self.oduncler):
            durum = "✓ İade Edildi" if o.iade_tarihi else "⏱ Devam Ediyor"
            tarih = o.odunc_tarihi.strftime("%d.%m.%Y")
            tag = "evn" if i % 2 == 0 else "odd"
            self.tablo_gecmis.insert(
                "", "end", values=(o.odunc_id, o.kitap.ad, o.uye.ad, tarih, durum),
                tags=(tag,)
            )
        self.tablo_gecmis.tag_configure("evn", background=ROW_BG)
        self.tablo_gecmis.tag_configure("odd", background=ROW_ALT)

        # Combobox'lar
        self._musait_kitaplar = [k for k in self.kitaplar if k.durum == "musait"]
        self.combo_kitap.configure(
            values=[f"[{k.kitap_id}] {k.ad}" for k in self._musait_kitaplar] or [""]
        )
        self.combo_kitap.set("")

        self.combo_uye.configure(
            values=[f"[{u.uye_id}] {u.ad}" for u in self.uyeler] or [""]
        )
        self.combo_uye.set("")

        self._aktif_oduncler = [o for o in self.oduncler if o.iade_tarihi is None]
        self.combo_aktif.configure(
            values=[f"#{o.odunc_id} {o.kitap.ad} → {o.uye.ad}" for o in self._aktif_oduncler] or [""]
        )
        self.combo_aktif.set("")

        # Rozetler
        self.rozet_kitap.deger_label.configure(text=str(len(self.kitaplar)))
        self.rozet_uye.deger_label.configure(text=str(len(self.uyeler)))
        self.rozet_aktif.deger_label.configure(text=str(len(self._aktif_oduncler)))


if __name__ == "__main__":
    app = KutuphaneArayuz()
    app.mainloop()
