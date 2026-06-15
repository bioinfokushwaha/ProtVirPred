import torch


def get_device():

    if torch.cuda.is_available():

        return torch.device("cuda")

    elif (
        hasattr(torch.backends, "mps")
        and torch.backends.mps.is_available()
    ):

        return torch.device("mps")

    else:

        return torch.device("cpu")


DEVICE = get_device()


def get_device_name():

    if DEVICE.type == "cuda":

        return torch.cuda.get_device_name(0)

    elif DEVICE.type == "mps":

        return "Apple Silicon GPU"

    else:

        return "CPU"