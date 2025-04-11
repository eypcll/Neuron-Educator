# 1) Bu program yildiz teknik universitesi EHM5108-Noron-Aglari dersinin odevinin ihtiyacini karsilayacak sekilde tasarlanmistir.
#   ders hocasi : tulay yildirim
# 2) Kullanmak icin once python3 kurulmalidir.
# 	Windows icin indirme linki:
# 		https://www.python.org/ftp/python/3.12.1/python-3.12.1-amd64.exe
# 	Ubuntu icin:
# 		sudo apt-get install python3
# 3) Windows kullanim:
# 	egitme.py dosyasinin oldugu klasor powershell ortaminda acilir.
# 	sonrasinda ornek data dosyalari metin dosyasi goruntuleyici ile incelenir.
# 	programin calistirmasini isteyecegimiz dataseti orneklere bakarak yazilir
# 	powershell e python3 ./egitme.py yazarak program calistirilir.
# 	program data setinin dosya adini soracaktir. dataseti dosyasinin adi yazilarak enter yapilir.
# 	program girdilerini ve ciktilarini -> giris-datalari ve cikis-datalari dosyasina yazar.
# 	istenilen sonuc datasini cikis-datalari dosyasi incelenerek kontrol edilir.
# 4) Ubuntu kulllanim:
# 	egitme.py dosyasinin oldugu klasor shell ortaminda acilir.
# 	sonrasinda ornek data dosyalari metin dosyasi goruntuleyici ile incelenir.
# 	programin calistirmasini isteyecegimiz dataseti orneklere bakarak yazilir
# 	shell e python3 ./egitme.py yazarak program calistirilir.
# 	program data setinin dosya adini soracaktir. dataseti dosyasinin adi yazilarak enter yapilir.
# 	program girdilerini ve ciktilarini -> giris-datalari ve cikis-datalari dosyasina yazar.
# 5) Onemli hususlar:
#   datalar json olarak kullanilmaktadir. json formatina uygun olayan datalarda hata verecektir. lutfen datalari json formatinda programa veriniz.

# yazar : eyup celal odabasioglu
# iletisim : eyupcelal96@gmail.com

import math
import json


def globals():
    global all_data


    filename = input("giris datalari dosya ismini giriniz --> \n")

    global cikis_datalari_file_name
    cikis_datalari_file_name = 'cikis-datalari'

    try:
        with open(filename,'r') as f:
            all_data = json.load(f)
    except:
        print("dosya gecersiz !!")
        exit(1)

    print("giris dosyasi --> " ,filename)
    print("cikis dosyasi --> ", cikis_datalari_file_name)
    
    with open('giris-datalari','w') as f:
        f.write(json.dumps(all_data,indent=4))

    global girisler
    
    girisler = all_data["girisler"]["x-degerleri"]

    global d_vektors

    d_vektors = all_data["girisler"]["d-degerleri"]

    global gecerli_ogrenme_kurali

    gecerli_ogrenme_kurali = all_data["ogrenme-kurali"]

    if gecerli_ogrenme_kurali == "perception" or gecerli_ogrenme_kurali == "delta" or gecerli_ogrenme_kurali == "widrow-hoff":
        if d_vektors:
            pass
        else:
            print("ogrenme algoritmasi d vektorlarini gerektiriyor !!")
            exit(1)

    global aktivasyon_fonksiyonu

    aktivasyon_fonksiyonu = all_data["aktivasyon-fonksiyonu"]

    global ogrenme_sabiti

    ogrenme_sabiti = all_data["ogrenme-sabiti"]

    global lamda

    lamda = all_data["lambda"]

    global egitme_adimi

    egitme_adimi = all_data["egitme-adimi"]

    global noron_agirlik_vektoru 

    noron_agirlik_vektoru = all_data["ilk-agirlik-vektoru"]

    global current_aktivasyon_fonk

    if aktivasyon_fonksiyonu == "bipolar-binary":
        current_aktivasyon_fonk = _bipolar_binary
    elif aktivasyon_fonksiyonu =="bipolar-surekli":
        current_aktivasyon_fonk = _bipolar_surekli
    else:
        print("aktivasyon fonksiyonu hatali!!")
        exit(1)

    global yuvarlama_ondalik_sayisi

    yuvarlama_ondalik_sayisi = all_data["yuvarlama-ondalik-sayisi"]

    global cikis_datalari

    cikis_datalari = {
        "agirlik-vektorleri" : [],
        "u-degerleri" : [],
        "delta-fonksiyon-sonuclari" : [],
        "widrow-hoff-fonksiyon-sonuclari" : [] ,
        "sonuncu-agirlik-vektoru" : []
    }


    pass


