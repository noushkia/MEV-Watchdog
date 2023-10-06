# Make the script executable with command chmod +x <fileName>.

echo "$(date -u)" "Finding hosts"
python3 rpc_finder/get_rpcs.py

echo "$(date -u)" "Filtering and sorting hosts"
python3 rpc_finder/rpc_vitals_check.py

echo "$(date -u)" "Running up inspectors"
python3 inspect_many.py -a 14500000 -b 16500000 -p 8

echo "$(date -u)" "Done"
