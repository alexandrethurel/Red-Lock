import torch

print(torch.version.cuda)  # Version CUDA de ton PyTorch
print(torch.cuda.is_available())  # Doit être True
print(torch.cuda.device_count())  # Doit être >= 1
print(torch.cuda.get_device_name(0))  # Nom de ton GPU