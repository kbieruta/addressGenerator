##Plik przechowujący funkcję do wygenerowania pojedynczego adresu i wyświetlenia
    # go w aplikacji
def generateAddress():
    CREDENTIALS = {
        'wsdl': 'https://uslugaterytws1.stat.gov.pl/wsdl/terytws1.wsdl',
        'username': 'Kacper.Bieruta',
        'password': 'NYnvs1UmW'
    }
##Login i hasło użytkownika aplikacji API TERYT oraz link, za pomocą którego pobierane są dane

    import random
    from zeep import Client
    from zeep.wsse.username import UsernameToken
##Import z random oraz zeep pozwoli na losowe wybranie elementów pobieranych list oraz
    # dogodne odwołanie się do API TERYT w celu pobrania danych

    token = UsernameToken(
        username=CREDENTIALS['username'],
        password=CREDENTIALS['password']
    )
    client = Client(wsdl=CREDENTIALS['wsdl'], wsse=token)
##zmienna client przechowuje dane logowania wraz z adresem API w celu dalszych odwołań do niego

    provinceList = client.service.PobierzListeWojewodztw('2022-01-01')
    provinceList_length = len(provinceList)
    provinceRandom = provinceList[random.randint(provinceList_length - provinceList_length, provinceList_length - 1)]
    provinceRandomName = provinceRandom.NAZWA.title()
    provinceSymbol = provinceRandom.WOJ
###Część kodu pobierająca listę województw oraz losowo wybierająca jedno z nich

    countyList = client.service.PobierzListePowiatow(provinceSymbol, '2022-01-01')
    countyList_length = len(countyList)
    countyRandom = countyList[random.randint(countyList_length - countyList_length, countyList_length - 1)]
    countySymbol = countyRandom.POW
###Część kodu pobierająca listę powiatów oraz losowo wybierająca jedno z nich z zakresu
    # wylosowanego województwa

    communityList = client.service.PobierzListeGmin(provinceSymbol, countySymbol, '2022-01-01')
    communityList_length = len(communityList)
    communityType = "3"
##zmienna określająca warunek wyjścia z pętli losowania gminy. "3" oznacza gminę miejsko-wiejską, która
    #niefortunnie nie przechowuje żadnych danych o miejscowościach ani adresach. Pętla pomija gminy
    #miejsko-wiejskie jednocześnie nie ograniczając puli losowanych danych, ponieważ miejscowości
    #znajdują się pod gminami miejskimi oraz wiejskimi
    while communityType == "3":
        communityRandom = communityList[
            random.randint(communityList_length - communityList_length, communityList_length - 1)]
        communitySymbol = communityRandom.GMI
        communityType = communityRandom.RODZ
###Część kodu pobierająca listę gmin oraz losowo wybierająca jedno z nich z zakresu
    # wylosowanego powiatu

    townList = client.service.PobierzListeMiejscowosciWRodzajuGminy(provinceSymbol, countySymbol, communitySymbol,
                                                                    communityType, '2022-01-01')
    townList_length = len(townList)
    townCounter = 1
    if communityType == "1" or communityType == "4":
        townRandom = townList[0]
        while communityRandom.NAZWA.title() != townRandom.Nazwa.title():
            townRandom = townList[townCounter]
            townCounter = townCounter + 1
    else:
        townRandom = townList[random.randint(townList_length - townList_length, townList_length - 1)]
##Ponieważ w liście miejscowości TERYT umieszczono zarówno miejscowości wraz z znajdującymi się w nich
    #dzielnicami, a w samych dzielnicach nie ma informacji o poszczególnych ulicach to stworzona
    #została powyższa pętla. Ma ona na celu wybranie z pobranej listy elementu opisującego miejscowość
    #dla gmin miejskich oraz dla miast na prawach powiatu pomijając ich dzielnice.
    #Nie można było wybrać konkretnego elementu listy dla każdej gminy, ponieważ miejscowość została
    #umieszczona w losowym elemencie listy.
    townSymbol = townRandom.Symbol
    townRandomName = townRandom.Nazwa.title()
###Część kodu pobierająca listę miejscowości oraz losowo wybierająca jedną z nich z zakresu
    #wylosowanej gminy

    streetList = client.service.PobierzListeUlicDlaMiejscowosci(provinceSymbol, countySymbol, communitySymbol,
                                                                communityType, townSymbol, False, True, '2022-01-01')
    isStreetList = isinstance(streetList, list)
    if isStreetList == True:
        streetList_length = len(streetList)
        streetRandomName = streetList[random.randint(streetList_length - streetList_length, streetList_length - 1)]\
                               .Nazwa1.title() +" "+ str(random.randint(1, 300))
    else:
        streetRandomName = townRandom.Nazwa.title() +" "+ str(random.randint(1, 300))
###Część kodu pobierająca listę ulic dla danej miejscowości oraz losowo wybierająca jedną z nich
    #z zakresu wylosowanej miejscowości. Jeśli wylosowana została wioska to nazwa ulicy jest
    #jednakowa z nazwą wioski.

    print("Województwo: " + provinceRandomName)
    print("Miejscowość: " + townRandomName)
    print("Ulica: " + streetRandomName)
###Część kodu wypisująca wylosowane Województwo, miejscowość oraz adres wylosowany na podstawie ulicy.
    #Możliwe jest dodanie wypisania kolejnych przykładowych danych jak np. Powiat, Gmina, Rodzaj Gminy
    # czy rodzaj ulicy(aleja, plac itp.).