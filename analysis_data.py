# import pandas as pd

# original_path = r"C:\Users\Tauhid Hasan\Desktop\model_output\allPathInfo(origin).csv"
# augmantated_path = r"C:\Users\Tauhid Hasan\Desktop\model_output\allPathInfo(augmentated).csv"

# df = pd.DataFrame(columns=['Dataset Name', 'Classes', 'Number of Image', 'Total image of the dataset', 'Status'])
# origin_data = pd.read_csv(original_path)
# augmantated_data = pd.read_csv(augmantated_path)

# expression = origin_data['expression'].unique().tolist()

# data_desc = {
#     "original_path": original_path,
#     "augmantated_path": augmantated_path
# }


# for da_des in data_desc.items():
#     status, path = da_des
#     data = pd.read_csv(path)

#     expression = data['expression'].unique().tolist()
#     print('=' * 100)
#     print(' ' * 40, f"Analyzing {status} Data")
#     print('=' * 100)
#     for exp in expression:
#         print('*' * 80)
#         print(' ' * 30, f"Analyzing {exp} expression")
#         print('*' * 80)

#         for dataset_name in data[data['expression'] == exp]['dataset'].unique().tolist():
#             dataset_data = data[(data['expression'] == exp) & 
#                                     (data['dataset'] == dataset_name)]
#             print('-' * 60)
#             print(' ' * 25, dataset_name)
#             print('-' * 60)
#             print(dataset_data['expression'].count())
#             emotion_data = dataset_data['emotion'].value_counts().to_dict()
#             print(emotion_data)

import os
import pandas as pd

original_path = r"C:\Users\Tauhid Hasan\Desktop\model_output\allPathInfo(origin).csv"
augmantated_path = r"C:\Users\Tauhid Hasan\Desktop\model_output\allPathInfo(augmentated).csv"

data_desc = {
    "original": pd.read_csv(original_path),
    "augmented": pd.read_csv(augmantated_path)
}

# clean columns
for status in data_desc:
    data_desc[status]['dataset'] = data_desc[status]['dataset'].astype(str).str.strip()
    data_desc[status]['expression'] = data_desc[status]['expression'].astype(str).str.strip().str.lower()
    data_desc[status]['emotion'] = data_desc[status]['emotion'].astype(str).str.strip().str.lower()

original_data = data_desc["original"]
aug_data = data_desc["augmented"]

print("Original expressions:", original_data['expression'].unique().tolist())
print("Augmented expressions:", aug_data['expression'].unique().tolist())

dataset_names = sorted(
    set(original_data['dataset'].dropna()) |
    set(aug_data['dataset'].dropna())
)

os.makedirs("data", exist_ok=True)

for dataset_name in dataset_names:
    all_rows = []

    print('*' * 100)
    print(' ' * 40, f"Analyzing {dataset_name}")
    print('*' * 100)

    for status, data in data_desc.items():
        filtered_dataset_data = data[data['dataset'] == dataset_name]

        if filtered_dataset_data.empty:
            continue

        total_dataset_images = filtered_dataset_data.shape[0]

        expressions = filtered_dataset_data['expression'].dropna().unique().tolist()
        print(f"{status} -> {dataset_name} expressions:", expressions)

        for exp in expressions:
            dataset_data = filtered_dataset_data[
                filtered_dataset_data['expression'] == exp
            ]

            total_expression_data = dataset_data.shape[0]
            emotion_data = dataset_data['emotion'].value_counts().to_dict()

            for emotion_name, image_count in emotion_data.items():
                all_rows.append({
                    'Dataset Name': dataset_name,
                    'Classes': emotion_name,
                    'Number of Image': image_count,
                    'Total image of the dataset': total_dataset_images,
                    'expression': exp,
                    'Total expression data': total_expression_data,
                    'Status': status
                })

    df = pd.DataFrame(all_rows, columns=[
        'Dataset Name',
        'Classes',
        'Number of Image',
        'Total image of the dataset',
        'expression',
        'Total expression data',
        'Status'
    ])

    output_path = f"data/dataset_summary_{dataset_name}.csv"
    df.to_csv(output_path, index=False)

    print(df)
    print(f"Saved: {output_path}")