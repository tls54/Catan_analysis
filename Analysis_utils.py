import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import MaxNLocator
from matplotlib.lines import Line2D


def plot_roll_distribution(series, title="Roll Distribution", dice_count=None):
    """
    Plots a histogram of dice rolls using Seaborn for improved visuals.

    Parameters:
        series (pd.Series): The input data (e.g., dice rolls)
        title (str): Title for the plot
        dice_count (int, optional): Number of dice (1 or 2). If None, will attempt to auto-detect.
    """
    # Ensure we have proper integer bins
    min_val = series.min()
    max_val = series.max()
    bins = np.arange(min_val, max_val + 2) - 0.5  # Offset for proper bin centering
    
    # Auto-detect dice count if not specified
    if dice_count is None:
        if min_val >= 1 and max_val <= 6:
            dice_count = 1  # Likely single die (d6)
        elif min_val >= 2 and max_val <= 12:
            dice_count = 2  # Likely two dice (2d6)
        else:
            dice_count = 0  # Unknown or custom dice configuration
    
    # Set up the figure
    plt.figure(figsize=(10, 6))
    
    # Create the plot with Seaborn
    ax = sns.histplot(
        series, 
        bins=bins,
        discrete=True,
        kde=False,
        stat="count",
        color="cornflowerblue",
        edgecolor="darkblue",
        linewidth=1.5,
        alpha=0.8
    )
    
    # Add expected distribution line based on dice count
    total_rolls = len(series)
    
    if dice_count == 1:  # Single die (d6)
        sides = max_val
        expected_prob = 1/sides
        expected_counts = {i: expected_prob * total_rolls for i in range(min_val, max_val + 1)}
        
        x_vals = list(expected_counts.keys())
        y_vals = list(expected_counts.values())
        ax.plot(x_vals, y_vals, 'o-', color='red', linewidth=2, 
                label='Expected Distribution', markersize=6)
        plt.legend()
            
    elif dice_count == 2:  # Two dice (2d6)

        # Expected probabilities for 2d6
        expected_probs = {
            2: 1/36, 3: 2/36, 4: 3/36, 5: 4/36, 6: 5/36, 7: 6/36,
            8: 5/36, 9: 4/36, 10: 3/36, 11: 2/36, 12: 1/36
        }
        
        # Scale the expected probabilities to match our data
        expected_counts = {k: v * total_rolls for k, v in expected_probs.items()}
        
        x_vals = list(expected_counts.keys())
        y_vals = list(expected_counts.values())
        ax.plot(x_vals, y_vals, 'o-', color='red', linewidth=2, 
                label='Expected Distribution', markersize=6)
        plt.legend()
    
    # Customize the plot
    plt.xticks(range(min_val, max_val + 1))
    plt.xlabel('Roll Value', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    
    # Add value labels on top of bars
    for p in ax.patches:
        height = p.get_height()
        if height > 0:  # Only add labels to bars with data
            ax.text(
                p.get_x() + p.get_width()/2.,
                height + 0.3,
                f'{int(height)}',
                ha="center", fontsize=9
            )
    
    # Add grid and style
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    sns.despine(left=False, bottom=False)
    plt.tight_layout()
    plt.show()



def compare_roll_distributions(series1, series2, label1="Series 1", label2="Series 2", 
                                title="Comparison of Roll Distributions", plot_type="side_by_side"):
    """
    Plots two dice roll distributions for comparison using Seaborn.

    Parameters:
        series1 (pd.Series): First set of dice roll data
        series2 (pd.Series): Second set of dice roll data
        label1 (str): Label for the first series
        label2 (str): Label for the second series
        title (str): Plot title
        plot_type (str): Type of plot to use:
            - "side_by_side": Bar chart with groups side by side (default)
            - "overlay": Overlaid histograms
            - "kde": Kernel density estimation plot
    """
    # Determine the range of values
    min_val = min(series1.min(), series2.min())
    max_val = max(series1.max(), series2.max())
    
    # Create a combined dataframe for easier plotting
    df1 = pd.DataFrame({
        'Value': series1, 
        'Distribution': label1
    })
    
    df2 = pd.DataFrame({
        'Value': series2, 
        'Distribution': label2
    })
    
    combined_df = pd.concat([df1, df2])
    
    # Set the style
    sns.set_style("whitegrid")
    plt.figure(figsize=(12, 7))
    
    if plot_type == "side_by_side":
        # Side-by-side bar chart
        ax = sns.countplot(
            data=combined_df,
            x='Value',
            hue='Distribution',
            palette=['cornflowerblue', 'lightcoral'],
            edgecolor='black',
            alpha=0.8
        )
        
        # Add count labels on top of bars
        for container in ax.containers:
            ax.bar_label(container, fmt='%d', fontsize=9)
            
    elif plot_type == "overlay":
        # Overlaid histograms
        bins = np.arange(min_val, max_val + 2) - 0.5
        
        ax = sns.histplot(
            data=combined_df,
            x='Value',
            hue='Distribution',
            bins=bins,
            discrete=True,
            stat='count',
            palette=['cornflowerblue', 'lightcoral'],
            alpha=0.6,
            multiple='layer',
            edgecolor='black',
            linewidth=1.5
        )
        
    elif plot_type == "kde":
        # Kernel density plots with rugs
        ax = sns.kdeplot(
            data=combined_df,
            x='Value',
            hue='Distribution',
            palette=['cornflowerblue', 'lightcoral'],
            linewidth=2.5,
            common_norm=False,
            fill=True,
            alpha=0.4
        )
        
        # Add rug plot to show actual data points
        sns.rugplot(
            data=combined_df,
            x='Value',
            hue='Distribution',
            palette=['cornflowerblue', 'lightcoral'],
            height=0.1,
            alpha=0.7
        )
    
    # Customize the plot
    plt.xlabel('Roll Value', fontsize=12)
    plt.ylabel('Frequency' if plot_type != "kde" else 'Density', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    
    # Set integer ticks on x-axis
    plt.xticks(range(min_val, max_val + 1))
    
    # Force y-axis ticks to be integers for count plots
    if plot_type != "kde":
        ax = plt.gca()
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    
    # Add legend with a title
    plt.legend(title="Distribution")
    
    sns.despine(left=False, bottom=False)
    plt.tight_layout()
    plt.show()
    
    # Print statistical comparison
    print(f"Statistical Summary:")
    print(f"{label1}: Mean = {series1.mean():.2f}, Median = {series1.median():.2f}, Std = {series1.std():.2f}")
    print(f"{label2}: Mean = {series2.mean():.2f}, Median = {series2.median():.2f}, Std = {series2.std():.2f}")




def plot_rolls_over_time(series, title="Rolls Over Time", xlabel="Roll Number", ylabel="Roll Value", 
                        highlight_sevens=True, show_average=True, rolling_window=None):
    """
    Plots a line graph showing roll values over time (roll sequence) with enhanced visuals.

    Parameters:
        series (pd.Series): Series of integer roll values ordered by time
        title (str): Plot title
        xlabel (str): Label for x-axis (default "Roll Number")
        ylabel (str): Label for y-axis (default "Roll Value")
        highlight_sevens (bool): Whether to highlight rolls of 7 (triggers the robber in Catan)
        show_average (bool): Whether to show the running average
        rolling_window (int): If provided, adds a rolling average line with specified window size
    """
    # Create a figure with a nice background style
    sns.set_style("whitegrid")
    plt.figure(figsize=(12, 7))
    
    # Plot the main roll values
    ax = plt.gca()
    
    # Determine if we're dealing with single dice (d6) or two dice (2d6)
    min_val = series.min()
    max_val = series.max()
    is_d6 = (min_val >= 1 and max_val <= 6)
    is_2d6 = (min_val >= 2 and max_val <= 12)
    
    # Create a colormap for the points based on roll values
    if is_2d6:
        # For 2d6, highlight 7s (triggers robber in Catan) and colorize other points
        # based on probability (rarer rolls are darker)
        colors = []
        sizes = []
        has_sevens = False
        
        for val in series:
            if val == 7 and highlight_sevens:
                colors.append('red')
                sizes.append(100)  # Larger marker for 7s
                has_sevens = True
            else:
                # Calculate probability-based color intensity
                # 7 is most common (6/36), 2 and 12 are least common (1/36)
                prob = {
                    2: 1/36, 3: 2/36, 4: 3/36, 5: 4/36, 6: 5/36, 7: 6/36,
                    8: 5/36, 9: 4/36, 10: 3/36, 11: 2/36, 12: 1/36
                }.get(val, 0)
                
                # Convert probability to color intensity (darker = rarer)
                intensity = 1 - (prob * 36 / 6)  # Normalize to 0-1 range
                colors.append(plt.cm.Blues(0.5 + intensity/2))
                sizes.append(60)  # Regular marker size
    else:
        # For single dice, use a gradient color scheme
        colors = plt.cm.viridis(np.linspace(0, 1, len(series)))
        sizes = [60] * len(series)  # Consistent size
        has_sevens = False
    
    # Plot the points with appropriate colors and sizes
    for i, (idx, val) in enumerate(series.items()):
        plt.scatter(idx, val, color=colors[i], s=sizes[i], zorder=3, edgecolor='black', linewidth=0.5)
    
    # Connect the points with a line
    plt.plot(series.index, series.values, color='gray', linestyle='-', alpha=0.5, zorder=1)
    
    # Add annotations for 7s if highlighting is enabled and we're using 2d6
    if highlight_sevens and is_2d6:
        sevens_count = 0
        for idx, val in series.items():
            if val == 7:
                sevens_count += 1
                plt.annotate(f"7", (idx, val), 
                             xytext=(0, 7), textcoords='offset points',
                             ha='center', fontsize=9, fontweight='bold', color='white')
        
        # Add a note about sevens
        if sevens_count > 0:
            plt.figtext(0.01, 0.01, f"Robber moves: {sevens_count} times", 
                        fontsize=9, style='italic')
    
    # Prepare legend elements
    legend_elements = []
    
    # Add roll type to legend 
    if is_d6:
        legend_elements.append(Line2D([0], [0], marker='o', color='gray', label='Single Die Roll',
                                     markerfacecolor=plt.cm.viridis(0.5), markersize=8, alpha=0.7,
                                     linestyle='-'))
    elif is_2d6:
        legend_elements.append(Line2D([0], [0], marker='o', color='gray', label='Two Dice Roll',
                                     markerfacecolor=plt.cm.Blues(0.7), markersize=8, alpha=0.7,
                                     linestyle='-'))
    
    # Add 7s to legend if they exist
    if has_sevens:
        legend_elements.append(Line2D([0], [0], marker='o', color='w', label='Robber (Roll of 7)',
                                     markerfacecolor='red', markersize=10,
                                     linestyle=''))
    
    # Add a running average line if requested
    if show_average:
        running_avg = [series.iloc[:i+1].mean() for i in range(len(series))]
        plt.plot(series.index, running_avg, color='green', linestyle='--', 
                 linewidth=2, alpha=0.7)
        legend_elements.append(Line2D([0], [0], color='green', lw=2, linestyle='--',
                                     label='Running Average'))
    
    # Add a rolling average if requested
    if rolling_window and rolling_window < len(series):
        rolling_avg = series.rolling(window=rolling_window, min_periods=1).mean()
        plt.plot(series.index, rolling_avg, color='purple', linestyle='-.',
                 linewidth=2, alpha=0.7)
        legend_elements.append(Line2D([0], [0], color='purple', lw=2, linestyle='-.',
                                     label=f'{rolling_window}-Roll Moving Average'))
    
    # Add reference lines for expected values
    if is_d6:
        plt.axhline(y=3.5, color='darkblue', linestyle=':', alpha=0.5, 
                   linewidth=1.5)
        legend_elements.append(Line2D([0], [0], color='darkblue', lw=1.5, linestyle=':',
                                     label='Expected Value (3.5)'))
    elif is_2d6:
        plt.axhline(y=7, color='darkblue', linestyle=':', alpha=0.5, 
                   linewidth=1.5)
        legend_elements.append(Line2D([0], [0], color='darkblue', lw=1.5, linestyle=':',
                                     label='Expected Value (7)'))
    
    # Add legend with all elements
    plt.legend(handles=legend_elements, loc='best')
    
    # Set axis labels and title
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    
    # Set y-axis to show only integer values and a reasonable range
    plt.yticks(range(min_val, max_val + 1))
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    
    # Set x-axis to show roll numbers at reasonable intervals
    num_rolls = len(series)
    if num_rolls <= 20:
        plt.xticks(series.index)
    else:
        # Choose a reasonable number of ticks based on plot width
        tick_step = max(1, num_rolls // 15)  # Show about 15 ticks max
        plt.xticks(series.index[::tick_step])
    
    # Add a grid for easier reading
    plt.grid(True, linestyle='--', alpha=0.4)
    
    # Add statistical information
    stats_text = (
        f"Mean: {series.mean():.2f}\n"
        f"Median: {series.median()}\n"
        f"Std Dev: {series.std():.2f}\n"
        f"Total Rolls: {len(series)}"
    )
    plt.figtext(0.01, 0.97, stats_text, fontsize=9, 
                bbox=dict(facecolor='white', alpha=0.5, boxstyle='round,pad=0.5'))
    
    # Remove spines
    sns.despine(left=False, bottom=False)
    
    plt.tight_layout()
    plt.show()





def compare_rolls_over_time(series1, series2, label1="Series 1", label2="Series 2", 
                            title="Comparison of Rolls Over Time", xlabel="Roll Number", ylabel="Roll Value",
                            highlight_sevens=True, show_running_avg=True, show_difference=True):
    """
    Plots two integer roll series over time for comparison with enhanced visuals.

    Parameters:
        series1 (pd.Series): First roll series (ordered by time)
        series2 (pd.Series): Second roll series (ordered by time)
        label1 (str): Label for first series
        label2 (str): Label for second series
        title (str): Plot title
        xlabel (str): X-axis label
        ylabel (str): Y-axis label
        highlight_sevens (bool): Whether to highlight rolls of 7
        show_running_avg (bool): Whether to show running averages
        show_difference (bool): Whether to show difference subplot
    """
    # Set the Seaborn style
    sns.set_style("whitegrid")
    
    # Determine if we're showing the difference subplot
    if show_difference:
        # Create a figure with two subplots (main plot and difference plot)
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 9), gridspec_kw={'height_ratios': [3, 1]})
    else:
        # Create a single plot
        fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # Determine if we're dealing with 2d6 (Catan standard) or something else
    min_val = min(series1.min(), series2.min())
    max_val = max(series1.max(), series2.max())
    is_2d6 = (min_val >= 2 and max_val <= 12)
    
    # Color setup
    color1 = 'cornflowerblue'
    color2 = 'lightcoral'
    
    # Plot first series with highlighting for 7s
    for i, (idx, val) in enumerate(series1.items()):
        if is_2d6 and val == 7 and highlight_sevens:
            ax1.scatter(idx, val, color='darkblue', s=100, zorder=3, edgecolor='black', linewidth=0.5)
        else:
            ax1.scatter(idx, val, color=color1, s=60, zorder=3, alpha=0.8, edgecolor='black', linewidth=0.5)
    
    # Plot second series with highlighting for 7s
    for i, (idx, val) in enumerate(series2.items()):
        if is_2d6 and val == 7 and highlight_sevens:
            ax1.scatter(idx, val, color='darkred', s=100, zorder=3, edgecolor='black', linewidth=0.5, marker='s')
        else:
            ax1.scatter(idx, val, color=color2, s=60, zorder=3, alpha=0.8, edgecolor='black', linewidth=0.5, marker='s')
    
    # Connect points with lines
    ax1.plot(series1.index, series1.values, color=color1, linestyle='-', alpha=0.6, zorder=2, linewidth=1.5)
    ax1.plot(series2.index, series2.values, color=color2, linestyle='-', alpha=0.6, zorder=2, linewidth=1.5)
    
    # Add running averages if requested
    if show_running_avg:
        # Calculate running averages
        running_avg1 = [series1.iloc[:i+1].mean() for i in range(len(series1))]
        running_avg2 = [series2.iloc[:i+1].mean() for i in range(len(series2))]
        
        # Plot running averages
        ax1.plot(series1.index, running_avg1, color='darkblue', linestyle='--', 
                linewidth=2, alpha=0.7, zorder=4)
        ax1.plot(series2.index, running_avg2, color='darkred', linestyle='--', 
                linewidth=2, alpha=0.7, zorder=4)
    
    # Add reference line for expected value if we're dealing with dice
    if is_2d6:
        ax1.axhline(y=7, color='black', linestyle=':', alpha=0.5, linewidth=1.5)
    elif min_val >= 1 and max_val <= 6:  # Likely single die
        ax1.axhline(y=3.5, color='black', linestyle=':', alpha=0.5, linewidth=1.5)
    
    # Create the legend elements
    legend_elements = [
        Line2D([0], [0], marker='o', color=color1, label=f"{label1}", markersize=8,
                markerfacecolor=color1, linestyle='-'),
        Line2D([0], [0], marker='s', color=color2, label=f"{label2}", markersize=8,
                markerfacecolor=color2, linestyle='-')
    ]
    
    # Add running average elements to legend if enabled
    if show_running_avg:
        legend_elements.extend([
            Line2D([0], [0], color='darkblue', lw=2, linestyle='--',
                label=f"{label1} Running Avg"),
            Line2D([0], [0], color='darkred', lw=2, linestyle='--',
                label=f"{label2} Running Avg")
        ])
    
    # Add 7s to legend if highlighted
    if is_2d6 and highlight_sevens:
        legend_elements.extend([
            Line2D([0], [0], marker='o', color='w', label=f"{label1} Robber (7)",
                markerfacecolor='darkblue', markersize=10, linestyle=''),
            Line2D([0], [0], marker='s', color='w', label=f"{label2} Robber (7)",
                markerfacecolor='darkred', markersize=10, linestyle='')
        ])
    
    # Add expected value to legend
    if is_2d6:
        legend_elements.append(Line2D([0], [0], color='black', lw=1.5, linestyle=':',
                                    label='Expected Value (7)'))
    elif min_val >= 1 and max_val <= 6:
        legend_elements.append(Line2D([0], [0], color='black', lw=1.5, linestyle=':',
                                    label='Expected Value (3.5)'))
    
    # Add the legend
    ax1.legend(handles=legend_elements, loc='best')
    
    # Set axis labels and title
    ax1.set_title(title, fontsize=14, fontweight='bold')
    ax1.set_xlabel(xlabel, fontsize=12)
    ax1.set_ylabel(ylabel, fontsize=12)
    
    # Set y-axis to show only integer values
    ax1.set_yticks(range(min_val, max_val + 1))
    
    # Add grid
    ax1.grid(True, linestyle='--', alpha=0.4)
    
    # Add statistical information for both series
    stats_text = (
        f"{label1}: Mean={series1.mean():.2f}, Median={series1.median()}, σ={series1.std():.2f}\n"
        f"{label2}: Mean={series2.mean():.2f}, Median={series2.median()}, σ={series2.std():.2f}"
    )
    
    ax1.text(0.01, 0.97, stats_text, transform=ax1.transAxes, fontsize=9,
            bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.5'),
            verticalalignment='top')
    
    # Plot the difference subplot if requested
    if show_difference:
        # Calculate difference where indexes overlap
        common_indices = series1.index.intersection(series2.index)
        diff_series = series1.loc[common_indices] - series2.loc[common_indices]
        
        # Plot the difference
        ax2.bar(diff_series.index, diff_series.values, color='lightgrey', 
                edgecolor='black', alpha=0.7)
        
        # Add a horizontal line at zero
        ax2.axhline(y=0, color='black', linestyle='-', linewidth=1)
        
        # Set labels
        ax2.set_xlabel(xlabel, fontsize=12)
        ax2.set_ylabel(f"Difference\n({label1} - {label2})", fontsize=12)
        
        # Set y-axis to show reasonable integer values
        max_diff = max(abs(diff_series.min()), abs(diff_series.max()))
        if max_diff > 0:
            ax2.set_yticks(range(-int(max_diff)-1, int(max_diff)+2))
        
        # Add grid to difference plot
        ax2.grid(True, linestyle='--', alpha=0.4)
        
        # Add difference statistics
        diff_stats = f"Diff Mean: {diff_series.mean():.2f}, Std: {diff_series.std():.2f}"
        ax2.text(0.01, 0.85, diff_stats, transform=ax2.transAxes, fontsize=9,
                bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.5'))
    
    # Remove spines
    sns.despine(ax=ax1, left=False, bottom=False)
    if show_difference:
        sns.despine(ax=ax2, left=False, bottom=False)
    
    plt.tight_layout()
    plt.show()
    
    # Print additional statistical information
    print(f"Statistical Summary:")
    print(f"{label1}: Mean = {series1.mean():.2f}, Median = {series1.median()}, Std Dev = {series1.std():.2f}")
    print(f"{label2}: Mean = {series2.mean():.2f}, Median = {series2.median()}, Std Dev = {series2.std():.2f}")
    
    if len(common_indices) > 0:
        print(f"Difference ({label1} - {label2}):")
        print(f"  Mean = {diff_series.mean():.2f}, Std Dev = {diff_series.std():.2f}")
        if is_2d6:
            print(f"  Robber moves: {label1}: {(series1 == 7).sum()}, {label2}: {(series2 == 7).sum()}")