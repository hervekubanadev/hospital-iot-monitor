echo "Starting log archiving process..."

TIMESTAMP=$(date + "%Y%m%d_%H%M")

for log_file in active_logs/*.log; do
    filename=$(basename "$log_file")
    base="${filename%.log}"
    new_name="${base}_${TIMESTAMP}.log"

   echo "Archiving $filename to archived_logs/$new_name"
   mv "$log_file" "archived_logs/$new_name"
