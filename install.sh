#!/bin/sh

set -eu

repo_url="https://github.com/ssannssarr/Utilitis"
workdir=""

cleanup() {
	if [ -n "${workdir}" ] && [ -d "${workdir}" ]; then
		rm -rf "${workdir}"
	fi
}

trap cleanup EXIT INT TERM

die() {
	printf '%s\n' "$1" >&2
	exit 1
}

command -v git >/dev/null 2>&1 || die "Error: git is required but was not found in PATH."
command -v python >/dev/null 2>&1 || command -v python3 >/dev/null 2>&1 || die "Error: python or python3 is required but was not found in PATH."

if command -v python >/dev/null 2>&1; then
	python_cmd="python"
else
	python_cmd="python3"
fi

if command -v uv >/dev/null 2>&1; then
	installer_cmd="uv tool install ."
else
	if [ -n "${VIRTUAL_ENV:-}" ]; then
		die "Error: deactivate the active virtual environment or install uv first if you want a non-.venv install."
	fi
	if ! "$python_cmd" -m pip --version >/dev/null 2>&1; then
		"$python_cmd" -m ensurepip --upgrade >/dev/null 2>&1 || true
	fi
	if "$python_cmd" -m pip --version >/dev/null 2>&1; then
		installer_cmd="$python_cmd -m pip install --user ."
	else
		die "Error: pip is required but could not be initialized."
	fi
fi

workdir="$(mktemp -d)"
printf '%s\n' "Cloning Utilitis into ${workdir}..."
if ! git clone "${repo_url}" "${workdir}/Utilitis"; then
	die "Error: failed to clone ${repo_url}."
fi

printf '%s\n' "Installing Utilitis globally..."
if ! (
	cd "${workdir}/Utilitis" &&
	eval "${installer_cmd}"
); then
	die "Error: package installation failed."
fi

printf '%s\n' "DONE!!"
