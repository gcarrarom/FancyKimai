#! /bin/bash

# Get the version from the version.json file and patch it
NEW_VERSION=$(jq -r '.patch += 1 | "\(.major).\(.minor).\(.patch)"' version.json)

# update the version in the pyproject.toml file
sed -i "s/version = \".*\"/version = \"$NEW_VERSION\"/g" pyproject.toml

# update the version in the version.json file
jq ".patch += 1" version.json > tmp.json
mv tmp.json version.json