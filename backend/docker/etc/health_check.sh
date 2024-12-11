#!/usr/bin/env bash
set -e

if [ ${MIXMATCH_ENABLE_API} == "true" ]; then
    curl --fail http://localhost:8000/api/health || exit 1
else
    exit 0
fi
