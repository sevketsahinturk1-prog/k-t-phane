"""
Dijital Kutuphane Sistemi - Sinif Tanimlari
Bu dosyada Kitap, Uye ve Odunc siniflari yer alir.
Her sinif sistemdeki bir varligi temsil eder.
"""

from datetime import datetime, timedelta


class Kitap:
    """Kutuphanedeki bir kitabi temsil eder."""

    def __init__(self, kitap_id, ad, yazar, kategori):
        self.kitap_id = kitap_id
        self.ad = ad
        self.yazar = yazar
        self.kategori = kategori
        # Durum: "musait" veya "odunc"
        self.durum = "musait"

    def kitap_durumu_degistir(self, yeni_durum):
        """Kitabin durumunu gunceller (musait / odunc)."""
        self.durum = yeni_durum

    def __str__(self):
        return f"[{self.kitap_id}] {self.ad} - {self.yazar} ({self.kategori}) - {self.durum.upper()}"


class Uye:
    """Kutuphane uyesini temsil eder."""

    def __init__(self, uye_id, ad, email):
        self.uye_id = uye_id
        self.ad = ad
        self.email = email
        # Uyenin elindeki aktif oduncler
        self.aktif_oduncler = []

    def kitap_odunc_al(self, kitap, odunc_listesi):
        """Verilen kitabi odunc alir. Yeni bir Odunc kaydi olusturur."""
        if kitap.durum != "musait":
            print(f"HATA: '{kitap.ad}' suanda musait degil.")
            return None
        odunc_id = len(odunc_listesi) + 1
        odunc = Odunc(odunc_id, kitap, self)
        kitap.kitap_durumu_degistir("odunc")
        self.aktif_oduncler.append(odunc)
        odunc_listesi.append(odunc)
        print(f"'{kitap.ad}' kitabi {self.ad} tarafindan odunc alindi.")
        return odunc

    def kitap_iade_et(self, odunc):
        """Verilen odunc kaydini iade eder."""
        if odunc not in self.aktif_oduncler:
            print("HATA: Bu odunc kaydi bu uyeye ait degil.")
            return
        odunc.kitap.kitap_durumu_degistir("musait")
        odunc.iade_tarihi = datetime.now()
        self.aktif_oduncler.remove(odunc)
        print(f"'{odunc.kitap.ad}' iade edildi.")

    def __str__(self):
        return f"[{self.uye_id}] {self.ad} - {self.email}"


class Odunc:
    """Bir odunc alma islemini temsil eder."""

    def __init__(self, odunc_id, kitap, uye):
        self.odunc_id = odunc_id
        self.kitap = kitap
        self.uye = uye
        self.odunc_tarihi = datetime.now()
        # Iade tarihi planlanan: 14 gun sonra (gercek iade yapilinca guncellenir)
        self.son_iade_tarihi = self.odunc_tarihi + timedelta(days=14)
        self.iade_tarihi = None  # Henuz iade edilmedi

    def __str__(self):
        durum = "Iade Edildi" if self.iade_tarihi else "Devam Ediyor"
        tarih = self.odunc_tarihi.strftime("%d.%m.%Y")
        return f"#{self.odunc_id} | {self.kitap.ad} -> {self.uye.ad} | {tarih} | {durum}"
