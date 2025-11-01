import matplotlib.pyplot as plt

def generate_benchmark_chart(): # Function made with the help of AI, benchmarking inputs made from running main.py file
    # Data from the Hard Complexity setting in your final output:
    
    algorithms = ['BFS', 'DFS', 'IDDFS', 'Best-First', 'A*']
    
    # input for the mean nodes expanded for Hard setting:
    # BFS: 60.60, DFS: 70.00, IDDFS: 177.00, Best-First: 50.40, A*: 68.60
    means = [60.60, 70.00, 177.00, 50.40, 68.60]
    
    # input for the std deviation for nodes expanded for Hard setting:
    # BFS: 32.24, DFS: 23.42, IDDFS: 161.96, Best-First: 29.42, A*: 40.36
    stds = [32.24, 23.42, 161.96, 29.42, 40.36]

    # Define colors for better contrast
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

    plt.figure(figsize=(10, 6))
    
    # Create the bar chart with error bars (Std Dev)
    bars = plt.bar(algorithms, means, yerr=stds, capsize=5, color=colors)

    plt.ylabel('Mean Nodes Expanded (Search Effort)', fontsize=12)
    plt.title('Search Effort Comparison (Hard Complexity: 100 Nodes)', fontsize=14)
    plt.ylim(0, max(means) * 1.2) # Set y-limit slightly higher than max mean
    plt.grid(axis='y', linestyle='--', alpha=0.6)

    # Add text labels on top of the bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 5, f'{yval:.2f}', ha='center', va='bottom')

    plt.tight_layout()
    
    # Save the chart as a PNG file
    plt.savefig('Node_Expansion_Comparison.png')
    plt.close()
    
    print("Chart saved successfully as 'Node_Expansion_Comparison.png'")

if __name__ == "__main__":
    generate_benchmark_chart()