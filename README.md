### Table of Contents  
[WG Gesucht Tool](#wg-gesucht-tool)
- [How it works](#how-it-works)
- [How to use it](#how-to-use-it)

[Setup EC2 instance](#setup-ec2-instance)
- [Install python](#install-python)
- [Install Chrome Web Browser and corresponding WebDriver](#install-chrome-web-browser-and-corresponding-webdriver)
- [Clone the project and setup environment](#clone-the-project-and-setup-environment)

# WG Gesucht Tool
Finding a new appartment can be difficult some times and it is important to be always alert to find the new adds. That's why I developed a Shared Flat Web Searcher for the Website [WG-Gesucht](https://www.wg-gesucht.de/en/), which is the most known tool for finding accommodation in Germany.

## How it works
- First of all, it is necessary to set the requirements to filter the search. In [objects.py](https://github.com/juan-alvarez99/wg-gesucht-tool/blob/main/modules/objects.py) there is a dictionary with all the implemented filters for my search such as the earliest date of move, my age and my gender. 
- Using [Selenium](https://selenium-python.readthedocs.io) the search is run from the website of WG-Gesucht and the filters are applied.
- Using [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) to scrap the html code parsing the data from each ad: rent prize, size of the room...
- In order to analyze the data to estimate the cost of a room in the searched city, the results of the search are sync with Google Sheet using [Sheety](https://sheety.co/docs) to generate an API endpoint to a specific sheet. There I can play some statistics!
- If during the search a new ad is found, the app is going to send me an email with a link to the WG ad


## How to use it
1. Clone the project and create the virtual environment from the requirements.txt file

***
# Setup EC2 instance
## Install python 

**Guide from [Krishan Kumar](https://www.linkedin.com/in/krishan2aws/)**

### Step 1: Update the system
First, update the package lists and install required dependencies:
```sh
sudo yum update -y
sudo yum groupinstall -y "Development Tools"
sudo yum install -y openssl-devel bzip2-devel libffi-devel zlib-devel wget make
```

### Step 2: Download and extract Python 3.12
Navigate to the /usr/src directory and download the Python 3.12 source code:

```sh
cd /usr/src
sudo wget https://www.python.org/ftp/python/3.12.0/Python-3.12.0.tgz
sudo tar xzf Python-3.12.0.tgz
```

### Step 3: Compile and install Python 3.12
Change to the Python source directory, configure the build, and install Python:

```sh
cd Python-3.12.0
sudo ./configure --enable-optimizations
sudo make altinstall
```

### Step 4: Verify the installation
Verify that Python 3.12 and pip3.12 have been installed correctly:

```sh
python3.12 --version
pip3.12 --version
```

### Step 5: Ensure pip is installed and updated
If pip is not installed, you can install it manually:

```sh
wget https://bootstrap.pypa.io/get-pip.py
sudo python3.12 get-pip.py
```

Upgrade pip to the latest version:

```sh
pip3.12 install --upgrade pip
```

### Step 6: Configure SSL certificates (if needed)
Ensure that pip can verify SSL certificates by installing the certifi package and configuring pip to use it:

```sh
pip3.12 install certifi
```

Create or modify the pip configuration file to specify the path to the certifi certificate bundle. For a global configuration:

```sh
sudo sh -c 'echo "[global]\ncert = $(python3.12 -m certifi)" > /etc/pip.conf'
```

For a user-specific configuration:

```sh
mkdir -p ~/.config/pip
echo -e "[global]\ncert = $(python3.12 -m certifi)" > ~/.config/pip/pip.conf
```

### Step 7: Verify the configuration
Ensure that pip3.12 is using the correct certificate bundle by running:

```sh
pip3.12 install requests
```
This command should install the requests package without any SSL errors.

***

## Install Chrome Web Browser and corresponding WebDriver

### Step 1: Install Google Chrome

Update the system 
```sh
sudo yum update -y
```

Create a file named `google-chrome.repo` in the yum repository directory
```sh
sudo vi /etc/yum.repos.d/google-chrome.repo
```

Add the following content to the file:
```sh
[google-chrome]
name=google-chrome
baseurl=https://dl.google.com/linux/chrome/rpm/stable/x86_64
enabled=1
gpgcheck=1
gpgkey=https://dl.google.com/linux/linux_signing_key.pub
```

Install Google Chrome
```sh
sudo yum install -y google-chrome-stable
```

### Step 3: Install ChromeDriver
Download the latest version of ChromeDriver that matches the installed version of Chrome, extract the downloaded file and move the `chromedriver` binary to `/usr/local/bin`
```sh
wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
```

***

## Clone the project and setup environment
### Step 1: Clone the project

```sh
git clone https://github.com/juan-alvarez99/wg-gesucht-tool.git
```

### Step 2: Create environment

```sh
python3 -m venv myenv
source myenv/bin/activate
```

### Step 3: Install all dependencies

```sh
pip install -r requirements.txt
```

### Step 4: Create a .env file with the following variables

```sh
DRIVER_PATH='/usr/local/bin/chromedriver'
CHROME_PATH=/usr/bin/google-chrome

# Sheety endpoint
SHEETY_ENDPOINT=
HEADER=

# Setup the notification manager 
EMAIL=
PASSWORD=
```

