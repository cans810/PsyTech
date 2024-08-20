def istege_gore_yuvarla(sayi):
    tam_kisim = int(sayi)  # Tam kısmı al
    ondalik_kisim = sayi - tam_kisim  # Ondalık kısmı al

    if ondalik_kisim > 0.5:  # Ondalık kısım 0.5'ten büyükse
        return tam_kisim + 1  # Yukarı yuvarla
    else:
        return tam_kisim  # Aşağı yuvarla veya sabit kal


def Bilmiyorum_Alt_Olcek(liste):
    """Boş kontorlü yapılacak function"""

    count_bos = liste.count("Boş")

    if count_bos > 0:
        print("Number of 'BOŞ' in the array:", count_bos)
        print("Indices where 'BOŞ' is found:")
        for index, value in enumerate(liste):
            if value == "Boş":
                print(index)
    else:
        print("No 'BOŞ' found in the array")

    return count_bos


def Erkek_L_Alt_Olcek(liste):
    """ort 6.45 ss  2.74"""

    hampuan = 0
    ortalama = 6.45
    ss = 2.74

    secilen_indexler = [14, 29, 44, 59, 74, 89, 104, 119, 134, 149, 164, 194
                        , 224, 254, 284]

    for index in secilen_indexler:
        if 0 <= index < len(liste):
            deger = liste[index]
            if deger == "Yanlış":
                hampuan += 1

    L_hesaplama = 10*(hampuan-ortalama)
    L_T_puanı = 50+(L_hesaplama/ss)

    return hampuan, round(L_T_puanı,2)


def Kadin_L_Alt_Olcek(liste):
    """ort 6 ss  2.25"""

    hampuan = 0
    ortalama = 6
    ss = 2.25

    secilen_indexler = [14, 29, 44, 59, 74, 89, 104, 119, 134, 149, 164, 194
                        , 224, 254, 284]

    for index in secilen_indexler:
        if 0<= index < len(liste):
            deger = liste[index]
            if deger =="Yanlış":
                hampuan +=1

    L_hesaplama = 10*(hampuan-ortalama)
    L_T_puanı = 50+(L_hesaplama/ss)

    return hampuan, round(L_T_puanı,2)


## F Alt Ölçeği
def Erkek_F_Alt_Olcek(liste):
    """ort 8.3 ss  4,62"""
    hampuan = 0
    ortalama = 8.3
    ss = 4.62

    Dcevap_indexler = [13,22,26,30,33,34,39,41,47,48,49
                       ,52,55,65,84,120,122,138,145,150,155,
                       167,183,196,199,201,204,205,208,209,
                       210,214,217,226,244,245,246,251,255,
                       268,274,285,290,292]

    Ycevap_indexler = [16,19,53,64,74,82,111,112,114,
                       163,168,176,184,195,198,219,
                       256,257,271,275]

    for index in Dcevap_indexler:
        if 0 <= index < len(liste):
            deger = liste[index]
            if deger =="Doğru":
                hampuan +=1


    for index in Ycevap_indexler:
        if 0 <=index < len(liste):
            deger = liste[index]
            if deger == "Doğru":
                hampuan +=1

    F_hesaplama = 10*(hampuan-ortalama)
    F_T_Puanı = 50+(F_hesaplama/ss)

    return hampuan, round(F_T_Puanı,2)

def Kadin_F_Alt_Olcek(liste):
    """ort 9.38 ss  5.16"""
    hampuan = 0
    ortalama = 9.38
    ss = 5.16

    Dcevap_indexler = [13,22,26,30,33,34,39,41,47,48,49
                       ,52,55,65,84,120,122,138,145,150,155,
                       167,183,196,199,201,204,205,208,209,
                       210,214,217,226,244,245,246,251,255,
                       268,274,285,290,292]

    Ycevap_indexler = [16,19,53,64,74,82,111,112,114,
                       163,168,176,184,195,198,219,
                       256,257,271,275]

    for index in Dcevap_indexler:
        if 0<= index < len(liste):
            deger = liste[index]
            if deger =="Doğru":
                hampuan +=1


    for index in Ycevap_indexler:
        if 0 <=index < len(liste):
            deger = liste[index]
            if deger == "Doğru":
                hampuan +=1

    F_hesaplama = 10*(hampuan-ortalama)
    F_T_Puanı = 50+(F_hesaplama/ss)

    return hampuan, round(F_T_Puanı,2)


