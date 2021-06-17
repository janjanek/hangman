## Setup
* pip install -r requirements.txt
* python src/server.py
* python src/client.py
Wszystkie pliki powinnyc znajdować w głównym folderze hangman
folder client_utils powinien zawierać plik trusted_certs.crt
folder server_utils powinien zawierać server.crt, server.key
w folderze hangman powinny znajdować się pliki client.py, server.py, game.py
Każda funkcja jest udokumaqntowana w kodzie co zwraca przyjmuje i za co odpowiada


## Hangman

1. Serwer oczekuje na połaczenie.
2. Klient nr 1 łaczy sie z serwerem.
3. Serwer oczekuje na klienta nr 2
4. Klient nr 2 łaczy sie z serwerem.
5. Serwer losuje kategorię z puli i to który gracz zaczyna
6. Serwer wysyła informację do klientów
o wylosowanej kategorii i który gracz zaczyna 
7. Klient nr 1 podaje swoje hasło
8. Klient nr 2 podaje swoje hasło
9. Serwer oczekuje na literę od wylosowanego klienta
10. Klient wysyła literę
11. Serwer sprawdza czy jest ona w haśle przeciwnika
12. Serwer wysyła hasło z uzupełnioną literą
13. Kroki 9-12 powtarzają się do
póki ktoś nie odgadnie hasła
14. W przypdaku odgadnięcia hasła
serwer wysyła informację o rezultacie gry.

Zestaw komend <br/>
end - koniec gry, serwer wysyła komendę o końcu gry do klientów

## Git workflow
* master - główny branch, rozwijany przez pull request tylko z dev
* dev - branch deweloperski pull request z feature branch lub fix_branch
po code rewiev
* feature_nazwa_funcjonalności - branch żyje tylko rozwojowo, po zakończeniu prac usuwany****************
* fix_nazwa_buga - po naprawie i code rewiev branch usuwany

## Wnioski końcowe

1. Co wyróżnia Wasze rozwiązanie w porównaniu do podobnych tego typu rozwiązań?
	* Gra za pomocą zastosowania 4 żyć jest bardziej dynamiczna. Dodatkowo, kiedy przeciwnik oddali się od komputera, użytkownik nie musi oczekiwać na jego powrót.
	* Na dynamikę rozgrywki wpływa także automatyczne parowanie użytkowników i tworzenie pokojów.
	* Kolejną zmianą względem innych produkcji jest losowanie kategorii wpisywanego hasła. Dzięki temu użytkownik może szybciej wymyślić hasło, a także wprowadza to możliwe nowe taktyki.

2. Jakie są wymagania sprzętowe i programowe Waszego produktu?

	Wymagania sprzętowe:
	* komputer,
	* klawiatura,
	* monitor,
	* połączenie z internetem.
		
	Wymagania programowe:
	* Python 3.7 lub wyższa wersja,
	* System operacyjny: Ubuntu, Windows, macOS.
		
3. Jakich bibliotek użyliście, czy stworzyliście własne?

	Wykorzystane biblioteki to: 
	* socket	- wykorzystana do tworzenia połączeń na niskim poziomie programistycznym,
	* sys		- wykorzystana do zdalnego zamknięcia programu klienta (w późniejszym czasie możliwość rozbudowania aplikacji o moderację w czasie rzeczywitym), 
	* threading	- wykorzystana do tworzenie wątków odpowiedzialnych za obsługę dużej liczby graczy,
	* ssl		- wykorzystana do bezpiecznego nawiązywania połączeń i szyfrowania ich,
	* random	- wykorzystana do wybierania pseudolosowej kategorii,
	* datatime	- wykorzystana do prawidłowej obłsługi logów,
	* time		- wykorzystana do obsługi przerw czasowych w programie.

4. Z czego jesteście najbardziej dumni, zadowoleni w Waszym projekcie?
	* Prędkości działania programu 
	* Czytelnego wyświetlania zgadywanych haseł.
	
5. Na jakie problemy napotkaliście i jak zostały rozwiązane?
	* Największym problemem jaki spotkaliśmy było stworzenie możliwości połączenia się wielu osób na serwer (a nie tylko dwóch), oraz łączenie ich dynamicznie w pary, w celu zwiększenia dynamiki gry. Problem ten został rozwiązany poprzez użycie wielowątkowości serwera. Każdy użytkownik otrzymuje swój wątek. 


