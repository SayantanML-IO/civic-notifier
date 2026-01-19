# Civic Notifier 🏛️

A Python automation tool that monitors government websites for new notifications, scrapes PDF contents for specific keywords (e.g., "recruitment", "tender"), and sends email alerts.

## 🚀 Features

* **Automated Scraping:** Monitors configured websites for new PDF documents.
* **Smart Filtering:** Downloads and parses PDFs to find specific keywords using `pdfplumber`.
* **Email Alerts:** Sends summaries via SMTP when relevant documents are found.
* **Duplicate Prevention:** Tracks processed links to avoid spamming.

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Libraries:** `requests`, `beautifulsoup4`, `pdfplumber`, `python-dotenv`, `pyyaml`
* **Deployment:** Render (Cron Job)

## ⚙️ Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/SayantanML-IO/civic-notifier.git](https://github.com/SayantanML-IO/civic-notifier.git)
    cd civic-notifier
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Credentials:**
    Create a file named `.env` in the root directory and add your email details:
    ```ini
    EMAIL_PASSWORD=your_actual_app_password
    SENDER_EMAIL=your_email@gmail.com
    RECEIVER_EMAIL=recipient_email@gmail.com
    ```

4.  **Configure Monitoring:**
    Edit `config.yaml` to add or remove websites and keywords.

5.  **Run the script:**
    ```bash
    python main.py
    ```
