import csv
import json
import argparse
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

# -----------------------------
# Parse command-line arguments
# -----------------------------
def parse_args():
    parser = argparse.ArgumentParser(description="Process orders CSV and output JSON summary.")
    # --input : path to CSV file
    parser.add_argument("--input", required=True, help="Path to orders CSV file")
    # --output : path to JSON output file (default: orders_summary.json)
    parser.add_argument("--output", default="orders_summary.json", help="Path to write JSON output")
    return parser.parse_args()

# -----------------------------
# Convert values safely to Decimal
# -----------------------------
def to_decimal(value):
    try:
        return Decimal(str(value))  # ensures precise arithmetic (better than float)
    except Exception:
        raise ValueError(f"Invalid numeric value: {value}")

# -----------------------------
# Load orders from CSV file
# -----------------------------
def load_orders(csv_path):
    records = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)  # reads CSV into dictionary per row
        required = {"sku", "quantity", "price"}  # required columns
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing required CSV columns: {', '.join(sorted(missing))}")

        # Loop through each row in CSV
        for i, row in enumerate(reader, start=1):
            try:
                sku = row["sku"].strip()
                qty = to_decimal(row["quantity"])
                price = to_decimal(row["price"])
                if qty < 0 or price < 0:
                    raise ValueError("Negative values are not allowed.")
                # Save valid record
                records.append({"sku": sku, "quantity": qty, "price": price})
            except Exception as e:
                raise ValueError(f"Row {i} invalid: {e}")
    return records

# -----------------------------
# Calculate total revenue
# -----------------------------
def calculate_total_revenue(records):
    total = Decimal("0")
    for r in records:
        total += r["quantity"] * r["price"]  # revenue = quantity × price
    # Round to 2 decimal places
    return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

# -----------------------------
# Find best-selling SKU
# -----------------------------
def find_best_selling_sku(records):
    qty_by_sku = defaultdict(Decimal)
    for r in records:
        qty_by_sku[r["sku"]] += r["quantity"]

    if not qty_by_sku:
        return {"sku": None, "total_quantity": 0}

    # Find SKU with highest quantity
    # Tie-breaking: alphabetical order
    best_sku = max(sorted(qty_by_sku.items(), key=lambda x: x[0]), key=lambda x: x[1])
    sku, total_qty = best_sku

    # Convert Decimal to int if whole number, else float
    total_qty_out = int(total_qty) if total_qty == total_qty.to_integral_value() else float(total_qty)
    return {"sku": sku, "total_quantity": total_qty_out}

# -----------------------------
# Build JSON output structure
# -----------------------------
def build_output(total_revenue, best_selling):
    return {
        "total_revenue": float(total_revenue),  # convert Decimal → float for JSON
        "best_selling_sku": {
            "sku": best_selling["sku"],
            "total_quantity": best_selling["total_quantity"]
        }
    }

# -----------------------------
# Main program flow
# -----------------------------
def main():
    args = parse_args()  # get input/output file paths
    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        raise FileNotFoundError(f"Input CSV not found at: {input_path}")

    # Step 1: Load CSV
    records = load_orders(input_path)
    # Step 2: Calculate revenue
    total_revenue = calculate_total_revenue(records)
    # Step 3: Find best-selling SKU
    best_selling = find_best_selling_sku(records)
    # Step 4: Build JSON result
    result = build_output(total_revenue, best_selling)

    # Save JSON to file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # Print JSON to terminal
    print(json.dumps(result, ensure_ascii=False, indent=2))

# -----------------------------
# Entry point
# -----------------------------
if __name__ == "__main__":
    main()