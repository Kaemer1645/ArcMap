# -*- coding: utf-8 -*-
"""ArcMap_Douglas_Peucker_Algorithm.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OKcs64L00Cb56Yumh-JL5LaBsQGVLsdj
"""

# -*- coding: utf-8 -*-
import arcpy, os
#rozbudowa funkcjonalnosci arcgis w przetwarzaniu danych przestrzennych
arcpy.env.overwriteOutput = True
def alg_douglas_peucker():
    try:
        #ustawienie sciezek pliku wejsciowego i wyjsciowego
        dane_geometria=arcpy.GetParameterAsText(0)
        shape=arcpy.GetParameterAsText(1)
        kursor_czytania=arcpy.da.SearchCursor(dane_geometria, ["SHAPE@"])
        arcpy.CreateFeatureclass_management(os.path.dirname(shape), os.path.basename(shape), "POLYLINE")
        cur_gml = arcpy.da.SearchCursor(dane_geometria,field_names="gml_id")
        arcpy.AddField_management(shape, "gml_ID", "TEXT", 30)
        cur = arcpy.da.InsertCursor(shape, ["SHAPE@","gml_ID"])
        #ustalenie parametru tolerancji
        tolerancja=arcpy.GetParameter(2)
        lista=[]
        gmly=[]
        #listy do odczytania geometrii i identyfikatora gml_ID z pliku wejsciowego
        for rowki in cur_gml:
            gmly.append(rowki)
        for row_czy in kursor_czytania:
            lista2 = czytaj2(row_czy[0])
            lista.append(lista2)
        listanowaobiekty=[]
        numeracja=-1
        #petfla for wchodzaca do pojedynczego obiektu w liscie ze wszystkimi liniami
        for obiekt in lista:
            numeracja+=1
            arcpy.AddWarning('Obiekt numer ***'+str(numeracja)+'***')
            pocz1=obiekt[0][0]
            kon1=obiekt[-1][0]
            listanum=[pocz1,kon1]
            warunek=1
            #funkcja while dzialajaca do momentu spelnienia wartosci boolowskiej
            while warunek==1:
                dopisz=[]
                licz=0
                #petla for ktora dzieli prosta w sposob poczatek-najwiekszy, najwiekszy-koniec itd.
                for k in range(0,(len(listanum)-1)):
                    max=-1
                    nrpocz=listanum[licz] #0
                    nrkon=listanum[licz+1]  #34
                    malyobiekt=obiekt[nrpocz:nrkon+1]
                    skrajne = prosta(obiekt[nrpocz][1], obiekt[nrpocz][2], obiekt[nrkon][1], obiekt[nrkon][2])
                    for wierzcholek in malyobiekt:
                        nrwie=wierzcholek[0]
                        odl=odleglosc_od_prostej(skrajne[0],skrajne[1],skrajne[2],wierzcholek[1],wierzcholek[2])
                        if pocz1==kon1:
                            continue
                        #wypisywanie odleglosci najwiekszej
                        if odl>max:
                            max=odl
                            nrmax=nrwie
                        else:    
                            arcpy.AddMessage('')
                    licz+=1
                    #sprawdzenie warunku tolerancji
                    if max>tolerancja:
                        dopisz.append(nrmax)
                nowalista=[]
                for f in listanum:
                    dopisz.append(f)        
                for p in dopisz:
                    nowalista.append(p)
                nowalista.sort()
                if nowalista!=listanum:
                    listanum=(nowalista)
                else:
                    warunek=0
            listanowaobiekty.append(listanum)
        #kod zapisujacy geometrie uproszczonego obiektu wraz z identyfikatorem gml_id
        i=-1
        for linia in listanowaobiekty:
            i+=1
            zakres=arcpy.Array()
            for wierzcholek in linia:
                zakres.add(arcpy.Point(lista[i][wierzcholek][1], lista[i][wierzcholek][2]))
                polilinia = arcpy.Polyline(zakres)
            cur.insertRow([polilinia,gmly[i][0]])
    #obsługa wyjątków
    except Exception, err:
        arcpy.AddError("blad alg_douglas_peucker")
        arcpy.AddError(sys.exc_traceback.tb_lineno)
        arcpy.AddError(err.message)
    finally:
            pass
#funkcja obliczajaca parametry A,B,C prostej
def prosta(x1,y1,x2,y2):
    try:
        if x1==x2 and y1==y2:
            arcpy.AddWarning('ERROR - PRZERWA W PROSTEJ - ZAPISZ JĄ JAKO OSOBNY OBIEKT')
        else:
            A=(y2-y1)/(x2-x1)
            B=-1
            C=y1-A*x1
            wspolczynniki=[A,B,C]
            return wspolczynniki
    # obsługa wyjątków
    except Exception, err:
        arcpy.AddError("blad prosta")
        arcpy.AddError(sys.exc_traceback.tb_lineno)
        arcpy.AddError(err.message)
    finally:
            pass
#funkcja liczaca odleglosc punktu od prostej
from math import sqrt
def odleglosc_od_prostej(A,B,C,xp,yp):
    try:
        odl_od_prostej=abs(A*xp+B*yp+C)/sqrt(A**2+B**2)
        return odl_od_prostej
    except Exception, err:
        arcpy.AddError("blad prosta")
        arcpy.AddError(sys.exc_traceback.tb_lineno)
        arcpy.AddError(err.message)
    finally:
            pass
# funkcja odczytujaca z pliku wejsciowego (geometrycznego) numer punktu oraz wspolrzedne x i y, nastepnie zwracajaca liste list
def czytaj2(geometria):
    ##-- geometria - obiekt geometryczny ArcGIS
    try:
        lista = []
        i = 0
        partnum = 0
        for part in geometria:
            pntcount = 0 
            for pnt in part:
                if pnt:
                    lista.append([pntcount, pnt.X, pnt.Y])  #x i y to metody
                    pntcount += 1 
            partnum +=1
        i +=1
        return lista
    # obsługa wyjątków
    except Exception, err:
        arcpy.AddError("blad czytaj2")
        arcpy.AddError(sys.exc_traceback.tb_lineno)
        arcpy.AddError(err.message)
    finally:
        del(i, partnum, pntcount, part, pnt, geometria, lista)
if __name__ == '__main__':
    alg_douglas_peucker()