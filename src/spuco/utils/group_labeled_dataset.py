from typing import Dict, List, Tuple
import torch
from torch.utils.data import Dataset

class GroupLabeledDataset(Dataset):
    def __init__(
        self, 
        dataset: Dataset,
        group_partition: Dict[Tuple[int, int], int],
    ):
        self.dataset = dataset
        self.group = torch.zeros(len(self.dataset))
        self.group_partition = group_partition
        
        group_idx = 0
        for key in sorted(group_partition.keys()):
            self.group[group_partition[key]] = group_idx
            group_idx += 1 
        self.num_groups = len(group_partition.keys())
        self.group = self.group.long().tolist()
        
    def __getitem__(self, index):
        return self.dataset.__getitem__(index) + (self.group[index],)
    
    def __len__(self):
        return len(self.dataset)