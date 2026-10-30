import re
import uuid
from datetime import datetime
from pathlib import Path

import numpy as np
import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps
from moviepy import ImageClip, concatenate_videoclips, vfx


# ==================================================
# CONFIGURATION
# ==================================================

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

VIDEO_WIDTH = 1280
VIDEO_HEIGHT = 720
FPS = 24
SCENE_DURATION = 4
FADE_DURATION = 0.35

st.set_page_config(
    page_title="Property Video Studio",
    page_icon="🏠",
    layout="wide"
)


# ==================================================
# FONT
# ==================================================

def get_font(size, bold=False):
    fonts = [
        r"C:\Windows\Fonts\arialbd.ttf" if bold
        else r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\segoeuib.ttf" if bold
        else r"C:\Windows\Fonts\segoeui.ttf",
    ]

    for font_path in fonts:
        if Path(font_path).exists():
            try:
                return ImageFont.truetype(font_path, size)
            except OSError:
                continue

    return ImageFont.load_default()


# ==================================================
# TEXT WRAPPING
# ==================================================

def wrap_text(draw, text, font, max_width):
    words = str(text).split()
    lines = []
    current_line = ""

    for word in words:
        candidate = f"{current_line} {word}".strip()
        box = draw.textbbox((0, 0), candidate, font=font)

        if box[2] - box[0] <= max_width:
            current_line = candidate
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines or [""]


def draw_wrapped_text(
    draw, text, x, y, font, fill,
    max_width, line_spacing=8
):
    for line in wrap_text(draw, text, font, max_width):
        draw.text((x, y), line, font=font, fill=fill)

        box = draw.textbbox((x, y), line, font=font)
        y += box[3] - box[1] + line_spacing

    return y


# ==================================================
# IMAGE BACKGROUND
# ==================================================

def create_background(uploaded_image=None):
    if uploaded_image is not None:
        uploaded_image.seek(0)

        with Image.open(uploaded_image) as source:
            source = ImageOps.exif_transpose(source).convert("RGB")
            background = ImageOps.fit(
                source,
                (VIDEO_WIDTH, VIDEO_HEIGHT),
                method=Image.Resampling.LANCZOS
            ).convert("RGBA")
    else:
        background = Image.new(
            "RGBA",
            (VIDEO_WIDTH, VIDEO_HEIGHT),
            (15, 32, 52, 255)
        )

    # Gradient-style dark overlay at the bottom
    overlay = Image.new(
        "RGBA",
        (VIDEO_WIDTH, VIDEO_HEIGHT),
        (0, 0, 0, 0)
    )
    draw = ImageDraw.Draw(overlay)

    for y in range(VIDEO_HEIGHT):
        opacity = int(15 + 185 * (y / VIDEO_HEIGHT))
        draw.line(
            [(0, y), (VIDEO_WIDTH, y)],
            fill=(5, 14, 24, opacity)
        )

    return Image.alpha_composite(background, overlay)


# ==================================================
# SCENE DESIGN
# ==================================================

def create_scene(
    image,
    title,
    subtitle,
    label="PROPERTY TOUR",
    price=""
):
    canvas = create_background(image)
    draw = ImageDraw.Draw(canvas)

    label_font = get_font(21, bold=True)
    title_font = get_font(49, bold=True)
    subtitle_font = get_font(27)
    price_font = get_font(29, bold=True)

    # Teal header label
    draw.rounded_rectangle(
        (55, 42, 365, 88),
        radius=14,
        fill=(0, 135, 125, 245)
    )

    draw.text(
        (75, 52),
        label.upper(),
        font=label_font,
        fill="white"
    )

    if price:
        draw.text(
            (60, 345),
            price,
            font=price_font,
            fill=(105, 255, 210, 255)
        )

    title_y = 405

    title_y = draw_wrapped_text(
        draw,
        title,
        60,
        title_y,
        title_font,
        "white",
        VIDEO_WIDTH - 120,
        5
    )

    draw_wrapped_text(
        draw,
        subtitle,
        62,
        min(title_y + 12, VIDEO_HEIGHT - 80),
        subtitle_font,
        (238, 244, 250, 255),
        VIDEO_WIDTH - 125,
        5
    )

    return np.asarray(canvas.convert("RGB"))


# ==================================================
# RULE-BASED SCRIPT GENERATOR
# ==================================================

def generate_script(
    name, location, price, property_type, features, contact
):
    script = [
        f"Discover {name}, located in {location}.",
        f"This property is a {property_type}, listed at {price}."
    ]

    if features:
        script.append(
            "Highlighted features include "
            + ", ".join(features)
            + "."
        )

    if contact.strip():
        script.append(f"For enquiries, {contact.strip()}.")
    else:
        script.append("Contact the property team for enquiries.")

    return "\n\n".join(script)


# ==================================================
# VIDEO GENERATION
# ==================================================

