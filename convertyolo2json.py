import os
import json
from datetime import datetime
import io

'''
用于转化标签格式 加载label studio 预标注
'''

def  xyxy2xywh(x1,y1,x2,y2,width,height):
    cx = (x1+x2)/2/width
    cy = (y1+y2)/2/height
    w  = (x2-x1)/width
    h = (y2-y1)/height
    return cx,cy,w,h
    

# Path to the folder containing the TXT files
folder_path = "/home/hongyuanyang/playground/label_anything/data_pool/5200_labels/test5200_labels"   # label 所在路径


imagePathKeyword = "test5200"    # image 所在 data_pool 下的名称
# Initialize a list to store the final JSON structure
json_data = []

width = 1280
height = 720

tmp = sorted(os.listdir(folder_path),key = lambda x :[i for i in map(int,x.split('.')[0].split("_"))],)

# Counter for generating unique IDs
annotation_id_counter = 1

# Iterate through each file in the folder
for filename in tmp:
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)
        
        # Read the content of the TXT file
        with open(file_path, 'r') as file:
            txt_data = file.read().strip()

        # Check if the file is empty
        if not txt_data:
            # Create the JSON structure for an empty file
            json_structure = {
                "id": annotation_id_counter,
                "annotations": [],
                "file_upload": f"output.json",
                "drafts": [],
                "predictions": [
                     {
                        "id": annotation_id_counter,
                        "completed_by": 1,
                        "result": [],
                        "was_cancelled": False,
                        "ground_truth": False,
                        "created_at": datetime.utcnow().isoformat() + "Z",
                        "updated_at": datetime.utcnow().isoformat() + "Z",
                        "draft_created_at": None,
                        "lead_time": 0,
                        "prediction": {},
                        "result_count": 0,
                        "unique_id": f"77c20cd7-93f5-431a-b730-97c1e9e08fa4{annotation_id_counter}",
                        "import_id": None,
                        "last_action": None,
                        "task": annotation_id_counter,
                        "project": 24,
                        "updated_by": 1,
                        "parent_prediction": None,
                        "parent_annotation": None,
                        "last_created_by": None
                    }
                ],
                "data": {
                    "image": f"/data/local-files/?d=data_pool/{imagePathKeyword}/{filename.split('.')[0]}.jpg"
                },
                "meta": {},
                "created_at": datetime.utcnow().isoformat() + "Z",
                "updated_at": datetime.utcnow().isoformat() + "Z",
                "inner_id": annotation_id_counter,
                "total_annotations": 1,
                "cancelled_annotations": 0,
                "total_predictions": 0,
                "comment_count": 0,
                "unresolved_comment_count": 0,
                "last_comment_updated_at": None,
                "project": 24,
                "updated_by": 1,
                "comment_authors": []
            }
            
            # Increment the annotation ID counter
            annotation_id_counter += 1
            
            # Append the JSON structure to the list
            json_data.append(json_structure)
            
        else:
            # Process each line in the TXT file
            lines = txt_data.split('\n')
            
            # Initialize variables to store information from multiple lines
            annotations = []
            id_label = 0
            for line in lines:
                parts = line.split()
                
                # Extract information from the line
                name = parts[0]
                # confidence = max(float(parts[1]), 0)
                # x1,y1,x2,y2 = map(int,parts[2:6])
                
                # mid_x,mid_y,w_ratio,h_ratio = xyxy2xywh(x1,y1,x2,y2,width,height)
                
                mid_x, mid_y, w_ratio, h_ratio= map(float, parts[1:5])
                
                # Create the result for each line
                result = {
                    "original_width": width,
                    "original_height": height,
                    "image_rotation": 0,
                    "value": {
                        "x": (mid_x - w_ratio/2) * 100,
                        "y": (mid_y - h_ratio/2) * 100,
                        "width": w_ratio * 100,
                        "height": h_ratio * 100,
                        "rotation": 0,
                        "rectanglelabels": [name]
                    },
                    "id": f"wDybrtKge{annotation_id_counter}{id_label}",
                    "from_name": "label",
                    "to_name": "image",
                    "type": "rectanglelabels",
                    "origin": "manual"
                }

                id_label += 1
                annotations.append(result)
            
            # Create the combined JSON structure
            json_structure = {
                "id": annotation_id_counter,
                "annotations": [],
                "file_upload": f"output.json",
                "drafts": [],
                "predictions": [
                    {
                        "id": annotation_id_counter,
                        "completed_by": 1,
                        "result": annotations,
                        "was_cancelled": False,
                        "ground_truth": False,
                        "created_at": datetime.utcnow().isoformat() + "Z",
                        "updated_at": datetime.utcnow().isoformat() + "Z",
                        "draft_created_at": None,
                        "lead_time": 0,  # Change this if lead time information is available
                        "prediction": {},
                        "result_count": len(annotations),
                        "unique_id": f"cc0919a3-cecf-4a76-a8e8-01b8204e{annotation_id_counter}",
                        "import_id": None,
                        "last_action": None,
                        "task": annotation_id_counter,
                        "project": 24,
                        "updated_by": 1,
                        "parent_prediction": None,
                        "parent_annotation": None,
                        "last_created_by": None
                    }
                ],
                "data": {
                    "image": f"/data/local-files/?d=data_pool/{imagePathKeyword}/{os.path.splitext(filename)[0]}.jpg"
                },
                "meta": {},
                "created_at": datetime.utcnow().isoformat() + "Z",
                "updated_at": datetime.utcnow().isoformat() + "Z",
                "inner_id": annotation_id_counter,
                "total_annotations": 1,
                "cancelled_annotations": 0,
                "total_predictions": 0,
                "comment_count": 0,
                "unresolved_comment_count": 0,
                "last_comment_updated_at": None,
                "project": 10,
                "updated_by": 1,
                "comment_authors": []
            }
            
            # Increment the annotation ID counter
            annotation_id_counter += 1
            
            # Append the JSON structure to the list
            json_data.append(json_structure)

# Convert the list to JSON
json_output = json.dumps(json_data, indent=4)

# Specify the output file path
output_file_path = folder_path.rsplit(os.sep,1)[0] + f"/{imagePathKeyword}output.json"

# Write the JSON data to the output file
with open(output_file_path, 'w') as output_file:
    output_file.write(json_output)


