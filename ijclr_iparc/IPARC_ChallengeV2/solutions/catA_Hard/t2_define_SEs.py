"""Module ID: 2
Title: define SEs
Specification: You have the structuring elements. Put them in a function so that I can get them later easily
Inputs: given in the project specification
Output: function
"""

def get_structuring_elements():
    """
    Returns the predefined structuring elements as a dictionary.

    Returns:
    dict of {str: list[list[int]]}: A dictionary where the keys are the structuring element names and the
    values are their corresponding 3x3 binary matrices, represented as nested lists.
    """
    structuring_elements = {
        'SE1': [[1, 0, 1], [0, 1, 0], [1, 0, 1]],
        'SE2': [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
        'SE3': [[0, 1, 0], [1, 0, 1], [0, 1, 0]],
        'SE4': [[1, 1, 1], [1, 0, 1], [1, 1, 1]],
        'SE5': [[0, 0, 1], [0, 0, 1], [0, 0, 1]],
        'SE6': [[1, 0, 0], [1, 0, 0], [1, 0, 0]],
        'SE7': [[1, 1, 1], [0, 0, 0], [0, 0, 0]],
        'SE8': [[0, 0, 0], [0, 0, 0], [1, 1, 1]]
    }

    return structuring_elements

if __name__ == '__main__':
    # To get a specific structuring element, you can use the function like this:
    se = get_structuring_elements()
    print(se)
    print(se['SE1'])  # prints [[1, 0, 1], [0, 1, 0], [1, 0, 1]]