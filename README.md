# TemuKampus — Lost and Found System

🇮🇩
Merupakan sebuah platfrom Lost and Found System, yang di buat dengan tujuan
untuk mempermudah para user dalam melaporkan kehilangan & penemuan barang di sekitar area lingkungan kampus.

🇺🇸
A web-based Lost and Found platform designed to help students and campus communities report, search, and recover lost or found items in the Universitas Negeri Surabaya (UNESA) campus environment.

## Overview

TemuKampus is a centralized information system that simplifies the process of reporting and finding lost belongings within the campus environment.

The platform provides an organized space where users can submit lost or found item reports, browse available reports, search for specific items, and contact the person responsible through WhatsApp.

## Features

- **Lost & Found Reporting** — Submit reports for lost or found belongings.
- **Item Search** — Search for items by name or location.
- **Status Filtering** — Filter reports based on their current status.
- **Image Upload** — Attach item photos to reports.
- **Report Statistics** — Display summaries of lost, found, and completed reports.
- **Status Management** — Mark reports as completed when an item has been returned.
- **Report Management** — Delete reports with confirmation.
- **WhatsApp Integration** — Contact the reporter through WhatsApp.
- **Interactive Interface** — Autumn-inspired visual design with animated backgrounds and falling leaf effects.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3 | Backend programming language |
| Flask | Web application framework |
| MySQL / MariaDB | Database management |
| HTML5 | Frontend structure |
| CSS3 | Styling and animations |
| JavaScript | Client-side interactions |
| WhatsApp Click-to-Chat | Communication integration |

## Project Structure

```text
lost-and-found-system/
│
├── database/
├── static/
├── uploads/
│
├── Main.py
├── index.html
├── style.css
├── background.js
│
├── background1.png
├── background2.png
├── background3.png
├── background4.png
│
├── requirements.txt
├── Procfile
│
└── PRD & SRD TemuKampus.md
```

## Requirements

Before installing the project, make sure you have:

- Python 3.10 or later
- pip (Python package manager)
- MySQL or MariaDB Server
- Git

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Anjaya-PureFrame/Lost-and-found-system.git
```

### 2. Navigate to the Project Directory

```bash
cd Lost-and-found-system
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

## Database Configuration

TemuKampus uses MySQL or MariaDB as its database management system.

Configure the database connection using the following environment variables:

| Variable | Description |
|---|---|
| MYSQLHOST | Database host |
| MYSQLUSER | Database username |
| MYSQLPASSWORD | Database password |
| MYSQLDATABASE | Database name |
| MYSQLPORT | Database port |

The default database name is `temukampus`.

Make sure the database and its tables are configured to match the application's database queries before running the application.

## Running the Application

After configuring the database and installing the required dependencies, run:

```bash
python Main.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

## Documentation

For more detailed information about the system requirements, product specifications, database design, and testing scenarios, see:

[PRD & SRD — TemuKampus](PRD%20%26%20SRD%20TemuKampus.md)

## Security Notes

- Never commit database credentials or secret keys to the repository.
- Store sensitive configuration in environment variables.
- Do not expose private user information.
- Validate uploaded files before processing them.

## Project Status

This repository is a web-based Lost and Found System project developed for the Universitas Negeri Surabaya (UNESA) campus environment.

## Author

**Anjaya-PureFrame**

GitHub: [@Anjaya-PureFrame](https://github.com/Anjaya-PureFrame)

---

*Developed as a software engineering project for campus-based lost and found management.*
