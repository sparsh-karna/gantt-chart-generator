#!/usr/bin/env python3
"""
Gantt Chart Generator

This script takes a CSV or Excel file as input and generates a detailed color-coded Gantt chart.
The input file should contain columns for task name, start date, end date, and optionally categories/resources.

Required columns:
- Task Name (or Task, Name)
- Start Date (or Start, Start_Date)
- End Date (or End, End_Date)

Optional columns:
- Category (for color coding)
- Resource (for grouping)
- Progress (percentage completion)
- Priority (High, Medium, Low)

Usage:
    python gantt_generator.py input_file.csv
    python gantt_generator.py input_file.xlsx
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
import numpy as np
from datetime import datetime, timedelta
import argparse
import sys
import os
from typing import Dict, List, Tuple, Optional
import seaborn as sns

class GanttGenerator:
    def __init__(self):
        # Color palette for different categories
        self.colors = [
            '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57',
            '#FF9FF3', '#54A0FF', '#5F27CD', '#00D2D3', '#FF9F43',
            '#10AC84', '#EE5A24', '#0FB9B1', '#3742FA', '#2F3542'
        ]
        self.priority_colors = {
            'High': '#E74C3C',
            'Medium': '#F39C12', 
            'Low': '#2ECC71',
            'Critical': '#8E44AD'
        }
        
    def read_data(self, file_path: str) -> pd.DataFrame:
        """Read data from CSV or Excel file"""
        file_ext = os.path.splitext(file_path)[1].lower()
        
        try:
            if file_ext == '.csv':
                df = pd.read_csv(file_path)
            elif file_ext in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_ext}")
                
            return df
        except Exception as e:
            print(f"Error reading file: {e}")
            sys.exit(1)
    
    def validate_and_clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validate and clean the input data"""
        # Normalize column names (case insensitive)
        df.columns = df.columns.str.strip()
        column_mapping = {}
        
        # Map common column name variations
        for col in df.columns:
            col_lower = col.lower()
            if col_lower in ['task', 'task name', 'task_name', 'name']:
                column_mapping[col] = 'Task Name'
            elif col_lower in ['start', 'start date', 'start_date', 'begin']:
                column_mapping[col] = 'Start Date'
            elif col_lower in ['end', 'end date', 'end_date', 'finish']:
                column_mapping[col] = 'End Date'
            elif col_lower in ['category', 'type', 'group']:
                column_mapping[col] = 'Category'
            elif col_lower in ['resource', 'assignee', 'owner']:
                column_mapping[col] = 'Resource'
            elif col_lower in ['progress', 'completion', '%']:
                column_mapping[col] = 'Progress'
            elif col_lower in ['priority', 'importance']:
                column_mapping[col] = 'Priority'
        
        df = df.rename(columns=column_mapping)
        
        # Check for required columns
        required_cols = ['Task Name', 'Start Date', 'End Date']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            print(f"Error: Missing required columns: {missing_cols}")
            print(f"Available columns: {list(df.columns)}")
            sys.exit(1)
        
        # Convert date columns
        try:
            df['Start Date'] = pd.to_datetime(df['Start Date'])
            df['End Date'] = pd.to_datetime(df['End Date'])
        except Exception as e:
            print(f"Error parsing dates: {e}")
            print("Please ensure dates are in a recognizable format (YYYY-MM-DD, MM/DD/YYYY, etc.)")
            sys.exit(1)
        
        # Add default values for optional columns
        if 'Category' not in df.columns:
            df['Category'] = 'Default'
        if 'Resource' not in df.columns:
            df['Resource'] = 'Unassigned'
        if 'Progress' not in df.columns:
            df['Progress'] = 0
        if 'Priority' not in df.columns:
            df['Priority'] = 'Medium'
        
        # Clean progress values
        df['Progress'] = pd.to_numeric(df['Progress'], errors='coerce').fillna(0)
        df['Progress'] = np.clip(df['Progress'], 0, 100)
        
        # Validate date logic
        invalid_dates = df[df['Start Date'] > df['End Date']]
        if not invalid_dates.empty:
            print("Warning: Found tasks with start date after end date:")
            print(invalid_dates[['Task Name', 'Start Date', 'End Date']])
        
        # Remove rows with missing essential data
        df = df.dropna(subset=['Task Name', 'Start Date', 'End Date'])
        
        return df
    
    def create_gantt_chart(self, df: pd.DataFrame, output_file: str = None, 
                          title: str = "Project Gantt Chart", dpi: int = 200) -> None:
        """Create and display the Gantt chart"""
        
        # Warning for large datasets
        if len(df) > 50:
            print(f"⚠️  Warning: Dataset contains {len(df)} tasks. For better visualization, ")
            print("   consider filtering data or the chart may be crowded.")
            print()
        
        # Sort by start date
        df = df.sort_values('Start Date')
        
        # Create figure and axis with proper spacing for legend
        num_tasks = len(df)
        # Conservative limits to avoid matplotlib image size errors
        fig_height = max(4, min(num_tasks * 0.25, 10))
        fig_width = 14  # Increased width to accommodate legend
        fig, ax = plt.subplots(figsize=(fig_width, fig_height))
        
        # Get unique categories and assign colors
        categories = df['Category'].unique()
        category_colors = {cat: self.colors[i % len(self.colors)] 
                          for i, cat in enumerate(categories)}
        
        # Calculate duration for each task
        df['Duration'] = (df['End Date'] - df['Start Date']).dt.days
        
        # Plot each task
        for i, (idx, task) in enumerate(df.iterrows()):
            start_date = task['Start Date']
            duration = task['Duration']
            category = task['Category']
            progress = task['Progress']
            priority = task['Priority']
            
            # Get color based on priority if available, otherwise use category
            if priority in self.priority_colors:
                bar_color = self.priority_colors[priority]
            else:
                bar_color = category_colors[category]
            
            # Create main task bar
            bar = Rectangle((mdates.date2num(start_date), i - 0.4), 
                          duration, 0.8, 
                          facecolor=bar_color, 
                          alpha=0.7,
                          edgecolor='black',
                          linewidth=0.5)
            ax.add_patch(bar)
            
            # Add progress bar if progress > 0
            if progress > 0:
                progress_width = duration * (progress / 100)
                # Create a darker shade of the same color for progress
                progress_color = bar_color if isinstance(bar_color, str) else '#2E8B57'
                progress_bar = Rectangle((mdates.date2num(start_date), i - 0.35), 
                                       progress_width, 0.7,
                                       facecolor=progress_color,
                                       alpha=0.9,
                                       edgecolor='none',  # Remove the outline
                                       linewidth=0)
                ax.add_patch(progress_bar)
                
                # Add progress text
                ax.text(mdates.date2num(start_date) + duration/2, i,
                       f'{progress:.0f}%',
                       ha='center', va='center',
                       fontsize=8, fontweight='bold',
                       color='white' if progress > 50 else 'black')
            
            # Add task name
            task_name = task['Task Name']
            if len(task_name) > 30:
                task_name = task_name[:27] + "..."
            
            ax.text(mdates.date2num(start_date) - 2, i,
                   task_name,
                   ha='right', va='center',
                   fontsize=9,
                   fontweight='bold')
            
            # Add resource info if available
            if task['Resource'] != 'Unassigned':
                ax.text(mdates.date2num(start_date) + duration + 1, i,
                       f"[{task['Resource']}]",
                       ha='left', va='center',
                       fontsize=8,
                       style='italic',
                       color='gray')
        
        # Customize the chart
        ax.set_ylim(-0.5, len(df) - 0.5)
        ax.set_yticks(range(len(df)))
        ax.set_yticklabels([])
        ax.invert_yaxis()
        
        # Set x-axis limits based on data range
        start_date = df['Start Date'].min()
        end_date = df['End Date'].max()
        # Add some padding
        padding = (end_date - start_date) * 0.05
        ax.set_xlim(start_date - padding, end_date + padding)
        
        # Format x-axis with appropriate interval based on project duration
        project_days = (end_date - start_date).days
        if project_days <= 30:
            ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
        elif project_days <= 90:
            ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
        else:
            ax.xaxis.set_major_locator(mdates.MonthLocator())
            
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_minor_locator(mdates.DayLocator(interval=7))  # Weekly minor ticks
        
        # Rotate date labels
        plt.xticks(rotation=45, ha='right')
        
        # Add grid
        ax.grid(True, linestyle='--', alpha=0.7, axis='x')
        ax.set_axisbelow(True)
        
        # Set title
        plt.title(title, fontsize=16, fontweight='bold', pad=20)
        
        # Create legend for categories
        legend_elements = []
        for category, color in category_colors.items():
            legend_elements.append(plt.Rectangle((0,0),1,1, facecolor=color, alpha=0.7, label=category))
        
        # Add priority legend if priorities are used
        if len(df['Priority'].unique()) > 1:
            for priority, color in self.priority_colors.items():
                if priority in df['Priority'].values:
                    legend_elements.append(plt.Rectangle((0,0),1,1, facecolor=color, alpha=0.7, 
                                                       label=f'{priority} Priority'))
        
        if legend_elements:
            # Place legend outside the plot area to avoid overlapping
            ax.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1.02, 0.5),
                     frameon=True, fancybox=True, shadow=True)
        
        # Add summary statistics in a better position
        total_tasks = len(df)
        completed_tasks = len(df[df['Progress'] == 100])
        avg_progress = df['Progress'].mean()
        
        stats_text = f"Total Tasks: {total_tasks}\nCompleted: {completed_tasks}\nAvg Progress: {avg_progress:.1f}%"
        # Position the stats box in top-right, outside the chart area
        ax.text(1.02, 0.98, stats_text, transform=ax.transAxes, 
               verticalalignment='top', horizontalalignment='left',
               bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8),
               fontsize=9)
        
        # Adjust layout to accommodate legend and stats box
        plt.tight_layout()
        plt.subplots_adjust(right=0.68)  # Make room for both legend and stats on the right
        
        # Save or show the chart
        try:
            if output_file:
                plt.savefig(output_file, dpi=dpi, bbox_inches='tight', 
                           facecolor='white', edgecolor='none')
                print(f"Gantt chart saved as: {output_file} (DPI: {dpi})")
            else:
                output_file = f"gantt_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                plt.savefig(output_file, dpi=dpi, bbox_inches='tight',
                           facecolor='white', edgecolor='none')
                print(f"Gantt chart saved as: {output_file} (DPI: {dpi})")
        except Exception as e:
            print(f"❌ Error saving chart at DPI {dpi}: {e}")
            print("Trying with medium resolution...")
            try:
                medium_dpi = max(120, dpi // 2)
                if not output_file:
                    output_file = f"gantt_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                plt.savefig(output_file, dpi=medium_dpi, bbox_inches='tight',
                           facecolor='white', edgecolor='none')
                print(f"Gantt chart saved as: {output_file} (DPI: {medium_dpi})")
            except Exception as e2:
                print(f"❌ Failed to save chart: {e2}")
                print("Chart displayed but not saved.")
        
        plt.close()  # Close the figure to free memory
    
    def generate_sample_data(self, output_file: str = "sample_project.csv") -> None:
        """Generate a sample CSV file for testing"""
        sample_data = {
            'Task Name': [
                'Project Planning',
                'Requirements Gathering',
                'System Design',
                'Database Setup',
                'Frontend Development',
                'Backend API Development',
                'Integration Testing',
                'User Acceptance Testing',
                'Documentation',
                'Deployment'
            ],
            'Start Date': [
                '2024-01-01', '2024-01-08', '2024-01-22', '2024-02-05',
                '2024-02-12', '2024-02-12', '2024-03-11', '2024-03-25',
                '2024-04-01', '2024-04-15'
            ],
            'End Date': [
                '2024-01-07', '2024-01-21', '2024-02-04', '2024-02-11',
                '2024-03-10', '2024-03-10', '2024-03-24', '2024-03-31',
                '2024-04-14', '2024-04-21'
            ],
            'Category': [
                'Planning', 'Analysis', 'Design', 'Development',
                'Development', 'Development', 'Testing', 'Testing',
                'Documentation', 'Deployment'
            ],
            'Resource': [
                'PM Team', 'BA Team', 'Architects', 'DB Team',
                'Frontend Team', 'Backend Team', 'QA Team', 'QA Team',
                'Tech Writers', 'DevOps Team'
            ],
            'Progress': [
                100, 100, 85, 90, 60, 70, 30, 0, 20, 0
            ],
            'Priority': [
                'High', 'High', 'High', 'Medium', 'High',
                'High', 'Medium', 'High', 'Low', 'Critical'
            ]
        }
        
        df = pd.DataFrame(sample_data)
        df.to_csv(output_file, index=False)
        print(f"Sample data generated: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Generate Gantt charts from CSV/Excel files')
    parser.add_argument('input_file', nargs='?', help='Input CSV or Excel file')
    parser.add_argument('-o', '--output', help='Output image file name')
    parser.add_argument('-t', '--title', default='Project Gantt Chart', help='Chart title')
    parser.add_argument('--dpi', type=int, default=200, help='Image resolution (DPI, default: 200)')
    parser.add_argument('--sample', action='store_true', help='Generate sample data file')
    
    args = parser.parse_args()
    
    generator = GanttGenerator()
    
    if args.sample:
        generator.generate_sample_data()
        return
    
    if not args.input_file:
        print("Error: Please provide an input file or use --sample to generate sample data")
        parser.print_help()
        sys.exit(1)
    
    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' not found")
        sys.exit(1)
    
    # Read and process data
    print(f"Reading data from: {args.input_file}")
    df = generator.read_data(args.input_file)
    
    print("Validating and cleaning data...")
    df = generator.validate_and_clean_data(df)
    
    print(f"Processing {len(df)} tasks...")
    
    # Generate chart
    generator.create_gantt_chart(df, args.output, args.title, args.dpi)

if __name__ == "__main__":
    main()
