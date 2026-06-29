# Performance Bottleneck Analysis - SecureStego

**Date**: June 25, 2026  
**Objective**: Identify and eliminate performance bottlenecks in steganography pipeline

---

## Critical Bottlenecks Identified

### 1. Image Module - Multiple Image Loads

**Location**: `steganography_service.py`, `edge_detector.py`, `edge_lsb_embedder.py`

**Problem**: The same image is loaded multiple times:
1. Line 97 in `edge_detector.py`: `cv2.imread(image_path, cv2.IMREAD_UNCHANGED)` for edge detection
2. Line 96 in `edge_lsb_embedder.py`: `cv2.imread(image_path, cv2.IMREAD_UNCHANGED)` for embedding
3. Line 85 in `edge_lsb_extractor.py`: `cv2.imread(image_path, cv2.IMREAD_UNCHANGED)` for extraction

**Impact**: High - File I/O is expensive, especially for large images

**Optimization**: Load image once and pass numpy array between functions

---

### 2. Image Module - Unnecessary Image Copy

**Location**: `edge_detector.py` line 105

**Problem**: `image = image.copy()` when clearing LSBs for LSB-invariant edge detection

**Impact**: Medium - Creates unnecessary memory allocation and copy operation

**Optimization**: Use in-place operations when possible

---

### 3. Image Module - PNG Compression Level 9

**Location**: `image_converter.py` line 152, `edge_lsb_embedder.py` line 147

**Problem**: `compress_level=9` (maximum compression) is very slow

**Impact**: High - Compression level 9 can take 2-3x longer than level 6

**Optimization**: Use compression level 6 (good compression, much faster)

---

### 4. Image Module - Repeated Edge Detection

**Location**: `steganography_service.py`

**Problem**: Edge detection is performed separately for embedding and extraction

**Impact**: Medium - Canny edge detection is computationally expensive

**Optimization**: Cache edge detection results when possible (not for security reasons, but for same file reprocessing)

---

### 5. Payload Serialization - Inefficient JSON Serialization

**Location**: `payload_serializer.py` line 153

**Problem**: `json.dumps(payload, separators=(',', ':'))` is called every time

**Impact**: Low - JSON serialization is fast but can be optimized

**Optimization**: Use faster JSON library (orjson) if available, or optimize structure

---

### 6. Crypto Service - Argon2id Key Derivation

**Location**: `crypto_service.py` lines 76-87

**Problem**: Argon2id is intentionally slow (memory-hard KDF)

**Impact**: High - This is by design for security

**Optimization**: None - Do not weaken security

---

### 7. Video Module - Frame Extraction

**Location**: `video_steganography_service.py`

**Problem**: Extracting all frames from video is expensive

**Impact**: Very High - Video processing is inherently slow

**Optimization**: Only extract frames needed for embedding (already implemented)

---

### 8. Audio Module - Full Audio Conversion

**Location**: `audio_steganography_service.py` line 147

**Problem**: Converts to WAV even if already WAV (comment: "even if already WAV, to get temp file")

**Impact**: Medium - Unnecessary conversion for WAV files

**Optimization**: Skip conversion if already WAV format

---

### 9. Document Module - PDF Parsing

**Location**: `document_steganography_service.py`

**Problem**: Full PDF parsing and rendering is expensive

**Impact**: High - PDF processing is inherently slow

**Optimization**: Cache parsed results when possible

---

## Performance Impact Summary

| Bottleneck | Impact | Optimization Difficulty | Security Impact |
|------------|--------|----------------------|----------------|
| Multiple image loads | High | Low | None |
| PNG compression level 9 | High | Low | None |
| Unnecessary image copy | Medium | Low | None |
| WAV conversion when already WAV | Medium | Low | None |
| Repeated edge detection | Medium | Medium | None |
| JSON serialization | Low | Low | None |
| Argon2id KDF | High | N/A | Security feature |
| Frame extraction | Very High | High | None |
| PDF parsing | High | Medium | None |

---

## Safe Optimizations to Apply

### Priority 1 (High Impact, Low Risk)

1. **Load image once and pass numpy array**
   - Modify `steganography_service.py` to load image once
   - Pass numpy array to edge detector and embedder
   - Expected improvement: 30-40% faster for image operations

2. **Reduce PNG compression level from 9 to 6**
   - Modify `image_converter.py` and `edge_lsb_embedder.py`
   - Expected improvement: 50-70% faster file saving
   - Trade-off: Slightly larger files (5-10%)

3. **Skip WAV conversion if already WAV**
   - Modify `audio_steganography_service.py`
   - Expected improvement: 20-30% faster for WAV files

### Priority 2 (Medium Impact, Low Risk)

4. **Remove unnecessary image copy**
   - Modify `edge_detector.py` to use in-place operations
   - Expected improvement: 10-15% faster edge detection

5. **Optimize JSON serialization**
   - Consider using orjson if available
   - Expected improvement: 5-10% faster serialization

### Priority 3 (Future Considerations)

6. **Cache edge detection results**
   - Only for same file reprocessing scenarios
   - Must not compromise security
   - Expected improvement: Significant for repeated operations

---

## Files to Modify

1. `backend/app/services/steganography_service.py` - Load image once
2. `backend/app/image_processing/image_converter.py` - Reduce compression level
3. `backend/app/steganography/edge_lsb_embedder.py` - Reduce compression level
4. `backend/app/image_processing/edge_detector.py` - Remove unnecessary copy
5. `backend/app/services/audio_steganography_service.py` - Skip WAV conversion

---

## Expected Overall Performance Improvement

- **Image embedding**: 40-60% faster
- **Image extraction**: 30-50% faster
- **Audio embedding**: 20-30% faster (for WAV files)
- **Video embedding**: Minimal change (bottleneck is frame extraction)
- **Document embedding**: Minimal change (bottleneck is PDF parsing)

---

## Verification Plan

1. Run existing test suite to ensure functionality unchanged
2. Create performance benchmarks before and after
3. Verify output files are identical (bit-for-bit comparison where applicable)
4. Verify security parameters unchanged
5. Verify all algorithms unchanged
