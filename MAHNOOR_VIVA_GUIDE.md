# Mahnoor's Viva Preparation Guide — Matplotlib + OpenCV

---

## File 1: `src/visualizer.py`

### Purpose
Generates statistical charts about the AI model's training data and usage patterns. Saves them as PNG images.

### Library Used
**Matplotlib** (for creating plots and charts)

### 5 Functions — Each Makes a Different Chart

| Function | Chart Type | What It Shows |
|----------|-----------|---------------|
| `plot_corpus_distribution()` | Pie chart + Bar chart | How many snippets are Python vs Bash vs C, and average code length per language |
| `plot_keyword_frequency()` | Horizontal bar chart | Top 20 most common keywords in the training data (e.g., "for", "if", "return") |
| `plot_tfidf_heatmap()` | Heatmap (color grid) | Which terms are important for which snippets — darker color = higher weight |
| `plot_topic_distribution()` | Pie chart | What topics users ask about most (Shell, C/OS, Python, etc.) |
| `plot_snippet_complexity()` | Scatter plot | Each dot is a snippet — X axis = number of keywords, Y axis = lines of code, color = language |

### Key Matplotlib Functions Used

| Function | What It Does |
|----------|-------------|
| `plt.subplots()` | Creates figure and axes (the canvas) |
| `ax.pie()` | Draws a pie chart |
| `ax.bar()` / `ax.barh()` | Draws vertical / horizontal bar charts |
| `ax.imshow()` | Draws a heatmap (2D color grid) |
| `ax.scatter()` | Draws a scatter plot (dots) |
| `ax.plot()` | Draws a line chart |
| `plt.savefig()` | Saves the chart as a PNG file |
| `plt.colorbar()` | Adds a color legend to heatmaps |
| `plt.tight_layout()` | Adjusts spacing so nothing overlaps |

### How to Explain in Viva

> "This file uses Matplotlib to visualize our model's data. For example, `plot_corpus_distribution` creates a pie chart showing that our model has 95 Python snippets, 44 Bash, and 35 C. The `plot_tfidf_heatmap` shows a color grid where each cell represents how important a keyword is for a specific snippet — this helps us understand how the TF-IDF scoring works visually. All charts are saved as PNG files in the `output/charts/` folder."

---

## File 2: `src/image_processor.py`

### Purpose
Processes images of code (screenshots, photos of whiteboards) to make them readable. Prepares them for text extraction (OCR).

### Library Used
**OpenCV** (cv2) for computer vision + **NumPy** for pixel array operations

### 5 Main Functions

| Function | What It Does | OpenCV Functions Used |
|----------|-------------|---------------------|
| `preprocess_for_ocr()` | Full pipeline: grayscale → blur → threshold → clean | `cv2.cvtColor()`, `cv2.GaussianBlur()`, `cv2.adaptiveThreshold()`, `cv2.morphologyEx()` |
| `detect_code_region()` | Finds where the code is in the image | `cv2.Canny()` (edge detection), `cv2.findContours()`, `cv2.boundingRect()` |
| `correct_perspective()` | Fixes angled/tilted photos to make them flat | `cv2.getPerspectiveTransform()`, `cv2.warpPerspective()` |
| `enhance_contrast()` | Makes text more visible in dark/bright images | `cv2.createCLAHE()` (adaptive histogram equalization) |
| `analyze_code_structure()` | Counts lines, measures indentation, calculates density | `cv2.threshold()` + NumPy array operations on pixel rows |

### Step-by-Step: How `preprocess_for_ocr()` Works

```
Step 1: cv2.imread()                    → Load the image from disk
Step 2: cv2.cvtColor(COLOR_BGR2GRAY)    → Convert color to grayscale (1 channel instead of 3)
Step 3: cv2.GaussianBlur((3,3))         → Smooth out noise/grain
Step 4: cv2.adaptiveThreshold()         → Convert to pure black & white, handles uneven lighting
Step 5: cv2.morphologyEx(MORPH_CLOSE)   → Clean up tiny dots and gaps in text
Step 6: cv2.imwrite()                   → Save the processed image
```

### How to Explain In Viva

