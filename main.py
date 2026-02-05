"""
Smart Surveillance System using YOLOv8
Real-time object detection and tracking on edge devices
"""

import cv2
import argparse
import yaml
import sys
from pathlib import Path
from datetime import datetime

# Import custom modules
try:
    from src.detector import ObjectDetector
    from src.tracker import ObjectTracker
    from src.alert_system import AlertSystem
except ImportError:
    print("Warning: Some modules not found. Running in demo mode.")
    ObjectDetector = None
    ObjectTracker = None
    AlertSystem = None


class SurveillanceSystem:
    """Main surveillance system class"""
    
    def __init__(self, config_path='config.yaml'):
        """Initialize the surveillance system"""
        self.config = self.load_config(config_path)
        self.running = False
        
        # Initialize components
        print("Initializing surveillance system...")
        # self.detector = ObjectDetector(self.config['detection'])
        # self.tracker = ObjectTracker()
        # self.alert_system = AlertSystem(self.config['alerts'])
        
    def load_config(self, config_path):
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            return config
        except FileNotFoundError:
            print(f"Config file {config_path} not found. Using defaults.")
            return self.get_default_config()
    
    def get_default_config(self):
        """Return default configuration"""
        return {
            'camera': {
                'source': 0,
                'fps': 15,
                'resolution': [640, 480]
            },
            'detection': {
                'confidence_threshold': 0.5,
                'nms_threshold': 0.4,
                'classes': [0, 2, 5, 7]  # person, car, bus, truck
            },
            'alerts': {
                'enabled': True,
                'loitering_time': 30,
                'webhook_url': ''
            }
        }
    
    def start(self, args):
        """Start the surveillance system"""
        print("""
        ╔════════════════════════════════════════════╗
        ║  Smart Surveillance System - YOLOv8        ║
        ║  Version: 1.0.0                            ║
        ║  Status: Running                           ║
        ╚════════════════════════════════════════════╝
        """)
        
        # Open camera
        camera_source = args.source if args.source is not None else self.config['camera']['source']
        print(f"\n📹 Opening camera: {camera_source}")
        
        cap = cv2.VideoCapture(camera_source)
        
        if not cap.isOpened():
            print("❌ Error: Could not open camera")
            return
        
        # Set camera properties
        width, height = self.config['camera']['resolution']
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        
        print(f"✅ Camera opened successfully")
        print(f"📐 Resolution: {width}x{height}")
        print(f"🎯 Target FPS: {self.config['camera']['fps']}")
        print(f"\n⌨️  Press 'q' to quit\n")
        
        self.running = True
        frame_count = 0
        start_time = datetime.now()
        
        try:
            while self.running:
                ret, frame = cap.read()
                
                if not ret:
                    print("❌ Error: Could not read frame")
                    break
                
                frame_count += 1
                
                # TODO: Process frame with YOLOv8
                # detections = self.detector.detect(frame)
                # tracked_objects = self.tracker.update(detections)
                # self.alert_system.check_alerts(tracked_objects)
                
                # Demo: Draw FPS and status
                fps = frame_count / (datetime.now() - start_time).total_seconds()
                
                cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame, "Smart Surveillance System", (10, 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                cv2.putText(frame, "YOLOv8 Detection - Demo Mode", (10, 90),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
                
                # Display frame
                if not args.headless:
                    cv2.imshow('Smart Surveillance', frame)
                
                # Record if enabled
                if args.record:
                    # TODO: Implement video recording
                    pass
                
                # Check for quit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("\n🛑 Stopping surveillance system...")
                    break
        
        except KeyboardInterrupt:
            print("\n🛑 Interrupted by user")
        
        finally:
            self.running = False
            cap.release()
            cv2.destroyAllWindows()
            
            # Print statistics
            elapsed_time = (datetime.now() - start_time).total_seconds()
            avg_fps = frame_count / elapsed_time if elapsed_time > 0 else 0
            
            print(f"\n📊 Session Statistics:")
            print(f"   Frames processed: {frame_count}")
            print(f"   Duration: {elapsed_time:.2f}s")
            print(f"   Average FPS: {avg_fps:.2f}")
            print(f"\n✅ System stopped successfully")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Smart Surveillance System using YOLOv8'
    )
    
    parser.add_argument(
        '--source',
        type=str,
        default=None,
        help='Camera source (0 for webcam, or RTSP URL)'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default='config.yaml',
        help='Path to configuration file'
    )
    
    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run without displaying video feed'
    )
    
    parser.add_argument(
        '--record',
        action='store_true',
        help='Record video to file'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='recordings/',
        help='Output directory for recordings'
    )
    
    parser.add_argument(
        '--alerts',
        action='store_true',
        help='Enable alert system'
    )
    
    parser.add_argument(
        '--zones',
        type=str,
        default=None,
        help='Path to zones configuration file'
    )
    
    args = parser.parse_args()
    
    # Create surveillance system
    system = SurveillanceSystem(args.config)
    
    # Start system
    try:
        system.start(args)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