## K Alt Ölçeği

def Erkek_K_Alt_Olcek(liste):
    #ortalama 13.19 ss 4.65
    secilen_indexler = [29, 38, 70, 88, 123, 128, 133, 137, 141, 147, 159, 169, 170, 179, 182, 216, 233, 266, 271, 295, 315, 321, 373, 382, 396, 397, 405, 460, 501]

    hampuan = 0
    ortalama = 13.19
    ss = 4.65
    for index in secilen_indexler:
        if 0 <= index < len(liste):
            deger = liste[index]
            if deger == "Yanlış":
                hampuan +=1

    # 97. indeksi özel olarak kontrol et
    if liste[95] == "Doğru":
        hampuan += 1
    elif liste[95] == "Yanlış":
        hampuan += 0

    K_hesaplama = 10*(hampuan-ortalama)
    K_T_puanı = 50+(K_hesaplama/ss)

    return hampuan, round(K_T_puanı,2)


def Kadin_K_Alt_Olcek(liste):
    #ortalama 11.82 ss 3.8
    secilen_indexler = [29, 38, 70, 88, 123, 128, 133, 137, 141, 147, 159, 169, 170, 179, 182, 216, 233, 266, 271, 295, 315, 321, 373, 382, 396, 397, 405, 460, 501]

    hampuan = 0
    ortalama = 11.82
    ss = 3.8
    for index in secilen_indexler:
        if 0 <= index < len(liste):
            deger = liste[index]
            if deger == "Yanlış":
                hampuan +=1

    # 97. indeksi özel olarak kontrol et
    if liste[95] == "Doğru":
        hampuan += 1
    elif liste[95] == "Yanlış":
        hampuan += 0

    K_hesaplama = 10*(hampuan-ortalama)
    K_T_puanı = 50+(K_hesaplama/ss)

    return hampuan, round(K_T_puanı,2)


## Hs Alt Ölçeği
def Erkek_Hs_Alt_Olcek(liste):
    #Ortalama 13.19 Standart Sapna 4.07
    ortalama = 13.19
    standartSapma = 4.07
    hampuan=0
    Dcevap_indexler = [1, 2, 6, 8, 17, 50, 54, 62, 67, 102, 129, 152, 154, 162, 174, 187, 189, 191, 229, 242, 273, 280]

    for index in Dcevap_indexler:
        if 0 <= index < len(liste):
            deger = liste[index]
            if deger =="Yanlış":
                hampuan +=1

    #Cevap anahtarında doğru olan soru numaraları
    #23,29,43,62,72,108,114,125,161,189,273
    Ycevap_indexler=[22, 28, 42, 61, 71, 107, 113, 124, 160, 188, 272]
    for index in Ycevap_indexler:
        if 0 <= index < len(liste):
            deger = liste[index]
            if deger == "Doğru":
                hampuan +=1

    hampuan_K_Alt, K_Alt_Olcek = Erkek_K_Alt_Olcek(liste)

    Hs_hesaplama = 10 * (hampuan - ortalama)
    Hs_T_puanı = (50 + (Hs_hesaplama / standartSapma)) + (hampuan_K_Alt * 0.5)

    return hampuan, round(Hs_T_puanı, 2)

def Kadin_Hs_Alt_Olcek(liste):
    #Ortalama 15.89 Standart Sapna 4.88
    ortalama = 15.89
    standartSapma = 4.88
    hampuan=0
    Dcevap_indexler = [1, 2, 6, 8, 17, 50, 54, 62, 67, 102, 129, 152, 154, 162, 174, 187, 189, 191, 229, 242, 273, 280]

    for index in Dcevap_indexler:
        if 0 <= index < len(liste):
            deger = liste[index]
            if deger == "Yanlış":
                hampuan +=1

    #Cevap anahtarında doğru olan soru numaraları
    #23,29,43,62,72,108,114,125,161,189,273
    Ycevap_indexler=[22, 28, 42, 61, 71, 107, 113, 124, 160, 188, 272]
    for index in Ycevap_indexler:
        if 0 <= index < len(liste):
            deger = liste[index]
            if deger == "Doğru":
                hampuan +=1

    hampuan_K_Alt, K_Alt_Olcek = Kadin_K_Alt_Olcek(liste)

    Hs_hesaplama = 10 * (hampuan - ortalama)
    Hs_T_puanı = (50 + (Hs_hesaplama / standartSapma)) + (hampuan_K_Alt * 0.5)

    return hampuan, round(Hs_T_puanı,2)

