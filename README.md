# Restaurant Assistant

## Prerequisites
- Python 3.7 or higher, x64 version.

### Installation
To use the restaurant assistant it needs to be installed, along with its dependencies.
It may be wise to create a virtual environment before installing to avoid overwriting existing installations.
To create the virtual environment and activate it:

```sh
python -m venv .env
.env\Scripts\activate.bat
```

To install the requirements and the program:

```sh
pip install -r requirements.txt
pip install -e .
```

### Usage
The program can be started in the CMD by running:

```sh
restaurant_assistant
```

### Parameters
Additional parameters can be given to the program to change its configuration for that run. The following options are available:


| Shorthand  | Full name     | Explanation                                                                                                                                  | Default          |
|------------|---------------|----------------------------------------------------------------------------------------------------------------------------------------------|------------------|
| -c         | --classifier  | Decides which classifier to use to classify the type of the user utterance. <br> Options: neural\_network, decision\_tree, keyword, majority | neural\_network  |
| -t         | --test        | Tests the classifier on its performance, reporting the F1 score and the accuracy.                                                            | False            |
| -s         | --speech      | Converts the program output to audio and plays it.                                                                                           | False            |
| -n         | --nr_recs     | Decides the maximum amount of recommendations that the system will give.                                                                     | 3                |
| -r         | --restart     | Allows for restarts of the program.                                                                                                          | False            |
| -u         | --uppercase   | Prints all program output with uppercase letters.                                                                                            | False            |
