# Scrapper

A simple project using **beautifulsoup** to scrapping web content.

## Installation

1. Install virtual environment in python.
```bash 
sudo apt-get install python3.10-venv 
```
2. Create a virtual environment, go to your project’s directory and run the following command.
```bash
python3 -m venv .venv
```
3. Activating a virtual environment with environment-specific python and pip executables into your shell’s
```bash
source .venv/bin/activate
```
4. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install packages.

```bash
pip install -r requirements.txt
```
5. Copy file **.env.example** to **.env** and add necessary environment
6. Run migration file.
```bash
python migration.py
```
7. Start scrapping
```bash
python main.py
```