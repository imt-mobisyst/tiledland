cd `dirname $0`/..

find . -type d -name '__pycache__' -prune -exec rm -rf '{}' +
