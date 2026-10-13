#include <iostream>
#include <vector>
#include <cmath>

using namespace std;

// Funkcja generująca dzielniki liczby n.
vector<int> WygenerujDzielniki(int n) {
  vector<int> male_dzielniki;  // Wektor przechowujący mniejsze dzielniki
  vector<int> duze_dzielniki;  // Wektor przechowujący większe dzielniki
  
  // Iteruj przez możliwe dzielniki do pierwiastka kwadratowego z n.
  for (int i = 1; i <= sqrt(n); ++i) {
    // Kiedy liczba i jest dzielnikiem n.
    if (n % i == 0) {
      // Dodaj dzielnik i do wektora mniejszych dzielników.
      male_dzielniki.push_back(i);   
      if (i * i != n) {
        // Oraz drugi dzielnik (n/i), o ile nie jest to kwadrat pierwiastka.
        duze_dzielniki.push_back(n / i); 
      }
    }
  }
  
  // Sklej listę dzielników, przy czym musimy odwrócić wektor dużych dzielników,
  // ponieważ jest on w porządku malejącym.
  vector<int> dzielniki = male_dzielniki;
  for (int i = duze_dzielniki.size() - 1; i >= 0; --i) {
    dzielniki.push_back(duze_dzielniki[i]);
  }
  
  return dzielniki;
}

int main() {
  // Pobierz dane wejściowe: a, b, c, d
  int a, b, c, d;
  cin >> a >> b >> c >> d;

  // Uporządkuj zmienne a i b, tak aby a <= b.
  if (a > b) {
    swap(a, b);
  }

  // Oblicz oczekiwaną liczbę kostek.
  // Rzutujemy tutaj na typ long long, jako że liczba 
  // ta może być duża i  wyjść poza typ int.
  long long wymagana_liczba_kostek = (long long)c * d;

  // Pobierz dzielniki liczby c i d
  vector<int> dzielniki_c = WygenerujDzielniki(c);
  vector<int> dzielniki_d = WygenerujDzielniki(d);

  // Przeszukaj możliwe kombinacje dzielników c i d.
  for (int dzielnik_c : dzielniki_c) {
    for (int dzielnik_d : dzielniki_d) {
      // Potencjalnym bokiem jest iloczyn dzielników.
      long long pierwszy_bok = (long long)dzielnik_c * dzielnik_d;
      // Zatem drugi bok to iloraz wymaganej liczby kostek 
      // przez długość pierwszego boku.
      long long drugi_bok = wymagana_liczba_kostek / pierwszy_bok;

      // Uporządkuj zmienne pierwszy_bok i drugi_bok, tak aby 
      // pierwszy_bok <= drugi_bok.
      if (pierwszy_bok > drugi_bok) {
        swap(pierwszy_bok, drugi_bok);
      }

      // I sprawdź, czy dane boki można uzyskać, tj. czy mieszczą się w czekoladzie.
      if (pierwszy_bok <= a && drugi_bok <= b) {
        cout << "TAK" << endl;
        return 0;
      }
    }
  }

  // Jeśli nie znaleziono odpowiedniej kombinacji, wypisz "NIE"
  cout << "NIE" << endl;

  return 0;
}
