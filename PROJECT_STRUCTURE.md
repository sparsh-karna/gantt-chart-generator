# Gantt Generator Project Structure

```
gantt-generator/
├── gantt_generator.py      # Main script
├── requirements.txt        # Python dependencies
├── setup.sh               # Installation script
├── validate.py            # Testing script
├── README.md              # Documentation
├── sample_project.csv     # Sample CSV data
├── sample_project.xlsx    # Sample Excel data
├── .gitignore            # Git ignore rules
└── myEnv/                # Virtual environment (local)
```

## Core Files

- **gantt_generator.py**: Main Gantt chart generation script
- **requirements.txt**: Python package dependencies
- **README.md**: Complete documentation and usage guide
- **setup.sh**: Automated setup script for easy installation

## Sample Data

- **sample_project.csv**: Example CSV file for testing
- **sample_project.xlsx**: Example Excel file for testing

## Utilities

- **validate.py**: Script to test installation and functionality
- **.gitignore**: Prevents clutter in version control

## Usage

1. Run `./setup.sh` or `pip install -r requirements.txt`
2. Test with `python3 validate.py`
3. Generate charts with `python3 gantt_generator.py --sample`
