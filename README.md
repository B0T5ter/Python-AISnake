# 🐍 Snake AI – Q-Learning

## 📌 Opis projektu
Jest to klasyczna gra Snake wzbogacona o **sztuczną inteligencję (AI) wykorzystującą Q-learning**. AI uczy się optymalnych ruchów poprzez metodę **wzmocnionego uczenia** i podejmuje decyzje na podstawie nagród i kar.

## 🎯 Funkcjonalności
✔️ Klasyczna rozgrywka Snake w Pygame  
✔️ AI oparte na **Q-learningu**  
✔️ System nagród i kar do optymalizacji ruchów  
✔️ Możliwość ręcznej gry oraz treningu AI  
✔️ Graficzna wizualizacja węża i procesu nauki  

Podczas urochomionego projektu można korzystać z klawiszy:

w - zwiększą prędkość gry

s - zmniejsza prędkość gdy

a/d - zmniejszenie/zwiększenie współczynnika epsilon

q - włączenie/wyłączenie animacji

e - włączenie/wyłączenie cyklicznej zmiany współczynnika epsilon

W razię chęci nauki go od zera wystarczy usnąć lub zmienić nazwę pliku **game_data.pkl**, 
gdzie przechowywane są jego wartości Q, rekord i liczba prób. Nowy plik zostanie stworzony w momencie włączenia programu

## 🛠️ Wymagania
Przed uruchomieniem projektu upewnij się, że masz zainstalowane:

- Python 3.8+
- Pygame
- NumPy

Możesz zainstalować wymagane biblioteki za pomocą:
```bash
pip install pygame numpy
```

## 🤖 Jak działa AI?
AI korzysta z **Q-learningu**, który aktualizuje wartości w tablicy Q na podstawie nagród:

🔹 **Nagrody:**  
- +10 za zebranie jedzenia 🍎  
- -100 za kolizję ze ścianą lub własnym ciałem ❌  
- Małe nagrody za ruchy poprawiające sytuację

🔹 **Eksploracja vs. Eksploatacja:**  
AI balansuje pomiędzy losowymi ruchami (eksploracja) a wykorzystaniem najlepszych znanych strategii (eksploatacja) za pomocą współczynnika **epsilon-greedy**.

## 📈 Możliwe ulepszenia
🔹 Zastosowanie **Deep Q-Network (DQN)** zamiast tablicowego Q-learningu  
🔹 Poprawa funkcji nagród, aby AI szybciej się uczyło  
🔹 Dynamiczna zmiana współczynnika epsilon dla lepszego treningu  
🔹 Testowanie różnych strategii ruchu i nauki  

## 📜 Licencja
Projekt jest dostępny na licencji MIT. Możesz dowolnie go rozwijać i modyfikować! 🎉

---

📧 **Kontakt:** Jeśli masz pytania lub pomysły na ulepszenia, skontaktuj się ze mną! 🚀

