# SRGAN Research Notes

## Learning Path for Understanding SRGAN

### Prerequisites (What You Need to Know First)

#### 1. Basic Concepts
- **Super-Resolution (SR)**: Taking a low-resolution image and generating a high-resolution version
- **Upscaling Factor**: How much bigger the output is (e.g., 4× means 100×100 → 400×400)
- **The Challenge**: When you enlarge an image, you're "guessing" missing pixels

#### 2. Traditional Approaches (and their problems)
| Method | How it works | Problem |
|--------|-------------|---------|
| Nearest Neighbor | Copy nearest pixel | Blocky, pixelated |
| Bicubic | Weighted average of neighbors | Blurry, no details |
| CNN + MSE | Neural network minimizing pixel error | Smooth, lacks texture |

#### 3. Key Metrics
- **PSNR (Peak Signal-to-Noise Ratio)**: Measures pixel-level accuracy (higher = closer to original)
- **SSIM (Structural Similarity)**: Measures structural similarity
- **MOS (Mean Opinion Score)**: Human perception rating (1-5 scale)

**Critical Insight**: High PSNR ≠ Good looking image!

---

## Part 1: The Core Problem SRGAN Solves

### Why MSE Loss Fails

When training with MSE (Mean Squared Error):
```
Loss = average( (predicted_pixel - actual_pixel)² )
```

The network learns to output the **average** of all possible solutions:
- If a pixel could be "dark texture" or "light texture"
- MSE encourages outputting the average → **blurry gray**

```
Example:
Possible solutions: [detailed grass] or [detailed leaves]
MSE output: [blurry green blob] (average of both)
```

This is illustrated in Figure 3 of the paper - MSE produces outputs that fall
BETWEEN the natural image manifold, not ON it.

---

## Part 2: The GAN Solution

### What is a GAN?

**Generative Adversarial Network** = Two networks competing:

```
┌─────────────┐         ┌───────────────┐
│  Generator  │ ──────► │ Discriminator │
│   (Artist)  │  fake   │   (Critic)    │
└─────────────┘  image  └───────────────┘
                              │
                              ▼
                        "Real or Fake?"
```

- **Generator (G)**: Creates SR images from LR input
- **Discriminator (D)**: Tries to tell real HR images from generated SR images

**Training Loop**:
1. G generates a fake HR image
2. D tries to classify it as real/fake
3. G improves to fool D
4. D improves to catch G
5. Repeat until G produces realistic images

---

## Part 3: SRGAN Architecture

### Generator Network (SRResNet)

```
Input (LR image)
    │
    ▼
┌─────────────────┐
│ Conv 9×9, 64    │  ← Initial feature extraction
│ PReLU           │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         │
┌─────────────────┐         │
│ Residual Block  │ ×16     │  ← 16 identical blocks
│ (Conv-BN-PReLU) │         │
│ (Conv-BN)       │         │
└────────┬────────┘         │
         │                  │
         ▼                  │
    [Element-wise Sum] ◄────┘  ← Skip connection
         │
         ▼
┌─────────────────┐
│ PixelShuffle ×2 │  ← Upscale 2×
│ PixelShuffle ×2 │  ← Upscale 2× (total 4×)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Conv 9×9, 3     │  ← Output RGB image
└─────────────────┘
    │
    ▼
Output (SR image)
```

### Residual Block Detail
```
Input
  │
  ├──────────────────────┐
  │                      │
  ▼                      │
Conv 3×3, 64             │
  │                      │
  ▼                      │
Batch Norm               │
  │                      │
  ▼                      │
PReLU                    │
  │                      │
  ▼                      │
Conv 3×3, 64             │
  │                      │
  ▼                      │
Batch Norm               │
  │                      │
  ▼                      │
[Add] ◄──────────────────┘
  │
  ▼
Output
```

### Discriminator Network

```
Input (HR or SR image)
    │
    ▼
┌─────────────────────────────────────┐
│ Conv blocks with increasing filters │
│ 64 → 64 → 128 → 128 → 256 → 256    │
│ → 512 → 512                         │
│ (stride=2 to reduce size)           │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│ Dense 1024 → LeakyReLU              │
│ Dense 1 → Sigmoid                   │
└────────────────┬────────────────────┘
                 │
                 ▼
        Probability (0-1)
        "How real is this image?"
```

---

