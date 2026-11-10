# Zadanie 1 — Rozwinięcie Shannona (2 poziomy: **b**, potem **c**)

**Funkcja:** `f(a, b, c, d)` z treści zadania:
`f(a, b, c, d) = a'c + a'b + ab'c'd + bd' + bc a'bc'`

---

## 0. Uwaga o zapisie funkcji z treści

Zapis literałowy z zadania 1 nie jest równoważny podanemu dalej w poleceniu
zapisowi sumy mintermów (przy dosłownym odczycie daje on zbór `{2,3,4,5,6,7,12,14}`,
więc zamiast `m9` i `m15` pojawia się nadmiarowe `m2`). Ponieważ w poleceniu SOP
zostało podane jako zapis **równoważny do sprawdzenia poprawności układu**, przyjmujemy
je jako funkcję wzorcową (normatywną):

```
f(a, b, c, d) = Σm(3, 4, 5, 6, 7, 9, 12, 14, 15)
```

Zapis Σm jest spójny z wyrażeniem ze wzoru źródłowego po korekcie oczywistej literówki
`a'c → a'cd` (końcowy człon z treści odczytamy jako `bc + a'bc'` — składnik `a'bc'`
jest pochłaniany przez `bc` i nic nie zmienia; dosłowne odczytanie całego wyrażenia
daje wynik różniący się jedynie mintermem m2):

```
a'cd + a'b + ab'c'd + bd' + bc  =  Σm(3,4,5,6,7,9,12,14,15)   ✔ (sprawdzone komputerowo, zob. §6)
```

Minimalna postać SOP (wyznaczona programem, kontrolnie):

```
f = a'b + bd' + bc + a'cd + ab'c'd
```

Przyjęta dalej numeracja mintermów: `m = a·8 + b·4 + c·2 + d` (a — bit najstarszy).

---

## 1. Tablica prawdy funkcji wzorcowej

| m | a b c d | f | | m | a b c d | f |
|---|---------|---|---|---|---------|---|
| 0  | 0 0 0 0 | 0 | | 8  | 1 0 0 0 | 0 |
| 1  | 0 0 0 1 | 0 | | 9  | 1 0 0 1 | **1** |
| 2  | 0 0 1 0 | 0 | | 10 | 1 0 1 0 | 0 |
| 3  | 0 0 1 1 | **1** | | 11 | 1 0 1 1 | 0 |
| 4  | 0 1 0 0 | **1** | | 12 | 1 1 0 0 | **1** |
| 5  | 0 1 0 1 | **1** | | 13 | 1 1 0 1 | 0 |
| 6  | 0 1 1 0 | **1** | | 14 | 1 1 1 0 | **1** |
| 7  | 0 1 1 1 | **1** | | 15 | 1 1 1 1 | **1** |

---

## 2. Poziom 1 — rozwinięcie Shannona względem **b**

Twierdzenie Shannona: `f = b'·f(a, 0, c, d) + b·f(a, 1, c, d)`

### Część `b = 0`

Do zbioru wchodzą mintermy z `b = 0`: **m3** (0 0 1 1) i **m9** (1 0 0 1).
W funkcji `f₀(a, c, d)` (zmienne `a c d`) jedynki stoją dla `(a,c,d) = 011` i `101`:

**Tablica Karnaugha f₀(a,c,d):**

| a \ cd | 00 | 01 | 11 | 10 |
|--------|----|----|----|----|
| **0**  | 0  | 0  | 1  | 0  |
| **1**  | 0  | 1  | 0  | 0  |

```
f₀(a, c, d) = a'cd + ac'd  (= d·(a ⊕ c))
```

### Część `b = 1`

Mintermy z `b = 1`: **m4, m5, m6, m7, m12, m14, m15**. Jedyne zero w `(a,c,d)` występuje
dla `(1, 0, 1)` — czyli `m13 = 1 1 0 1`, którego nie ma w zbiorze.

**Tablica Karnaugha f₁(a,c,d):**

| a \ cd | 00 | 01 | 11 | 10 |
|--------|----|----|----|----|
| **0**  | 1  | 1  | 1  | 1  |
| **1**  | 1  | 0  | 1  | 1  |

```
f₁(a, c, d) = (a c' d)' = a' + c + d'
```

### Po poziomie 1:

```
f = b'·(a'cd + ac'd) + b·(a' + c + d')
```

---

## 3. Poziom 2 — rozwinięcie Shannona względem **c**

Każdą z części rozwijamy analogicznie: `g = c'·g(c = 0) + c·g(c = 1)`.

### Gałąź `b = 0`:  `f₀ = a'cd + ac'd = c'·f₀₀ + c·f₀₁`

| | co zostaje | wynik |
|---|---|---|
| `f₀₀ = f(a, 0, 0, d)` | z mintermów z `b = 0, c = 0` zostaje tylko **m9** → `a = 1, d = 1` | **`f₀₀ = a·d`** |
| `f₀₁ = f(a, 0, 1, d)` | z `b = 0, c = 1` zostaje tylko **m3** → `a = 0, d = 1` | **`f₀₁ = a'·d`** |

