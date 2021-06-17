## Setup
* pip install -r requirements.txt
* python src/server.py
* python src/client.py

## Hangman
1. Serwer oczekuje na połaczenie.
2. Klient nr 1 łączy się z serwerem.
3. Klient nr 2 łączy się z serwerem.
4. Serwer przesyła informację o rozpoczętej grze.
5. Serwer losuje kategorię z puli
6. Serwer wysyła informację do klientów
7. Klient nr 1 podaje swoje hasło
8. Klient nr 2 podaje swoje hasło
9. Serwer oczekuje na literę od wylosowanego klienta
10. Klient wysyła literę
11. Serwer sprawdza czy jest ona w haśle przeciwnika
12. Jeśli litera jest poprawna: serwer wysyła hasło z uzupełnioną literą
13. Jeśli litera jest błędna: Klient traci 1 życie, 
    serwer przesyła informację o utracie życia.
15. Kroki 10-13 powtarzają się do póki ktoś nie odgadnie
    hasła, lub nie straci wszystkich żyć
16. W przypdaku odgadnięcia hasła serwer
    wysyła informację o rezultacie gry.


## Disconnect Command
end - koniec gry  


## Git workflow
* master - główny branch, rozwijany przez pull request tylko z dev
* dev - branch deweloperski pull request z feature branch lub fix_branch
po code rewiev
* feature_nazwa_funcjonalności - branch żyje tylko rozwojowo, po zakończeniu prac usuwany****************
* fix_nazwa_buga - po naprawie i code rewiev branch usuwany