def _bipolar_surekli(u):
    return (2/(1+math.exp(-lamda*u))) - 1

def _bipolar_binary(u):
    if u >= 0: return 1 
    else: return -1 

def _turev_delta(u):
    return (1/2)*(1-(current_aktivasyon_fonk(u)**2))

def _turev_widrow_hoff(u):
    return 1

def _widrow_hoff(u):
    return u

def _algoritmaya_dayali_fonksiyon(u,d=None):

    if gecerli_ogrenme_kurali == "hebb":
        res = ogrenme_sabiti*current_aktivasyon_fonk(u)
        res = round(res,yuvarlama_ondalik_sayisi)
        return res
    elif gecerli_ogrenme_kurali == "perception":
        if current_aktivasyon_fonk(u) == d:
            return None
        else:
            return ogrenme_sabiti*(d-current_aktivasyon_fonk(u))
    elif gecerli_ogrenme_kurali == "delta":
        res = ogrenme_sabiti*(d-current_aktivasyon_fonk(u))*_turev_delta(u)
        res = round(res,yuvarlama_ondalik_sayisi)
        cikis_datalari["delta-fonksiyon-sonuclari"].append(res)
        return res
    elif gecerli_ogrenme_kurali == "widrow-hoff":
        res = ogrenme_sabiti*(d-_widrow_hoff(u))*_turev_widrow_hoff(u)
        res = round(res,yuvarlama_ondalik_sayisi)
        cikis_datalari["widrow-hoff-fonksiyon-sonuclari"].append(res)
        return res
    else:
        print("ogrenme algoritmasi hatali !!")
        exit(1)
    pass

def net(w,x):
    res = 0
    for k,v in enumerate(w):
        for l,t in enumerate(v):
            res += t*x[k]
    res = round(res,yuvarlama_ondalik_sayisi)
    return res

def vektor_carpim(sabit,vektor):
    yeni_vector = []
    for v in vektor:
        yeni_vector.append(round(v*sabit,yuvarlama_ondalik_sayisi))
    return yeni_vector

def vektor_toplam(vektor1,vektor2):
    yeni_vektor = []
    for k,v in enumerate(vektor1):
        # print(v,k)
        res = v[0]+vektor2[k]
        res = round(res,yuvarlama_ondalik_sayisi)
        yeni_vektor.append(res)
    return yeni_vektor

def yeni_agirlik_vektoru(agirlik_1,u,x,d=None):
    if d:
        agirlik_carpimi = _algoritmaya_dayali_fonksiyon(u,d)
    else:
        agirlik_carpimi = _algoritmaya_dayali_fonksiyon(u)
    if agirlik_carpimi:
        v = vektor_carpim(agirlik_carpimi,x)
        # print(v,agirlik_1)
        res = vektor_toplam(agirlik_1,v)
        # print(res)
        yeni_vektor = []
        for r in res:
            yeni_vektor.append([r])
        # print(yeni_vektor)
        return yeni_vektor
    else:
        return agirlik_1


if __name__ == "__main__":
    global all_data
    globals()

    giris_sayisi = len(girisler)
    
    w = noron_agirlik_vektoru
    giris = 0
    w_old = noron_agirlik_vektoru
    find_counter = 0
    cikis_datalari["agirlik-vektorleri"].append(w)
    for adim in range(0,egitme_adimi):
        # print(giris)
        u = net(w,girisler[giris])
        cikis_datalari["u-degerleri"].append(u)
        if d_vektors:
            w = yeni_agirlik_vektoru(w,u,girisler[giris],d_vektors[giris])
            if w_old == w:
                find_counter +=1
        else:
            w = yeni_agirlik_vektoru(w,u,girisler[giris])
        
        cikis_datalari["agirlik-vektorleri"].append(w)
        giris +=1
        if giris > giris_sayisi -1:
            if find_counter == giris_sayisi:
                break
            else:
                find_counter = 0
            giris = 0
        w_old = w
        pass
    # print(w)
    cikis_datalari["sonuncu-agirlik-vektoru"] = w
    with open(cikis_datalari_file_name,'w') as f:
        f.write(json.dumps(cikis_datalari,indent=4))

    
