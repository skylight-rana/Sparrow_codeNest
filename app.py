import streamlit as st
from pathlib import Path
from detect import run
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

# --- App Configuration ---
st.set_page_config(
    page_title="Pest Detection",
    page_icon="🌾",
    layout="wide",
)

# --- Custom CSS Styling ---
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #4CAF50;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    .sub-header {
        font-size: 1.25rem;
        color: #555;
        text-align: center;
        margin-bottom: 40px;
    }
    .section-header {
        font-size: 1.5rem;
        color: #333;
        margin-top: 30px;
        margin-bottom: 10px;
        border-bottom: 2px solid #4CAF50;
        padding-bottom: 5px;
    }
    .button {
        background-color: #4CAF50;
        color: white;
        font-size: 1rem;
        border-radius: 5px;
        padding: 10px 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Main App ---
st.markdown('<div class="main-header">Sparrow</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Powered Insect Detection in Plant Fields</div>',
            unsafe_allow_html=True)
# --- Display Pest Detection Information ---
st.markdown(
    """
    <div class="section-header">Pests Detectable by Sparrow</div>
    <p><strong>Sparrow</strong> can detect the following pests:</p>
    <ul>
        <li>Leaf-folder</li>
        <li>Green-leafhopper</li>
        <li>Rice-bug</li>
        <li>Stem-borer</li>
        <li>Whorl-maggot</li>
    </ul>
    <p>Please upload an image or video for detection!</p>
    """,
    unsafe_allow_html=True
)

# --- Output Directory ---
output_dir = Path("output/detection_results")
output_dir.mkdir(parents=True, exist_ok=True)

# --- Parameters ---
weights_path = "../best.pt"  # Path to the YOLO model
data_path = "data.yaml"  # Dataset YAML


def clear_output_directory(directory: Path):
    """Clears all files in the specified directory."""
    for file in directory.iterdir():
        if file.is_file():
            file.unlink()


# --- Webcam Video Transformer ---
class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.image = None

    def transform(self, frame):
        self.image = frame.to_image()
        return frame


# --- Layout: Sidebar for Input Selection ---
st.sidebar.header("Upload or Capture")
input_type = st.sidebar.radio("Choose Input Type", ["Upload File", "Webcam Capture"])

# --- File Upload Section ---
if input_type == "Upload File":
    st.markdown('<div class="section-header">Upload Image or Video</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Select an image or video file:", type=["jpg", "png", "mp4"])

    if uploaded_file:
        # Save uploaded file
        clear_output_directory(output_dir)
        input_file_path = output_dir / uploaded_file.name
        with open(input_file_path, "wb") as f:
            f.write(uploaded_file.read())

        #st.image(input_file_path, caption="Uploaded File", width=10, use_column_width=True)

        if st.button("Run Detection", key="upload"):
            with st.spinner("Running detection on the uploaded file..."):
                try:
                    run(
                        weights=weights_path,
                        source=str(input_file_path),
                        imgsz=(640, 640),
                        conf_thres=0.25,
                        project="output",
                        name="detection_results",
                        exist_ok=True,
                    )
                    result_file_path = output_dir / uploaded_file.name
                    if result_file_path.exists():
                        st.success("Detection complete!")
                    else:
                        st.warning("Output image not found!")

                except Exception as e:
                    st.error(f"Error: {e}")

# --- Webcam Capture Section ---
elif input_type == "Webcam Capture":
    st.markdown('<div class="section-header">Capture from Webcam</div>', unsafe_allow_html=True)
    webcam_input = webrtc_streamer(key="webcam", video_transformer_factory=VideoTransformer)

    if webcam_input.video_transformer and webcam_input.video_transformer.image is not None:
        captured_image_path = output_dir / "captured_image.jpg"
        webcam_input.video_transformer.image.save(captured_image_path, format="JPEG")
        st.image(captured_image_path, caption="Captured Image", use_column_width=True)

        if st.button("Run Detection", key="webcam"):
            with st.spinner("Detecting objects in the captured image..."):
                try:
                    run(
                        weights=weights_path,
                        source=str(captured_image_path),
                        imgsz=(640, 640),
                        conf_thres=0.25,
                        project="output",
                        name="detection_results",
                        exist_ok=True,
                    )
                    st.success("Detection complete!")
                    result_image_path = output_dir / "captured_image.jpg"
                    if result_image_path.exists():
                        st.image(result_image_path, caption="Detected Output", use_column_width=True)
                    else:
                        st.warning("Output image not found!")

                except Exception as e:
                    st.error(f"Error: {e}")

# --- Detected Files Section ---
st.markdown('<div class="section-header">Detected Pest</div>', unsafe_allow_html=True)

# Check for any files in the directory (images and videos)
detected_files = list(output_dir.glob("*.*"))

# Filter only image and video files
image_video_files = [file for file in detected_files if file.suffix.lower() in [".jpg", ".png", ".mp4"]]

if image_video_files:
    for file in image_video_files:
        with open(file, "rb") as f:
            # For images
            if file.suffix.lower() in [".jpg", ".png"]:
                st.image(file, caption=file.name, use_column_width=True)
            # For videos
            elif file.suffix.lower() == ".mp4":
                st.markdown(f"### {file.name}")  # Display the caption as text
                st.video(file)

            st.download_button(
                label=f"Download {file.name}",
                data=f.read(),
                file_name=file.name,
                mime="application/octet-stream",  # Appropriate MIME type for general files
            )
else:
    st.write("No detected files available.")

# --- Footer ---
st.markdown('<div class="sub-header">Developed with ❤️ by CodeNest</div>', unsafe_allow_html=True)
