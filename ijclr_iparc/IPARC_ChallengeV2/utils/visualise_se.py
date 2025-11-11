import matplotlib.pyplot as plt
from IPARC_ChallengeV2.ListSelEm import list_se_3x3, list_se_3x3_names, list_se_5x5, list_se_5x5_names

# Function to plot structuring elements
def plot_structuring_elements(se_list, se_names, title):
    fig, axes = plt.subplots(1, len(se_list), figsize=(15, 5))
    fig.suptitle(title)
    for ax, se, name in zip(axes, se_list, se_names):
        print(name, se)
        ax.imshow(se, cmap='gray')
        ax.set_title(name)
        # ax.axis('off')
        for spine in ax.spines.values():  # Access all 4 borders (top, bottom, left, right)
            spine.set_color('blue')  # Set border color to blue
            spine.set_linewidth(2)  # Optional: Set border thickness
    plt.show()

# Plot 3x3 structuring elements
plot_structuring_elements(list_se_3x3, list_se_3x3_names, '3x3 Structuring Elements')

# Plot 5x5 structuring elements
plot_structuring_elements(list_se_5x5, list_se_5x5_names, '5x5 Structuring Elements')