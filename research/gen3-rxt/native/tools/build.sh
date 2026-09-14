#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
args=()
if [[ -n "${RXT_DEPS:-}" ]]; then
  args+=("-DRXT_DEPS=$RXT_DEPS")
elif [[ -d /workspace/GEN-RXT-R1/deps/usr ]]; then
  args+=("-DRXT_DEPS=/workspace/GEN-RXT-R1/deps/usr")
fi
build_dir=${RXT_BUILD_DIR:-/var/tmp/gen3-rxt/build/$(basename "$PWD")}
cmake -S . -B "$build_dir" -DCMAKE_CUDA_COMPILER=/usr/local/cuda/bin/nvcc -DCMAKE_BUILD_TYPE=Release "${args[@]}"
cmake --build "$build_dir" -j "${RXT_BUILD_JOBS:-4}"
mkdir -p bin
cp "$build_dir/gen-rxt" bin/gen-rxt.new
mv bin/gen-rxt.new bin/gen-rxt
