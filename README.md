# Kids Activity Helper

A simple web application to help parents find educational activities, books, and experiments for their children.

## Features
- Select child's age group (3-5, 6-8, 9-12).
- Choose an interest (Science, Arts, Reading).
- Get curated recommendations.

## Tech Stack
- **Python**
- **Streamlit**: For the web interface.
- **uv**: For extremely fast Python package management.

## How to Run Locally

1.  **Clone the repository** (if you haven't already):
    ```bash
    git clone <your-repo-url>
    cd <your-repo-folder>
    ```

2.  **Install uv**:
    If you don't have `uv` installed, follow the instructions [here](https://docs.astral.sh/uv/getting-started/installation/) or run:
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

3.  **Run the App**:
    `uv` will automatically create a virtual environment and install dependencies the first time you run the command.
    ```bash
    uv run streamlit run app.py
    ```

4.  **Access the App**:
    The app will open in your browser automatically. If not, check the terminal for the URL (usually `http://localhost:8501`).

## Deployment

To share this app with others, you can deploy it for free on **Render**, **Railway**, or **Streamlit Cloud**.
