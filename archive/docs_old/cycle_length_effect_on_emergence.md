# Вплив довжини циклу на структуру emergent hierarchy

**Дата:** 12 грудня 2025  
**Дослідження:** Валідація Engineering Emergence (Jansma & Hoel, 2025)  
**Система:** Порівняння 6-state vs 8-state two-cycle систем

---

## РЕЗЮМЕ

Виявлено залежність між довжиною циклу в TPM та складністю emergent hierarchy:
- Коротші цикли (length-3) → складніша ієрархія (3 emergent scales)
- Довші цикли (length-4) → простіша ієрархія (1 emergent scale, "balloon")

---

## МЕТОДОЛОГІЯ

**Системи:**
- 6-state: два незалежні 3-цикли  
- 8-state: два незалежні 4-цикли

**Параметри:**
- Базовий p_self = 0.20 (ймовірність залишитись у стані)
- Sensitivity range: p_self ∈ [0.0, 0.5], крок 0.05

**Виправлення:** 
Microscale партиція виключена з підрахунку emergent scales (відповідно до концептуального визначення авторів).

---

## РЕЗУЛЬТАТИ

### Baseline метрики (p_self = 0.20)

| Метрика | 6-state | 8-state | Різниця |
|---------|---------|---------|---------|
| CP(microscale) | 0.7207 | 0.7594 | +5.36% |
| CP(macroscale) | 1.0000 | 1.0000 | 0% |
| ΔCP | 0.2793 | 0.2406 | -13.83% |
| Emergent scales | 3 | 1 | -2 |

### Структура emergent hierarchy

**6-state система (complex hierarchy):**
```
Scale 1: ((0,), (1,), (2,), (3,4,5))
  CP = 0.7293, ΔCP = 0.0086
  Один цикл згрупований, інший роздроблений

Scale 2: ((0,1,2), (3,), (4,), (5,))
  CP = 0.7293, ΔCP = 0.0086
  Інший цикл згрупований, перший роздроблений

Scale 3: ((0,1,2), (3,4,5))
  CP = 1.0000, ΔCP = 0.2707
  Обидва цикли згруповані (optimal macroscale)
```

**8-state система (balloon hierarchy):**
```
Scale 1: ((0,1,2,3), (4,5,6,7))
  CP = 1.0000, ΔCP = 0.2406
  Тільки optimal macroscale (обидва цикли згруповані)
```

### Trends across p_self parameter

**CP(microscale) degradation:**
- 6-state: 0.8892 → 0.6131 (Δ = -0.2761)
- 8-state: 0.9045 → 0.6667 (Δ = -0.2379)

**ΔCP growth:**
- 6-state: 0.1108 → 0.3869 (Δ = +0.2761)
- 8-state: 0.0955 → 0.3333 (Δ = +0.2379)

**Emergent scales stability:**
- 6-state: 3 scales стабільно для всіх p_self > 0
- 8-state: 1 scale стабільно для всіх p_self > 0

---

## ІНТЕРПРЕТАЦІЯ

### Механізм впливу довжини циклу

**Короткі цикли (length-3):**
- Формують проміжні "asymmetric" масштаби
- Один цикл може бути згрупований, інший роздроблений
- Ці проміжні масштаби мають малий але позитивний ΔCP (~0.0086)
- Результат: градуальна ієрархія з 3 рівнями

**Довгі цикли (length-4):**
- Проміжні asymmetric масштаби не мають позитивного ΔCP
- Пряма емердженція від microscale до optimal macroscale
- Результат: "balloon" - єдиний emergent scale

### Архітектурний принцип

Довші цикли мають вищий microscale CP, тому:
1. Базовий рівень більш "організований"
2. Менший "простір" для проміжної емердженції
3. Одразу стрибок до perfect determinism (CP = 1.0)

Коротші цикли мають нижчий microscale CP, тому:
1. Базовий рівень більш "шумний"
2. Більший "простір" для градуальної емердженції
3. Проміжні масштаби додають малі incremental gains

---

## УЗГОДЖЕНІСТЬ З СТАТТЕЮ

**Figure 4 (v2), система ii:**
> "system with two length-4 cycles"  
> Spath = 0.00, Srow = 0.00  
> Візуалізація показує "balloon" shape

**Наші результати:** 8-state two 4-cycles ✓ balloon (1 emergent scale)

**Примітка:** Стаття НЕ обговорює детально 6-state систему, тому наше відкриття про 3 emergent scales є новим спостереженням.

---

## ВИСНОВКИ

1. Довжина циклу впливає на складність emergent hierarchy
2. Цей ефект стабільний across параметр noise (p_self)
3. Balloon hierarchies асоціюються з довшими циклами
4. Complex hierarchies виникають при коротших циклах
5. Обидва типи досягають CP(macro) = 1.0 (perfect determinism)

---

## ФАЙЛИ

**Код:**
- `code/sensitivity_analysis_6state_corrected.py`
- `code/sensitivity_analysis_8state.py`
- `code/comparative_analysis_corrected.py`
- `code/inspect_6state_emergent_scales.py`

**Дані:**
- `results/sensitivity_analysis_6state_corrected.pkl`
- `results/sensitivity_analysis_8state.pkl`

**Візуалізації:**
- `figures/comparative_analysis_corrected.png`
- `figures/sensitivity_analysis_plots.png`

---

## НАСТУПНІ КРОКИ

1. Дослідити проміжні довжини циклів (length = 5, 6, 7...)
2. Перевірити гіпотезу на інших типах структур
3. Формалізувати зв'язок між cycle length та hierarchy complexity
4. Порівняти з іншими системами з Figure 4

---

## ОНОВЛЕННЯ: Дослідження 10-state системи

**Дата:** 12 грудня 2025 (продовження)

### Додаткова система

**10-state: два незалежні 5-цикли**
- Метод: Branching Greedy Algorithm (350 sampled partitions)
- CP(micro) = 0.7827
- CP(macro) = 1.0000
- ΔCP = 0.2173
- **Emergent scales: 1 (balloon)**

### Розширені результати

| System | Cycle Length | CP(micro) | ΔCP | Emergent | Type |
|--------|--------------|-----------|-----|----------|------|
| 6-state | 3 | 0.7207 | 0.2793 | 3 | Complex |
| 8-state | 4 | 0.7594 | 0.2406 | 1 | Balloon |
| 10-state | 5 | 0.7827 | 0.2173 | 1 | Balloon |

### Уточнена гіпотеза

**Критична довжина циклу: length ≤ 3**

- **Короткі цикли (length = 3):** Complex hierarchy з проміжними scales
- **Довгі цикли (length ≥ 4):** Balloon hierarchy, пряма емердженція

**Механізм:**
Довші цикли мають вищий CP(microscale), що залишає менше "простору" для проміжних emergent scales. Система одразу "стрибає" до perfect determinism без градуальних кроків.

**Тренд:**
```
CP(micro): 0.7207 → 0.7594 → 0.7827  (зростає з довжиною)
ΔCP:       0.2793 → 0.2406 → 0.2173  (падає з довжиною)
Emergent:  3      → 1      → 1       (різкий перехід при length=4)
```

### Методологічна примітка

Для систем n ≥ 10 використано Branching Greedy Algorithm замість brute force через обчислювальну складність. Brute force практичний тільки для n ≤ 9 (Bell(9) = 21,147 партицій).

---
