def custom_input(message, options) -> int:
    # This function takes a message and a list of options as parameters.
    try:
        just_list(options)  # Print the list of options for the user to choose from
        value = int(input(message))  # Get an integer input from the user
        if value < 1 or value > len(options):  # If the input is not a valid option number, raise a ValueError
            raise ValueError
        return value  # Return the selected option number
    except ValueError:  # If a ValueError is raised (i.e., the input is invalid), print an error message and call the function again
        print("Invalid input. Please try again.")
        return custom_input(message, options)


def just_list(options):
    # This function takes a list of options as a parameter and prints each option with a number
    for i, option_ in enumerate(options):
        print(f"{i + 1}. {option_}")


def input_with_type_validator(message, type_validator=str):
    # This function takes a message and a type validator function as parameters.
    try:
        value = input(message).strip()  # Get an input value from the user
        if not type_validator(value) or value == "":  # If the input value fails the type validation or is empty, raise a ValueError
            raise ValueError
        return value  # Return the validated input value
    except ValueError:  # If a ValueError is raised (i.e., the input is invalid), print an error message and call the function again
        print("Invalid input. Please try again.")
        return input_with_type_validator(message, type_validator)
