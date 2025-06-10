#!/bin/bash

echo "Sage Running..."

# 提取第一个 code cell 的 source，并写入 temp.sage
python3 -c "
import nbformat
nb = nbformat.read(open('dprf-new-docker-share.ipynb'), as_version=4)
code = nb.cells[0]['source']
with open('first_cell.sage', 'w') as f:
    f.write(code)
"

# 用 sage 执行这段代码
sage first_cell.sage
