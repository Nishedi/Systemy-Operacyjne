# Konrad Pempera
## Systemy operacyjne Projekt
## Gra poszukiwacze skarbów w apokalipisie Zombie (Wirusa)

##
## Instrukcja gry:
- Twoim celem jest wyeliminowanie jak największej liczby przeciwników, jednocześnie unikając kontaktu z nimi
- używaj strzałek do zmiany kierunku poruszania się gracza
- aby strzelić wciśnij spację
- zbieraj amunicje, jej liczba jest ograniczona!

## Implementacja

Głównym  celem realizowanego projektu było wykonanie aplikacji, która wykorzystuje wielowątkowość oraz sekcje krytyczne. Stworzona gra powstała z użyciem języka Python z biblioteką threading. Stworzono osiem klas tj.

- klasa main - najważniejsza klasa aplikacji, w niej uruchomiona zostaje pętla główna aplikacji służąca za wizualizacje tego co się dzieje na planszy gry, dodatkowo klasa obsługuje ekran startowy oraz końcowy. Podczas odpowiedniej interakcji z oferowanym interfejsem, skrypt uruchamia wątki i grę, a także je kończy,
- klasa map - w tej klasie zaimplementowano wczytywanie mapy z pliku oraz obsługę interakcji z mapą, np. sprawdzenie co się znajduje pod zadaną pozycją czy uaktualnienie mapy. Klasa realizuje także metodę wyszukującą najkrótszą ściężkę do celu, a także metody potrzebne do uruchomienia jej. 
- klasa threadmenager - odpowiedzialana za poprawne uruchomienie wszystkich wątków na początku gry, zakończenei wszystkich wątków podczas zakończenia gry, a także za uruchamianie wątków podczas trwania gry. Dodatkowo klasę rozszerzono o funkcję, która sprawdza czy pocisk trafił w jakiegokolwiek z wrogów. Zdecydowano, że ta funkcja będzie znajdować się w tym miejscu ze względu na fakt, iż trzeba sprawdzić każdego przeciwnika czy nie został trafiony ponieważ sprawdzenie tylko na podstawie mapy (jak w przypadku innych obiektów) jest niewystarczające (przeciwników jest wiele, mapa tekstowa nie koduje jaki obiekt jest na danej pozycji tylko czy jakiś jest),
- klasa object - po niej dziedziczą inne klasy obiektów (bullet, enemy, player), zawiera metody, po których dziedziczą potomkowie. Część z nich to tylko metody abstrakcyjne, które są rozszerzane przez inne klasy. Powstała z myślą o uproszczeniu kodu (zniwelowaniu nadmiarowości),
- klasa player - odpowiada za gracza, przechowuje ścieżki do zdjęć (w zależności od kierunku poruszania zmienia się zdjęcie), zmienne, które przechowują wynik oraz pozostałą liczbę amunicji. Dodatkowo klasa odpowiada za wykonanie strzału (uruchamia wątek pocisku z odpowiednimi parametrami), posiada pętlę główną wątku, sprawdza kolizję, sprawdza czy na polu, na którym jest gracz znajduje się amunicja. Ostatecznie klasa posiada funkcję, która definiuje sposób poruszania się gracza i sterowanie kierunkiem poruszania się w zależności od wciśnietęgo klawisza,
- klasa enemy - zawiera podobne funkcje (z odpowiednią implementacją) co klasa player za wyjątkiem funkcji odpowiadającej za strzelanie czy sprawdzającej czy obiekt znajduje się na polu z amunicją. Ponadto funkcja korzysta z funkcji zawartej w klasie map, która pozwala na wyszukanie gracza jeżeli znajduje się on w zasięgu widzenia. Metoda ta jest zrealizowana za pomocą algorytmu BFS (przeszukiwanie grafu wszerz).
- klasa bullet - podobnie jak powyżej, zawiera swoje implementacje funkcji do poruszania czy obsługi pętli głównej
- klasa photos - najprostsza klasa zawiera informacje o ścieżkach do zdjęć, które są wykorzystywane w grze

## Wątki
W grze zaimplementowano 7 wątków:
- wątek główny - odpowiada za wyświetlanie gry, obsługę klawiszy, wyświetlanie wyniku, sprawdzanie czy gra się zakończyła (w celu wyświetlenia poprawnej informacji)
- wątek gracza - odpowiada za poruszanie się gracza, strzelanie, sprawdzanie kolizji
- wątek przeciwników - odpowiada za poruszanie się przeciwników, strzelanie, sprawdzanie kolizji
- wątek pocisku - odpowiada za poruszanie się pocisku, sprawdzanie kolizji
- wątek dodający amunicję - co określony czas dodaje amunicję na planszy
- wątek dodający przeciwników - co określony czas dodaje przeciwników na planszy
- wątek kontrolujący inne wątki - sprawdza czy gra się zakończyła, kończy wątki gracza, przeciwników, pocisku, dodający amunicję, dodający przeciwników

## Sekcje krytyczne
W grze zaimplementowano dwie sekcje krytyczne:
- sekcja krytyczna gracza - wykorzystywana przez pociski. Jest zabezpieczona przez mutex. Dotyczy tylko zmiennej przechowującej wynik i jej celem jest zapewnienie, że dwa pociski w jednym czasie nie będą jej edytowały.
- sekcja krytyczna mapy - najważniejsza sekcja krytyczna. Również zabezpieczona przez mutex. Jej głównym zadaniem jest nie dopuszczenie do sytuacji, w której dwa obiekty (gracz, przeciwnik, pocisk) znajdują się na tym samym polu. W przypadku, gdy dwa obiekty chcą uzyskać dostęp do tego samego obiektu, pierwszy z nich uzyskuje dostęp, a drugi czeka na zwolnienie obiektu. Z tej sekcji korzystają praktycznie wszystkie wątki (player, bullet, enemy).
- sekcja krytyczna listy wątków - zabezpieczona przez mutex. Jej celem jest zapewnienie, że wątki nie będą dodawane ani usuwane z listy w jednym czasie (tylko jeden wątek może to robić w jednym czasie).

## Testy
Podczas testowania aplikacji zablokowano możliwość zakończenia gry poprzez kontakt z przeciwnikiem i ustawiono wiadomość wyświetlającą się gdy wątek wykonuje ruch (gdy nie może nic nie jest wyświetlano). Poczekano aż wszystkie pola zostaną zajęte. Zauważono, że żaden wątek nie wyświetlał wiadomości o zmianie pozycji, co sugeruje, że synchronizacja tego elementu jest poprawna. Dodatkowo przeprowadzano manualne testy, które polegały na wzrokowym sprawdzeniu czy wszystkie obiekty poruszają się poprawnie oraz zgodnie z założeniem - nie zauważono, żadnych problemów.