# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt

# Assuming you have DataFrames with Tony's data and opponents' data
# Example data (replace with actual data)
tony_data = {
    "SLpM": 4.94,
    "Str. Acc.": 45,
    "TD Avg.": 0.39,
    "Sub. Avg.": 0.9
}

opponent_data = {
    "SLpM": 5.5,
    "Str. Acc.": 50,
    "TD Avg.": 0.8,
    "Sub. Avg.": 1.2
}

# Extract relevant metrics for comparison
metrics_of_interest = ['SLpM', 'Str. Acc.', 'TD Avg.', 'Sub. Avg.']

# Create DataFrames for comparison
tony_metrics = pd.DataFrame({metric: [tony_data[metric]] for metric in metrics_of_interest}, index=['Tony'])
opponent_metrics = pd.DataFrame({metric: [opponent_data[metric]] for metric in metrics_of_interest}, index=['Opponent'])

# Concatenate DataFrames
comparison_df = pd.concat([tony_metrics, opponent_metrics])

# Transpose the DataFrame for better visualization
comparison_df = comparison_df.T

# Visualize the comparisonpip
ax = comparison_df.plot(kind='bar', title='Comparison of Fight Metrics: Tony vs. Opponent with Longer Reach', rot=0)
ax.set_xlabel('Metrics')
ax.set_ylabel('Values')
plt.show()
