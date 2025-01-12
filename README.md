# Sparrow_codeNest: AI-Powered Pest Detection

Sparrow is a Streamlit-based application designed to detect pests in plant fields using AI models. The app leverages the power of YOLO for real-time image and video pest detection, helping farmers and researchers monitor and mitigate pest-related issues efficiently.

---

## Features

- **Pest Detection**: Detects common pests like Leaf-folder, Green-leafhopper, Rice-bug, Stem-borer, and Whorl-maggot.
- **Input Flexibility**: Supports image and video uploads, as well as real-time webcam capture.
- **Customizable Output**: Provides downloadable detection results for further analysis.
- **Interactive UI**: Built with Streamlit for a seamless and interactive user experience.

---

## Installation

Follow these steps to set up the application on your local system:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/skylight-rana/Sparrow_codeNest.git
   cd Sparrow_codeNest

2. **Install Dependencies**: Make sure you have Python 3.8+ installed. Install the required packages:
   ```bash
   pip install -r requirements.txt
   
4. **Download YOLOv5 Model**: Place your YOLOv5 model weights (best.pt) in the root directory or update the path in app.py if located elsewhere.

5. **Run the Application**: Launch the Streamlit app:
   ```bash
   streamlit run app.py

**Usage**
**Upload an Image or Video**
  1. Choose the Upload File option in the sidebar.
  2. Upload an image (.jpg, .png) or video (.mp4) for detection.
  3. Click the Run Detection button to process the input.

**Use Webcam for Real-Time Detection**
  1. Choose the Webcam Capture option in the sidebar.
  2. Capture a frame from the webcam.
  3. Click the Run Detection button to analyze the captured frame.

**Download Results**
  Detected files (images/videos) will appear in the output section. You can view or download them directly.

**Dependencies**
  - Python 3.8+
  - Streamlit
  - PyTorch
  - YOLOv5
  - OpenCV
