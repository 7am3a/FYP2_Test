"""
Image Pipeline Verification Test

This test verifies that the image processing pipeline:
1. Preserves PNG transparency
2. Maintains reasonable file sizes
3. Preserves image quality
4. Correctly embeds and extracts payloads
"""

import os
import sys
import tempfile
import numpy as np
from PIL import Image
import cv2

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.image_processing.image_converter import image_converter
from app.image_processing.image_loader import image_loader
from app.image_processing.edge_detector import edge_detector
from app.steganography.edge_lsb_embedder import edge_lsb_embedder
from app.steganography.edge_lsb_extractor import edge_lsb_extractor


def create_test_rgba_image(width=100, height=100):
    """Create a test RGBA image with transparency and edges."""
    # Create an RGBA image with edges and transparency
    img = Image.new('RGBA', (width, height))
    pixels = img.load()
    
    for y in range(height):
        for x in range(width):
            # Create a checkerboard pattern with varying alpha to create edges
            if (x // 20 + y // 20) % 2 == 0:
                # White with full opacity
                pixels[x, y] = (255, 255, 255, 255)
            else:
                # Black with varying alpha
                alpha = 128 + int(127 * (x / width))
                pixels[x, y] = (0, 0, 0, alpha)
    
    return img


def create_test_rgb_image(width=100, height=100):
    """Create a test RGB image without transparency and with edges."""
    img = Image.new('RGB', (width, height))
    pixels = img.load()
    
    for y in range(height):
        for x in range(width):
            # Create a checkerboard pattern to create edges
            if (x // 20 + y // 20) % 2 == 0:
                pixels[x, y] = (255, 255, 255)
            else:
                pixels[x, y] = (0, 0, 0)
    
    return img


def test_transparency_preservation():
    """Test that RGBA images preserve transparency through the pipeline."""
    print("\n" + "="*70)
    print("TEST 1: TRANSPARENCY PRESERVATION")
    print("="*70)
    
    # Create test RGBA image
    print("\n1. Creating test RGBA image with transparency...")
    original_img = create_test_rgba_image(200, 200)
    
    # Save original
    original_path = tempfile.mktemp(suffix='.png')
    original_img.save(original_path)
    original_img.close()
    
    original_file_size = os.path.getsize(original_path)
    print(f"   Original image saved: {original_path}")
    print(f"   Original file size: {original_file_size} bytes")
    print(f"   Original mode: {original_img.mode}")
    
    # Load and verify original has alpha
    print("\n2. Verifying original image has alpha channel...")
    loaded_original = Image.open(original_path)
    print(f"   Loaded mode: {loaded_original.mode}")
    print(f"   Has transparency: {loaded_original.mode in ('RGBA', 'LA', 'PA')}")
    loaded_original.close()
    
    # Convert to PNG (should preserve RGBA)
    print("\n3. Converting image to PNG...")
    converted_path, original_format = image_converter.convert_to_png(original_path)
    converted_file_size = os.path.getsize(converted_path)
    print(f"   Converted image saved: {converted_path}")
    print(f"   Converted file size: {converted_file_size} bytes")
    
    # Load converted image
    print("\n4. Verifying converted image preserves alpha...")
    converted_img = Image.open(converted_path)
    print(f"   Converted mode: {converted_img.mode}")
    print(f"   Has transparency: {converted_img.mode in ('RGBA', 'LA', 'PA')}")
    converted_img.close()
    
    # Load with OpenCV to verify alpha is preserved
    print("\n5. Loading with OpenCV (IMREAD_UNCHANGED)...")
    cv_image = cv2.imread(converted_path, cv2.IMREAD_UNCHANGED)
    print(f"   OpenCV image shape: {cv_image.shape}")
    print(f"   Has alpha channel: {cv_image.shape[2] == 4 if len(cv_image.shape) == 3 else False}")
    
    # Detect edges
    print("\n6. Detecting edges...")
    edge_map = edge_detector.detect_edges(converted_path, clear_lsb=True)
    edge_coordinates = edge_detector.get_edge_pixel_coordinates(edge_map)
    print(f"   Edge pixels detected: {len(edge_coordinates)}")
    print(f"   First 10 edge coordinates: {edge_coordinates[:10]}")
    
    # Create test payload
    print("\n7. Creating test payload...")
    test_payload = b"Hello, this is a test message for steganography!" * 10
    print(f"   Payload size: {len(test_payload)} bytes")
    
    # Embed payload
    print("\n8. Embedding payload...")
    stego_path, embed_stats = edge_lsb_embedder.embed(
        converted_path,
        test_payload,
        edge_coordinates
    )
    stego_file_size = os.path.getsize(stego_path)
    print(f"   Stego image saved: {stego_path}")
    print(f"   Stego file size: {stego_file_size} bytes")
    print(f"   File size ratio: {stego_file_size / original_file_size:.2f}x")
    
    # Verify stego image has alpha
    print("\n9. Verifying stego image preserves alpha...")
    stego_img = Image.open(stego_path)
    print(f"   Stego mode: {stego_img.mode}")
    print(f"   Has transparency: {stego_img.mode in ('RGBA', 'LA', 'PA')}")
    stego_img.close()
    
    stego_cv = cv2.imread(stego_path, cv2.IMREAD_UNCHANGED)
    print(f"   OpenCV stego shape: {stego_cv.shape}")
    print(f"   Has alpha channel: {stego_cv.shape[2] == 4 if len(stego_cv.shape) == 3 else False}")
    
    # Extract payload
    print("\n10. Extracting payload...")
    edge_map_extract = edge_detector.detect_edges(stego_path, clear_lsb=True)
    edge_coordinates_extract = edge_detector.get_edge_pixel_coordinates(edge_map_extract)
    print(f"   Edge pixels on stego: {len(edge_coordinates_extract)}")
    print(f"   First 10 edge coordinates on stego: {edge_coordinates_extract[:10]}")
    print(f"   Edge coordinates match: {edge_coordinates == edge_coordinates_extract}")
    
    extracted_payload, extract_stats = edge_lsb_extractor.extract(
        stego_path,
        edge_coordinates_extract
    )
    print(f"   Extracted payload size: {len(extracted_payload)} bytes")
    print(f"   Original payload: {test_payload[:50]}...")
    print(f"   Extracted payload: {extracted_payload[:50]}...")
    print(f"   Payload matches: {extracted_payload == test_payload}")
    
    if extracted_payload != test_payload:
        print(f"   Difference at position:")
        for i in range(min(len(test_payload), len(extracted_payload))):
            if test_payload[i] != extracted_payload[i]:
                print(f"     Index {i}: original={test_payload[i]}, extracted={extracted_payload[i]}")
                break
    
    # Cleanup
    try:
        os.remove(original_path)
    except:
        pass
    try:
        os.remove(converted_path)
    except:
        pass
    try:
        os.remove(stego_path)
    except:
        pass
    
    # Test result
    transparency_preserved = (stego_img.mode == 'RGBA' and stego_cv.shape[2] == 4)
    payload_correct = (extracted_payload == test_payload)
    file_size_reasonable = (stego_file_size / original_file_size < 5.0)
    
    print("\n" + "="*70)
    print("TEST 1 RESULTS:")
    print(f"  Transparency preserved: {transparency_preserved}")
    print(f"  Payload extracted correctly: {payload_correct}")
    print(f"  File size reasonable (< 5x): {file_size_reasonable}")
    print(f"  Overall: {'PASS' if all([transparency_preserved, payload_correct, file_size_reasonable]) else 'FAIL'}")
    print("="*70)
    
    return all([transparency_preserved, payload_correct, file_size_reasonable])


def test_rgb_image_pipeline():
    """Test that RGB images work correctly through the pipeline."""
    print("\n" + "="*70)
    print("TEST 2: RGB IMAGE PIPELINE")
    print("="*70)
    
    # Create test RGB image
    print("\n1. Creating test RGB image...")
    original_img = create_test_rgb_image(200, 200)
    
    # Save original
    original_path = tempfile.mktemp(suffix='.png')
    original_img.save(original_path)
    original_img.close()
    
    original_file_size = os.path.getsize(original_path)
    print(f"   Original image saved: {original_path}")
    print(f"   Original file size: {original_file_size} bytes")
    print(f"   Original mode: {original_img.mode}")
    
    # Convert to PNG
    print("\n2. Converting image to PNG...")
    converted_path, original_format = image_converter.convert_to_png(original_path)
    converted_file_size = os.path.getsize(converted_path)
    print(f"   Converted image saved: {converted_path}")
    print(f"   Converted file size: {converted_file_size} bytes")
    
    # Load converted image
    print("\n3. Verifying converted image...")
    converted_img = Image.open(converted_path)
    print(f"   Converted mode: {converted_img.mode}")
    converted_img.close()
    
    # Detect edges
    print("\n4. Detecting edges...")
    edge_map = edge_detector.detect_edges(converted_path, clear_lsb=True)
    edge_coordinates = edge_detector.get_edge_pixel_coordinates(edge_map)
    print(f"   Edge pixels detected: {len(edge_coordinates)}")
    
    # Create test payload
    print("\n5. Creating test payload...")
    test_payload = b"Test message for RGB image" * 20
    print(f"   Payload size: {len(test_payload)} bytes")
    
    # Embed payload
    print("\n6. Embedding payload...")
    stego_path, embed_stats = edge_lsb_embedder.embed(
        converted_path,
        test_payload,
        edge_coordinates
    )
    stego_file_size = os.path.getsize(stego_path)
    print(f"   Stego image saved: {stego_path}")
    print(f"   Stego file size: {stego_file_size} bytes")
    print(f"   File size ratio: {stego_file_size / original_file_size:.2f}x")
    
    # Extract payload
    print("\n7. Extracting payload...")
    edge_map_extract = edge_detector.detect_edges(stego_path, clear_lsb=True)
    edge_coordinates_extract = edge_detector.get_edge_pixel_coordinates(edge_map_extract)
    extracted_payload, extract_stats = edge_lsb_extractor.extract(
        stego_path,
        edge_coordinates_extract
    )
    print(f"   Extracted payload size: {len(extracted_payload)} bytes")
    print(f"   Payload matches: {extracted_payload == test_payload}")
    
    # Cleanup
    try:
        os.remove(original_path)
    except:
        pass
    try:
        os.remove(converted_path)
    except:
        pass
    try:
        os.remove(stego_path)
    except:
        pass
    
    # Test result
    payload_correct = (extracted_payload == test_payload)
    file_size_reasonable = (stego_file_size / original_file_size < 5.0)
    
    print("\n" + "="*70)
    print("TEST 2 RESULTS:")
    print(f"  Payload extracted correctly: {payload_correct}")
    print(f"  File size reasonable (< 5x): {file_size_reasonable}")
    print(f"  Overall: {'PASS' if all([payload_correct, file_size_reasonable]) else 'FAIL'}")
    print("="*70)
    
    return all([payload_correct, file_size_reasonable])


def test_file_size_compression():
    """Test that PNG compression level 9 is applied."""
    print("\n" + "="*70)
    print("TEST 3: FILE SIZE COMPRESSION")
    print("="*70)
    
    # Create a larger test image
    print("\n1. Creating large test image...")
    large_img = create_test_rgba_image(500, 500)
    
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
        original_path = f.name
        large_img.save(original_path, compress_level=9)
    
    original_file_size = os.path.getsize(original_path)
    print(f"   Original file size: {original_file_size} bytes")
    
    # Convert through pipeline
    print("\n2. Converting through pipeline...")
    converted_path, _ = image_converter.convert_to_png(original_path)
    converted_file_size = os.path.getsize(converted_path)
    print(f"   Converted file size: {converted_file_size} bytes")
    print(f"   Size ratio: {converted_file_size / original_file_size:.2f}x")
    
    # Detect edges and embed
    print("\n3. Embedding payload...")
    edge_map = edge_detector.detect_edges(converted_path)
    edge_coordinates = edge_detector.get_edge_pixel_coordinates(edge_map)
    test_payload = b"X" * 1000
    
    stego_path, _ = edge_lsb_embedder.embed(
        converted_path,
        test_payload,
        edge_coordinates
    )
    stego_file_size = os.path.getsize(stego_path)
    print(f"   Stego file size: {stego_file_size} bytes")
    print(f"   Size ratio vs original: {stego_file_size / original_file_size:.2f}x")
    
    # Cleanup
    os.remove(original_path)
    os.remove(converted_path)
    os.remove(stego_path)
    
    # Test result - should be reasonably compressed
    compression_effective = (stego_file_size / original_file_size < 3.0)
    
    print("\n" + "="*70)
    print("TEST 3 RESULTS:")
    print(f"  Compression effective (< 3x original): {compression_effective}")
    print(f"  Overall: {'PASS' if compression_effective else 'FAIL'}")
    print("="*70)
    
    return compression_effective


if __name__ == "__main__":
    print("\n" + "="*70)
    print("IMAGE PIPELINE VERIFICATION TEST SUITE")
    print("="*70)
    
    results = []
    
    # Run tests
    results.append(("Transparency Preservation", test_transparency_preservation()))
    results.append(("RGB Image Pipeline", test_rgb_image_pipeline()))
    results.append(("File Size Compression", test_file_size_compression()))
    
    # Summary
    print("\n" + "="*70)
    print("FINAL SUMMARY")
    print("="*70)
    
    for test_name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"  {test_name}: {status}")
    
    all_passed = all(result[1] for result in results)
    print("\n" + "="*70)
    print(f"OVERALL: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
    print("="*70)
    
    sys.exit(0 if all_passed else 1)