> "This file uses OpenCV to process code images. If a student takes a photo of code on a whiteboard, the image might be tilted, have bad lighting, or be noisy. My code fixes all of that: `preprocess_for_ocr` converts to grayscale, removes noise with Gaussian blur, and uses adaptive thresholding to handle uneven lighting. `correct_perspective` uses `getPerspectiveTransform` to straighten tilted photos. `analyze_code_structure` uses NumPy to count how many lines of code are in the image by analyzing pixel rows."

---

## File 3: `analyze_model.py`

### Purpose
A demo script that runs all 4 libraries (NumPy, Pandas, Matplotlib, OpenCV) together in one execution.

### What It Does Step by Step

| Step | Library | What Happens |
|------|---------|-------------|
| Step 1 | — | Loads the trained model (230 snippets) |
| Step 2 | **NumPy** | Builds TF-IDF matrix, tests cosine similarity on sample queries |
| Step 3 | **Pandas** | Creates DataFrames, shows corpus stats (snippets per language, avg lines, keyword frequency) |
| Step 4 | **Matplotlib** | Generates 4 chart PNGs (corpus distribution, keyword frequency, complexity scatter, TF-IDF heatmap) |
| Step 5 | **OpenCV** | Creates a demo code image with `cv2.putText()`, then preprocesses it, enhances contrast, analyzes structure |

### How to Explain in Viva

> "This is the integration script. When you run `python analyze_model.py`, it demonstrates all 4 libraries working together. NumPy builds the scoring matrix, Pandas analyzes the data, Matplotlib saves charts to `output/charts/`, and OpenCV creates and processes a sample code image. It proves that all libraries are actually being used in the project, not just imported."

---

## Output Folders

### `output/charts/` — Generated Chart Files

| File | What It Shows |
|------|--------------|
| `corpus_distribution.png` | Pie chart: Python 41%, Bash 19%, C 15% + bar chart of avg code lines |
| `keyword_frequency.png` | Top 15 keywords: "for" (92), "if" (77), "return" (76), etc. |
| `snippet_complexity.png` | Scatter plot: blue dots = Python, green = Bash, red = C |
| `tfidf_heatmap.png` | Color grid showing term importance across snippets |

### `output/processed/` — Generated Image Files

| File | What It Shows |
|------|--------------|
| `demo_code_input.png` | A code image created by OpenCV with `putText()` |
| `demo_code_input_processed.png` | Same image after thresholding (black & white, clean) |
| `demo_code_input_enhanced.png` | Same image after CLAHE contrast enhancement |

---

## Quick Answers for Common Viva Questions

**Q: Why Matplotlib?**
> To visualize how our model works — what languages it knows, which keywords are most common, how TF-IDF weights are distributed.

**Q: Why OpenCV?**
> So users can take a photo of code and the system can preprocess it for reading. It handles noise, bad lighting, and tilted angles.

**Q: What is adaptive thresholding?**
> Normal thresholding uses one cutoff value for the whole image. Adaptive thresholding calculates different cutoffs for different regions — so it works even if one corner is bright and another is dark.

**Q: What is perspective correction?**
> If you take a photo at an angle, the code looks like a trapezoid. `getPerspectiveTransform` calculates a matrix to warp it back into a rectangle.

**Q: What does CLAHE do?**
> It's Contrast Limited Adaptive Histogram Equalization. It improves contrast locally (in small tiles) so faded text becomes readable without over-brightening already bright areas.

**Q: What is the TF-IDF heatmap showing?**
> Each row is a code snippet, each column is a keyword. The color intensity shows how important that keyword is for that snippet. Bright = high weight, dark = low weight.

**Q: What is Gaussian Blur?**
> It smooths the image by averaging each pixel with its neighbors using a bell-curve (Gaussian) weighting. This removes small noise/grain without destroying text edges.

**Q: What is Canny edge detection?**
> It finds the boundaries/edges in an image by looking for sharp changes in pixel intensity. We use it to find the outline of the code block in a photo.

**Q: What does `cv2.findContours()` do?**
> It traces the outlines of shapes in a binary (black/white) image. We use it to find the largest rectangle — which is likely the code region.

**Q: What is morphological operation (MORPH_CLOSE)?**
> It fills small gaps in text characters. "Close" = dilate then erode — it connects nearby white pixels without making text thicker.

---

## How to Run the Demo

```bash
python analyze_model.py
```

This will print stats to terminal AND generate all chart/image files in the `output/` folder.
