### Who buys the cake

#### Overview
The Cake Buyer App is a simple GUI application developed in Python using Tkinter. It helps a group of friends determine who should buy the cake next, ensuring everyone pays approximately the same amount over time.

#### Prerequisites
Before running the Cake Buyer App, ensure you have Python installed on your computer. This application was developed using Python 3.8 or newer. You can download Python from [https://python.org](https://python.org).

#### Setup

##### 1. Clone the repository
First, clone the repository or download the `cake_buyer_app.py` script to your local machine. You can do this using Git or by directly downloading the file if it's hosted online.

```bash
git clone https://github.com/mrmultifunk/who-buys-the-cake.git
cd who-buys-the-cake
```

##### 2. Create a virtual environment
Navigate to the project directory and create a Python virtual environment. This will allow you to install packages without affecting the global Python installation.

```bash
python -m venv venv
```

This command creates a new directory named `venv` where the virtual environment files are stored.

##### 3. Activate the virtual environment
Before running the script or installing any dependencies, activate the virtual environment:

**On Windows:**
```bash
.\venv\Scripts\activate
```

**On macOS and Linux:**
```bash
source venv/bin/activate
```

##### 4. Install dependencies
Currently, the Cake Buyer App only requires Tkinter, which is included with Python.

#### Running the Application
With the virtual environment activated and dependencies installed, you can run the application:

```bash
python cake_buyer_app.py
```

#### Building an Executable
To distribute your application as an executable:

1. **Install PyInstaller:**
   ```bash
   pip install pyinstaller
   ```

2. **Create an Executable:**
   Navigate to your project directory and run PyInstaller with your script:

   ```bash
   pyinstaller --onefile --windowed --icon=images\wbtc.ico cake_buyer_app.py
   ```

   - `--onefile`: Creates a single executable file.
   - `--windowed`: Prevents a command-line window from showing up in GUI applications.
   - `--icon`: Sets the icon for the executable.

   After running the command, find your `.exe` in the `dist` directory.

#### Exiting the Application
To stop the application, simply close the application window. To deactivate the virtual environment and return to your global Python environment, use the following command:

```bash
deactivate
```

#### Contributing
Contributions to the Cake Buyer App are welcome. Please fork the repository, make your changes, and submit a pull request.
