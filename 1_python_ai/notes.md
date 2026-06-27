# Windows Development Environment Setup Guide for AI Engineering

> **Target Audience:** Beginners using Windows for Python Development, AI/ML, FastAPI, and Software Engineering.

# Prerequisites

The following software should be installed before starting development:

1. Python 3.10+
2. Visual Studio Code
3. Terminal Setup
4. uv (Package Manager)

# 1. Install Python (>= 3.10)

## Why Python?

Python is the primary programming language used for AI and machine learning.


## Download Python

Download the latest stable version:

https://www.python.org/downloads/windows/

Choose:

**Windows Installer (64-bit)**

## Verify Installation

Open **Git Bash** or **PowerShell**

```bash
python --version
```

Expected:

```text
Python 3.14.0
```

Also try

```bash
python3 --version
```

Sometimes on Windows you will see

```text
Python was not found; run without arguments to install from the Microsoft Store...
```

This is completely normal. Windows uses the command:

```python``` instead of ```python3```

If you're following Linux/macOS tutorials, just mentally replace:

```python3 app.py``` –> ```python app.py```


```pip3 install pandas``` –> ```python -m pip install pandas```


## Optional: Make python3 work on Windows

### Step 1

Disable Microsoft Store aliases

Go to

```
Settings
    Apps
        Advanced App Settings
            App Execution Aliases
```

Turn OFF

* python.exe
* python3.exe


### Step 2

Create a PowerShell alias

```powershell
Set-Alias python3 python
```

# 2. Install Visual Studio Code

## Download

https://code.visualstudio.com/

Install using default settings.

# 3. Terminal Setup

## What is a Terminal?

A terminal allows you to communicate with your computer using commands.

Almost all professional software development happens inside a terminal.

Examples:

```bash
git clone
```

## Difference between CMD, PowerShell and Git Bash

### CMD

* Old Windows command prompt
* Very limited
* Mostly legacy


### PowerShell

* Modern Windows shell
* Powerful scripting
* Great Windows administration

### Git Bash

Git Bash provides a Linux-like terminal on Windows.

Examples:

```bash
ls
```

These commands are used on: **Linux, Azure, GCP, Remote Servers, Docker Containers**

Learning Git Bash means your commands transfer directly to real-world Linux environments.

Use **Git Bash as your default profile** inside Windows Terminal.

## Install Git for Windows

### Download

https://git-scm.com/download/win

Install with default settings. This installs Git and Git Bash

### Verify

Open Git Bash

Run

```bash
git --version
```

Example

```text
git version 2.xx.x.windows.x
```

# 4. Install uv

## What is uv?

uv is an extremely fast Python package manager and project manager written in Rust.

It replaces tools like: pip, virtualenv, pip-tools, poetry (many workflows)

## What is a Package?

A package is reusable code written by someone else. Like pandas, numpy, etc.

Instead of writing everything yourself, you install packages.


## What is a Project Manager?

A project manager helps you:

* Create virtual environments
* Install packages
* Lock dependency versions
* Reproduce projects
* Manage project metadata


## Virtual Environments

### Why do we need Virtual Environments?

Different projects require different package versions.

For example, if project A needs pandas==2.0, but Project B needs pandas==2.3

A virtual environment isolates each project's dependencies.

### 0. Install uv

Open Git Bash

```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Restart your terminal.

Verify

```bash
uv --version
```

### 1. Create a New Project

Initialize a project

```bash
uv init my_project
```

Move into the project

```bash
cd my_project
```

### 2. Synchronize Dependencies

```bash
uv sync
```

Installs everything listed in the project configuration.

### 3. Create Virtual Environment

```bash
uv venv --python 3.12
```

This creates

```
.venv
```

### 4. Activate Environment (Windows)

PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

Git Bash

```bash
source .venv/Scripts/activate
```

### 5. Deactivate

```bash
deactivate
```

### 6. Installing Packages

Install a package

```bash
uv add pandas
```

Install multiple

```bash
uv add pandas numpy matplotlib
```