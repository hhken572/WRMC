# import segmentation_models_pytorch as smp
# import torch.nn as nn
# from tqdm import tqdm
# import torch
# # from data import DefectDataset

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# # 1. Khởi tạo U-Net với backbone ResNet-18
# model = smp.Unet(
#     encoder_name="resnet18",
#     encoder_weights="imagenet",
#     in_channels=3,
#     classes=3  # 0: nền, 1: đốm xám, 2: lỗi chữ trắng
# ).to(device)

# # 2. Định nghĩa hàm Loss & Optimizer
# class CombinedLoss(nn.Module):
#     def __init__(self):
#         super().__init__()
#         self.dice = smp.losses.DiceLoss(mode="multiclass", from_logits=True)
#         self.ce = nn.CrossEntropyLoss()

#     def forward(self, pred, target):
#         return self.dice(pred, target) + self.ce(pred, target)

# criterion = CombinedLoss()
# optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4, weight_decay=1e-4)

# # 3. DataLoader
# train_dataset = DefectDataset("dataset/train/images", "dataset/train/masks", transform=train_transform)
# val_dataset = DefectDataset("dataset/val/images", "dataset/val/masks", transform=val_transform)

# train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True, num_workers=2)
# val_loader = DataLoader(val_dataset, batch_size=8, shuffle=False, num_workers=2)

# # 4. Training loop
# epochs = 30
# best_val_loss = float("inf")

# for epoch in range(epochs):
#     model.train()
#     total_train_loss = 0.0
#     for images, masks in tqdm(train_loader, desc=f"Epoch {epoch+1}/{epochs} [Train]"):
#         images, masks = images.to(device), masks.to(device)

#         optimizer.zero_grad()
#         outputs = model(images)
#         loss = criterion(outputs, masks)
#         loss.backward()
#         optimizer.step()

#         total_train_loss += loss.item()

#     # Đánh giá validation
#     model.eval()
#     total_val_loss = 0.0
#     with torch.no_grad():
#         for images, masks in val_loader:
#             images, masks = images.to(device), masks.to(device)
#             outputs = model(images)
#             loss = criterion(outputs, masks)
#             total_val_loss += loss.item()

#     avg_train_loss = total_train_loss / len(train_loader)
#     avg_val_loss = total_val_loss / len(val_loader)
#     print(f"Epoch {epoch+1} - Train Loss: {avg_train_loss:.4f} | Val Loss: {avg_val_loss:.4f}")

#     if avg_val_loss < best_val_loss:
#         best_val_loss = avg_val_loss
#         torch.save(model.state_dict(), "best_resnet18_unet.pth")
#         print("--> Đã lưu checkpoint tốt nhất.")





import os
import cv2
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm
import albumentations as A
from albumentations.pytorch import ToTensorV2
import segmentation_models_pytorch as smp

# 1. Định nghĩa Class Dataset
class DefectDataset(Dataset):
    def __init__(self, img_dir, mask_dir, transform=None):
        self.img_dir = img_dir
        self.mask_dir = mask_dir
        # Chỉ lấy các file ảnh hợp lệ
        valid_exts = ('.jpg', '.jpeg', '.png', '.bmp')
        self.img_names = sorted([f for f in os.listdir(img_dir) if f.lower().endswith(valid_exts)])
        self.transform = transform

    def __len__(self):
        return len(self.img_names)

    def __getitem__(self, idx):
        img_name = self.img_names[idx]
        img_path = os.path.join(self.img_dir, img_name)
        
        # Mask luôn là file .png trùng tên gốc
        base_name = os.path.splitext(img_name)[0]
        mask_path = os.path.join(self.mask_dir, f"{base_name}.png")

        image = cv2.imread(img_path)
        if image is None:
            raise FileNotFoundError(f"Không tìm thấy hoặc không đọc được ảnh: {img_path}")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        if mask is None:
            raise FileNotFoundError(f"Không tìm thấy mask tương ứng: {mask_path}")

        if self.transform is not None:
            augmented = self.transform(image=image, mask=mask)
            image = augmented["image"]
            mask = augmented["mask"]

        return image, mask.long()

# 2. Định nghĩa Augmentations
train_transform = A.Compose([
    A.Resize(512, 512),
    A.HorizontalFlip(p=0.5),
    A.VerticalFlip(p=0.5),
    A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
    ToTensorV2(),
])

val_transform = A.Compose([
    A.Resize(512, 512),
    A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
    ToTensorV2(),
])

# 3. Định nghĩa Loss Function
class CombinedLoss(nn.Module):
    def __init__(self, weights=None):
        super().__init__()
        self.dice = smp.losses.DiceLoss(mode="multiclass", from_logits=True)
        self.ce = nn.CrossEntropyLoss(weight=weights)

    def forward(self, pred, target):
        return self.dice(pred, target) + self.ce(pred, target)



# 4. Hàm Main để chạy training (bắt buộc trên Windows khi dùng DataLoader)
def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"--> Đang sử dụng thiết bị: {device}")

    # Khởi tạo U-Net với backbone ResNet-18
    model = smp.Unet(
        encoder_name="resnet50",
        encoder_weights="imagenet",
        in_channels=3,
        classes=4  # 0: background, 1: NG_S, 2: NG_H, 3: NG_N
    ).to(device)


    # Trong hàm main():
    # Trọng số cho 4 class: [Background, NG_S, NG_H, NG_N]
    class_weights = torch.tensor([0.5, 1.5, 1.5, 1.5], dtype=torch.float).to(device)
    criterion = CombinedLoss(weights=class_weights)

    # criterion = CombinedLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4, weight_decay=1e-4)

    # Khởi tạo Datasets & DataLoaders
    # Lưu ý: trên Windows nếu bị treo tiến trình, đổi num_workers=0
    train_dataset = DefectDataset("dataset/train/images", "dataset/train/masks", transform=train_transform)
    val_dataset = DefectDataset("dataset/val/images", "dataset/val/masks", transform=val_transform)

    train_loader = DataLoader(train_dataset, batch_size=2, shuffle=True, num_workers=2)
    val_loader = DataLoader(val_dataset, batch_size=2, shuffle=False, num_workers=2)

    epochs = 50
    best_val_loss = float("inf")

    for epoch in range(epochs):
        model.train()
        total_train_loss = 0.0
        for images, masks in tqdm(train_loader, desc=f"Epoch {epoch+1}/{epochs} [Train]"):
            images, masks = images.to(device), masks.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, masks)
            loss.backward()
            optimizer.step()

            total_train_loss += loss.item()

        model.eval()
        total_val_loss = 0.0
        with torch.no_grad():
            for images, masks in val_loader:
                images, masks = images.to(device), masks.to(device)
                outputs = model(images)
                loss = criterion(outputs, masks)
                total_val_loss += loss.item()

        avg_train_loss = total_train_loss / len(train_loader)
        avg_val_loss = total_val_loss / len(val_loader)
        print(f"Epoch {epoch+1} - Train Loss: {avg_train_loss:.4f} | Val Loss: {avg_val_loss:.4f}")

        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            torch.save(model.state_dict(), "resnet50_unet_4cls.pth")
            print("--> Đã lưu checkpoint tốt nhất!")

if __name__ == "__main__":
    main()