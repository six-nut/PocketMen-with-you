# Model licenses

PocketMen source code is MIT. Neural model weights are not bundled in this repository and keep their original licenses.

## Default

### FLUX.2 [klein] 4B

Model id: `black-forest-labs/FLUX.2-klein-4B`

License: Apache-2.0.

PocketMen uses this as the default neural-local backend because it supports generation, image editing and multi-reference editing while remaining suitable for commercial/open-source downstream use under its published license.

## Optional Identity-Max

### Qwen-Image-Edit-2511

Model id: `Qwen/Qwen-Image-Edit-2511`

License: Apache-2.0.

PocketMen uses it only when explicitly selected or when a user needs heavier identity-sensitive editing.

## Not a default backend

### FLUX.2 [dev]

The FLUX [dev] model family is distributed under Black Forest Labs' non-commercial model license. PocketMen therefore does not enable it as the project's general default, even though it can offer higher local quality on large GPUs.

Always review upstream license terms before changing the backend matrix.
