import torch
from torch import save
import torch.utils.tensorboard as tb
from models import RegressionLinear
from dataset import load_data
from os import path


def train(args):
    model = RegressionLinear(in_features=5, out_features=1)

    device = (
        torch.device("cuda")
        if torch.cuda.is_available()
        else torch.device("cpu")
    )
    print(f"Using Device: {device}")
    model = model.to(device)
    if args.continue_training:
        model.load_state_dict(torch.load(path.join(path.dirname(path.abspath(__file__)), 'parking.th')))
    if args.log_dir is not None:
        train_logger = tb.SummaryWriter(path.join(args.log_dir, "train"))
        valid_logger = tb.SummaryWriter(path.join(args.log_dir, "valid"))

    train_data, valid_data = load_data(batch_size=1280)
    loss = torch.nn.MSELoss()
    # Define optimizer
    optimizer = torch.optim.SGD(model.parameters(), lr=args.learning_rate)

    global_step = 0
    for epoch in range(args.num_epoch):
        print(f"starting epoch: {epoch}")
        model.train()
        for features, label in train_data:
            features, label = features.to(device), label.to(device)

            output = model(features)

            loss_val = loss(output, label)
            if train_logger is not None:
                train_logger.add_scalar("loss", loss_val, global_step)

            optimizer.zero_grad()
            loss_val.backward()
            optimizer.step()
            global_step += 1

        model.eval()
        loss_vals = []
        for features, label in valid_data:
            features, label = features.to(device), label.to(device)
            output = model(features)
            loss_vals.append(loss(output, label))
        avg_vloss = sum(loss_vals) / len(loss_vals)
        if valid_logger:
            valid_logger.add_scalar("accuracy", avg_vloss, global_step)
        print(
            f"epoch {epoch} \t learning rate ={optimizer.param_groups[0]['lr']} \t most recent loss val = {loss_val} \t validation loss = {avg_vloss} "
        )

    save(
        model.state_dict(),
        path.join(path.dirname(path.abspath(__file__)), "parking.th"),
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("--log_dir")
    # Put custom arguments here
    parser.add_argument("-n", "--num_epoch", type=int, default=50)
    parser.add_argument("-lr", "--learning_rate", type=float, default=1e-3)
    parser.add_argument('-c', '--continue_training', action='store_true')

    args = parser.parse_args()
    train(args)
