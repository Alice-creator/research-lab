import kagglehub

# Download latest version
path = kagglehub.dataset_download("takihasan/div2k-dataset-for-super-resolution")

print("Path to dataset files:", path)