## D Alt Ölçeği
def Erkek_D_Alt_Olcek(liste):
    #ort 20.63 ss = 4.76
    ort = 20.63
    ss=4.76
    hampuan=0
    Dcevap_indexler = [4, 12, 22, 31, 40, 42, 51, 66, 85, 103, 129, 137, 141, 157, 158, 181, 188, 192, 235, 258]
    Ycevap_indexler = [1, 7, 8, 17, 29, 35, 38, 45, 50, 56, 57, 63, 79, 87, 88, 94, 97, 106, 121, 130, 144, 151, 152, 153, 154, 159, 177, 190, 206, 207, 232, 240, 241, 247, 262, 269, 270, 284, 295]


    for index in Dcevap_indexler:
        if 0 <= index < len(liste):
            deger = liste[index]
            if deger == "Doğru":
                hampuan +=1

    for index in Ycevap_indexler:
        if 0 <= index < len(liste):
            deger = liste[index]
            if deger == 'Yanlış':
                hampuan +=1

    D_hesaplama = 10*(hampuan-ort)
    D_T_puanı = 50+(D_hesaplama/ss)

    return hampuan, round(D_T_puanı,2)

def Kadin_D_Alt_Olcek(liste):
    #ort 23.86 ss = 5.08
    ort = 23.86
    ss = 5.08
    hampuan=0
    Dcevap_indexler = [4, 12, 22, 31, 40, 42, 51, 66, 85, 103, 129, 137, 141, 157, 158, 181, 188, 192, 235, 258]
    Ycevap_indexler = [1, 7, 8, 17, 29, 35, 38, 45, 50, 56, 57, 63, 79, 87, 88, 94, 97, 106, 121, 130, 144, 151, 152, 153, 154, 159, 177, 190, 206, 207, 232, 240, 241, 247, 262, 269, 270, 284, 295]


    for index in Dcevap_indexler:
        if 0 <= index < len(liste):
            deger = liste[index]
            if deger == "Doğru":
                hampuan +=1

    for index in Ycevap_indexler:
        if 0 <= index < len(liste):
            deger = liste[index]
            if deger == 'Yanlış':
                hampuan +=1

    D_hesaplama = 10*(hampuan-ort)
    D_T_puanı = 50+(D_hesaplama/ss)

    return hampuan, round(D_T_puanı,2)


## HY Alt ölçeği
def Erkek_Hy_Alt_Olcek(liste):
    #ort 19.31 ss 4.71
    hampuan = 0
    ort = 19.31
    ss = 4.71
    Dcevap_indexler = [9, 22, 31, 42, 43, 46, 75, 113, 178, 185, 188, 237, 252]
    Ycevap_indexler = [1, 2, 5, 6, 7, 8, 11, 25, 29, 50, 54, 70, 88, 92, 102, 106, 108, 123, 127, 128, 135, 136, 140, 146, 152, 159, 161, 162, 169, 171, 173, 174, 179, 187, 189, 191, 200, 212, 229, 233, 242, 264, 266, 273, 278, 288, 291]


    for index in Dcevap_indexler:
        deger = liste[index]
        if deger == "Doğru":
            hampuan +=1

    for index in Ycevap_indexler:
        if 0 <= index < len(liste):
            deger = liste[index]
            if deger == "Yanlış":
                hampuan +=1

    Hy_hesaplama = 10*(hampuan - ort)
    Hy_T_puanı = 50+(hampuan / ss)

    return hampuan, round(Hy_T_puanı,2)

