import matplotlib.pyplot as plt

# Top-K categories
categories = ["TOP 20", "TOP 40", "TOP 60", "TOP 80", "TOP 100"]

# Runtime data for 5,000,000 transactions
naive_avg = [727.8721, 762.4198, 815.555, 836.1751, 843.6318]
heuristic_avg = [827.4073, 840.6344, 856.9411, 863.1453, 904.9607]
user_define_avg = [585.2622, 622.7732, 631.9967, 642.9455, 651.6969]

# X-axis positions
x = range(len(categories))
width = 0.25

# Plotting
plt.figure(figsize=(10, 6))
plt.bar([i - width for i in x], user_define_avg, width=width, label="User Define", color="#1f77b4")
plt.bar(x, naive_avg, width=width, label="Naive", color="#ff7f0e")
plt.bar([i + width for i in x], heuristic_avg, width=width, label="Heuristic", color="#2ca02c")

# Labels and styling
plt.xticks(ticks=x, labels=categories)
plt.xlabel("Top-K")
plt.ylabel("Run Time (seconds)")
plt.title("Run Time Comparison (5,000,000 Transactions)")
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Save to file
plt.savefig('analysis/analysis_col_chart_5000000_transactions.pdf')
