#!/bin/bash
sed -i.bak "s/version = \"[0-9]*.[0-9]*.[0-9]*\"/version = \"$1\"/" pyproject.toml
sed -i.bak "s/version: str = \"[0-9]*.[0-9]*.[0-9]*\"/version: str = \"$1\"/" app/config.py
