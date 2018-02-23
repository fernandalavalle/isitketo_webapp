#!/bin/bash
# Downloads the latest copy of the DocStringChecker plugin.

set -x

OUTPUT_DIR=$(dirname "$0")
OUTPUT_FILE="${OUTPUT_DIR}/lint.py"

wget \
  https://chromium.googlesource.com/chromiumos/chromite/+/master/cli/cros/lint.py?format=TEXT \
  -O - | \
  base64 --decode | sed "s/visit_function(/visit_functiondef(/" > "$OUTPUT_FILE"
