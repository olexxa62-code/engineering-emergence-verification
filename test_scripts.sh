#!/bin/bash

echo "======================================================================"
echo "ТЕСТ 1: Синтаксична перевірка Python файлів"
echo "======================================================================"
echo ""

error_count=0

for script in code/*.py data/*.py; do
    if [ -f "$script" ]; then
        echo -n "Перевірка $script ... "
        if python3 -m py_compile "$script" 2>/dev/null; then
            echo "[OK]"
        else
            echo "[FAILED]"
            python3 -m py_compile "$script"
            ((error_count++))
        fi
    fi
done

echo ""
echo "Помилок синтаксису: $error_count"

if [ $error_count -gt 0 ]; then
    echo "[FAILED] Виправте помилки перед продовженням"
    exit 1
fi

echo ""
echo "======================================================================"
echo "ТЕСТ 2: Перевірка імпортів"
echo "======================================================================"
echo ""

echo "Тест імпорту numpy..."
python3 -c "import numpy; print(f'NumPy version: {numpy.__version__}')" || exit 1

echo "Тест імпорту matplotlib..."
python3 -c "import matplotlib; print(f'Matplotlib version: {matplotlib.__version__}')" || exit 1

echo ""
echo "[OK] Всі бібліотеки доступні"

echo ""
echo "======================================================================"
echo "ТЕСТ 3: Швидкий тест data файлів"
echo "======================================================================"
echo ""

echo "Тест six_state_two_cycle.py..."
python3 -c "
import sys
sys.path.insert(0, 'data')
from six_state_two_cycle import create_two_cycle_tpm
T = create_two_cycle_tpm(p_self=0.2)
assert T.shape == (6, 6), 'Wrong shape'
assert abs(T.sum(axis=1) - 1.0).max() < 1e-10, 'Not stochastic'
print(f'  [OK] 6-state TPM: shape {T.shape}, stochastic')
" || exit 1

echo "Тест eight_state_two_four_cycles.py..."
python3 -c "
import sys
sys.path.insert(0, 'data')
from eight_state_two_four_cycles import create_tpm
T = create_tpm(p_self=0.2)
assert T.shape == (8, 8), 'Wrong shape'
assert abs(T.sum(axis=1) - 1.0).max() < 1e-10, 'Not stochastic'
print(f'  [OK] 8-state TPM: shape {T.shape}, stochastic')
" || exit 1

echo "Тест ten_state_two_five_cycles.py..."
python3 -c "
import sys
sys.path.insert(0, 'data')
from ten_state_two_five_cycles import create_two_five_cycle_tpm
T = create_two_five_cycle_tpm(p_self=0.2)
assert T.shape == (10, 10), 'Wrong shape'
assert abs(T.sum(axis=1) - 1.0).max() < 1e-10, 'Not stochastic'
print(f'  [OK] 10-state TPM: shape {T.shape}, stochastic')
" || exit 1

echo ""
echo "======================================================================"
echo "ТЕСТ 4: Швидкий тест core функцій"
echo "======================================================================"
echo ""

echo "Тест ce2_core.py..."
python3 -c "
import sys
sys.path.insert(0, 'code')
from ce2_core import calculate_determinism, calculate_degeneracy, calculate_cp
import numpy as np

# Тестовий TPM (2x2 детермінований)
T = np.array([[0.0, 1.0], [1.0, 0.0]])
det = calculate_determinism(T)
deg = calculate_degeneracy(T)
cp = calculate_cp(T)

print(f'  Determinism: {det:.4f}')
print(f'  Degeneracy: {deg:.4f}')
print(f'  CP: {cp:.4f}')
assert det == 1.0, f'Determinism should be 1.0, got {det}'
assert cp == 1.0, f'CP should be 1.0 for permutation, got {cp}'
print('  [OK] Core functions work correctly')
" || exit 1

echo ""
echo "======================================================================"
echo "ВСІ БАЗОВІ ТЕСТИ ПРОЙДЕНО!"
echo "======================================================================"
echo ""
echo "Скрипти готові до використання"
