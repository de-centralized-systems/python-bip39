#!/usr/bin/env bash

# Increments the relevant version part by one:
# Usage: ./bump.sh <major|minor|patch> 
#   e.g: ./bump.sh patch
#
# Usage: ./bump.sh <version-from> <version-to>
# 	e.g: ./bump.sh 1.1.1 2.0

set -e

# Define which files to update and the pattern to look for
# $1 Current version
# $2 New version
function bump_files() {
	bump_version setup.py "version=\"$1\"" "version=\"$2\""
	#bump_version package.json "\"version\": \"$1\"" "\"version\": \"$2\""
	#bump_version README.md "my-plugin v$current_version" "my-plugin v$new_version"
}

function bump_version() {
	echo -n "Updating $1..."
	tmp_file=$(mktemp)
	rm -f "$tmp_file"
	sed -i "s/$2/$3/1w $tmp_file" $1
	if [ -s "$tmp_file" ]; then
		echo "Done"
	else
		echo "Nothing to change"
	fi
	rm -f "$tmp_file"
}

function confirm() {
	read -r -p "$@ [Y/n]: " confirm

	case "$confirm" in
		[Nn][Oo]|[Nn])
			echo "Aborting."
			exit
			;;
	esac
}

# main:

if [ "$1" == "" ]; then
	echo >&2 "No argument given. Aborting."
	exit 1
fi

if [ "$1" == "major" ] || [ "$1" == "minor" ] || [ "$1" == "patch" ]; then
	#current_version=$(grep -Po '(?<="version": ")[^"]*' package.json)
	current_version=$(grep -Po '(?<=version=")[^"]*' setup.py)

	IFS='.' read -a version_parts <<< "$current_version"

	major=${version_parts[0]}
	minor=${version_parts[1]}
	patch=${version_parts[2]}

	case "$1" in
		"major")
			major=$((major + 1))
			minor=0
			patch=0
			;;
		"minor")
			minor=$((minor + 1))
			patch=0
			;;
		"patch")
			patch=$((patch + 1))
			;;
	esac
	new_version="$major.$minor.$patch"
else
	if [ "$2" == "" ]; then
		echo >&2 "No 'to' version set. Aborting."
		exit 1
	fi
	current_version="$1"
	new_version="$2"
fi

if ! [[ "$new_version" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
	echo >&2 "'to' version doesn't look like a valid semver version tag (e.g: 1.2.3). Aborting."
	exit 1
fi

confirm "Bump version number from $current_version to $new_version?"

bump_files "$current_version" "$new_version"