**Tablice Karnaugha f₀₀ i f₀₁ (zmienne a, d):**

| f₀₀ = a·d | d=0 | d=1 | | f₀₁ = a'·d | d=0 | d=1 |
|---|---|---|---|---|---|---|
| a=0 | 0 | 0 | | a=0 | 0 | 1 |
| a=1 | 0 | 1 | | a=1 | 0 | 0 |

Sprawdzenie: `c'·f₀₀ + c·f₀₁ = c'·a·d + c·a'·d = a'cd + ac'd` ✔

### Gałąź `b = 1`:  `f₁ = a' + c + d' = c'·f₁₀ + c·f₁₁`

| | co zostaje | wynik |
|---|---|---|
| `f₁₀ = f(a, 1, 0, d)` | mintermy `b = 1, c = 0`: **m4** (a=0,d=0), **m5** (a=0,d=1), **m12** (a=1,d=0) → jedynki wszędzie poza `(a,d) = (1,1)` | **`f₁₀ = a' + a·d' = a' + d'`** |
| `f₁₁ = f(a, 1, 1, d)` | mintermy `b = 1, c = 1`: **m6, m7, m14, m15** — wszystkie cztery są w zbiorze | **`f₁₁ = 1`** |

**Tablice Karnaugha f₁₀ i f₁₁ (zmienne a, d):**

| f₁₀ = a' + d' | d=0 | d=1 | | f₁₁ | d=0 | d=1 |
|---|---|---|---|---|---|---|
| a=0 | 1 | 1 | | a=0 | 1 | 1 |
| a=1 | 1 | 0 | | a=1 | 1 | 1 |

(absorpcja: `a' + a·d' = (a' + a)(a' + d') = a' + d'`)

### Postać końcowa (dwupoziomowe rozwinięcie Shannona)

```
                poziom 2 (c)              poziom 1 (b)
f = b'·[ c'·(a·d)  + c·(a'·d) ]  +  b·[ c'·(a' + d') + c·1 ]
```

Rozwinięta iloczyn-suma:

```
f = b'c'·a·d  +  b'c·a'·d  +  bc'·a'  +  bc'·d'  +  b·c
```

**Funkcje rezydualne zależą wyłącznie od `a` i `d`** — stąd układ wymaga tylko
4 inwerterów, 3 bramek AND/OR do odtworzenia rezydualnych, 3 multiplekserów 2:1
i stałej 1. Rozwinięcie zostało zweryfikowane formalnie (symulacja + sprawdzenie
symbolowe, zob. §5–6): `f(Shannona) ≡ f(SOP) ≡ Σm(3,4,5,6,7,9,12,14,15)` dla wszystkich 16 kombinacji wejść. ✔

---

## 4. Schemat w Logisim-Evolution

Plik: **`zadanie1/zadanie1.circ`** (format projektu Logisim-Evolution ≥ 3.x; powstał i został
zweryfikowany w oparciu o źródła Logisim-Evolution v5.0.0: `github.com/logisim-evolution/logisim-evolution`).
Podgląd schematu: **`zadanie1/schemat.png`** (wygenerowany z tych samych współrzędnych, co plik .circ).

### Struktura układu — 3 multipleksery 2:1 + bramki

**Poziom 2 (sterowanie `c`):**

| MUX | Wejście 0 (c = 0) | Wejście 1 (c = 1) | Wybór | Wyjście |
|-----|-------------------|-------------------|-------|---------|
| MUX#1 | `f00 = a·d` (AND) | `f01 = a'·d` (AND) | `c` | `g0` |
| MUX#2 | `f10 = a' + d'` (OR) | `1` (Constant) | `c` | `g1` |

**Poziom 1 (sterowanie `b`):**

| MUX | Wejście 0 (b = 0) | Wejście 1 (b = 1) | Wybór | Wyjście |
|-----|-------------------|-------------------|-------|---------|
| MUX#3 | `g0` | `g1` | `b` | **`f (Shannon)`** |

Bramki towarzyszące: 4 × NOT (generacja `a'`, `b'`, `c'`, `d'`), 2 × AND (`f00`, `f01`), 1 × OR (`f10`), 1 × Constant 1.
Połączenia między elementami prowadzone są przewodami oraz **tunelami** (▷) —
tunele o tej samej etykiecie (np. `a`, `an`, `f00`, `g1`…) są elektrycznie jednym węzłem,
co upraszcza rysowanie.

Na tym samym arkuszu, poniżej linii przerywanej, narysowany jest **równoważny układ SOP**:
9 bramek AND4 (mintermy m3, m4, m5, m6, m7, m9, m12, m14, m15) + 1 bramka OR-9 → `f (SOP)`,
oraz na dole — **układ porównujący**: bramka XNOR, której wyjście `zgodne` świeci/wskazuje 1,
gdy oba układy dają ten sam wynik.

### Jak sprawdzić w symulacji

1. Otworzyć `zadanie1.circ` w Logisim-Evolution.
2. Narzędziem **Poke Tool** klikać piny `a`, `b`, `c`, `d`, przechodząc wszystkie 16 kombinacji.
3. Dla każdej kombinacji wyjścia `f (Shannon)` i `f (SOP)` powinny być równe, więc pin
   **`zgodne` = 1 zawsze**.
