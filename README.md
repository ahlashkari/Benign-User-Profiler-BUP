![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Paramiko](https://img.shields.io/badge/SSH-Paramiko-4B8BBE?style=for-the-badge&logo=ssh&logoColor=white)
![Requests](https://img.shields.io/badge/HTTP-Requests-FF6B6B?style=for-the-badge&logo=python&logoColor=white)
![BeautifulSoup](https://img.shields.io/badge/Parsing-BeautifulSoup-306998?style=for-the-badge&logo=python&logoColor=white)
![PyAutoGUI](https://img.shields.io/badge/Automation-PyAutoGUI-FFD43B?style=for-the-badge&logo=python&logoColor=black)
![Firefox](https://img.shields.io/badge/Browser-Firefox-FF7139?style=for-the-badge&logo=firefox&logoColor=white)


![](https://github.com/ahlashkari/Benign-User-Profiler-BUP/blob/main/bccc.jpg)

# Benign User Profiler (BUP)
BUP is a tool for generating benign user traffic patterns for security research and testing. It simulates realistic user behavior across various protocols and applications.

# Table of Contents

- [Benign User Profiler](#BenignUserProfiler)
- [Usage](#Usage)
- [Installation](#installation)
- [Features](#Features)
- [Architecture](#Architecture)
- [Citation and Copywrite 2024](#Citation&Copywrite2024)
- [Project Team members](#ProjectTeammembers)
- [Acknowledgement](#Acknowledgement)



# BenignUserProfiler


## Major Updates

### Removed Selenium Dependency
- Replaced Selenium-based browser automation with a lightweight approach using requests and BeautifulSoup
- Enhanced traffic models to provide detailed feedback for better visibility of operations
- Added simulation modes for all models to enable testing without actual external connections

### HTTP Model Enhancements
- Completely rewrote the HTTP model to use requests and BeautifulSoup instead of Selenium
- Added detailed webpage browsing simulation with realistic scrolling feedback
- Enhanced YouTube watching simulation with detailed interaction messages
- Improved feedback with detailed progress during all operations

### Email Model Enhancements
- Enhanced both SMTP (email sending) and IMAP (email checking) models
- Added Lorem Ipsum API integration for realistic email content generation
- Implemented simulation modes for both email models
- Added attachment handling capabilities
- Enhanced feedback with detailed progress messages during operations

### FTP Model Enhancements
- Added support for both regular FTP and FTPS (SSL)
- Enhanced FTP model to provide detailed feedback during operations
- Added file upload and download capabilities with progress tracking
- Implemented simulation mode to avoid actual server connections

### SSH Model Enhancements
- Added improved command execution feedback
- Implemented simulation mode with realistic command output generation
- Enhanced error handling and connection management
- Added support for both password and key-based authentication

### Configuration Updates
- Created a comprehensive configuration structure with examples for all models
- Added simulation mode options to avoid actual server connections
- Added detailed configuration options for each model
- Implemented better defaults for ease of use



# Usage

## Standard Execution

To execute the program with simulated traffic, run this command:

```bash
benign-user-profiler
```

You can use `-h` to see different options of the program:

```bash
# Run with default config file
benign-user-profiler

# Run with a specific config file
benign-user-profiler --config /path/to/config.json

# Run with parallel execution
benign-user-profiler --parallel

# Run with work hours restrictions (9am-5pm by default)
benign-user-profiler --work-hours

# Run with custom work hours
benign-user-profiler --work-hours "10:00-18:00"

# Run with randomized task execution (shuffles task order regardless of start times)
benign-user-profiler --randomize
```

## Real Traffic Generation

For realistic traffic generation with actual browser interaction, use the included script:

```bash
# Run with real browser interaction
./run_traffic.sh

# Run in headless mode (no visible browser windows)
./run_traffic.sh --headless

# Run in simulation mode (no real browser interaction)
./run_traffic.sh --simulate
```

### Requirements for Real Traffic

Real traffic generation has the following dependencies:

#### Linux:
- Firefox browser
- xdotool (for keyboard/mouse simulation)
- LibreOffice (for document creation)

#### Windows:
- Firefox browser
- PowerShell (for application control)
- Microsoft Office (for document creation)

The `run_traffic.sh` script will check for these dependencies and warn you if any are missing.

## Usage Examples

### HTTP/Web Browsing
```python
http_model = HTTPModel()
model_config = {
    "websites": ["https://www.example.com"],
    "browse_time": [20, 60],
    "scroll_min": 3,
    "scroll_max": 8
}
http_model.model_config = model_config
http_model.generate()
```

### YouTube Watching
```python
youtube_model = HTTPModel()
model_config = {
    "youtube_videos": ["https://www.youtube.com/watch?v=example123"],
    "youtube_min_watch": 30,
    "youtube_max_watch": 60,
    "youtube_engagement": True
}
youtube_model.model_config = model_config
youtube_model.generate()
```

### Email Sending (SMTP)
```python
smtp_model = SMTPModel()
model_config = {
    "service": "gmail",
    "sender": "test@gmail.com",
    "password": "password",
    "receivers": ["recipient@example.com"],
    "generate_content": True
}
smtp_model.model_config = model_config
smtp_model.generate()
```

### Email Checking (IMAP)
```python
imap_model = IMAPModel()
model_config = {
    "service": "gmail",
    "username": "test@gmail.com",
    "password": "password"
}
imap_model.model_config = model_config
imap_model.generate()
```

### FTP Operations
```python
ftp_model = FTPModel(ssl=False)  # For FTPS, use ssl=True
model_config = {
    "address": "ftp.example.com",
    "username": "user",
    "password": "password",
    "browse": ["/"]
}
ftp_model.model_config = model_config
ftp_model.generate()
```

### SSH Operations
```python
ssh_model = SSHModel()
model_config = {
    "address": "ssh.example.com",
    "username": "user",
    "password": "password",
    "commands": [
        {"str": "ls -la", "show_output": True}
    ]
}
ssh_model.model_config = model_config
ssh_model.generate()
```

## Task Scheduling and Randomization

By default, tasks are scheduled and executed based on their start times. You can enable task randomization in two ways:

1. Using the `--randomize` command-line flag: This will randomize all tasks regardless of their configured start times.
2. Setting `"randomize": true` in individual model configurations: This allows you to control which specific tasks/models should be randomized.

When randomization is enabled, tasks will be executed in a random order rather than strictly by their start times. This creates more realistic and less predictable traffic patterns.

This project has been successfully tested on Ubuntu 22.04. It should work on other versions of Ubuntu OS (or even Debian OS) as long as your system has the necessary python3 packages (you can see the required packages in the `requirements.txt` file).

# Installation

# Features

- **Multi-protocol support**: HTTP/HTTPS, SSH, FTP/SFTP, SMTP, IMAP, and command-line operations
- **Real Browser Support**: Interact with real Firefox browser for authentic traffic generation
- **YouTube support**: Visit YouTube, search for videos, watch content, and interact with playback controls
- **SoundCloud integration**: Browse and listen to music on SoundCloud
- **Google Search**: Perform Google searches and click on search results
- **Media download simulation**: Download images from various sources like Unsplash
- **Email capabilities**: Send and receive emails with attachments via Gmail and other providers
- **Application launching**: Open and interact with random applications on Windows and Linux
- **Office document integration**: Create and save documents using Microsoft Office (Windows) or LibreOffice (Linux) for email attachments
- **Network scanning**: Ping local network addresses to simulate network discovery
- **Scheduling**: Configure frequency and timing of activities with work hours restrictions and optional task randomization
- **Cross-platform**: Works on Linux and Windows with platform-specific implementations


# Architecture


![](./architecture.svg)


# Citation&Copywrite2024 


 
For citation in your works and also to understand BUP completely, you can find below the published paper:

"Toward Generating a New Cloud-Based Distributed Denial of Service (DDoS) Dataset and Cloud Intrusion Traffic Characterization", Shafi, MohammadMoein, Arash Habibi Lashkari, Vicente Rodriguez, and Ron Nevo.; Information 15, no. 4: 195. https://doi.org/10.3390/info15040195

```
@Article{info15040195,
AUTHOR = {Shafi, MohammadMoein and Lashkari, Arash Habibi and Rodriguez, Vicente and Nevo, Ron},
TITLE = {Toward Generating a New Cloud-Based Distributed Denial of Service (DDoS) Dataset and Cloud Intrusion Traffic Characterization},
JOURNAL = {Information},
VOLUME = {15},
YEAR = {2024},
NUMBER = {4},
ARTICLE-NUMBER = {195},
URL = {https://www.mdpi.com/2078-2489/15/4/195},
ISSN = {2078-2489},
DOI = {10.3390/info15040195}
}
  ```




# ProjectTeammembers 

* [**Arash Habibi Lashkari:**](http://ahlashkari.com/index.asp) Founder and supervisor

* [**Amirhossein Ahmadnejad Roudsari:**](https://github.com/aahmadnejad) Graduate researcher and developer - York University

* [**Moein Shafi:**](https://github.com/moein-shafi) Graduate researcher and developer - York University



# Acknowledgement
This project has been made possible through funding from the Natural Sciences and Engineering Research Council of Canada — NSERC (#RGPIN-2020-04701) and Canada Research Chair (Tier II) - (#CRC-2021-00340) to Arash Habibi Lashkari.

