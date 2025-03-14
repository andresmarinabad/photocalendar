#!/bin/bash
apt install texlive texlive-latex-extra texlive-fonts-extra
python3 -m venv .env
source .env/bin/activate
pip install -r src/requirements.txt
