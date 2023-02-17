def c_TypeError(param_name: str, correct: str, wrong: str) -> TypeError:
    """
    Returns TypeError built from given params

    parameters:
        param_name: str - name of parameter
        correct: str - correct expected data type
        wrong: str - data type of param that param_name is refering too
    returns:
        TypeError(prebuilt message)
    """
    return TypeError(f"param:{param_name} must be type<{correct}> not type<{wrong}>")
