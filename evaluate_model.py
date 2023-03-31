import torch
from torch import save
import torch.utils.tensorboard as tb
from models import RegressionLinear
from dataset import load_test_data
from os import path
import csv

model = RegressionLinear(in_features=5, out_features=1)
device = (
        torch.device("cuda")
        if torch.cuda.is_available()
        else torch.device("cpu")
    )
print(f"Using Device: {device}")
model = model.to(device)
model.load_state_dict(torch.load(path.join(path.dirname(path.abspath(__file__)), 'parking.th')))

test_data = load_test_data(batch_size=1280)
loss = torch.nn.MSELoss()
model.eval()
data = []
loss_vals=[]
for features, label in test_data:
    features, label = features.to(device), label.to(device)
    output = model(features)
    loss_val = loss(output, label)
    loss_vals.append(loss_val)

    features = features.data.cpu().tolist()
    label = label.data.cpu().tolist()
    output = output.data.cpu().tolist()
    data.append(zip(features,label,output))

avg_vloss = sum(loss_vals) / len(loss_vals)
print(f"loss = {avg_vloss}")


# open the CSV file in write mode
with open('eval.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    # write the data to the CSV file
    for row in data:
        for col in row:
            writer.writerow(col[0] + col[1] + col[2])