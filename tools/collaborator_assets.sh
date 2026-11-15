#!/bin/sh
# Reuse the standard local qmcpy runtime; CI can supply its existing venv.
set -eu
script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
if [ -n "${COLLABORATOR_PYTHON:-}" ]; then
  collaborator_python=$COLLABORATOR_PYTHON
elif [ -x /opt/miniconda3/envs/qmcpy/bin/python ]; then
  collaborator_python=/opt/miniconda3/envs/qmcpy/bin/python
elif [ -x "$HOME/.conda/envs/qmcpy/bin/python" ]; then
  collaborator_python="$HOME/.conda/envs/qmcpy/bin/python"
else
  collaborator_python=python3
fi
exec "$collaborator_python" "$script_dir/collaborator_assets.py" "$@"
