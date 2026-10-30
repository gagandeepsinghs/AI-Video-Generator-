# AI Property Video Generator

A local Python web application that creates a short real-estate
promotional video from property details and uploaded photographs. The
app uses template-based text and image scenes; it does not require a
paid API or an external AI model.

## Features

-   Streamlit web interface for entering property information.
-   Upload 4--8 property images (JPG, JPEG, PNG, or WEBP).
-   Create an opening title, property-photo scenes, and a final enquiry
    scene.
-   Add property name, location, price, type, and feature captions.
-   Apply fade-in and fade-out transitions.
-   Export a downloadable MP4 video.
-   Generate a simple promotional script from the supplied property
    facts.
-   Validate required fields and report invalid image uploads.

## Technology Stack

-   Python
-   Streamlit --- web interface
-   MoviePy --- video composition and MP4 export
-   Pillow --- image processing and text overlays
-   NumPy --- image frame conversion
-   FFmpeg --- video encoding support provided through MoviePy's
    imageio-ffmpeg dependency

## Project Structure

``` text
AI Property Video Generator/
├── .venv/                 # Local virtual environment (created during setup)
├── app.py                 # Main Streamlit application
├── requirements.txt        # Python dependencies
├── output/                # Generated MP4 files
└── README.md               # Project documentation
```

The `output/` directory is created automatically when the application
starts. Keep `.venv/` local to your machine; it does not need to be
submitted.

## Requirements

-   Windows 10/11
-   Python installed and available through the `py` launcher
-   Internet access for the initial package installation
-   Enough disk space for dependencies and generated videos

## Installation (Windows PowerShell)

Open a terminal and run:

``` powershell
Set-Location "F:\AI Automation Projects\AI Property Video Generator"

# Create a virtual environment (only needed once)
py -m venv .venv

# Activate it
.\.venv\Scripts\Activate.ps1

# Install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell blocks environment activation, run this in the same
terminal session, then activate again:

``` powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Run the Application

From the project folder, with the virtual environment activated:

``` powershell
python -m streamlit run app.py
```

Streamlit will print a local URL in the terminal (normally
`http://localhost:8501`). Open that address in your browser if it does
not open automatically.

## How to Use

1.  Enter the property name, location, and price.
2.  Select the property type.
3.  Enter a contact message or call-to-action.
4.  Add property features, one feature per line.
5.  Upload 4--8 valid property images.
6.  Click **Generate MP4 Video** and wait for rendering to finish.
7.  Preview the generated video in the app.
8.  Use **Download MP4** to save a copy.
9.  The generated video is also saved in the project's `output/`
    directory.

## Output Details

-   Format: MP4
-   Resolution: 1280 × 720 (landscape)
-   Frame rate: 24 FPS
-   Scenes: opening title, one scene per uploaded photo, and final
    enquiry scene
-   Scene timing: approximately 4 seconds per scene, with short fade
    transitions
-   Audio: not included in the current version

Output filenames include the property name and a timestamp to reduce
accidental overwrites.

## Example Test Data

Use synthetic details for testing:

-   Property name: Green Valley Residency
-   Location: Mohali, Punjab
-   Price: ₹75 Lakh
-   Property type: 2 BHK Apartment
-   Features: Covered Parking, Spacious Balcony, Modular Kitchen, 24x7
    Security
-   Contact: Call us today for an enquiry
-   Images: Four separate property photographs (exterior, living room,
    bedroom, kitchen)

Use only details that are actually supplied. Do not present sample
information as a verified real listing.

## Troubleshooting

### `py` or `python` is not recognized

Install Python and ensure the Python launcher is available. Reopen the
terminal after installation.

### PowerShell activation is blocked

Run the `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`
command shown in the installation section and activate the environment
again.

### `ModuleNotFoundError`

Confirm that `.venv` is activated and run:

``` powershell
python -m pip install -r requirements.txt
```

### Video generation fails

-   Confirm that 4--8 images were uploaded.
-   Try standard JPG or PNG images.
-   Check the full error shown in the Streamlit app or terminal.
-   Confirm there is sufficient free disk space in the project drive.
-   Ensure the dependencies installed without errors.

### Text does not fit or looks different

The app uses available Windows fonts with a fallback. Very long property
names or feature text may require shorter wording.

## Approach and Limitations

This prototype uses **rule-based templates**, not a generative AI model.
It builds a promotional script from the entered property facts and adds
captions to image scenes. No external API key is required.

Current limitations: - No AI-generated narration or voice-over audio. -
No background music. - No database or user authentication. - Images are
fitted to a landscape frame and may be cropped. - Video content is based
only on user-provided information; the app does not verify property
claims. - This is a prototype, not a production real-estate publishing
system.

## Dependencies and External Services

The application dependencies are listed in `requirements.txt`. The
current implementation does not call an external AI API or require an
API key. Package installation requires internet access, but video
generation runs locally after installation.

## Submission Checklist

-   [ ] `app.py` included
-   [ ] `requirements.txt` included
-   [ ] `README.md` included
-   [ ] Application launches successfully
-   [ ] Test with at least four images
-   [ ] Generate and inspect at least one sample MP4
-   [ ] Include the sample MP4 in the submission
-   [ ] Prepare a short demo and explain the approach and limitations

## License

This project was created as an assignment prototype. Add a license only
if one is required by your submission instructions.