def Kadin_Hy_Alt_Olcek(liste):
    #ort 22.33 ss 5.31
    hampuan = 0
    ort = 22.33
    ss=5.31
    Dcevap_indexler = [9, 22, 31, 42, 43, 46, 75, 113, 178, 185, 188, 237, 252]
    Ycevap_indexler = [1, 2, 5, 6, 7, 8, 11, 25, 29, 50, 54, 70, 88, 92, 102, 106, 108, 123, 127, 128, 135, 136, 140, 146, 152, 159, 161, 162, 169, 171, 173, 174, 179, 187, 189, 191, 200, 212, 229, 233, 242, 264, 266, 273, 278, 288, 291]


    for index in Dcevap_indexler:
        deger = liste[index]
        if deger == "Doğru":
            hampuan +=1

    for index in Ycevap_indexler:
        if 0 <= index < len(liste):
            deger = liste[index]
            if deger == "Yanlış":
                hampuan +=1

    Hy_hesaplama = 10*(hampuan - ort)
    Hy_T_puanı = 50+(hampuan / ss)

    return hampuan, round(Hy_T_puanı,2)


## PD Alt Ölçeği
def Erkek_Pd_Alt_Olcek(liste):
    """ort 22.22 ss 4.45"""
    hampuan= 0
    ort = 22.22
    ss = 4.45
    Dcevap_indexler = [15, 20, 23, 31, 32, 34, 37, 41, 60, 66, 83, 93, 101, 105, 109, 117, 126, 214, 215, 223, 238, 243, 244, 283]
    Ycevap_indexler = [7, 19, 36, 81, 90, 95, 106, 133, 136, 140, 154, 169, 170, 172, 179, 182, 200, 230, 234, 236, 247, 266, 286, 288, 293, 295]


    for index in Dcevap_indexler:
        if 0 <= index < len(liste):
            deger = liste[index]
            if deger == "Doğru":
                hampuan +=1

    for index in Ycevap_indexler:
        if 0 <= index < len(liste):
            deger = liste[index]
            if deger == "Yanlış":
                hampuan +=1

    Pd_hesaplama = 10*(hampuan - ort)
    Pd_T_puanı = 50+(hampuan / ss)

    return hampuan, round(Pd_T_puanı,2)

def Kadin_Pd_Alt_Olcek(liste):
    """ort 22.84 ss 4.51"""
    hampuan= 0
    ort = 22.84
    ss = 4.51
    Dcevap_indexler = [15, 20, 23, 31, 32, 34, 37, 41, 60, 66, 83, 93, 101, 105, 109, 117, 126, 214, 215, 223, 238, 243, 244, 283]

    Ycevap_indexler = [7, 19, 36, 81, 90, 95, 106, 133, 136, 140, 154, 169, 170, 172, 179, 182, 200, 230, 234, 236, 247, 266, 286, 288, 293, 295]


    for index in Dcevap_indexler:
        if 0 <= index < len(liste):
            deger = liste[index]
            if deger == "Doğru":
                hampuan +=1

    for index in Ycevap_indexler:
        if 0 <= index < len(liste):
            deger = liste[index]
            if deger == "Yanlış":
                hampuan +=1

    Pd_hesaplama = 10*(hampuan - ort)
    Pd_T_puanı = 50+(hampuan / ss)

    return hampuan, round(Pd_T_puanı,2)


## MF Alt Ölçeği
def Erkek_Mf_Alt_Olcek(liste):
    """ort 29.21 ss 3.82"""
    hampuan=0
    ort = 29.21
    ss=3.82
    Dcevap_indexler = [3, 24, 68, 69, 73, 76, 77, 86, 91, 125, 131, 133, 139, 148, 178, 186, 202, 203, 216, 225, 230, 238, 260, 277, 281, 294, 296, 298]

    Ycevap_indexler = [0, 18, 25, 27, 78, 79, 80, 88, 98, 111, 114, 115, 116, 119, 132, 143, 175, 197, 212, 213, 218, 220, 222, 228, 248, 253, 259, 261, 263, 279, 282, 299]


    for index in Dcevap_indexler:
        if 0 <= index < len(liste):
            deger = liste[index]
            if deger == "Doğru":
                hampuan +=1

    for index in Ycevap_indexler:
        if 0 <= index < len(liste):
            deger=liste[index]
            if deger == "Yanlış":
                hampuan +=1


    Mf_hesaplama = 10*(hampuan - ort)
    Mf_T_puanı = 50+(hampuan / ss)

    return hampuan, round(Mf_T_puanı,2)

