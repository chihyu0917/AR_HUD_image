# Thermal Imaging Object Detection and AR HUD Driver Warning Interface
# 熱成像物件辨識與AR HUD駕駛警示介面開發​
- Using Thermal Images in Object Detection to develop Forward-collision Warning Systems in different weather. Therefore, combining AR HUD and FCW can decrease car accidents with providing car information to drivers.
- 以熱成像感測克服光源雨霧等影響，達到全天候感知之FCW功能​。AR投影行車與警示資訊，提升駕駛體驗、提供更安全便捷之行車體驗​。
## Table of Contents

- [Installation](#installation)
- [How to use](#how-to-use)
- [Videos Demonstration](#videos-demonstration)

## Installation
- Platform Requirements: [jetson-utils](https://github.com/dusty-nv/jetson-utils) on NVIDIA Jetson Platform
1. `test_all_v2`: full version
    - 按照`說明文件.txt`安裝`test_rendering_v8`的jetson-utils
    - run `test.sh`
    - gldisplay: change the transparent background or the black background
2. `test_all`: simple version, without patterns of radars and blind spots, old images and transparent background
    - 按照`說明文件.txt`安裝`test_rendering_v6`的jetson-utils
    - run `test.sh`
## How to use
- `test.sh`: change different videos and csv files
- `receive_detection_fcw.py`: modify the animation
- `udp_sender.py`: read infos from csv files and send socket to display patterns 
## Videos Demonstration

