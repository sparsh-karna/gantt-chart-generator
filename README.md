# Gantt Chart Generator

A Python script that generates detailed, color-coded Gantt charts from CSV or Excel files. Perfect for project management, task tracking, and timeline visualization.

## Features

- 📊 **Multiple Input Formats**: Supports both CSV and Excel files
- 🎨 **Color Coding**: Automatic color assignment by category or priority
- 📈 **Progress Tracking**: Visual progress bars showing task completion
- 👥 **Resource Management**: Display task assignments and resources
- 🏷️ **Priority Levels**: Color-coded priority indicators (High, Medium, Low, Critical)
- 📋 **Smart Column Detection**: Automatically detects common column name variations
- 📊 **Summary Statistics**: Shows total tasks, completed tasks, and average progress
- 🖼️ **High-Quality Output**: Saves charts as high-resolution PNG images

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Quick Start

### Generate Sample Data
To get started quickly, generate a sample project file:

```bash
python gantt_generator.py --sample
```

This creates `sample_project.csv` with example project data.

### Create a Gantt Chart
```bash
python gantt_generator.py sample_project.csv
```

## Usage

## 🧪 Testing the Installation

After running the setup, you can quickly test the Gantt chart generator:

```bash
# Quick test method
python3 validate.py

# Or manual testing:
# 1. Generate sample data
python3 gantt_generator.py --sample

# 2. Create a Gantt chart from the sample data
python3 gantt_generator.py sample_project.csv

# 3. Check that the chart was created
ls -la *.png
```

You should see a new PNG file with the generated Gantt chart.

## 📋 Usage Examples

### Basic Usage
```bash
# Generate a Gantt chart from CSV
python3 gantt_generator.py project_data.csv

# Generate with custom output filename
python3 gantt_generator.py project_data.csv -o my_gantt_chart.png

# Generate with custom title
python3 gantt_generator.py project_data.csv -t "My Project Timeline"

# Generate from Excel file
python3 gantt_generator.py project_data.xlsx -o excel_chart.png

# Create sample data for testing
python3 gantt_generator.py --sample
```

### Advanced Examples
```bash
# Complete project timeline with custom title and output
python3 gantt_generator.py data.csv -o "Q1_project_timeline.png" -t "Q1 2024 Development Roadmap"

# High-resolution chart for printing (300 DPI)
python3 gantt_generator.py data.csv -o timeline.png --dpi 300

# Lower resolution for web use (100 DPI)
python3 gantt_generator.py data.csv -o web_timeline.png --dpi 100

# Process multiple files (bash loop)
for file in *.csv; do
    python3 gantt_generator.py "$file" -o "${file%.csv}_gantt.png"
done
```

### Advanced Usage
```bash
python gantt_generator.py input_file.xlsx -o my_gantt_chart.png -t "My Project Timeline"
```

### Command Line Options
- `input_file`: Path to your CSV or Excel file
- `-o, --output`: Output image file name (optional)
- `-t, --title`: Custom chart title (default: "Project Gantt Chart")
- `--dpi`: Image resolution in DPI (default: 200, range: 72-300)
- `--sample`: Generate sample data file for testing

## Input File Format

### Required Columns
Your input file must contain these columns (case-insensitive):

| Column Name | Accepted Variations | Description |
|-------------|-------------------|-------------|
| Task Name | Task, Name | Name of the task |
| Start Date | Start, Start_Date, Begin | Task start date |
| End Date | End, End_Date, Finish | Task end date |

### Optional Columns
| Column Name | Accepted Variations | Description |
|-------------|-------------------|-------------|
| Category | Type, Group | Task category for color coding |
| Resource | Assignee, Owner | Person/team assigned to task |
| Progress | Completion, % | Completion percentage (0-100) |
| Priority | Importance | Task priority (High, Medium, Low, Critical) |

### Date Formats
The script accepts various date formats including:
- `YYYY-MM-DD` (2024-01-15)
- `MM/DD/YYYY` (01/15/2024)
- `DD/MM/YYYY` (15/01/2024)
- `YYYY/MM/DD` (2024/01/15)

## Example Input Files

### CSV Example (`project.csv`)
```csv
Task Name,Start Date,End Date,Category,Resource,Progress,Priority
Project Planning,2024-01-01,2024-01-07,Planning,PM Team,100,High
Requirements Gathering,2024-01-08,2024-01-21,Analysis,BA Team,100,High
System Design,2024-01-22,2024-02-04,Design,Architects,85,High
Database Setup,2024-02-05,2024-02-11,Development,DB Team,90,Medium
Frontend Development,2024-02-12,2024-03-10,Development,Frontend Team,60,High
Backend API Development,2024-02-12,2024-03-10,Development,Backend Team,70,High
Integration Testing,2024-03-11,2024-03-24,Testing,QA Team,30,Medium
User Acceptance Testing,2024-03-25,2024-03-31,Testing,QA Team,0,High
Documentation,2024-04-01,2024-04-14,Documentation,Tech Writers,20,Low
Deployment,2024-04-15,2024-04-21,Deployment,DevOps Team,0,Critical
```

### Excel Example
Create an Excel file with the same column structure as the CSV example above.

## Chart Features

### Color Coding
- **By Category**: Each category gets a unique color from a predefined palette
- **By Priority**: Priority levels override category colors:
  - 🔴 **Critical**: Purple
  - 🟠 **High**: Red
  - 🟡 **Medium**: Orange
  - 🟢 **Low**: Green

### Visual Elements
- **Progress Bars**: Clean progress overlay without distracting outlines
- **Task Labels**: Task names displayed to the left of bars
- **Resource Tags**: Resource assignments shown to the right
- **Grid Lines**: Weekly grid for easy date reading
- **Legend**: Properly positioned outside the chart area to avoid overlapping
- **Statistics Box**: Summary information in the top-left corner
- **High Resolution**: Configurable DPI from 72 to 300 for different use cases

## Troubleshooting

### Common Issues

**"Missing required columns" error**
- Check that your file has Task Name, Start Date, and End Date columns
- Column names are case-insensitive and accept variations

**"Error parsing dates" error**
- Ensure dates are in a recognizable format
- Check for empty date cells
- Verify date consistency (start date before end date)

**Chart looks cramped**
- The chart automatically adjusts height based on number of tasks
- For many tasks, the image will be taller
- Use the `-o` option to save as a file for better viewing

### Tips for Better Charts
1. **Keep task names concise** (under 30 characters for best display)
2. **Use consistent categories** for better color grouping
3. **Set realistic progress values** (0-100)
4. **Order tasks logically** in your input file (by start date or dependency)

## Example Output

The generated Gantt chart includes:
- Color-coded task bars
- Progress indicators
- Resource assignments
- Priority-based coloring
- Timeline grid
- Summary statistics
- Professional legend

## Dependencies

- `pandas`: Data manipulation and CSV/Excel reading
- `matplotlib`: Chart generation and visualization
- `seaborn`: Enhanced color palettes
- `numpy`: Numerical operations
- `openpyxl`: Excel file support (.xlsx)
- `xlrd`: Excel file support (.xls)

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this tool!
