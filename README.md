# Advanced ListDiff
A powerful, fast, and easy-to-use self-hosted tool to compare two lists of items. Instantly find the intersection, differences, and duplicates between two sets of data. Built with Flask and Gunicorn, and containerized with Docker for easy deployment.

**[➡️ Live Demo Link (Optional: Add a link if you host a public version)](https://listdiff.selfhostapps.com/)**

---

## ✨ Features

*   **Multiple Comparison Modes:** Calculates Intersection, Unique Items (A-only & B-only), Symmetric Difference, Union, and Duplicates within each list.
*   **Flexible Input:** Paste lists directly into text areas or upload `.txt` and `.csv` files.
*   **Smart Parsing:**
    *   Handles various delimiters (newline, comma, space, tab, etc.).
    *   Includes a "Clean Up" button to standardize messy data before comparing.
*   **Powerful Options:**
    *   Case-insensitive comparison.
    *   Option to trim leading/trailing whitespace.
*   **User-Friendly Interface:**
    *   Clean, modern UI with a responsive layout.
    *   **Dark Mode** with automatic theme detection and persistence.
    *   Live counts of total and unique items as you type.
*   **Easy Data Export:** Download comparison results as a single, organized `.csv` file.
*   **Optimized for Self-Hosting:** Lightweight, secure, and easy to deploy with Docker.
---

## 🚀 Self-Hosting with Docker Compose (Production)
This is the recommended way to run Advanced ListDiff. It's simple, reliable, and will automatically restart the application if your server reboots.

### Prerequisites
You must have [Docker](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/) installed on your server.

### Step 1: Create a Directory
Create a dedicated directory on your server where you will store the configuration file.

```bash
mkdir listdiff-server
cd listdiff-server
```

### Step 2: Create `docker-compose.yml` File
Create a new file in this directory named `docker-compose.yml`.

```bash
touch docker-compose.yml
```

### Step 3: Paste the Configuration
Open the `docker-compose.yml` file and paste the following content.

```yaml
version: '3.8'

services:
  advanced-listdiff:
    image: manimo/advanced-listdiff:latest
    
    # This maps the standard HTTP port (80) to the app's internal port.
    # To use a different port, change "80:9050" to "YOUR_PORT:9050".
    ports:
      - "8080:9050"
      
    # Ensures the app always restarts if it stops or the server reboots.
    restart: unless-stopped
```

### Step 4: Start the Application
Run the following command from within the `listdiff-server` directory to start the application.

```bash
docker-compose up -d
```

Your self-hosted instance of Advanced ListDiff is now running! You can access it at `http://your_server_ip:8080`.
---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).