4. Wersja zweryfikowana programowo (generator + symulator w `tools/build_circuit.py`) —
   wynik dla wszystkich 16 kombinacji:

| m | a b c d | f (Shannon) | f (SOP) | zgodne |
|---|---------|:-:|:-:|:-:|
| 0  | 0 0 0 0 | 0 | 0 | 1 |
| 1  | 0 0 0 1 | 0 | 0 | 1 |
| 2  | 0 0 1 0 | 0 | 0 | 1 |
| 3  | 0 0 1 1 | 1 | 1 | 1 |
| 4  | 0 1 0 0 | 1 | 1 | 1 |
| 5  | 0 1 0 1 | 1 | 1 | 1 |
| 6  | 0 1 1 0 | 1 | 1 | 1 |
| 7  | 0 1 1 1 | 1 | 1 | 1 |
| 8  | 1 0 0 0 | 0 | 0 | 1 |
| 9  | 1 0 0 1 | 1 | 1 | 1 |
| 10 | 1 0 1 0 | 0 | 0 | 1 |
| 11 | 1 0 1 1 | 0 | 0 | 1 |
| 12 | 1 1 0 0 | 1 | 1 | 1 |
| 13 | 1 1 0 1 | 0 | 0 | 1 |
| 14 | 1 1 1 0 | 1 | 1 | 1 |
| 15 | 1 1 1 1 | 1 | 1 | 1 |

`f (Shannon) = f (SOP) = Σm(3,4,5,6,7,9,12,14,15)` dla wszystkich 16 kombinacji — układ działa poprawnie. ✔

### Lista użytych elementów Logisim-Evolution

| Biblioteka | Elementy |
|---|---|
| Wiring | Pin (wejścia/wyjścia), Tunnel, Constant |
| Gates | NOT, AND (2, 4 wejścia), OR (2, 9 wejść), XNOR |
| Plexers | Multiplexer (2:1, select = 1 bit, domyślnie bez wejścia enable) |
| Base | Text (opisy sekcji) |

---

## 5. Odpowiedź zbiorcza (do przepisania na kartkę)

```
Poziom 1 (b):   f = b'·f₀(a,c,d) + b·f₁(a,c,d)
                f₀(a,c,d) = a'cd + ac'd
                f₁(a,c,d) = a' + c + d'          (= (ac'd)')

Poziom 2 (c):   f₀ = c'·f₀₀ + c·f₀₁
                f₁ = c'·f₁₀ + c·f₁₁

                f₀₀ = f(a,0,0,d) = ad
                f₀₁ = f(a,0,1,d) = a'd
                f₁₀ = f(a,1,0,d) = a' + d'       (= a' + ad')
                f₁₁ = f(a,1,1,d) = 1

Rozw. końcowe:  f = b'·c'·(a·d) + b'·c·(a'·d) + b·c'·(a' + d') + b·c·1
                f = b'c'ad + b'ca'd + bc'a' + bc'd' + bc
```

## 6. Jak uzyskano i jak zweryfikowano wyniki (dowód cyfrowy)

* Minterm `Σm(3,4,5,6,7,9,12,14,15)` oraz postać minimalna policzone funkcją `SOPform` z biblioteki
  `sympy`; rozwinięcia Shannona policzone przez podstawienie `b=0/1`, `c=0/1` i ponowną minimalizację —
  wyniki jw.; rekonstrukcja `b'(c'ad + ca'd) + b(c'(a'+d') + c)` daje funkcję identyczną z `Σm(...)` (sprawdzone symbolicznie).
* Plik `.circ` został wygenerowany i **odsymulowany programowo** (`tools/build_circuit.py`):
  symulator odtwarza semantykę bramek, multiplekserów (select=0 → wejście 0), tuneli i przewodów,
  dla wszystkich 16 kombinacji a,b,c,d — wszystkie zgodnie z SOP, bez pływających wejść i bez konfliktów sterowników.
  (Logisim-Evolution nie da się uruchomić w tym środowisku — binarki release nie są osiągalne —
  dlatego poprawność potwierdzono niezależnym symulatorem odczytującym wygenerowany plik oraz zgodnością
  geometrii portów z kodem źródłowym Logisim-Evolution v5.0.0; ostateczne kliknięcie w symulacji GUI
  zostało opisane w §4 i jest trywialne.)
* Równoważność `a'cd + a'b + ab'c'd + bd' + bc` z podanym SOP potwierdzono numerycznie dla wszystkich 16 mintermów. ✔

## 7. Zawartość katalogu `zadanie1/`

| plik | opis |
|---|---|
| `zadanie1.circ` | schemat Logisim-Evolution: rozwinięcie Shannona (3 mux 2:1), równoważny SOP, układ porównujący XNOR |
| `schemat.png`   | podgląd schematu (wygenerowany z identycznych współrzędnych) |
| `tools/build_circuit.py` | generator pliku `.circ` + symulator weryfikujący 16 kombinacji |
| `tools/render_preview.py` | generator podglądu `schemat.png` |
| `rozwiazanie.md` | niniejszy dokument |
