#!/bin/bash

# Create a clean directory for downloads
mkdir -p test_dl
rm -rf test_dl/*

# Activate venv
source venv_linux/bin/activate

echo "Testing pip download for maturin and cryptography with Python 3.11 target..."

# Attempt 1: Just python-version
echo "--- Attempt 1: --python-version 3.11 --only-binary=:all: ---"
pip download \
    --dest test_dl \
    --python-version 3.11 \
    --only-binary=:all: \
    maturin cryptography \
    && echo "Attempt 1 SUCCESS" || echo "Attempt 1 FAILED"

rm -rf test_dl/*

# Attempt 2: python-version + platform (manylinux_2_28)
echo "--- Attempt 2: --python-version 3.11 --platform manylinux_2_28_x86_64 --only-binary=:all: ---"
pip download \
    --dest test_dl \
    --python-version 3.11 \
    --platform manylinux_2_28_x86_64 \
    --only-binary=:all: \
    maturin cryptography \
    && echo "Attempt 2 SUCCESS" || echo "Attempt 2 FAILED"

rm -rf test_dl/*

# Attempt 3: python-version + platform + implementation + abi
echo "--- Attempt 3: Full flags (cp311) ---"
pip download \
    --dest test_dl \
    --python-version 3.11 \
    --platform manylinux_2_28_x86_64 \
    --implementation cp \
    --abi cp311 \
    --only-binary=:all: \
    maturin cryptography \
    && echo "Attempt 3 SUCCESS" || echo "Attempt 3 FAILED"
