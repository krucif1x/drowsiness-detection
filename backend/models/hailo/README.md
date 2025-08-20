BlazeDetectorBase is a base class for "Blaze"-style detectors (BlazeFace, BlazePalm, etc.) 
These models predict detection (boxes +keypoints) from fixed-size inputs using an "anchor"
grid and then postprocess those predictions into final boxes in your original image space

Quick Glossary:
1. Anchors: Predefined refrence boxes tiled over the image. The netowrk predicts offsets relative to these
2. Stride: How far you move between adjacent anchor centers on a feature map (e.g.,

