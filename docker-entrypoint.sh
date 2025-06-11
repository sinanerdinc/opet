#!/bin/sh
set -e

case "$1" in
    "cli")
        shift  # Remove the first argument (cli)
        exec opet-cli "$@"
        ;;
    "api")
        shift  # Remove the first argument (api)
        exec python -m opet.server.run "$@"
        ;;
    *)
        echo "Usage: docker run [OPTIONS] opet [cli|api] [ARGS...]"
        exit 1
        ;;
esac 