# GEN3-RXT native source and simulations

Published 14 September 2026. This is the C++/CUDA/GMP **GEN3-RXT-R7.1** research engine used by the joint RH, ATOM3D and Starbreaker campaign. That deployment used the R3 foundation. The current workstation installation is R4; see the [September 16 source supplement](../gen3-r4/README.md).

## Code and source inputs

The [native source tree](native/src) contains the complete R7.1 translation units: exact engine/store, ATOM3D, Starbreaker, horizon formation, RH, construction, training and domain transfer. Every source file matches the [R7.1 build manifest](native/NATIVE_UPDATE_MANIFEST.json). [Source packets](native/source) include the inherited immutable domain, core-memory, training and horizon inputs plus the R7.1 RH overlay. The [source export manifest](../SOURCE_EXPORT.json) records original paths and SHA-256 values.

## Build and execute

The recorded build targets NVIDIA architecture 120 and requires CUDA 12.8+, CMake 3.24+, a C++20 compiler, OpenMP, OpenSSL, GMP/GMPXX and nlohmann-json development headers. From this directory:

```sh
cmake -S native -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j 4
./build/gen-rxt
```

The final command prints the native command-line interface. See [main.cpp](native/src/main.cpp) for the `daemon` and JSON `call` interfaces and [example packets](native/examples). Configure a new local state directory for a new simulation; workstation and pod private checkpoint keys are not part of the source distribution. The saved production run used its acquired checkpoint, so a fresh machine starts with the supplied source inputs rather than that evolved root. This publication verifies source identity; a CUDA rebuild has not been run on this workstation.

## Recorded simulations and implications

[Starbreaker](../starbreaker/README.md) and [ATOM3D](../atom3d/README.md) explain the domain outputs. The [feedback report](../evidence/GEN3_RXT_RH_WEEKEND1/DOMAIN_FEEDBACK_R7.md), [completion](../evidence/GEN3_RXT_RH_WEEKEND1/results/R71_DOMAIN_FEEDBACK_COMPLETION.json), [learned models](../evidence/GEN3_RXT_RH_WEEKEND1/results/R71_FINAL_DOMAIN_FIT.json), and [native qualification](../evidence/GEN3_RXT_RH_WEEKEND1/results/R71_DOMAIN_QUALIFICATION.json) publish the recorded 36,864 fresh A3D41 families, 1,216 SB histories and 288 horizon cases, 252 formed. Native class-balanced learning retains the previous 45 construction policies and six core-memory packages. The completed R4 dataset contains 1,590,144 families; it is a separate recorded stage, not an extra count added to the R7.1 completion.

The signed receiver and common-minimum features connect construction decisions to exact source histories. Development scores are 847/936 for common minima and 1 for the signed SB target. These are development results for the named targets. RH's uniform signed-growth estimate remains the open mathematical task described in [the RH section](../rh/README.md).
