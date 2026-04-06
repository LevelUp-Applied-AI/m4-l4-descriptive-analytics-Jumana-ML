"""Lab 4 — Descriptive Analytics: Student Performance EDA

Conduct exploratory data analysis on the student performance dataset.
Produce distribution plots, correlation analysis, hypothesis tests,
and a written findings report.

Usage:
    python eda_analysis.py
"""
import os
import pandas as pd
import numpy as np
import matplotlib
# Use 'Agg' backend to safely generate and save plots in the background without opening GUI windows
matplotlib.use("Agg") 
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


def load_and_profile(filepath):
    """Load the dataset and generate a data profile report."""
    print("--- Loading Data and Profiling ---")
    
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(filepath)
    df = df.copy()
    
    # Calculate dataset dimensions and missing values percentage
    rows, cols = df.shape
    missing_counts = df.isna().sum()
    missing_pct = (missing_counts / len(df)) * 100
    
    # Ensure the output directory exists before saving files
    os.makedirs('output', exist_ok=True)
    
    # 1. Write the Data Profile to a text file
    with open('output/data_profile.txt', 'w', encoding='utf-8') as f:
        f.write("=== Data Profile Report ===\n\n")
        
        # Document dataset shape
        f.write(f"1. Shape:\n- Rows: {rows}\n- Columns: {cols}\n\n")
        
        # Document data types for each column
        f.write("2. Data Types:\n")
        f.write(df.dtypes.to_string() + "\n\n")
        
        # Document missing values
        f.write("3. Missing Values (Count and Percentage):\n")
        for col in df.columns:
            f.write(f"- {col}: {missing_counts[col]} missing ({missing_pct[col]:.2f}%)\n")
            
        # Document cleaning decisions and statistical reasoning
        f.write("\n4. Handling Decisions and Reasoning:\n")
        f.write("- commute_minutes: Impute with median. \n")
        f.write("  Reasoning: It has ~10% missing values. Dropping 10% of the data might lead to loss of valuable information. We use the median instead of the mean because commute times can have outliers (e.g., extremely long commutes), and the median is robust to outliers.\n\n")
        
        f.write("- study_hours_weekly: Drop missing rows. \n")
        f.write("  Reasoning: It has ~5% missing values (which is a small percentage). Since it is roughly Missing Completely At Random (MCAR), dropping these few rows will not significantly affect the dataset's statistical power.\n")

    # 2. Execute Data Cleaning
    # Fill missing commute times with the median value to resist outliers
    commute_median = df['commute_minutes'].median()
    df['commute_minutes'] = df['commute_minutes'].fillna(commute_median)
    
    # Fill missing scholarships with 'None' assuming they represent self-funded students
    df['scholarship'] = df['scholarship'].fillna('None')
    
    # Drop rows where study_hours_weekly is missing to preserve correlation validity
    df = df.dropna(subset=['study_hours_weekly'])
    
    return df