def Kadin_Mf_Alt_Olcek(liste):
    """ort 32.98 ss 3.67"""
    hampuan=0
    ort = 32.98
    ss=3.67
    Dcevap_indexler = [3, 24, 69, 73, 76, 77, 86, 91,
                       125, 131,132, 133, 139, 148, 186,
                       202, 203, 216, 225, 238, 260,
                       277, 281, 294, 298]

    Ycevap_indexler = [0, 18, 25, 27, 68, 78, 79, 80, 88, 98, 111, 114,115, 116, 119, 132, 143, 175,178, 197, 212, 213, 218, 220, 222, 228,230, 248, 253, 259, 261, 263, 279, 282, 296,299]


    for index in Dcevap_indexler:
        if 0 <= index < len(liste):
            deger = liste[index]
            if deger == "Doğru":
                hampuan +=1

    for index in Ycevap_indexler:
        if 0 <= index < len(liste):
            deger=liste[index]
            if deger == "Yanlış":
                hampuan +=1


    Mf_hesaplama = 10*(hampuan - ort)
    Mf_T_puanı = 50+(hampuan / ss)

    return hampuan, round(Mf_T_puanı,2)


## PA Alt ölçek
def Erkek_Pa_Alt_Olcek(liste):
    """ort 11.12 ss 4.03"""
    hampuan = 0
    ort = 11.12
    ss = 4.03
    Dcevap_indexler = [14, 15, 21, 23, 26, 34, 109, 120, 122, 126, 150, 156, 157, 201, 274, 283, 290, 292, 298, 304, 316, 337, 340, 363, 364]

    Ycevap_indexler = [92, 106, 108, 110, 116, 123, 267, 280, 293, 312, 315, 318, 326, 346, 347]

    for index in Dcevap_indexler:
        if 0 <= index < len(liste):
            deger = liste[index]
            if deger == "Doğru":
                hampuan +=1

    for index in Ycevap_indexler:
        if 0<= index < len(liste):
            deger=liste[index]
            if deger=="Yanlış":
                hampuan += 1


    Pa_hesaplama = 10*(hampuan-ort)
    Pa_T_Puanı = 50+(Pa_hesaplama/ss)

    return hampuan, round(Pa_T_Puanı,2)


def Kadin_Pa_Alt_Olcek(liste):
    """ort 11.93 ss 4.17"""
    hampuan = 0
    ort = 11.93
    ss = 4.17
    Dcevap_indexler = [14, 15, 21, 23, 26, 34, 109, 120, 122, 126, 150, 156, 157, 201, 274, 283, 290, 292, 298, 304, 316, 337, 340, 363, 364]

    Ycevap_indexler = [92, 106, 108, 110, 116, 123, 267, 280, 293, 312, 315, 318, 326, 346, 347]

    for index in Dcevap_indexler:
        if 0 <= index < len(liste):
            deger = liste[index]
            if deger == "Doğru":
                hampuan +=1

    for index in Ycevap_indexler:
        if 0<= index < len(liste):
            deger=liste[index]
            if deger=="Yanlış":
                hampuan += 1


    Pa_hesaplama = 10*(hampuan-ort)
    Pa_T_Puanı = 50+(Pa_hesaplama/ss)

    return hampuan, round(Pa_T_Puanı,2)


