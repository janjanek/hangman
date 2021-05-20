## Hangman

1. Serwer oczekuje na połaczenie.
2. Klient nr 1 łaczy sie z serwerem.
3. Serwer oczekuje na wiadomosc.
4. Klient nr 1 wysyła komendę START.
5. Serwer oczekuje na klienta nr 2
6. Klient nr 2 łaczy sie z serwerem.
7. Serwer oczekuje na wiadomość
8. Klient nr 2 wysyła komendę START
9. Serwer losuje kategorię z puli i to który gracz zaczyna
10. Serwer wysyła informację do klientów
o wylosowanej kategorii i który gracz zaczyna 
11. Klient nr 1 podaje swoje hasło
12. Klient nr 2 podaje swoje hasło
13. Serwer oczekuje na literę od wylosowanego klienta
14. Klient wysyła literę
15. Serwer sprawdza czy jest ona w haśle przeciwnika
16. Serwer wysyła hasło z uzupełnioną literą
17. Kroki 14-16 powtarzają się do
póki ktoś nie odgadnie hasła
18. W przypdaku odgadnięcia hasła
serwer wysyła informację o rezultacie gry.

Zestaw komend
start - zgłoszenie gotowości klienta
end - koniec gry
ok - potwierdzenie przyjęcia informacji
other_player - informacja, że jest kolej drugiego gracza
pass <hasło> - wysyłanie hasła przez klienta
filled_pass <hasło z uzupełnieniami> - wysyłanie hasła z uzupełnieniami
letter <literka> - wysłanie litery przez klienta
info <tekst> - przesyłanie informacji o wygranej/przegranej
i oczekiwaniu na gracza
