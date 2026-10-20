"""Execute analysis.ipynb in a fresh Jupyter kernel."""

import argparse
from pathlib import Path
import time

import nbformat
from nbclient import NotebookClient

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--offline-check', action='store_true',
                    help='Block external socket connections from the notebook kernel')
args = parser.parse_args()

root = Path(__file__).resolve().parents[1]
nb = nbformat.read(root / 'analysis.ipynb', as_version=4)
nbformat.validate(nb)

# The kernel needs local connections to Jupyter; external connections are blocked.
if args.offline_check:
    guard = nbformat.v4.new_code_cell('''
import socket
_original_connect = socket.socket.connect
_original_connect_ex = socket.socket.connect_ex
def _local_only(self, address):
    if isinstance(address, tuple) and address[0] not in ('127.0.0.1', '::1', 'localhost'):
        raise RuntimeError('Offline validation: external network access denied')
    return _original_connect(self, address)
def _local_only_ex(self, address):
    if isinstance(address, tuple) and address[0] not in ('127.0.0.1', '::1', 'localhost'):
        raise RuntimeError('Offline validation: external network access denied')
    return _original_connect_ex(self, address)
socket.socket.connect = _local_only
socket.socket.connect_ex = _local_only_ex
''')
    nb.cells.insert(0, guard)

start = time.perf_counter()
NotebookClient(nb, timeout=180, kernel_name='python3',
               resources={'metadata': {'path': str(root)}}).execute()

if args.offline_check:
    nb.cells.pop(0)
    for cell in nb.cells:
        if cell.cell_type == 'code' and cell.execution_count is not None:
            cell.execution_count -= 1
        for output in cell.get('outputs', []):
            if output.get('execution_count') is not None:
                output.execution_count -= 1

nbformat.validate(nb)
nbformat.write(nb, root / 'analysis.ipynb')
print(f'Executed {sum(cell.cell_type == "code" for cell in nb.cells)} code cells '
      f'in {time.perf_counter() - start:.1f} s (offline check: {args.offline_check}).')
