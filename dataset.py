import torch
from torch.utils.data import Dataset, DataLoader, random_split

import os
import csv

# Define your custom dataset
class ParkingDataset(Dataset):
    def __init__(self):
        self.inputs = []
        self.targets = []

    def add_file(self, dataset_path):
        with open(dataset_path, "r") as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row
            for row in reader:
                self.inputs.append(
                    [
                        float(row[0]),
                        float(row[1]),
                        float(row[2]),
                        float(row[3]),
                        float(row[4]),
                    ]
                )
                self.targets.append([float(row[5])])

    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, idx):
        input_data = torch.tensor(self.inputs[idx], dtype=torch.float32)
        target_data = torch.tensor(self.targets[idx], dtype=torch.float32)
        return input_data, target_data


def load_data(batch_size=128):
    dataset = ParkingDataset()

    years = [2020, 2021, 2022, 2023]
    months = range(1, 13)
    for year in years:
        for month in months:
            filename = f"etl/data/processed/{year}/{month}/parking_data.csv"
            if os.path.isfile(filename):
                dataset.add_file(dataset_path=filename)

    num_train_samples = int(0.8 * len(dataset))
    num_val_samples = len(dataset) - num_train_samples
    train_dataset, val_dataset = random_split(
        dataset, [num_train_samples, num_val_samples]
    )
    train_data = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    valid_data = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

    return train_data, valid_data

def load_test_data(batch_size=128):
    dataset = ParkingDataset()
    filename = f"etl/data/test/parking_data.csv"
    dataset.add_file(dataset_path=filename)

    test_data = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    return test_data

train_data, valid_data = load_data()
