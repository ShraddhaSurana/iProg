import json
import numpy as np
import matplotlib.pyplot as plt

def plot_task_images(data):
    """
    Function to plot the input and output images
    :param data: The data containing the input and output images
    :return: -
    """
    num_images = len(data)
    fig, axes = plt.subplots(num_images, 2, figsize=(10, 5 * num_images))

    fig.suptitle('')  # Empty suptitle to create space
    axes[0, 0].set_title('Input Images', pad=8, fontsize=22)
    axes[0, 1].set_title('Output Images', pad=8, fontsize=22)

    for i, d in enumerate(data):
        input_img = np.array(d['input'])
        output_img = np.array(d['output'])

        axes[i, 0].imshow(input_img, cmap='gray')
        # axes[i, 0].set_title('Input Image')
        # axes[i, 0].axis('off')
        axes[i, 0].set_xticks([])  # Hide x-axis ticks
        axes[i, 0].set_yticks([])
        for spine in axes[i, 0].spines.values():
            spine.set_color('blue')
            spine.set_linewidth(2)

        axes[i, 1].imshow(output_img, cmap='gray')
        # axes[i, 1].set_title('Output Image')
        # axes[i, 1].axis('off')
        axes[i, 1].set_xticks([])  # Hide x-axis ticks
        axes[i, 1].set_yticks([])
        for spine in axes[i, 1].spines.values():
            spine.set_edgecolor('blue')
            spine.set_linewidth(2)
    plt.tight_layout(h_pad=1.0)
    plt.savefig("catB_Task000", bbox_inches='tight', dpi=300)
    plt.show()

def visualize_task(json_file: str):
    """
    Function to visualize the task images
    :param json_file: The json file containing the task images
    :return: -
    """
    with open(json_file, 'r') as f:
        data = json.load(f)
    plot_task_images(data)


if __name__ == '__main__':
    # In order of toughness to solve.
    visualize_task('../Dataset/CatA_Simple/Task016.json')
    visualize_task('../Dataset/CatA_Hard/Task007.json')
    visualize_task('../Dataset/CatB_Sequence/Task007.json')
    visualize_task('../Dataset/CatB_Selection/Task007.json')
    visualize_task('../Dataset/CatB_Iteration/Task007.json')
    visualize_task('../Dataset/CatB_Hard/Task007.json')