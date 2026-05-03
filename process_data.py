import csv
import glob
import os

input_files = sorted(glob.glob(os.path.join('data', 'daily_sales_data_*.csv')))
output_rows = []

for filepath in input_files:
    with open(filepath, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['product'].strip().lower() != 'pink morsel':
                continue
            price = float(row['price'].replace('$', '').strip())
            quantity = int(row['quantity'].strip())
            sales = price * quantity
            output_rows.append({
                'sales': f'${sales:.2f}',
                'date': row['date'].strip(),
                'region': row['region'].strip(),
            })

with open('output.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['sales', 'date', 'region'])
    writer.writeheader()
    writer.writerows(output_rows)

print(f"Done. {len(output_rows)} rows written to output.csv")