## PT Alt ölçek
def Erkek_Pt_Alt_Olcek(liste):
    """ort 27.90 ss 6.3"""
    hampuan = 0
    ort = 27.9
    ss = 6.3
    Dcevap_indexler = [9, 14, 21, 31, 40, 66, 75, 85, 93, 101, 105, 141, 158, 181, 188, 216, 237, 265, 300, 303, 304, 316, 320, 335, 336, 339, 341, 342, 343, 345, 348, 350, 351, 355, 356, 357, 358, 359, 360]

    Ycevap_indexler = [2, 7, 35, 121, 151, 163, 177, 328, 352]

    for index in Dcevap_indexler:
        if 0 <= index < len(liste):
            deger = liste[index]
            if deger == "Doğru":
                hampuan +=1

    for index in Ycevap_indexler:
        if 0 <= index < len(liste):
            deger=liste[index]
            if deger == "Yanlış":
                hampuan +=1

    Pt_hesaplama = 10*(hampuan-ort)
    Pt_T_puanı = 50+(Pt_hesaplama/ss)

    return hampuan, round(Pt_T_puanı,2)


def Kadin_Pt_Alt_Olcek(liste):
    """ort 29.9 ss 6.59"""
    hampuan = 0
    ort = 29.9
    ss = 6.59
    Dcevap_indexler = [9, 14, 21, 31, 40, 66, 75, 85, 93, 101, 105, 141, 158, 181, 188, 216, 237, 265, 300, 303, 304, 316, 320, 335, 336, 339, 341, 342, 343, 345, 348, 350, 351, 355, 356, 357, 358, 359, 360]

    Ycevap_indexler = [2, 7, 35, 121, 151, 163, 177, 328, 352]

    for index in Dcevap_indexler:
        if 0 <= index < len(liste):
            deger = liste[index]
            if deger == "Doğru":
                hampuan +=1

    for index in Ycevap_indexler:
        if 0 <= index < len(liste):
            deger=liste[index]
            if deger == "Yanlış":
                hampuan +=1

    Pt_hesaplama = 10*(hampuan-ort)
    Pt_T_puanı = 50+(Pt_hesaplama/ss)

    return hampuan, round(Pt_T_puanı,2)


## Sc Alt Ölçek
def Erkek_Sc_Alt_Olcek(liste):
    """ort 29.82 ss 9.05"""
    hampuan = 0
    ort =29.82
    ss = 9.05
    Dcevap_indexler = [14,15,20,21,23,31,32,34,37,39,
                       40,46,51,75,96,103,120,155,156,
                       158,167,178,181,193,201,209,211,
                       237,240,250,258,265,272,281,290,
                       296,300,302,304,306,311,319,323,
                       324,331,333,334,338,340,344,348,
                       349,351,353,354,355,359,362,363]
    Ycevap_indexler = [7,16,19,36,64,102,118,176,177,186,
                       191,195,219,275,280,305,308,321,329]

    for index in Dcevap_indexler:
        if 0 <= index < len(liste):
            deger = liste[index]
            if deger == "Doğru":
                hampuan +=1

    for index in Ycevap_indexler:
        if 0 <= index < len(liste):
            deger=liste[index]
            if deger=="Yanlış":
                hampuan += 1

    Sc_Hesaplama = 10*(hampuan-ort)
    Sc_T_Puanı = 50+(hampuan/ss)

    return hampuan, round(Sc_T_Puanı,2)



def Kadin_Sc_Alt_Olcek(liste):
    """ort 31.06 ss 8.2"""
    hampuan = 0
    ort =31.06
    ss = 8.2
    Dcevap_indexler = [14,15,20,21,23,31,32,34,37,39,
                       40,46,51,75,96,103,120,155,156,
                       158,167,178,181,193,201,209,211,
                       237,240,250,258,265,272,281,290,
                       296,300,302,304,306,311,319,323,
                       324,331,333,334,338,340,344,348,
                       349,351,353,354,355,359,362,363]
    Ycevap_indexler = [7,16,19,36,64,102,118,176,177,186,
                       191,195,219,275,280,305,308,321,329]

    for index in Dcevap_indexler:
        if 0 <= index < len(liste):
            deger = liste[index]
            if deger == "Doğru":
                hampuan +=1

    for index in Ycevap_indexler:
        if 0 <= index < len(liste):
            deger=liste[index]
            if deger=="Yanlış":
                hampuan += 1

    Sc_Hesaplama = 10*(hampuan-ort)
    Sc_T_Puanı = 50+(hampuan/ss)

    return hampuan, round(Sc_T_Puanı,2)


