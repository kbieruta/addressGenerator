from addressGen import generateAddress
from addressCSV import exportAddresses
##import funkcji do generowania i eksportu danych

isProcessFinished = False
##Zmienna informująca czy program ma zostać zakończony
while isProcessFinished == False:
    print("-----------------------------------")
    print("Generator losowych danych testowych \n")
    print("1: Generuj pojedynczy adres")
    print("2: Wygeneruj i wyeksportuj do pliku CSV określoną ilość adresów")
    print("quit: Zakończ program \n")
    decision = input("Wybierz funkcję spośród powyższych. \n")
##Wypisanie dostępnych opcji oraz zmienna przechowująca wprowadzoną decyzję

    match decision:
        case "1":
            print(" Trwa generowanie adresu \n")
            generateAddress()
            input("\n Proces zakończony. Wciśnij Enter, żeby kontynuować.")
        case "2":
            quantityOfRows = int(input("Wprowadź żądaną liczbę rekordów do wygenerowania z zakresu \n"))
            print(" Trwa generowanie pliku CSV \n")
            exportAddresses(quantityOfRows)
            input("\n Dane zostały zapisane do pliku. Wciśnij Enter, żeby kontynuować.")
        case "quit":
            isProcessFinished = True
        case other:
            print(" Nie rozpoznano wyboru. Spróbuj jeszcze raz.")
            input(" Wciśnij Enter, żeby kontynuować.")
##Część kodu porównująca decyzję do odpowiednich opcji i przekierowująca do ich wykonania

input(" Zakończono program. Wciśnij Enter, żeby zamknąć okno.")