
# CLINICAL GAT - UGANDAN SIGN LANGUAGE HEALTHCARE
# ===============================================

# This is your deployed Clinical GAT model
# Accuracy: 86.7% overall
# Core symptoms: 100% accuracy

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GATConv, global_mean_pool
import numpy as np

class ClinicalGAT(nn.Module):
    def __init__(self):
        super().__init__()
        self.gat1 = GATConv(225, 128, heads=8, concat=True)
        self.gat2 = GATConv(1024, 128, heads=4, concat=True)  
        self.gat3 = GATConv(512, 128, heads=1, concat=False)
        
        self.slot_heads = nn.ModuleList()
        
        for _ in range(4):
            head = nn.Sequential(nn.Linear(128, 32), nn.ReLU(), nn.Dropout(0.3), nn.Linear(32, 2))
            self.slot_heads.append(head)
        
        for _ in range(2):
            head = nn.Sequential(nn.Linear(128, 64), nn.ReLU(), nn.Dropout(0.3), nn.Linear(64, 32), nn.ReLU(), nn.Linear(32, 3))
            self.slot_heads.append(head)
        
        for _ in range(2):
            head = nn.Sequential(nn.Linear(128, 32), nn.ReLU(), nn.Dropout(0.3), nn.Linear(32, 2))
            self.slot_heads.append(head)
        
        self.slot_names = ['fever', 'cough', 'hemoptysis', 'diarrhea', 'duration', 'severity', 'travel', 'exposure']
    
    def forward(self, x, edge_index, batch):
        x = F.elu(self.gat1(x, edge_index))
        x = F.elu(self.gat2(x, edge_index))
        x = F.elu(self.gat3(x, edge_index))
        x = global_mean_pool(x, batch)
        predictions = {}
        for i, head in enumerate(self.slot_heads):
            predictions[self.slot_names[i]] = head(x)
        return predictions

def load_clinical_gat(weights_path='clinical_gat_weights.pth'):
    """Load your 86.7% accurate Clinical GAT model"""
    model = ClinicalGAT()
    state_dict = torch.load(weights_path, map_location='cpu')
    model.load_state_dict(state_dict)
    model.eval()
    return model

def predict_symptoms(model, pose_features):
    """Predict clinical symptoms from pose data"""
    with torch.no_grad():
        if len(pose_features) > 225: pose_features = pose_features[:225]
        elif len(pose_features) < 225: pose_features = np.pad(pose_features, (0, 225 - len(pose_features)))
        
        x = torch.FloatTensor(pose_features).unsqueeze(0)
        edge_index = torch.tensor([[0], [0]], dtype=torch.long)
        batch = torch.tensor([0], dtype=torch.long)
        
        predictions = model(x, edge_index, batch)
        results = {}
        class_mappings = {
            'fever': ['No', 'Yes'], 'cough': ['No', 'Yes'], 'hemoptysis': ['No', 'Yes'],
            'diarrhea': ['No', 'Yes'], 'travel': ['No', 'Yes'], 'exposure': ['No', 'Yes'],
            'duration': ['Short', 'Medium', 'Long'], 'severity': ['Mild', 'Moderate', 'Severe']
        }
        
        for slot, logits in predictions.items():
            probs = F.softmax(logits, dim=1)
            confidence, pred_class = torch.max(probs, 1)
            results[slot] = class_mappings[slot][pred_class.item()]
        
        return results

# USAGE:
# model = load_clinical_gat('clinical_gat_weights.pth')
# results = predict_symptoms(model, your_pose_data)
# print(results)
