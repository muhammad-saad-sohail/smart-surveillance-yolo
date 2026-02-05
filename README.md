# 🎥 Real-Time Smart Surveillance System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat&logo=python)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-purple?style=flat)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?style=flat&logo=opencv)
![Raspberry Pi](https://img.shields.io/badge/Raspberry_Pi-4-red?style=flat&logo=raspberry-pi)
![License](https://img.shields.io/badge/License-MIT-blue?style=flat)

**AI-powered surveillance system using YOLOv8 for real-time object detection on edge devices**

[Video Demo](https://youtube.com/watch?v=demo) · [Report Bug](https://github.com/muhammad-saad-sohail/smart-surveillance-yolo/issues) · [Request Feature](https://github.com/muhammad-saad-sohail/smart-surveillance-yolo/issues)

</div>

---

## 🎯 Overview

A lightweight, efficient surveillance system that runs on edge devices like Raspberry Pi 4, utilizing YOLOv8 for real-time object detection and tracking. The system can identify people, vehicles, and suspicious activities with high precision while maintaining **15 FPS performance** on resource-constrained hardware.

### Key Highlights

- ⚡ **15 FPS** on Raspberry Pi 4
- 🎯 **82% precision** in suspicious activity detection
- 📉 **40% reduction** in false positives
- 🚀 Custom-trained on **3,000+ annotated images**
- 🔔 **Real-time alerts** via REST API

---

## ✨ Features

### 🤖 **Advanced Object Detection**
- **Multi-class Detection**: People, vehicles, suspicious objects
- **Real-time Tracking**: Maintains object IDs across frames
- **Zone-based Monitoring**: Define custom detection zones
- **Crowd Detection**: Identify gatherings and congestion

### 🚨 **Intelligent Alert System**
- **Suspicious Activity Detection**: Loitering, intrusion, abandoned objects
- **REST API Notifications**: Webhook integration for alerts
- **Email/SMS Alerts**: Instant notifications to security personnel
- **Alert Prioritization**: Critical vs. informational alerts

### 📊 **Analytics & Reporting**
- **Activity Heatmaps**: Visualize high-traffic areas
- **Dwell Time Analysis**: Track how long people stay in zones
- **Traffic Flow Reports**: Entry/exit counts and patterns
- **Incident Logs**: Searchable database of events

### 🎮 **User-Friendly Interface**
- **Live Video Dashboard**: Real-time monitoring with overlays
- **Playback System**: Review recorded footage with filters
- **Configuration Panel**: Adjust sensitivity and zones
- **Mobile App Support**: Monitor on-the-go

### ⚙️ **Edge Computing Optimization**
- **Model Quantization**: INT8 optimization for speed
- **Efficient Inference**: Optimized for ARM processors
- **Low Bandwidth**: Local processing reduces data transfer
- **Offline Capable**: Works without internet connection

---

## 🚀 Installation

### Hardware Requirements

**Minimum:**
- Raspberry Pi 4 (4GB RAM)
- USB Camera or IP Camera
- 32GB microSD card (Class 10)
- Power supply (5V 3A)

**Recommended:**
- Raspberry Pi 4 (8GB RAM)
- Google Coral USB Accelerator (for better FPS)
- High-quality IP camera with night vision
- 64GB+ microSD card

### Software Prerequisites

- Python 3.8+
- OpenCV 4.x
- Raspberry Pi OS (64-bit) or Ubuntu 20.04+

### Step-by-Step Setup

#### 1. Clone the Repository

```bash
git clone https://github.com/muhammad-saad-sohail/smart-surveillance-yolo.git
cd smart-surveillance-yolo
```

#### 2. Install System Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install OpenCV dependencies
sudo apt install -y python3-opencv libopencv-dev

# Install other requirements
sudo apt install -y python3-pip git cmake
```

#### 3. Install Python Packages

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

#### 4. Download YOLOv8 Model

```bash
# Download pre-trained model
python scripts/download_model.py

# Or use custom trained model
# Place your model in: models/yolov8_custom.pt
```

#### 5. Configure the System

Edit `config.yaml`:

```yaml
# Camera Configuration
camera:
  source: 0  # 0 for USB camera, or RTSP URL for IP camera
  fps: 15
  resolution: [640, 480]

# Detection Settings
detection:
  confidence_threshold: 0.5
  nms_threshold: 0.4
  classes: [0, 2, 5, 7]  # person, car, bus, truck

# Alert Configuration
alerts:
  enabled: true
  loitering_time: 30  # seconds
  webhook_url: "https://your-webhook.com/alerts"
```

#### 6. Run the System

```bash
# Start the surveillance system
python main.py

# With GPU acceleration (if available)
python main.py --device cuda

# Run in headless mode (no display)
python main.py --headless
```

---

## 💻 Usage

### Basic Operation

```bash
# Start with default settings
python main.py

# Specify camera source
python main.py --source rtsp://192.168.1.100:554/stream

# Record video
python main.py --record --output recordings/

# Enable alerts
python main.py --alerts

# Run on specific zones
python main.py --zones zones/entrance.json
```

### Web Dashboard

```bash
# Start web interface
python web_app.py

# Access at: http://raspberry-pi-ip:5000
```

### API Usage

#### Get Live Status
```bash
curl http://localhost:5000/api/status
```

**Response:**
```json
{
  "status": "running",
  "fps": 15.2,
  "detected_objects": {
    "person": 3,
    "car": 1
  },
  "active_alerts": 0
}
```

---

## 📊 Performance Metrics

### Detection Performance

| Metric | Value |
|--------|-------|
| **Precision** | 82% |
| **Recall** | 78% |
| **F1-Score** | 0.80 |
| **mAP@0.5** | 0.79 |
| **FPS (Raspberry Pi 4)** | 15 |
| **Inference Time** | ~65ms |

### False Positive Reduction

| Version | False Positive Rate |
|---------|---------------------|
| Baseline YOLOv8 | 18.3% |
| Custom Trained | 10.9% |
| **Improvement** | **40.4% reduction** |

---

## 📁 Project Structure

```
smart-surveillance-yolo/
│
├── main.py                    # Main application entry point
├── config.yaml               # Configuration file
├── requirements.txt          # Python dependencies
├── README.md                 # This file
│
├── models/                   # Trained models
│   ├── yolov8n.pt           # Default YOLOv8 nano
│   └── yolov8_custom.pt     # Custom trained model
│
├── src/                      # Source code
│   ├── __init__.py
│   ├── detector.py          # Object detection module
│   ├── tracker.py           # Object tracking
│   ├── alert_system.py      # Alert generation
│   └── video_processor.py   # Video stream handling
│
├── web_app.py               # Web dashboard
├── scripts/                 # Utility scripts
├── data/                    # Training dataset
├── recordings/              # Saved video clips
└── docs/                    # Documentation
```

---

## 🛠️ Technologies Used

### Computer Vision
- **YOLOv8** - State-of-the-art object detection
- **OpenCV** - Video processing and computer vision
- **DeepSORT** - Multi-object tracking

### Backend
- **Flask/FastAPI** - REST API server
- **SQLite** - Event database

### Edge Computing
- **ONNX Runtime** - Optimized inference
- **TensorRT** (optional) - NVIDIA GPU acceleration

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📄 License

MIT License - see LICENSE file for details.

---

## 👨‍💻 Author

**Muhammad Saad Sohail**

- Email: rajasaadsohail646@gmail.com
- LinkedIn: [linkedin.com/in/saadsohail](https://linkedin.com/in/saadsohail)
- GitHub: [@muhammad-saad-sohail](https://github.com/muhammad-saad-sohail)

---

<div align="center">

**⭐ Star this repo if you find it useful! ⭐**

*Securing spaces with AI*

</div>
