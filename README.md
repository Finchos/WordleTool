# 🟩🟨⬜ Wordle Solver & Assistant

Elegantní a rychlý pomocník pro hru Wordle s moderním grafickým rozhraním. Aplikace nevyužívá jen prostou filtraci možností, ale k výběru optimálního dalšího tahu používá pokročilý **Minimax algoritmus**, který matematicky minimalizuje počet zbývajících řešení v tom nejhorším možném scénáři.

## ✨ Klíčové funkce

* **Chytrý mozek (Minimax):** Kalkuluje neprůstřelný další tah nezávisle na tom, jak zákeřná tajenka je.
* **Moderní GUI:** Postaveno na frameworku `CustomTkinter` s plnou podporou Dark Mode a responzivním designem.
* **Intuitivní ovládání:** * Podpora globální klávesnice – slova prostě píšeš a mažeš jako ve skutečné hře.
  * Změna barev (šedá ➔ žlutá ➔ zelená) probíhá pouhým kliknutím na políčko.
  * Klávesou `Enter` okamžitě vyhodnotíš tah.
* **Přehled možností:** Neustále aktualizovaný seznam všech zbývajících platných anglických slov přímo na obrazovce.
* **Architektura:** Čisté oddělení logiky (`solver.py`) od vzhledu (`gui.py`).

## 🚀 Jak to spustit

Máš dvě možnosti, jak aplikaci používat:

### Možnost 1: Spuštění ze zdrojového kódu (pro vývojáře)
1. Ujisti se, že máš nainstalovaný Python 3.8 a novější.
2. Nainstaluj potřebnou knihovnu pro GUI:
   ```bash
   pip install customtkinter
