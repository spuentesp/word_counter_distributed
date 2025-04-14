FROM debian:bullseye

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
  curl gnupg lsb-release build-essential cmake libssl-dev \
  libzeroc-ice3.7 libzeroc-ice-dev zeroc-ice-slice zeroc-ice-compilers && \
  ldconfig

# Set Ice environment variables
ENV Ice_HOME=/usr
ENV Ice_SLICE_DIR=/usr/share/Ice/slice

# Copy necessary files
COPY nodo_cpp/ ./nodo_cpp/
COPY shared/ ./shared/

# Generate C++ files from .ice definitions
RUN slice2cpp -Ishared shared/WordCount.ice --output-dir ./nodo_cpp/

# Build
RUN mkdir -p build && cd build && \
    cmake ../nodo_cpp && \
    make

EXPOSE 10000
# Run
CMD ["./build/nodo_cpp"]