def generate_video(
    name,
    location,
    price,
    property_type,
    features,
    contact,
    images
):
    clips = []
    final_video = None

    try:
        # Opening scene
        opening = create_scene(
            None,
            name,
            f"{property_type} | {location}",
            label="PROPERTY SHOWCASE",
            price=price
        )

        clips.append(
            ImageClip(opening).with_duration(SCENE_DURATION)
        )

        # Photo scenes
        for index, image in enumerate(images):
            if features:
                feature = features[index % len(features)]
                subtitle = f"Property highlight: {feature}"
                title = feature
            else:
                title = name
                subtitle = f"Discover this {property_type}"

            scene = create_scene(
                image,
                title,
                subtitle,
                label=f"SCENE {index + 1:02d}",
                price=price if index == 0 else ""
            )

            clips.append(
                ImageClip(scene).with_duration(SCENE_DURATION)
            )

        # Final enquiry scene
        ending = create_scene(
            None,
            "Interested in This Property?",
            contact.strip() or "Contact us for more information",
            label="ENQUIRE TODAY",
            price=price
        )

        clips.append(
            ImageClip(ending).with_duration(SCENE_DURATION)
        )

        # Transitions
        transitioned_clips = [
            clip.with_effects([
                vfx.FadeIn(FADE_DURATION),
                vfx.FadeOut(FADE_DURATION)
            ])
            for clip in clips
        ]

        final_video = concatenate_videoclips(
            transitioned_clips,
            method="compose",
            padding=-FADE_DURATION
        )

        safe_name = re.sub(
            r"[^a-zA-Z0-9_-]+",
            "_",
            name
        ).strip("_")[:50] or "property"

        filename = (
            f"{safe_name}_"
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_"
            f"{uuid.uuid4().hex[:5]}.mp4"
        )

        output_path = OUTPUT_DIR / filename

        final_video.write_videofile(
            str(output_path),
            fps=FPS,
            codec="libx264",
            audio=False,
            preset="medium",
            logger="bar"
        )

        return output_path

    finally:
        if final_video is not None:
            final_video.close()

        for clip in clips:
            try:
                clip.close()
            except Exception:
                pass


# ==================================================
# STREAMLIT INTERFACE
# ==================================================

st.title("🏠 Property Video Studio")
st.write(
    "Turn property details and photographs into "
    "a promotional MP4 video."
)

st.caption(
    "Local template-based generation | No paid API required"
)

with st.sidebar:
    st.header("About")
    st.write("Create real-estate promotional videos automatically.")
    st.write("Output format: MP4")
    st.write("Resolution: 1280 × 720")
    st.write("Frame rate: 24 FPS")
    st.write("External AI/API: Not used")


with st.form("property_details_form"):
    st.header("1. Property Information")

    col1, col2 = st.columns(2)

    with col1:
        property_name = st.text_input(
            "Property Name *",
            placeholder="Green Valley Residency"
        )

        location = st.text_input(
            "Location *",
            placeholder="Mohali, Punjab"
        )

        price = st.text_input(
            "Price *",
            placeholder="₹75 Lakh"
        )

    with col2:
        property_type = st.selectbox(
            "Property Type",
            [
                "2 BHK Apartment",
                "3 BHK Apartment",
                "Villa",
                "Independent House",
                "Studio Apartment",
                "Commercial Property",
                "Residential Plot"
            ]
        )

        contact = st.text_input(
            "Contact / Call to Action",
            placeholder="Call us today for an enquiry"
        )

    features_input = st.text_area(
        "Property Features (one per line)",
        placeholder=(
            "Covered Parking\n"
            "Spacious Balcony\n"
            "Modular Kitchen\n"
            "24x7 Security"
        )
    )

    st.header("2. Upload Property Images")

    uploaded_images = st.file_uploader(
        "Upload 4 to 8 JPG, JPEG, PNG or WEBP images",
        type=["jpg", "jpeg", "png", "webp"],
        accept_multiple_files=True
    )

    generate_button = st.form_submit_button(
        "Generate MP4 Video",
        type="primary",
        use_container_width=True
    )


if generate_button:
    errors = []

    if not property_name.strip():
        errors.append("Property name is required.")

    if not location.strip():
        errors.append("Property location is required.")

    if not price.strip():
        errors.append("Property price is required.")

    if not uploaded_images or len(uploaded_images) < 4:
        errors.append("Please upload at least 4 images.")

    if uploaded_images and len(uploaded_images) > 8:
        errors.append("Please upload no more than 8 images.")

    # Validate each image before rendering
    if uploaded_images:
        for image in uploaded_images:
            try:
                image.seek(0)
                with Image.open(image) as opened_image:
                    opened_image.verify()
                image.seek(0)
            except Exception:
                errors.append(
                    f"Invalid or unreadable image: {image.name}"
                )

    if errors:
        for error in errors:
            st.error(error)

    else:
        features = [
            item.strip()
            for item in features_input.splitlines()
            if item.strip()
        ]

        progress = st.progress(0)

        try:
            script = generate_script(
                property_name,
                location,
                price,
                property_type,
                features,
                contact
            )

            progress.progress(15)

            with st.spinner(
                "Rendering video. Please wait..."
            ):
                output_path = generate_video(
                    property_name,
                    location,
                    price,
                    property_type,
                    features,
                    contact,
                    uploaded_images
                )

            progress.progress(100)

            st.success("Video generated successfully!")

            st.header("3. Video Preview")

            st.video(str(output_path))

            with open(output_path, "rb") as video_file:
                video_bytes = video_file.read()

            st.download_button(
                "⬇ Download MP4",
                data=video_bytes,
                file_name=output_path.name,
                mime="video/mp4",
                use_container_width=True
            )

            st.header("4. Generated Voice-over Script")

            st.text_area(
                "Promotional Script",
                value=script,
                height=180
            )

            st.caption(
                f"Saved on your project drive: {output_path}"
            )

        except Exception as error:
            st.error(
                "Video generation failed. "
                "Check the error details below."
            )
            st.exception(error)


st.divider()

st.caption(
    "Prototype note: Script generation uses supplied facts "
    "and templates. This version does not generate speech "
    "or use an external generative AI model."
)