## Part 4: The Perceptual Loss Function

### Total Loss Formula
```
L_total = L_content + 0.001 × L_adversarial
```

### Content Loss Options

**Option 1: MSE Loss (not recommended)**
```python
L_MSE = mean((I_SR - I_HR)²)
```
- High PSNR but blurry results

**Option 2: VGG Loss (recommended)**
```python
L_VGG = mean((VGG(I_SR) - VGG(I_HR))²)
```
- Compare feature maps from pre-trained VGG19
- VGG/5.4 (deeper layer) captures texture/content better
- Lower PSNR but much better perceptual quality

### Adversarial Loss
```python
L_adversarial = -log(D(G(I_LR)))
```
- Encourages G to produce images that D thinks are real
- Pushes output toward "natural image manifold"

---

## Part 5: Training Strategy

### Step 1: Pre-train SRResNet
- Train generator alone with MSE loss
- Get good initial weights
- ~10⁶ iterations

### Step 2: Train SRGAN
- Initialize G with SRResNet weights
- Train G and D alternately
- Use perceptual loss (VGG + adversarial)
- 10⁵ iterations at lr=10⁻⁴
- 10⁵ iterations at lr=10⁻⁵

### Training Details
- Dataset: 350K ImageNet images
- Batch: 16 random 96×96 HR crops
- Optimizer: Adam (β₁=0.9)
- GPU: NVIDIA Tesla M40

---

## Part 6: Key Results & Insights

### Quantitative Results (BSD100 dataset, 4× upscaling)

| Method | PSNR | SSIM | MOS |
|--------|------|------|-----|
| Bicubic | 25.94 | 0.6935 | 1.47 |
| SRCNN | 26.68 | 0.7291 | 1.87 |
| SRResNet | **27.58** | **0.7620** | 2.29 |
| SRGAN | 25.16 | 0.6688 | **3.56** |
| Original | ∞ | 1 | 4.46 |

### Key Insight
- SRResNet: Best PSNR/SSIM (pixel accuracy)
- SRGAN: Best MOS (human perception) - closest to original!
- **PSNR and human perception are NOT correlated**

### Visual Comparison
```
Bicubic:   Blurry, no detail
SRResNet:  Sharp but smooth (lacks texture)
SRGAN:     Detailed textures, photo-realistic
```

---

## Glossary

| Term | Definition |
|------|------------|
| SR | Super-Resolution |
| HR | High-Resolution |
| LR | Low-Resolution |
| GAN | Generative Adversarial Network |
| MSE | Mean Squared Error |
| PSNR | Peak Signal-to-Noise Ratio |
| SSIM | Structural Similarity Index |
| MOS | Mean Opinion Score |
| VGG | Visual Geometry Group (pretrained CNN) |
| PReLU | Parametric ReLU activation |
| BN | Batch Normalization |
| PixelShuffle | Sub-pixel convolution for upscaling |

---

## Reading Order for the Paper

1. **Abstract** (page 1) - Get the main idea
2. **Figure 1 & 2** (pages 1-2) - See visual results
3. **Section 1.1.3** (page 3) - Understand why MSE fails
4. **Figure 3** (page 3) - Key conceptual diagram
5. **Section 2.1** (page 4) - Architecture overview
6. **Figure 4** (page 5) - Network diagrams
7. **Section 2.2** (pages 5-6) - Loss functions
8. **Table 2** (page 8) - Main results
9. **Figure 5** (page 7) - MOS distribution

---

## Next Steps

1. [ ] Understand basic CNN operations (Conv, ReLU, BatchNorm)
2. [ ] Learn about residual connections (ResNet paper)
3. [ ] Study GANs basics (Goodfellow 2014)
4. [ ] Implement SRResNet (generator only)
5. [ ] Add discriminator and adversarial training
6. [ ] Implement VGG perceptual loss
7. [ ] Train on a small dataset
8. [ ] Evaluate results

---

## References for Prerequisites

1. **CNNs**: CS231n Stanford course
2. **ResNet**: "Deep Residual Learning" (He et al., 2016)
3. **GANs**: "Generative Adversarial Nets" (Goodfellow et al., 2014)
4. **VGG**: "Very Deep Convolutional Networks" (Simonyan & Zisserman, 2015)
5. **PixelShuffle**: "Real-Time Single Image SR" (Shi et al., 2016)
