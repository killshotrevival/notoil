import random
import string

################################################### Main Declaration ###############################

def generate_random_string(length: int = 10):
    """
    Generate a random string of a given length

    Args:
        length (int, optional): The length of the random string. Defaults to 10

    Returns:
        str: A random string of the given length
    """
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))