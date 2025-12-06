# Code Trimmer Python - Dockerfile
# Multi-stage build for minimal production image

# Build stage
FROM python:3.11-slim as builder

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy source code
COPY . .

# Install the package
RUN pip install --no-cache-dir --user .

# Production stage
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Create non-root user
RUN useradd -m -s /bin/bash codetrimmer

# Switch to non-root user
USER codetrimmer
WORKDIR /home/codetrimmer

# Set default command
ENTRYPOINT ["codetrimmer"]
CMD ["--help"]

# Labels
LABEL org.opencontainers.image.title="Code Trimmer Python"
LABEL org.opencontainers.image.description="File formatting and whitespace normalization utility"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.source="https://github.com/pbaletkeman/code-trimmer-python"
LABEL org.opencontainers.image.licenses="MIT"

# Usage examples:
#
# Build:
#   docker build -t codetrimmer-python .
#
# Run:
#   docker run --rm -v $(pwd):/project codetrimmer-python trim /project
#
# Dry-run:
#   docker run --rm -v $(pwd):/project codetrimmer-python trim /project --dry-run
