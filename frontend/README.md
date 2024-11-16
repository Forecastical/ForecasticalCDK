# Forecastical Frontend Setup Guide

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation Steps](#installation-steps)
   - [macOS](#macos)
   - [Linux](#linux)
   - [Windows](#windows)
3. [Project Setup](#project-setup)
4. [Running the Development Server](#running-the-development-server)
5. [Troubleshooting](#troubleshooting)

## Prerequisites

- Open your command line/terminal and know how to use it
- Be prepared to install our various packages detailed below

## Installation Steps

### macOS

1. Install Homebrew (if not preinstalled):
   ```
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. Install Node.js and npm:
   ```
   brew install node
   ```

3. Install Vue CLI:
   ```
   npm install -g @vue/cli
   ```

### Linux

1. Update the package manager:
   - For Ubuntu/Debian:
     ```
     sudo apt update && sudo apt upgrade
     ```
   - For Fedora:
     ```
     sudo dnf update
     ```

2. Install Node.js and npm:
   - For Ubuntu/Debian:
     ```
     sudo apt install nodejs npm
     ```
   - For Fedora:
     ```
     sudo dnf install nodejs npm
     ```

3. Install Vue CLI:
   ```
   sudo npm install -g @vue/cli
   ```

### Windows

1. Download and install Node.js: https://nodejs.org/

2. Install Vue CLI using command prompt or terminal or powershell, etc:
   ```
   npm install -g @vue/cli
   ```

## Project Setup

1. Clone the repository:
   ```
   git clone https://github.com/Forecastical/ForecasticalCDK.git
   cd ForecasticalCDK
   ```

2. Install project dependencies:
   ```
   npm install
   ```

   Install additonal auxiliary packages may also be necessary to run the app:
   ```
   npm install concurrently
   ```

## Running the Development Server

1. Start the development server:
   ```
   npm run serve
   ```

2. Go to `http://localhost:8080` (or the URL provided in the terminal output) in your favorite web browser that supports vue.

## Other dev options to run the app

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```


## Troubleshooting

- Permission errors on macOS or Linux? -> try using `sudo` before the commands.
- Permissions for windows? -> run Command Prompt or PowerShell or Terminal as an admin.
- Missing an npm package? -> run `npm install `` followed by the missing package.
- Other issues with npm? -> clear the npm cache:
  ```
  npm cache clean --force
  ```
  Then, delete the `node_modules` folder and `package-lock.json` file, and run `npm install` again.

For any other issues, please check the project's issue tracker on GitHub or reach out to our dev team.
