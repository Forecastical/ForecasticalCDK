# Forecastical Frontend Setup Guide

This guide will walk you through setting up the development environment for the Forecastical frontend project. Follow the steps for your operating system to get started.

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

- Basic knowledge of command-line interfaces
- Internet connection for downloading necessary tools and dependencies

## Installation Steps

### macOS

1. Install Homebrew (if not already installed):
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

1. Update your package manager:
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

1. Download and install Node.js from the official website: https://nodejs.org/

2. Open Command Prompt or PowerShell as administrator and install Vue CLI:
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

## Running the Development Server

1. Start the development server:
   ```
   npm run serve
   ```

2. Open your web browser and navigate to `http://localhost:8080` (or the URL provided in the terminal output).

## Troubleshooting

- If you encounter permission errors on macOS or Linux, try using `sudo` before the commands.
- For Windows users, ensure that you're running Command Prompt or PowerShell as an administrator.
- If you face issues with npm, try clearing the npm cache:
  ```
  npm cache clean --force
  ```
  Then, delete the `node_modules` folder and `package-lock.json` file, and run `npm install` again.

For any other issues, please check the project's issue tracker on GitHub or reach out to the development team.
