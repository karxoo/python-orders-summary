# 📦 Python Orders Summary

A lightweight Python tool that processes order data from CSV files and generates a JSON summary.

## 📂 Project Structure
```text
.
├── .venv/                # Python virtual environment
├── .gitignore            # Files to exclude from Git
├── main.py               # Application entry point
├── orders_data.csv       # Sample input data
└── README.md             # Project documentation
```

## ⚡ Getting Started
### 1. Clone the repo
```bash
git clone https://github.com/karxoo/python-orders-summary.git
cd python-orders-summary
```

### 2. Set up Environment
```bash
# Activate virtual environment (Windows)
.\.venv\Scripts\activate
```

### 3. Run the Processor
```bash
python main.py
```

## 🔍 Example Output
- Input: orders_data.csv
- Output: (JSON printed to console or saved to file)

```json
{
  "total_revenue": 710,
  "best_selling_sku": {
    "sku": "SKU-A123",
    "total_quantity": 5
  }
}
```
