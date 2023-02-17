import cv2
import sys
import torch

# Load the pre-trained YOLOv5 model
model = torch.load("best.pt")
model.eval()

# Load an image for object detection
# img = cv2.imread("1-강원-17-허-2711.jpg")
img = ["1-강원-17-허-2711.jpg"]

# Run object detection on the image
output = model(img)

# Extract the bounding boxes and class labels from the output
# boxes = output[0]["boxes"]
# labels = output[0]["labels"]
output_bndbox = output.pandas().xyxy[0][:][0]
print(output_bndbox)

# Label the objects in the image based on the class labels
# for box, label in zip(boxes, labels):
#     x1, y1, x2, y2 = box.astype(int)
#     cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
#     cv2.putText(img, f"{label}", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

# Save the labeled image
# cv2.imwrite("labeled_image.jpg", img)
