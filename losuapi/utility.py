def c_TypeError(param_name: str, correct: str, wrong: str)-> TypeError:
    return TypeError(f"param:{param_name} must be type<{correct}> not type<{wrong}>")