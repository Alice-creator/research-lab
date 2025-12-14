# Bayesian Network Mining Project

## 📌 Project Title

**English**: Design and Analysis of Algorithms Searching for Top-K High-Utility Bayesian Networks of Itemsets in Uncertain Databases

**Tiếng Việt**: Thiết kế và phân tích các thuật toán tìm kiếm top-K mạng Bayesian tiện ích cao của các tập mục trong cơ sở dữ liệu không chắc chắn

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository:**
   ```bash
   git clone git@github.com:Alice-creator/Bayesian-network.git
   cd bayesian-network
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Algorithms

#### 1. Naive Bayes Miner
```bash
cd naive_bayes_miner
python bayes_miner.py
```

#### 2. Heuristic Bayes Miner
```bash
cd heuristic_bayes_miner
python bayes_miner.py
```

#### 3. User-Defined Bayes Miner (Optimized)
```bash
cd user_define_bayes_miner
python bayes_miner.py
```

#### 4. Generate Performance Analysis Charts
```bash
python analysis.py
```

---

## 📊 Project Structure

```
bayesian-network/
├── README.md                          # This file
├── analysis.py                        # Performance analysis and visualization
├── analysis/                          # Generated analysis charts (PDF format)
│   ├── analysis_col_chart_*.pdf      # Runtime comparison charts
│   ├── user_database_*.pdf           # User-defined algorithm results
│   ├── heuristic_database_*.pdf      # Heuristic algorithm results
│   └── navie_*.pdf                   # Naive algorithm results
├── naive_bayes_miner/                 # Naive implementation
│   ├── bayes_miner.py                # Main algorithm
│   ├── utility_item.py               # Data structures
│   └── helper.py                     # Utility functions
├── heuristic_bayes_miner/            # Heuristic implementation
│   ├── bayes_miner.py                # Main algorithm with heuristics
│   ├── utility_item.py               # Data structures
│   └── helper.py                     # Utility functions
├── user_define_bayes_miner/          # Optimized implementation
│   ├── bayes_miner.py                # Optimized algorithm
│   ├── utility_item.py               # Data structures
│   └── helper.py                     # Utility functions
└── Papers/                           # Research papers and documentation
```

---

## 🔬 Algorithm Descriptions

### 1. Naive Bayes Miner
- **Purpose**: Basic implementation without optimizations
- **Features**: Standard depth-first search for itemset mining
- **Performance**: Baseline for comparison

### 2. Heuristic Bayes Miner
- **Purpose**: Enhanced with heuristic-based pruning
- **Features**: Uses utility and probability heuristics for ordering
- **Performance**: Moderate improvements over naive approach

### 3. User-Defined Bayes Miner
- **Purpose**: Optimized version with advanced pruning strategies
- **Features**: 
  - Early termination optimization
  - User-defined support parameters
  - Enhanced probability-based pruning
- **Performance**: ~23% faster than naive, ~28% faster than heuristic

---

## 🎯 Usage Examples

### Basic Usage
```python
from user_define_bayes_miner.bayes_miner import BayesianMiner
from user_define_bayes_miner.helper import create_utility_dict

# Sample database
DATABASE = [
    {
        "items": ["A", "B", "(CD)"],
        "quantities": [2, 1, 3],
        "profits": [6, 5, 9],
        "probabilities": [0.8, 0.75, 0.6]
    },
    # ... more transactions
]

# Create and run miner
miner = BayesianMiner(
    utility_dict=create_utility_dict(DATABASE),
    top_k=10,
    min_sup=0.5,
    transactions=len(DATABASE),
    database_utility=calculate_total_utility(DATABASE)
)

miner.run()
results = miner.get_top_k_candidates()
print(results)
```

### Customizing Parameters
- **`top_k`**: Number of top utility itemsets to find
- **`min_sup`**: Minimum support threshold (probability)
- **`support_probability`**: Additional support for uncertain items
- **`support_utility`**: Additional utility for uncertain items