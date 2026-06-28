def get_device():
    try:
        import torch
    except ImportError:
        return "cpu"

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
    try:
        import torch
    except ImportError:
        return "CPU"
    device = get_device()
    if hasattr(device, "type") and device.type == "cuda":
        return torch.cuda.get_device_name(0)
    elif hasattr(device, "type") and device.type == "mps":
        return "Apple Silicon GPU"
    return "CPU"
