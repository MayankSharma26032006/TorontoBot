# Start from a small official Python image (same Python version as requirements.txt)
FROM python:3.14-slim

# All commands below run inside /app in the container
WORKDIR /app

# Print logs immediately instead of buffering them
ENV PYTHONUNBUFFERED=1

# sentence-transformers needs PyTorch. The default Linux PyTorch wheel bundles
# multi-GB GPU libraries this app never uses, so install the small CPU-only build
# first — pip below then reuses it instead of downloading the GPU version.
RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch

# Install the Python packages. Docker caches this step, so it only re-runs
# when requirements.txt changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code (including src/materials) into the image.
# .env is NOT copied here — .dockerignore keeps it out of the image.
COPY src ./src

# Streamlit uses this port
EXPOSE 8501

# Start the Streamlit UI on 0.0.0.0 so it is reachable from outside the container
CMD ["streamlit", "run", "src/streamlitMain.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]