## MA Alt ölçek
def Erkek_Ma_Alt_Olcek(liste):
    """ort 19.96 ss 4.4 """
    hampuan = 0
    ort =19.96
    ss=4.4
    Dcevap_indexler = [10,12,20,21,58,63,72,96,99,
                       108,126,133,142,155,156,166,
                       180,193,211,221,225,227,231,
                       232,237,239,249,250,262,265,
                       267,270,276,278,297]
    Ycevap_indexler = [100,104,110,118,119,147,165,170,179,266,288]

    for index in Dcevap_indexler:
        if 0 <= index < len(liste):
            deger = liste[index]
            if deger == "Doğru":
                hampuan +=1


    for index in Ycevap_indexler:
        if 0 <= index < len(liste):
            deger=liste[index]
            if deger=="Yanlış":
                hampuan +=1


    Ma_Hesaplama = 10*(hampuan-ort)
    Ma_T_Puanı = 50+(hampuan/ss)

    return hampuan, round(Ma_T_Puanı,2)


def Kadin_Ma_Alt_Olcek(liste):
    """ort 19.72 ss 4.62 """
    hampuan = 0
    ort =19.72
    ss=4.62
    Dcevap_indexler = [10,12,20,21,58,63,72,96,99,
                       108,126,133,142,155,156,166,
                       180,193,211,221,225,227,231,
                       232,237,239,249,250,262,265,
                       267,270,276,278,297]
    Ycevap_indexler = [100,104,110,118,119,147,165,170,179,266,288]

    for index in Dcevap_indexler:
        if 0 <= index < len(liste):
            deger = liste[index]
            if deger == "Doğru":
                hampuan +=1


    for index in Ycevap_indexler:
        if 0 <= index < len(liste):
            deger=liste[index]
            if deger=="Yanlış":
                hampuan +=1


    Ma_Hesaplama = 10*(hampuan-ort)
    Ma_T_Puanı = 50+(hampuan/ss)

    return hampuan, round(Ma_T_Puanı,2)


## Si Alt ölçek
def Erkek_Si_Alt_Olcek(liste):
    """ort 25.86 ss 7.87"""
    ort = 25.86
    ss=7.87
    hampuan = 0
    Dcevap_indexler = [31,66,81,110,116,123,137,146,
                       170,171,179,200,235,266,277,
                       291,376,382,397,410,426,435,
                       454,472,486,548,563]
    Ycevap_indexler = [24,32,56,90,98,118,125,142,192,207,
                       228,230,253,261,280,295,308,352,358,
                       370,390,399,414,439,445,448,449,450,
                       461,468,478,480,481,504,520,546]

    for index in Dcevap_indexler:
        if 0 <= index < len(liste):
            deger = liste[index]
            if deger == "Doğru":
                hampuan +=1


    for index in Ycevap_indexler:
        if 0<= index < len(liste):
            deger=liste[index]
            if deger=="Yanlış":
                hampuan+=1


    Si_Hesaplama = 10*(hampuan-ort)
    Si_T_Puanı = 50+(hampuan/ss)

    return hampuan, round(Si_T_Puanı,2)

def Kadin_Si_Alt_Olcek(liste):
    """ort 29.88 ss 7.52"""
    ort = 89.88
    ss=7.52
    hampuan = 0
    Dcevap_indexler = [31,66,81,110,116,123,137,146,
                       170,171,179,200,235,266,277,
                       291,376,382,397,410,426,435,
                       454,472,486,548,563]
    Ycevap_indexler = [24,32,56,90,98,118,125,142,192,207,
                       228,230,253,261,280,295,308,352,358,
                       370,390,399,414,439,445,448,449,450,
                       461,468,478,480,481,504,520,546]

    for index in Dcevap_indexler:
        if 0 <= index < len(liste):
            deger = liste[index]
            if deger == "Doğru":
                hampuan +=1


    for index in Ycevap_indexler:
        if 0<= index < len(liste):
            deger=liste[index]
            if deger=="Yanlış":
                hampuan+=1


    Si_Hesaplama = 10*(hampuan*ort)
    Si_T_Puanı = 50+(hampuan/ss)

    return hampuan, round(Si_T_Puanı,2)