def plot_distributions(df):
    """Create distribution plots for key numeric variables."""
    print("--- Generating Distribution Plots ---")
    os.makedirs('output', exist_ok=True)

    # 1. Plot the distribution of GPAs using a histogram with a Kernel Density Estimate (KDE) line
    plt.figure(figsize=(10, 6))    
    sns.histplot(df['gpa'], kde=True, color='skyblue')
    plt.title('Distribution of Student GPAs (Left-Skewed)', fontsize=14)
    plt.xlabel('GPA (0.0 - 4.0)', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.savefig('output/gpa_distribution.png', bbox_inches='tight') # ALWAYS Save BEFORE close
    plt.close()

    # 2. Compare GPA across Internship statuses using a Boxplot
    plt.figure(figsize=(10, 6))
    sns.boxplot(
        data=df, 
        x='has_internship', 
        y='gpa', 
        hue='has_internship', 
        palette='Set2', 
        legend=False
    )
    plt.title('GPA Comparison by Internship Status', fontsize=14)
    plt.xlabel('Currently has Internship?', fontsize=12)
    plt.ylabel('GPA', fontsize=12)
    plt.savefig('output/internship_vs_gpa.png', bbox_inches='tight')
    plt.close()

    # 3. Use a dynamic loop to generate and save histograms for the remaining numeric columns
    numeric_cols = ['study_hours_weekly', 'attendance_pct', 'commute_minutes', "course_load"]
    for col in numeric_cols:
        plt.figure(figsize=(10, 6))
        sns.histplot(df[col].dropna(), kde=True, color='#34495e', bins=30)
        plt.title(f'Distribution of {col.replace("_", " ").title()}', fontsize=14)
        plt.xlabel(col.replace("_", " ").title(), fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.savefig(f'output/{col}_distribution.png', bbox_inches='tight')
        plt.close()


def plot_correlations(df):
    """Analyze and visualize relationships between numeric variables."""
    print("--- Generating Correlation Analysis ---")
    
    # Isolate numeric columns to prevent errors when calculating correlations
    numeric_cols = df.select_dtypes(include=[np.number]).drop(columns=['student_id'], errors='ignore')
    
    # Calculate Pearson correlation matrix
    corr_matrix = numeric_cols.corr(method='pearson')
    
    # 1. Create and save a Heatmap visualization of the correlation matrix
    plt.figure(figsize=(12, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", center=0, linewidths=0.5)
    plt.title('Pearson Correlation Matrix: HTU Student Features', fontsize=16)
    plt.savefig('output/pearson_correlation.png', bbox_inches='tight')
    plt.close()

    # Extract the top 2 highest correlated pairs mathematically (excluding self-correlation)
    sol = (corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)).stack().sort_values(ascending=False))
    top_pairs = sol.head(2)
    print("\n--- Top 2 Correlated Pairs ---")
    print(top_pairs)

    # 2. Create a scatter plot with a regression line for the strongest relationship (Study Hours vs GPA)
    plt.figure(figsize=(10, 6))
    sns.regplot(data=df, x='study_hours_weekly', y='gpa', scatter_kws={'alpha':0.4}, line_kws={'color':'red'})
    plt.title('Correlation: Weekly Study Hours vs. GPA', fontsize=14)
    plt.xlabel('Study Hours Per Week', fontsize=12)
    plt.ylabel('GPA', fontsize=12)
    plt.savefig('output/study_hours_vs_gpa.png', bbox_inches='tight')
    plt.close()

    # 3. Create a boxplot showing the impact of Department on GPA (Fixed: Added savefig)
    plt.figure(figsize=(10, 6)) # Added figure size to prevent overlapping
    sns.boxplot(
        data=df, 
        x='department', 
        y='gpa', 
        hue='department', 
        palette='Pastel1', 
        legend=False
    )
    plt.title('Impact of department on Student GPA', fontsize=14)
    plt.xlabel('Department', fontsize=12)
    plt.ylabel('GPA', fontsize=12)
    plt.savefig('output/department_vs_gpa.png', bbox_inches='tight') # Saved the plot successfully
    plt.close() # Closed the plot safely


def run_hypothesis_tests(df):
    """Run statistical tests to validate observed patterns."""
    print("\n--- Running Hypothesis Tests ---")
    
    # 1. Independent T-Test: Compare GPA between students with and without internships
    # Isolate the two groups
    gpa_intern = df[df['has_internship'] == 'Yes']['gpa'].dropna()
    gpa_no_intern = df[df['has_internship'] == 'No']['gpa'].dropna()
    
    # Perform Welch's t-test (equal_var=False handles unequal variances better)
    t_stat, p_value = stats.ttest_ind(gpa_intern, gpa_no_intern, equal_var=False)
    
    # Calculate Cohen's d to measure the actual "Effect Size" of having an internship
    n1, n2 = len(gpa_intern), len(gpa_no_intern)
    s1, s2 = np.var(gpa_intern, ddof=1), np.var(gpa_no_intern, ddof=1)
    pooled_std = np.sqrt(((n1 - 1) * s1 + (n2 - 1) * s2) / (n1 + n2 - 2))
    cohen_d = (np.mean(gpa_intern) - np.mean(gpa_no_intern)) / pooled_std
    
    # Output Results for Hypothesis 1
    print("--- Hypothesis Test: Internship vs GPA ---")
    print(f"t-statistic: {t_stat:.4f}, p-value: {p_value:.4f}, Cohen's d: {cohen_d:.4f}")
    
    if p_value < 0.05:
        print("Interpretation: There is a statistically significant difference in GPA between students with and without internships.")
        if cohen_d > 0:
            print("Effect Size: The positive Cohen's d indicates that students with internships tend to have higher GPAs.")
        else:            
            print("Effect Size: The negative Cohen's d indicates that students without internships tend to have higher GPAs.")
    else:     
        print("Interpretation: There is no statistically significant difference in GPA between students with and without internships.")  

    # 2. Chi-Squared Test: Check if scholarship types are biased toward specific departments
    # Create a cross-tabulation table linking scholarships and departments
    contingency_table = pd.crosstab(df['scholarship'], df['department'])
    
    # Execute the Chi-Squared test
    chi2_stat, chi2_p, dof, expected = stats.chi2_contingency(contingency_table)
    
    # Output Results for Hypothesis 2
    print("\n--- Hypothesis Test: Scholarship vs Department ---")
    print(f"Chi-squared statistic: {chi2_stat:.4f}, p-value: {chi2_p:.4f}")
    
    if chi2_p < 0.05:
        print("Interpretation: There is a statistically significant association between scholarship status and department.")
        print("This suggests that certain departments may have higher scholarship rates, which could be due to departmental funding policies or student demographics.")
    else:
        print("Interpretation: There is no statistically significant association between scholarship status and department.\n")


def main():
    """Orchestrate the full EDA pipeline."""
    # This acts as the main controller that executes all functions in logical order
    
    # Ensure the output directory exists
    os.makedirs("output", exist_ok=True)
    filepath = os.path.join('data', 'student_performance.csv')

    # Step 1: Load data, profile it, and clean missing values
    df = load_and_profile(filepath)

    # Step 2: Generate and save univariate distribution plots
    plot_distributions(df)

    # Step 3: Analyze correlations and save bivariate relationship plots
    plot_correlations(df)

    # Step 4: Run statistical Math Tests to prove/disprove hypotheses
    run_hypothesis_tests(df)
    
    # Print success message to terminal
    print("✅ EDA Analysis Complete! Please check the 'output' folder for your generated charts and text profile.")


# Standard Python construct to ensure main() runs only when script is executed directly
if __name__ == "__main__":
    main()