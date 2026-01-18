import os
import shutil
import pandas as pd

base_dir = "data/pest_images/"
train_img_dir = os.path.join(base_dir, "train")
train_csv_path = os.path.join(base_dir, "train.csv")

df = pd.read_csv(train_csv_path)

file_col = df.columns[0]   # image path
label_col = df.columns[1]  # pest label

moved = 0
missing = 0

for _, row in df.iterrows():
    full_path = str(row[file_col])
    label = str(row[label_col]).strip()

    # ✅ extract only filename from kaggle path
    filename = os.path.basename(full_path)

    src = os.path.join(train_img_dir, filename)
    dst_dir = os.path.join(base_dir, label)
    dst = os.path.join(dst_dir, filename)

    os.makedirs(dst_dir, exist_ok=True)

    if os.path.exists(src):
        shutil.move(src, dst)
        moved += 1
    else:
        missing += 1

print("===================================")
print(f"✅ Images moved successfully: {moved}")
print(f"⚠️ Images not found locally: {missing}")
print("Dataset arrangement completed.")
