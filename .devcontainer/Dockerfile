FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    build-essential cmake pkg-config bison flex libpng-dev zlib1g-dev python3 zip git ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# RGBDS
RUN git clone --depth=1 https://github.com/gbdev/rgbds.git /opt/rgbds \
 && cmake -S /opt/rgbds -B /opt/rgbds/build -DCMAKE_BUILD_TYPE=Release \
 && cmake --build /opt/rgbds/build -j"$(nproc)" \
 && cmake --install /opt/rgbds/build
ENV PATH="/usr/local/bin:${PATH}"
