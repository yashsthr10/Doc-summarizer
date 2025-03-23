# Book Summarizer

Tired of slogging through 500-page novels? Let our Book Summarizer do the heavy lifting and deliver a concise summary so you can skip to the good parts. Built with OpenAI's GPT-3.5 Turbo, LangChain, and Streamlit, this tool transforms long texts into bite-sized insights—because who really has time to read it all?

## Features

* **Automated Summarization:** Condenses books and lengthy texts into a neat summary.
* **Multi-File Support:** Processes both PDF and plain text files.
* **Chunked Processing:** Splits large documents into manageable pieces to overcome prompt limitations.
* **Formatting:** Neatly formats the final summary for easy reading.
* **Simple Deployment:** Easily containerized with Docker and deployable to Kubernetes on GCP (if you dare to go cloud).

## Requirements

* Python 3.12 or later
* Required packages listed in `requirements.txt`
* Docker (optional, for containerization)
* A Kubernetes cluster on GCP (optional, for cloud deployment)

## Installation

1. **Clone the Repository:**

```bash
git clone https://github.com/yashsthr/doc-summarizer.git
cd doc-summarizer
```

2. **Set Up a Virtual Environment:**

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

3. **Install Dependencies:**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Usage

1. **Run the Application Locally:**
   Simply execute the script:

```bash
python app.py
```

This will read your input file (e.g., `doc.pdf`), generate a summary, format it, and save it to `summary.txt`.

## Deployment

1. **Docker Deployment:**
   Build your Docker image:

```bash
docker build -t doc-summarizer .
```

Run your container:

```bash
docker run -p 8501:8501 doc-summarizer
```

2. **Kubernetes Deployment (Optional):**
   If you fancy the cloud life, apply the Kubernetes manifests:

```bash
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
```

Your app will be accessible via the LoadBalancer's external IP.

## Contributing

Contributions are welcome! Feel free to fork the repo and submit pull requests. Just keep it simple—no unnecessary complications, please. We're all about clean, efficient code (and a dash of humor).

## License

This project is licensed under the MIT License. See the LICENSE file for details.

*Doc Summarizer* — Because reading entire books is so last century. Enjoy your newfound free time, and happy summarizing!
