"""
Performance Profiler for SecureStego
Measures execution time for each stage of the embedding pipeline
"""

import time
import os
import tempfile
from typing import Dict, List
from app.services.crypto_service import crypto_service
from app.utils.payload_serializer import payload_serializer
from app.image_processing.edge_detector import edge_detector
from app.image_processing.image_converter import image_converter
from app.steganography.edge_lsb_embedder import edge_lsb_embedder
from app.services.steganography_service import steganography_service


class PerformanceProfiler:
    """Profiles performance of steganography pipeline"""
    
    def __init__(self):
        self.timings = {}
    
    def time_operation(self, name: str, func):
        """Time an operation and record result"""
        start = time.time()
        result = func()
        elapsed = time.time() - start
        self.timings[name] = elapsed
        print(f"{name}: {elapsed:.4f}s")
        return result
    
    def profile_image_embedding(self, image_path: str, message: str, password: str):
        """Profile complete image embedding workflow"""
        print(f"\n=== Profiling Image Embedding ===")
        print(f"Image: {image_path}")
        print(f"Message size: {len(message)} bytes")
        
        # Step 1: Encryption
        print("\n--- Encryption ---")
        encrypt_result = self.time_operation(
            "Encryption (Argon2id + AES-256-GCM)",
            lambda: crypto_service.encrypt_message(message, password)
        )
        
        # Step 2: Payload serialization
        print("\n--- Payload Serialization ---")
        payload_dict = self.time_operation(
            "Create payload dict",
            lambda: payload_serializer.create_payload(
                encrypt_result["ciphertext"],
                encrypt_result["salt"],
                encrypt_result["iv"],
                encrypt_result["algorithm"],
                encrypt_result["kdf"]
            )
        )
        
        payload_binary = self.time_operation(
            "Serialize to binary",
            lambda: payload_serializer.serialize_to_binary(payload_dict)
        )
        
        # Step 3: Image conversion
        print("\n--- Image Conversion ---")
        temp_png_path, original_format = self.time_operation(
            f"Convert {original_format} to PNG",
            lambda: image_converter.convert_to_png(image_path)
        )
        
        # Step 4: Edge detection
        print("\n--- Edge Detection ---")
        edge_map = self.time_operation(
            "Edge detection (Canny)",
            lambda: edge_detector.detect_edges(temp_png_path, clear_lsb=True)
        )
        
        edge_coordinates = self.time_operation(
            "Get edge coordinates",
            lambda: edge_detector.get_edge_pixel_coordinates(edge_map)
        )
        
        # Step 5: Capacity calculation
        print("\n--- Capacity Calculation ---")
        capacity_info = self.time_operation(
            "Calculate capacity",
            lambda: edge_lsb_embedder.calculate_capacity(len(edge_coordinates))
        )
        
        # Step 6: Embedding
        print("\n--- Embedding ---")
        stego_path, stats = self.time_operation(
            "Embed payload (LSB)",
            lambda: edge_lsb_embedder.embed(temp_png_path, payload_binary, edge_coordinates)
        )
        
        # Step 7: Cleanup
        print("\n--- Cleanup ---")
        self.time_operation(
            "Cleanup temp files",
            lambda: self._cleanup(temp_png_path, stego_path)
        )
        
        # Summary
        print("\n=== Performance Summary ===")
        total_time = sum(self.timings.values())
        for name, elapsed in sorted(self.timings.items(), key=lambda x: x[1], reverse=True):
            percent = (elapsed / total_time) * 100
            print(f"{name}: {elapsed:.4f}s ({percent:.1f}%)")
        print(f"Total: {total_time:.4f}s")
        
        return self.timings
    
    def _cleanup(self, *paths):
        """Clean up temporary files"""
        for path in paths:
            if path and os.path.exists(path):
                os.remove(path)


def main():
    """Run performance profiling"""
    # Create a test image
    import numpy as np
    from PIL import Image
    
    print("Creating test image...")
    test_image = np.random.randint(0, 255, (1920, 1080, 3), dtype=np.uint8)
    test_pil = Image.fromarray(test_image)
    
    temp_dir = tempfile.gettempdir()
    test_image_path = os.path.join(temp_dir, "test_performance.png")
    test_pil.save(test_image_path)
    
    # Test parameters
    message = "A" * 1000  # 1KB message
    password = "test_password_123"
    
    # Run profiler
    profiler = PerformanceProfiler()
    timings = profiler.profile_image_embedding(test_image_path, message, password)
    
    # Cleanup
    if os.path.exists(test_image_path):
        os.remove(test_image_path)
    
    return timings


if __name__ == "__main__":
    main()
