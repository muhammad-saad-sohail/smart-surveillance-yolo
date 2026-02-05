"""
Object Detection Module
YOLOv8-based object detector optimized for surveillance
"""

import cv2
import numpy as np
from typing import List, Dict, Tuple

try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    print("Warning: ultralytics not installed. Using mock detector.")


class ObjectDetector:
    """
    YOLOv8 object detector for surveillance applications
    Detects people, vehicles, and other objects in real-time
    """
    
    def __init__(self, config: Dict):
        """
        Initialize the object detector
        
        Args:
            config: Detection configuration dictionary
        """
        self.config = config
        self.confidence_threshold = config.get('confidence_threshold', 0.5)
        self.nms_threshold = config.get('nms_threshold', 0.4)
        self.target_classes = config.get('classes', [0, 2, 5, 7])
        
        # Class names (COCO dataset)
        self.class_names = {
            0: 'person',
            1: 'bicycle',
            2: 'car',
            3: 'motorcycle',
            5: 'bus',
            7: 'truck'
        }
        
        # Load model
        if YOLO_AVAILABLE:
            self.model = YOLO('yolov8n.pt')  # YOLOv8 nano for speed
            print("✅ YOLOv8 model loaded successfully")
        else:
            self.model = None
            print("⚠️  Running in demo mode (no model loaded)")
    
    def detect(self, frame: np.ndarray) -> List[Dict]:
        """
        Detect objects in a frame
        
        Args:
            frame: Input image (BGR format)
            
        Returns:
            List of detection dictionaries with keys:
            - bbox: [x1, y1, x2, y2]
            - confidence: float
            - class_id: int
            - class_name: str
        """
        if self.model is None:
            # Return mock detections for demo
            return self._mock_detections(frame)
        
        # Run inference
        results = self.model(frame, conf=self.confidence_threshold)
        
        detections = []
        for result in results:
            boxes = result.boxes
            
            for box in boxes:
                # Extract box information
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])
                
                # Filter by target classes
                if class_id in self.target_classes:
                    detections.append({
                        'bbox': [int(x1), int(y1), int(x2), int(y2)],
                        'confidence': confidence,
                        'class_id': class_id,
                        'class_name': self.class_names.get(class_id, f'class_{class_id}')
                    })
        
        return detections
    
    def _mock_detections(self, frame: np.ndarray) -> List[Dict]:
        """
        Generate mock detections for demo purposes
        
        Args:
            frame: Input image
            
        Returns:
            List of mock detection dictionaries
        """
        height, width = frame.shape[:2]
        
        # Create some mock detections
        detections = []
        
        # Mock person detection
        if np.random.random() > 0.5:
            x1 = int(width * 0.3)
            y1 = int(height * 0.2)
            x2 = int(width * 0.5)
            y2 = int(height * 0.8)
            
            detections.append({
                'bbox': [x1, y1, x2, y2],
                'confidence': 0.85,
                'class_id': 0,
                'class_name': 'person'
            })
        
        # Mock car detection
        if np.random.random() > 0.7:
            x1 = int(width * 0.6)
            y1 = int(height * 0.5)
            x2 = int(width * 0.9)
            y2 = int(height * 0.9)
            
            detections.append({
                'bbox': [x1, y1, x2, y2],
                'confidence': 0.78,
                'class_id': 2,
                'class_name': 'car'
            })
        
        return detections
    
    def draw_detections(
        self,
        frame: np.ndarray,
        detections: List[Dict],
        show_confidence: bool = True
    ) -> np.ndarray:
        """
        Draw bounding boxes and labels on frame
        
        Args:
            frame: Input image
            detections: List of detections
            show_confidence: Whether to show confidence scores
            
        Returns:
            Annotated frame
        """
        frame_copy = frame.copy()
        
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            confidence = det['confidence']
            class_name = det['class_name']
            
            # Choose color based on class
            if class_name == 'person':
                color = (0, 255, 0)  # Green
            elif class_name in ['car', 'truck', 'bus']:
                color = (255, 0, 0)  # Blue
            else:
                color = (0, 255, 255)  # Yellow
            
            # Draw bounding box
            cv2.rectangle(frame_copy, (x1, y1), (x2, y2), color, 2)
            
            # Create label
            if show_confidence:
                label = f"{class_name}: {confidence:.2f}"
            else:
                label = class_name
            
            # Draw label background
            label_size, _ = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1
            )
            label_w, label_h = label_size
            
            cv2.rectangle(
                frame_copy,
                (x1, y1 - label_h - 10),
                (x1 + label_w, y1),
                color,
                -1
            )
            
            # Draw label text
            cv2.putText(
                frame_copy,
                label,
                (x1, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1
            )
        
        return frame_copy
    
    def get_detection_stats(self, detections: List[Dict]) -> Dict:
        """
        Get statistics about detections
        
        Args:
            detections: List of detections
            
        Returns:
            Dictionary with detection statistics
        """
        stats = {}
        
        for det in detections:
            class_name = det['class_name']
            stats[class_name] = stats.get(class_name, 0) + 1
        
        return stats


# Demo usage
if __name__ == "__main__":
    import sys
    
    # Test configuration
    config = {
        'confidence_threshold': 0.5,
        'nms_threshold': 0.4,
        'classes': [0, 2, 5, 7]
    }
    
    detector = ObjectDetector(config)
    
    # Try to open webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam")
        sys.exit(1)
    
    print("\n🎥 Object Detection Demo")
    print("Press 'q' to quit\n")
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        # Detect objects
        detections = detector.detect(frame)
        
        # Draw detections
        annotated_frame = detector.draw_detections(frame, detections)
        
        # Get stats
        stats = detector.get_detection_stats(detections)
        
        # Display stats
        y_offset = 30
        for class_name, count in stats.items():
            text = f"{class_name}: {count}"
            cv2.putText(
                annotated_frame,
                text,
                (10, y_offset),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )
            y_offset += 30
        
        cv2.imshow('Object Detection Demo', annotated_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
