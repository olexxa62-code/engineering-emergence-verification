#!/bin/bash
# Перевірка headers у всіх Python файлах

echo "======================================================================"
echo "ПЕРЕВІРКА СТАНДАРТНИХ HEADERS"
echo "======================================================================"

echo -e "\n1. ПРИКЛАДИ HEADERS:"
echo "----------------------------------------------------------------------"

# Перевіряємо кілька ключових файлів
files=(
    "code/ce2_core.py"
    "code/algorithm1_brute_force.py"
    "code/algorithm2_greedy.py"
    "data/six_state_two_cycle.py"
    "data/eight_state_two_four_cycles.py"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo -e "\n▶ $file:"
        head -n 7 "$file"
        echo "..."
    fi
done

echo -e "\n======================================================================"
echo "2. СТАТИСТИКА:"
echo "======================================================================"

total_py=$(find code/ data/ -name "*.py" -type f 2>/dev/null | wc -l)
with_header=$(grep -l "Verification of Engineering Emergence" code/*.py data/*.py 2>/dev/null | wc -l)
without_header=$((total_py - with_header))

echo "Всього Python файлів:     $total_py"
echo "З правильним header:      $with_header"
echo "Без header:               $without_header"

if [ $without_header -gt 0 ]; then
    echo -e "\n⚠️ ФАЙЛИ БЕЗ HEADER:"
    for file in code/*.py data/*.py; do
        if ! grep -q "Verification of Engineering Emergence" "$file" 2>/dev/null; then
            echo "  - $file"
        fi
    done
else
    echo -e "\n✓ ВСІ ФАЙЛИ МАЮТЬ СТАНДАРТНИЙ HEADER!"
fi

echo -e "\n======================================================================"
echo "3. ПЕРЕВІРКА ТІТУЛАТУРИ:"
echo "======================================================================"

# Перевіряємо чи є всі елементи
echo -e "\nНаявність ключових елементів:"
grep -h "Verification of Engineering Emergence" code/*.py data/*.py 2>/dev/null | wc -l | xargs echo "  'Verification...' знайдено:"
grep -h "Jansma & Hoel, 2025" code/*.py data/*.py 2>/dev/null | wc -l | xargs echo "  'Jansma & Hoel':"
grep -h "Author: Oleksii Onasenko" code/*.py data/*.py 2>/dev/null | wc -l | xargs echo "  'Author':"
grep -h "Developer: SubstanceNet" code/*.py data/*.py 2>/dev/null | wc -l | xargs echo "  'Developer':"

echo -e "\n======================================================================"
