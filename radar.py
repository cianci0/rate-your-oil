import matplotlib.figure as figure
from math import pi

def radarchart(values, average_values, output_file='static/radar_chart.svg'):
    categories = ['Fruity', 'Grassy', 'Salty', 'Sweet', 'Floral', 'Pungent', 'Citrusy']
    num_vars = len(categories)

    angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
    angles += angles[:1]

    fig = figure.Figure(figsize=(7, 7))
    ax = fig.add_subplot(111, polar=True)

    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=12, ha='center', va='center')

    ax.set_yticklabels([])
    ax.set_ylim(0, 100)

    if average_values:
        print(len(average_values), len(values))
        
        average_values += average_values[:1]
        ax.plot(angles, average_values, linewidth=0, linestyle='solid', color='lightgray')
        ax.fill(angles, average_values, 'lightgray', alpha=1)

    if values:
        values += values[:1]
        ax.plot(angles, values, linewidth=1, linestyle='solid', color='#ffd500')
        ax.fill(angles, values, '#ffd500', alpha=0.5)

    fig.savefig(output_file, format='svg')
