import torch.nn as nn

class Net_Conv(nn.Module):
    def __init__(self, num_features, num_categories):
        super(Net_Conv, self).__init__()
        p = 1
        self.conv1 = nn.Conv1d(1, 32, kernel_size=5, stride=1, padding='same')
        self.maxpool1 = nn.MaxPool1d(kernel_size=5, stride=2, padding=1)
        self.conv2 = nn.Conv1d(32, 64, kernel_size=5, stride=1, padding='same')
        self.maxpool2 = nn.MaxPool1d(kernel_size=5, stride=2, padding=1)
        self.conv3 = nn.Conv1d(64, 128, kernel_size=5, stride=1, padding='same')
        self.maxpool3 = nn.MaxPool1d(kernel_size=5, stride=2, padding=1)
        self.dropout = nn.Dropout(0.2)
        self.conv4 = nn.Conv1d(128, 128, kernel_size=5, stride=1, padding='same')
        self.maxpool4 = nn.MaxPool1d(kernel_size=5, stride=2, padding=1)
        self.flatten = nn.Flatten()
        input_size = ((((num_features - p) // 2 - p) // 2 - p) // 2 - p) // 2
        self.fc1 = nn.Linear(128 * input_size, 4 * num_categories)  # 3776  2 * num_features

        self.fc12 = nn.Linear(4 * num_categories, 2 * num_categories)
        self.fc2 = nn.Linear(2 * num_categories, num_categories)
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = x.view(x.size(0), -1).unsqueeze(1)
        x = self.conv1(x)
        x = self.relu(x)
        x = self.maxpool1(x)
        x = self.conv2(x)
        x = self.relu(x)
        x = self.maxpool2(x)
        x = self.conv3(x)
        x = self.relu(x)
        x = self.maxpool3(x)
        x = self.dropout(x)
        x = self.conv4(x)
        x = self.relu(x)
        x = self.maxpool4(x)
        x = self.flatten(x)
        x = self.fc1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc12(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.sigmoid(x)
        return x
