"""
WAAD ELKENIN - CYBERPULSE DETECTION SYSTEM
Main entry point for the detection engine
"""
from waad_detection_engine import DetectionEngine
from waad_detection_runner import run_detector
import sys

def main():
    print("=" * 60)
    print("WAAD ELKENIN - CyberPulse Detection System")
    print("=" * 60)
    print("Detection Rules: WESF1-WESF5")
    print("API Integration: http://3.145.146.136:5000/api/add-detection")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            from waad_detection_tests import run_all_tests
            run_all_tests()
        elif sys.argv[1] == "run":
            run_detector()
        elif sys.argv[1] == "parse":
            from waad_log_parser import parse_logs
            parse_logs()
    else:
        print("Usage:")
        print("  python waad_main.py test   # Run all tests")
        print("  python waad_main.py run    # Run detection engine")
        print("  python waad_main.py parse  # Parse auth logs")
        
if __name__ == "__main__":
    main()
