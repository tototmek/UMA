# Instrukcja testów wg Tomka

### Część badania parametrów
Tutaj nie do końca wiem jakie są te parametry i jaki będzie ich wpływ, implementowałeś ten algorytm więc dobrze będziesz wiedział jakie eksperymenty zrobić.

Ważne, aby w wynikach znalazły się wykresy przedstawiające czas przejścia oraz sumaryczną nagrodę na przestrzeni epok w procesie uczenia. Powinno tam być fajnie widać różnice w dynamice procesu uczenia dla różnych wartości różnych parametrów.

Sądzę, że szczególnie ciekawy okaże sie parametr epsilon, bo to głównie on reguluje balans między eksploracją a eksploatacją. Może to być widoczne na suchych liczbach - wynikach testu po uczeniu, ale myślę że lepsze będą właśnie wykresy na przestrzeni epok. Powinno wyjść tak, że kiedy wybierana jest zazwyczaj strategia optymalna uczenie startuje szybciej, ale może utknąć na minimum lokalnym - ustabilizować się na jakiejś wartości naegrody. Kiedy często wybierana jest strategia losowa uczenie będzie wolniejsze, ale raczej zejdzie do lepszego rozwiązania. Może się jednak okazać, że dla zbyt dużego epsilona uczenie będzie tak wolne, że nigdy nie dojdziemy do sensownej strategii - warto umieścić to we wnioskach.

### Część badania uniwersalności agentów

Na początek weź jakiegoś normalnie nauczonego agenta (tablicę Q) albo naucz od nowa i przetestuj na różnych nowych trasach. Mam nadzieję, że będzie w miarę dawał radę, ale nie będzie idealny. Jakieś przedstawienie suchych wyników czy coś. Dalej proponujemy metody stworzenia agenta, który będzie radził sobie lepiej na przeróżnych trasach. Dajemy trzy rozwiązania:

1. Wybór najlepszego agenta z dużej puli agentów - trenujesz dużo agentów (każdego na innym torze, może również z innymi parametrami algorytmu) i powtarzasz dla każdego test podobny do tego na początku. Porównujesz wyniki różnych agentów, wybierasz najlepszego spośród nich. Tutaj może być jakiś wniosek dlaczego naszym zdaniem ten agent wyszedł najlepszy. Może to kwestia doboru parametrów (np. lepsza eksploracja) lub bardziej różnorodny tor który pozwolił mu nauczyć się różnych rodzajów terenu.

2. Stworzenie agenta poprzez uśrednienie strategii - Tablica Q nowego agenta to średnia tablic Q wszystkich agentów wytrenowanych w poprzednim punkcie. Powinno moim zdaniem wyjść lepiej niż po prostu przy wyborze najlepszego agenta. Oczywiście sprawdzasz to ponownie testując na dużej puli przeróżnych tras.

3. Metoda ensemble - wybór akcji przez agenta to głosowanie agentów utworzonych w punkcie 1. W każdym kroku, każdy z agentów wybiera akcję, a ostatecznie podjęta zostaje ta akcja, którą wybrano najwięcej razy. Nie wiem czy będzie lepiej niż przy uśrednieniu tablic Q, za to prawie na pewno będzie lepiej niż w podpunkcie 1.

Tutaj zrób podsumowanie wyników eksperymentu i wybierz najlepszy sposób. Możesz przerobić example.py na demo, w którym najlepszy z agentów jeździ po losowym torze.

