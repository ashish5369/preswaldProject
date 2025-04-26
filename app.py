from preswald import text, plotly, connect, get_df, table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import traceback
from datetime import datetime

# Helper function to handle datetime serialization
def convert_dates_to_str(df):
    """Convert datetime columns to strings to avoid serialization issues"""
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.strftime('%Y-%m-%d')
    return df

# Application header with creative styling
text("# Glassdoor Insights Dashboard")
text("### Analysis of Employee Reviews and Work Environment")

# Load and display intro text
text("""
# 🚀 Welcome to Glassdoor Insights

This interactive dashboard analyzes Glassdoor company reviews
to help job seekers make informed decisions about potential employers.

## Dashboard Sections:
1. Company Ratings Overview
2. Work-Life Balance Analysis
3. Location and Role Analysis
""")

# Connect to our datasets
try:
    connect()
    
    # Try to load the review data
    review_df = None
    try:
        review_df = get_df('review_data')
        if review_df is not None:
            text("✅ Successfully loaded Glassdoor data")
            text(f"Available columns: {', '.join(review_df.columns)}")
    except Exception as e:
        text("⚠️ Could not load Glassdoor data: " + str(e))
    
    if review_df is not None:
        # SECTION 1: COMPANY RATINGS OVERVIEW
        text("## 1. Company Ratings Overview")
        
        try:
            # Use the specific column names from the dataset
            company_column = 'firm'
            rating_column = 'overall_rating'
            date_column = 'date_review'
            
            # Convert rating to numeric if needed
            review_df[rating_column] = pd.to_numeric(review_df[rating_column], errors='coerce')
            
            # Identify top companies with most reviews
            company_counts = review_df[company_column].value_counts()
            top_companies = company_counts.nlargest(10).index.tolist()
            
            text(f"### Top Companies by Number of Reviews")
            for i, (company, count) in enumerate(company_counts.nlargest(10).items(), 1):
                text(f"{i}. {company}: {count} reviews")
            
            # Filter for top companies
            filtered_df = review_df[review_df[company_column].isin(top_companies)]
            
            # Rating distribution by company
            fig = px.box(
                filtered_df,
                x=company_column,
                y=rating_column,
                color=company_column,
                title='Rating Distribution by Top Companies',
                labels={
                    rating_column: 'Overall Rating',
                    company_column: 'Company'
                }
            )
            fig.update_layout(template='plotly_white')
            plotly(fig)
            
            # Display average ratings
            avg_ratings = filtered_df.groupby(company_column)[rating_column].agg(['mean', 'count']).reset_index()
            avg_ratings.columns = [company_column, 'Average Rating', 'Number of Reviews']
            avg_ratings['Average Rating'] = avg_ratings['Average Rating'].round(1)
            
            fig = px.bar(
                avg_ratings,
                x=company_column,
                y='Average Rating',
                text='Average Rating',
                color='Average Rating',
                title='Average Ratings by Company',
                hover_data=['Number of Reviews'],
                labels={
                    'Average Rating': 'Average Rating (1-5)',
                    company_column: 'Company',
                },
                color_continuous_scale='Viridis'
            )
            fig.update_layout(template='plotly_white')
            plotly(fig)
            
            # Create scatter plot of ratings over time
            try:
                review_df[date_column] = pd.to_datetime(review_df[date_column], errors='coerce')
                # Filter out rows with invalid dates
                valid_dates_df = review_df[~review_df[date_column].isna()].copy()
                
                # Group by company and date (month) for a cleaner trend line
                valid_dates_df['month_year'] = valid_dates_df[date_column].dt.strftime('%Y-%m')
                monthly_avg = valid_dates_df.groupby([company_column, 'month_year']).agg({
                    rating_column: 'mean'
                }).reset_index()
                
                # Only show top 5 companies to avoid overcrowding
                top5_companies = company_counts.nlargest(5).index.tolist()
                monthly_trend = monthly_avg[monthly_avg[company_column].isin(top5_companies)]
                
                fig = px.line(
                    monthly_trend,
                    x='month_year',
                    y=rating_column,
                    color=company_column,
                    title='Rating Trends Over Time',
                    labels={
                        rating_column: 'Average Rating',
                        'month_year': 'Month-Year',
                        company_column: 'Company'
                    },
                    markers=True
                )
                fig.update_layout(
                    template='plotly_white',
                    xaxis={'tickangle': 45}
                )
                plotly(fig)
                
                text("""
                ### Rating Trends Analysis:
                - Monitor how company ratings have changed over time
                - Identify companies with improving or declining employee satisfaction
                - Consider the trajectory of ratings when evaluating potential employers
                """)
            except Exception as e:
                text(f"Note: Couldn't analyze review dates: {str(e)}")
            
        except Exception as e:
            text(f"⚠️ Error analyzing rating data: {str(e)}")
            traceback.print_exc()

        # SECTION 2: WORK-LIFE BALANCE ANALYSIS
        text("## 2. Work-Life Balance Analysis")
        
        try:
            # Use the specific work-life balance column from the dataset
            wlb_column = 'work_life_balance'
            
            # Convert to numeric if needed
            review_df[wlb_column] = pd.to_numeric(review_df[wlb_column], errors='coerce')
            
            # Display statistical summary
            wlb_stats = review_df.groupby(company_column)[wlb_column].agg(['mean', 'median', 'std', 'count']).reset_index()
            wlb_stats.columns = [company_column, 'Average', 'Median', 'Std Dev', 'Count']
            wlb_stats['Average'] = wlb_stats['Average'].round(1)
            wlb_stats['Median'] = wlb_stats['Median'].round(1)
            wlb_stats['Std Dev'] = wlb_stats['Std Dev'].round(1)
            
            # Filter for top companies with sufficient data
            wlb_stats_filtered = wlb_stats[wlb_stats['Count'] >= 5].sort_values('Average', ascending=False)
            
            if len(wlb_stats_filtered) > 0:
                text("### Work-Life Balance Rankings")
                for i, row in wlb_stats_filtered.head(10).iterrows():
                    text(f"{i+1}. {row[company_column]}: {row['Average']}/5.0 (based on {row['Count']} reviews)")
            
            # Compare work-life balance across companies
            fig = px.box(
                filtered_df,
                x=company_column,
                y=wlb_column,
                color=company_column,
                title='Work-Life Balance by Company',
                labels={
                    wlb_column: 'Work-Life Balance Rating',
                    company_column: 'Company'
                }
            )
            fig.update_layout(template='plotly_white')
            plotly(fig)
            
            # Compare overall rating vs work-life balance
            fig = px.scatter(
                filtered_df,
                x=wlb_column,
                y=rating_column,
                color=company_column,
                size=rating_column,
                hover_data=[company_column, 'job_title'],
                title='Work-Life Balance vs. Overall Rating',
                labels={
                    wlb_column: 'Work-Life Balance Rating',
                    rating_column: 'Overall Rating',
                    company_column: 'Company'
                }
            )
            fig.update_layout(template='plotly_white')
            plotly(fig)
            
            # Add a simple scatter plot without trendline (since statsmodels is missing)
            # Calculate correlation manually
            correlation = review_df[[wlb_column, rating_column]].dropna().corr().iloc[0,1]
            corr_text = f"Correlation coefficient: {correlation:.2f}"
            
            # Create a scatter plot without trendline
            wlb_df = review_df[[wlb_column, rating_column]].dropna().copy()
            wlb_df['count'] = 1
            wlb_count = wlb_df.groupby([wlb_column, rating_column]).count().reset_index()
            
            fig = px.scatter(
                wlb_count,
                x=wlb_column,
                y=rating_column,
                size='count',
                title=f'Correlation: Work-Life Balance vs. Overall Rating<br>{corr_text}',
                labels={
                    wlb_column: 'Work-Life Balance Rating',
                    rating_column: 'Overall Rating',
                    'count': 'Number of Reviews'
                },
                opacity=0.7
            )
            fig.update_layout(template='plotly_white')
            plotly(fig)
            
            text("""
            ### Key Insights:
            - Companies with higher work-life balance tend to have higher overall ratings
            - Consider prioritizing companies with consistent (less variable) work-life balance scores
            - The size of each bubble represents the number of reviews with that specific rating combination
            """)
            
        except Exception as e:
            text(f"⚠️ Error analyzing work-life balance data: {str(e)}")
            traceback.print_exc()
        
        # SECTION 3: LOCATION AND ROLE ANALYSIS
        text("## 3. Location and Role Analysis")
        
        try:
            # Analyze ratings by location
            location_column = 'location'
            job_title_column = 'job_title'
            current_column = 'current'
            
            # Location analysis
            if location_column in review_df.columns:
                # Extract city or region from location
                def extract_city(location_str):
                    if not isinstance(location_str, str):
                        return "Unknown"
                    parts = location_str.split(',')
                    if len(parts) > 0:
                        return parts[0].strip()
                    return location_str
                
                review_df['city'] = review_df[location_column].apply(extract_city)
                
                # Get top locations
                location_counts = review_df['city'].value_counts()
                top_locations = location_counts.nlargest(15).index.tolist()
                
                # Average ratings by location
                location_ratings = review_df[review_df['city'].isin(top_locations)].groupby('city').agg({
                    rating_column: ['mean', 'count'],
                    wlb_column: 'mean'
                }).reset_index()
                
                location_ratings.columns = ['City', 'Average Rating', 'Number of Reviews', 'Work-Life Balance']
                location_ratings = location_ratings.sort_values('Average Rating', ascending=False)
                
                fig = px.bar(
                    location_ratings,
                    x='City',
                    y='Average Rating',
                    text='Average Rating',
                    color='Work-Life Balance',
                    hover_data=['Number of Reviews'],
                    title='Average Ratings by Location',
                    labels={
                        'Average Rating': 'Overall Rating',
                        'City': 'City/Region',
                        'Work-Life Balance': 'Work-Life Balance'
                    },
                    color_continuous_scale='Viridis'
                )
                fig.update_layout(template='plotly_white')
                plotly(fig)
            
            # Job title analysis
            if job_title_column in review_df.columns:
                # Get top job titles
                job_counts = review_df[job_title_column].value_counts()
                top_jobs = job_counts.nlargest(10).index.tolist()
                
                # Average ratings by job title
                job_ratings = review_df[review_df[job_title_column].isin(top_jobs)].groupby(job_title_column).agg({
                    rating_column: ['mean', 'count'],
                    wlb_column: 'mean'
                }).reset_index()
                
                job_ratings.columns = ['Job Title', 'Average Rating', 'Number of Reviews', 'Work-Life Balance']
                job_ratings = job_ratings.sort_values('Average Rating', ascending=False)
                
                fig = px.bar(
                    job_ratings,
                    x='Job Title',
                    y=['Average Rating', 'Work-Life Balance'],
                    barmode='group',
                    title='Ratings by Job Title',
                    labels={
                        'value': 'Rating (1-5)',
                        'Job Title': 'Job Title',
                        'variable': 'Rating Type'
                    }
                )
                fig.update_layout(template='plotly_white')
                plotly(fig)
            
            # Current vs Former Employee Analysis
            if current_column in review_df.columns:
                # Create a simplified current employee marker
                def simplify_current(status):
                    if not isinstance(status, str):
                        return "Unknown"
                    if "current" in status.lower():
                        return "Current Employee"
                    elif "former" in status.lower():
                        return "Former Employee"
                    else:
                        return "Unknown"
                
                review_df['employment_status'] = review_df[current_column].apply(simplify_current)
                
                # Compare ratings between current and former employees
                status_ratings = review_df.groupby('employment_status').agg({
                    rating_column: ['mean', 'count'],
                    wlb_column: 'mean'
                }).reset_index()
                
                status_ratings.columns = ['Status', 'Average Rating', 'Count', 'Work-Life Balance']
                
                fig = px.bar(
                    status_ratings[status_ratings['Status'] != "Unknown"],
                    x='Status',
                    y=['Average Rating', 'Work-Life Balance'],
                    barmode='group',
                    title='Current vs. Former Employee Ratings',
                    text='Count',
                    labels={
                        'value': 'Rating (1-5)',
                        'Status': 'Employment Status',
                        'variable': 'Rating Type'
                    }
                )
                fig.update_layout(template='plotly_white')
                plotly(fig)
                
                text("""
                ### Current vs. Former Employee Analysis:
                - Comparing ratings between current and former employees can reveal potential bias
                - Significant differences may indicate changing company culture or conditions
                - Former employees often provide more critical feedback
                """)
            
        except Exception as e:
            text(f"⚠️ Error analyzing location and role data: {str(e)}")
            traceback.print_exc()
        
        # DATA EXPLORER SECTION
        text("## Raw Data Explorer")
        text("Sample of the Glassdoor reviews data (first 20 rows):")
        
        # Convert all datetime columns to strings to avoid serialization issues
        display_df = review_df.head(20).copy()
        display_df = convert_dates_to_str(display_df)
        table(display_df)
            
    else:
        text("## ⚠️ No Data Available")
        text("Please check your data source configuration in preswald.toml")
        
except Exception as e:
    text("## ⚠️ Error Loading Data")
    text(f"An error occurred: {str(e)}")
    text("Please check your data source configuration in preswald.toml")
    traceback.print_exc()