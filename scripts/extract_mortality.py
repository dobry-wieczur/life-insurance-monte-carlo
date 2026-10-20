"""Recreate the mortality CSV from the bundled GUS Table A workbook."""

import csv
import hashlib
from pathlib import Path

import openpyxl

root = Path(__file__).resolve().parents[1]
source = root / 'data/source/gus_table_a_2025.xlsx'
expected_hash = '5dfcaa6b785770ec9c8bc09e26d406222c7f87d7d92af5f1b414d0352ac0fbf8'
assert hashlib.sha256(source.read_bytes()).hexdigest() == expected_hash, 'Unexpected GUS workbook'

workbook = openpyxl.load_workbook(source, read_only=True, data_only=True)
sheet = workbook['Ogółem mężczyźni']
assert sheet['A5'].value == 'x' and sheet['B5'].value == 'qx'
assert sheet['B6'].value == 'Mężczyźni ogółem'

rows = []
for age, row in [(30, 37), (45, 52), (60, 67)]:
    assert sheet[f'A{row}'].value == age
    cell = f'B{row}'
    q = sheet[cell].value
    assert isinstance(q, (int, float)) and 0 <= q <= 1
    rows.append((age, f'{q:.5f}', 'male', cell))

workbook.close()
assert [float(row[1]) for row in rows] == [0.00117, 0.00346, 0.01313]

with (root / 'data/mortality_2025.csv').open('w', newline='') as file:
    writer = csv.writer(file, lineterminator='\n')
    writer.writerow(['age', 'q_x', 'sex', 'source_cell'])
    writer.writerows(rows)

print('Extracted GUS mortality data:', rows)
