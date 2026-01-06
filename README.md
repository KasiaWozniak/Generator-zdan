# Generator-zdan

## Instalacja systemu

Aplikacja została zaprojektowana jako rozwiązanie webowe uruchamiane w środowisku lokalnym. Ze względu na wykorzystanie specjalistycznych bibliotek do przetwarzania języka naturalnego oraz gotowej bazy wiedzy, jej uruchomienie wymaga wcześniejszego przygotowania odpowiedniego środowiska Python. W niniejszym rozdziale opisano procedurę instalacji i konfiguracji projektu z wykorzystaniem zalecanego środowiska programistycznego PyCharm.

Do poprawnego działania systemu niezbędne jest posiadanie interpretera języka Python w wersji 3.10 oraz opcjonalnie systemu kontroli wersji Git umożliwiającego sklonowanie projektu, a także zintegrowanego środowiska programistycznego np. PyCharm w wersji Community lub Professional. Komponenty te stanowią podstawę do dalszej konfiguracji aplikacji oraz jej uruchomienia w trybie deweloperskim.

Pierwszym etapem instalacji jest pobranie kodu źródłowego projektu wraz z dołączoną bazą słów. Projekt dystrybuowany jest z wcześniej wygenerowanymi plikami danych w formacie JSON, umieszczonymi w katalogu \texttt{semantic}, co eliminuje konieczność czasochłonnego przetwarzania dokumentów źródłowych podczas pierwszego uruchomienia. Repozytorium projektu należy pobrać na dysk lokalny lub sklonować z wykorzystaniem systemu kontroli wersji Git. Kod źródłowy projektu jest dostępny w serwisie GitHub pod adresem: https://github.com/KasiaWozniak/Generator-zdan/tree/master
lub poprzez link:
https://github.com/KasiaWozniak/Generator-zdan/tree/master,


Po otwarciu projektu w środowisku PyCharm konieczna jest instalacja wymaganych pakietów określonych w pliku \texttt{requirements.txt}. Proces ten można przeprowadzić z poziomu terminala wpisując komendę: \texttt{``pip install -r requirements.txt''}, co zapewnia spójność środowiska wykonawczego z konfiguracją projektu.

Najprostszym ze sposobów na uruchomienie aplikacji jest zrobienie tego z poziomu terminala, przechodząc do katalogu głównego projektu \texttt{Generator zdań} i wpisując komendę \texttt{``python -m generator\_app.main''}.

Po poprawnym uruchomieniu w terminalu powinny pojawić się komunikaty potwierdzające start serwera deweloperskiego, wraz z informacją o adresie lokalnym, pod którym aplikacja jest dostępna. Po uruchomieniu serwera system może być używany za pośrednictwem dowolnej przeglądarki internetowej, łącząc się z aplikacją pod adresem lokalnym serwera.
