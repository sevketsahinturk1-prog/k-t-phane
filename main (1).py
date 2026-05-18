"""
Dijital Kutuphane Sistemi - Ana Program
Konsol tabanli menu ile sistemi yonetir.
"""

from siniflar import Kitap, Uye, Odunc


# Sistemdeki tum verileri tutan listeler
kitaplar = []
uyeler = []
oduncler = []


def ornek_veri_yukle():
    """Test icin baslangic verilerini ekler."""
    kitaplar.append(Kitap(1, "Suc ve Ceza", "Dostoyevski", "Roman"))
    kitaplar.append(Kitap(2, "1984", "George Orwell", "Distopya"))
    kitaplar.append(Kitap(3, "Sefiller", "Victor Hugo", "Roman"))
    kitaplar.append(Kitap(4, "Olasiliksiz", "Adam Fawer", "Bilim Kurgu"))

    uyeler.append(Uye(1, "Ahmet Yilmaz", "ahmet@mail.com"))
    uyeler.append(Uye(2, "Ayse Demir", "ayse@mail.com"))


def kitaplari_listele():
    """Tum kitaplari ekrana yazdirir."""
    print("\n--- KITAPLAR ---")
    if not kitaplar:
        print("Kayitli kitap yok.")
        return
    for k in kitaplar:
        print(k)


def uyeleri_listele():
    """Tum uyeleri ekrana yazdirir."""
    print("\n--- UYELER ---")
    if not uyeler:
        print("Kayitli uye yok.")
        return
    for u in uyeler:
        print(u)


def kitap_ekle():
    """Yeni bir kitap ekler."""
    kitap_id = len(kitaplar) + 1
    ad = input("Kitap adi: ")
    yazar = input("Yazar: ")
    kategori = input("Kategori: ")
    kitaplar.append(Kitap(kitap_id, ad, yazar, kategori))
    print("Kitap eklendi.")


def uye_ekle():
    """Yeni bir uye ekler."""
    uye_id = len(uyeler) + 1
    ad = input("Ad Soyad: ")
    email = input("Email: ")
    uyeler.append(Uye(uye_id, ad, email))
    print("Uye eklendi.")


def kitap_bul(kitap_id):
    """ID'ye gore kitap bulur, yoksa None doner."""
    for k in kitaplar:
        if k.kitap_id == kitap_id:
            return k
    return None


def uye_bul(uye_id):
    """ID'ye gore uye bulur, yoksa None doner."""
    for u in uyeler:
        if u.uye_id == uye_id:
            return u
    return None


def odunc_ver():
    """Bir uyeye kitap odunc verir."""
    kitaplari_listele()
    uyeleri_listele()
    try:
        k_id = int(input("Kitap ID: "))
        u_id = int(input("Uye ID: "))
    except ValueError:
        print("Gecersiz giris.")
        return

    kitap = kitap_bul(k_id)
    uye = uye_bul(u_id)
    if not kitap or not uye:
        print("Kitap veya uye bulunamadi.")
        return
    uye.kitap_odunc_al(kitap, oduncler)


def iade_al():
    """Aktif bir odunc kitabi iade alir."""
    aktif = [o for o in oduncler if o.iade_tarihi is None]
    if not aktif:
        print("Aktif odunc kayit yok.")
        return
    print("\n--- AKTIF ODUNCLER ---")
    for o in aktif:
        print(o)
    try:
        o_id = int(input("Iade edilecek odunc ID: "))
    except ValueError:
        print("Gecersiz giris.")
        return
    odunc = next((o for o in oduncler if o.odunc_id == o_id), None)
    if not odunc:
        print("Odunc kayit bulunamadi.")
        return
    odunc.uye.kitap_iade_et(odunc)


def odunc_gecmisi():
    """Tum odunc kayitlarini gosterir."""
    print("\n--- ODUNC GECMISI ---")
    if not oduncler:
        print("Henuz hicbir odunc islemi yapilmamis.")
        return
    for o in oduncler:
        print(o)


def menu():
    """Ana menuyu calistirir."""
    ornek_veri_yukle()
    while True:
        print("\n===== DIJITAL KUTUPHANE SISTEMI =====")
        print("1. Kitaplari listele")
        print("2. Uyeleri listele")
        print("3. Yeni kitap ekle")
        print("4. Yeni uye ekle")
        print("5. Kitap odunc ver")
        print("6. Kitap iade al")
        print("7. Odunc gecmisi")
        print("0. Cikis")
        secim = input("Seciminiz: ").strip()

        if secim == "1":
            kitaplari_listele()
        elif secim == "2":
            uyeleri_listele()
        elif secim == "3":
            kitap_ekle()
        elif secim == "4":
            uye_ekle()
        elif secim == "5":
            odunc_ver()
        elif secim == "6":
            iade_al()
        elif secim == "7":
            odunc_gecmisi()
        elif secim == "0":
            print("Cikis yapiliyor...")
            break
        else:
            print("Gecersiz secim, tekrar deneyin.")


if __name__ == "__main__":
    menu()
