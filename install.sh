echo "[INFO] Setting permissions"
chmod u+w .

echo "[INFO] Installing dependencies"
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    python -m termnovel
fi