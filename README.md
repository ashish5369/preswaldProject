# Glassdoor Insights

![Glassdoor Insights Logo](images/logo.png)

## Overview

Glassdoor Insights is an interactive analytics tool designed to help organizations and job seekers gain valuable insights from Glassdoor reviews and interview experiences. This application provides comprehensive analysis of employee sentiment, workplace culture, management effectiveness, and more through an intuitive web interface.

## Features

- **Sentiment Analysis**: Analyze positive and negative sentiment across company reviews
- **Topic Modeling**: Identify common themes and topics within employee reviews
- **Management Effectiveness**: Track management ratings and identify patterns in leadership feedback
- **Work-Life Balance**: Compare work-life balance metrics across companies and industries
- **Company Comparisons**: Benchmark organizations against industry standards
- **Interactive Visualizations**: Explore data through dynamic charts and graphs
- **Custom Filtering**: Filter reviews by date, location, job title, and more

## Technology Stack

- **Frontend**: Streamlit
- **Data Processing**: Python (pandas, numpy)
- **Data Visualization**: Plotly, Matplotlib, Seaborn
- **Text Analysis**: NLTK, spaCy

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/preswaldProject.git
   cd preswaldProject
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

## Configuration

The application configuration is stored in `preswald.toml`:

```toml
[project]
title = "Glassdoor Insights"
description = "An interactive tool for analyzing Glassdoor reviews and interview experiences"
version = "1.0.0"
port = 8501
slug = "glassdoor-insights"
entrypoint = "app.py"

[branding]
name = "Glassdoor Insights"
logo = "images/logo.png"
favicon = "images/favicon.ico"
primaryColor = "#6366f1"
secondaryColor = "#4f46e5"
```

## Data

The application uses Glassdoor review data stored in CSV format. The dataset includes:

- Company names
- Review dates
- Job titles
- Employee status (current/former)
- Locations
- Ratings across multiple dimensions
- Detailed review text (pros and cons)

## Key Insights

The dataset reveals several important trends about workplace environments:

1. **Management Quality**: Many reviews highlight the critical impact of management style on employee satisfaction
2. **Work-Life Balance**: A common theme across industries is the importance of flexibility and reasonable working hours
3. **Recognition**: Employees frequently mention the need for recognition and appreciation of their work
4. **Career Growth**: Opportunities for progression and development are consistently valued
5. **Compensation**: Fair pay relative to workload is a significant factor in employee satisfaction

## Usage Examples

```python
# Import the required libraries
import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
@st.cache_data
def load_data():
    return pd.read_csv("data/glassdoor_reviews.csv")

df = load_data()

# Create visualizations
st.title("Management Rating by Company")
fig = px.box(df, x="firm", y="senior_mgmt",
             title="Senior Management Ratings Distribution")
st.plotly_chart(fig)
```


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Contact

Project Link: 
