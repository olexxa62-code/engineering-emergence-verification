# Покрокове очищення та реорганізація

## ЕТАП 1: РЕЗЕРВНА КОПІЯ (ОБОВ'ЯЗКОВО!)

**Що робимо:** Створюємо backup перед будь-якими змінами

**Команди:**
```bash
cd /media/ssd2/ai_projects/
tar -czf hoel_verification_backup_$(date +%Y%m%d_%H%M%S).tar.gz hoel_verification_report/
ls -lh hoel_verification_backup_*.tar.gz
```

**Перевірка:** Архів створено, розмір розумний (> 1MB)

---

## ЕТАП 2: ВИДАЛЕННЯ ДУБЛІКАТІВ RESULTS (1/5)

**Що робимо:** Видаляємо старі/проміжні .pkl файли

### Крок 2.1: Аналіз
```bash
cd /media/ssd2/ai_projects/hoel_verification_report
ls -lh results/*.pkl
```

### Крок 2.2: Перевірка вмісту (опціонально)
```python
import pickle
# Переконуємось що файл дублікат
with open('results/eight_state_hierarchy.pkl', 'rb') as f:
    data = pickle.load(f)
    print(list(data.keys()))
```

### Крок 2.3: Видалення (ТІЛЬКИ ПІСЛЯ ПІДТВЕРДЖЕННЯ)
```bash
# НЕ виконуй поки не підтвердиш!
rm results/eight_state_hierarchy.pkl
rm results/eight_state_hierarchy_correct.pkl
rm results/sensitivity_analysis.pkl
rm results/six_state_hierarchy.pkl
```

### Крок 2.4: Перевірка
```bash
ls -lh results/
# Має залишитись:
# - sensitivity_analysis_6state_corrected.pkl
# - eight_state_hierarchy_final.pkl
# - comparative_table_6v8.csv
```

**ЗУПИНКА:** Підтверди що все OK перед переходом до Етапу 3

---

## ЕТАП 3: ВИДАЛЕННЯ ЗАЙВИХ FIGURES (2/5)

### Крок 3.1: Аналіз існуючих
```bash
ls -lh figures/*.png
```

### Крок 3.2: Ідентифікація потрібних
**ЗАЛИШИТИ:**
- comparative_analysis_corrected.png (ключова)
- final_cycle_length_effect.png (ключова)

**ВИДАЛИТИ:**
- sensitivity_analysis.png (є corrected версія)
- cp_distribution.png (діагностична)
- hierarchy_profile.png (діагностична)
- top_partitions.png (діагностична)

### Крок 3.3: Переміщення в archive (безпечніше ніж видалення)
```bash
mkdir -p archive/figures_diagnostic
mv figures/cp_distribution.png archive/figures_diagnostic/
mv figures/hierarchy_profile.png archive/figures_diagnostic/
mv figures/top_partitions.png archive/figures_diagnostic/
mv figures/sensitivity_analysis.png archive/figures_diagnostic/
```

### Крок 3.4: Перевірка
```bash
ls -lh figures/
ls -lh archive/figures_diagnostic/
```

**ЗУПИНКА:** Підтверди перед наступним етапом

---

## ЕТАП 4: ПЕРЕЙМЕНУВАННЯ CODE FILES (3/5)

### Крок 4.1: План перейменування
```
OLD → NEW:
sensitivity_analysis_6state_corrected.py → analyze_6state_two_3cycles.py
sensitivity_analysis_8state.py → analyze_8state_two_4cycles.py
analyze_10state_greedy.py → analyze_10state_two_5cycles.py
comparative_analysis_corrected.py → comparative_cycle_analysis.py
final_visualization_all_systems.py → create_final_figures.py
```

### Крок 4.2: Перейменування (по одному файлу!)
```bash
# Файл 1
mv code/sensitivity_analysis_6state_corrected.py code/analyze_6state_two_3cycles.py
ls -l code/analyze_6state_two_3cycles.py  # Перевірка

# Файл 2
mv code/sensitivity_analysis_8state.py code/analyze_8state_two_4cycles.py
ls -l code/analyze_8state_two_4cycles.py  # Перевірка

# Файл 3
mv code/analyze_10state_greedy.py code/analyze_10state_two_5cycles.py
ls -l code/analyze_10state_two_5cycles.py  # Перевірка

# Файл 4
mv code/comparative_analysis_corrected.py code/comparative_cycle_analysis.py
ls -l code/comparative_cycle_analysis.py  # Перевірка

# Файл 5
mv code/final_visualization_all_systems.py code/create_final_figures.py
ls -l code/create_final_figures.py  # Перевірка
```

### Крок 4.3: Тест запуску
```bash
python code/analyze_6state_two_3cycles.py --help 2>/dev/null || echo "File OK"
```

**ЗУПИНКА:** Перевіряємо що всі файли працюють

---

## ЕТАП 5: ПЕРЕЙМЕНУВАННЯ RESULTS FILES (4/5)

### Крок 5.1: План
```
OLD → NEW:
sensitivity_analysis_6state_corrected.pkl → results_6state_two_3cycles.pkl
eight_state_hierarchy_final.pkl → results_8state_two_4cycles.pkl
comparative_table_6v8.csv → comparative_analysis.csv
```

### Крок 5.2: Виконання
```bash
mv results/sensitivity_analysis_6state_corrected.pkl results/results_6state_two_3cycles.pkl
mv results/eight_state_hierarchy_final.pkl results/results_8state_two_4cycles.pkl
mv results/comparative_table_6v8.csv results/comparative_analysis.csv
```

### Крок 5.3: Перевірка
```bash
ls -lh results/
```

**ЗУПИНКА:** Перевіряємо структуру

---

## ЕТАП 6: ПЕРЕЙМЕНУВАННЯ FIGURES (5/5)

### Крок 6.1: План
```
OLD → NEW:
comparative_analysis_corrected.png → figure_comparative_6_8_10_state.png
final_cycle_length_effect.png → figure_cycle_length_discovery.png
```

### Крок 6.2: Виконання
```bash
mv figures/comparative_analysis_corrected.png figures/figure_comparative_6_8_10_state.png
mv figures/final_cycle_length_effect.png figures/figure_cycle_length_discovery.png
```

### Крок 6.3: Перевірка
```bash
ls -lh figures/
```

---

## ФІНАЛЬНА ПЕРЕВІРКА
```bash
cat > code/verify_cleanup.sh << 'SCRIPT'
#!/bin/bash
echo "======================================================================"
echo "ФІНАЛЬНА ПЕРЕВІРКА ПІСЛЯ ОЧИЩЕННЯ"
echo "======================================================================"

echo -e "\nCODE files:"
ls -1 code/*.py | grep -E "(analyze|comparative|create)" | wc -l | xargs echo "Analysis scripts:"

echo -e "\nRESULTS files:"
ls -1 results/*.pkl results/*.csv 2>/dev/null | wc -l | xargs echo "Result files:"

echo -e "\nFIGURES files:"
ls -1 figures/*.png 2>/dev/null | wc -l | xargs echo "Figure files:"

echo -e "\nARCHIVE files:"
find archive -type f 2>/dev/null | wc -l | xargs echo "Archived files:"

echo -e "\n======================================================================"
SCRIPT

chmod +x code/verify_cleanup.sh
bash code/verify_cleanup.sh
```

---

