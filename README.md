# AI Data Analyst Assistant

A fun side project exploring whether AI can actually do the job of a junior data analyst.

## Why I Built This

We keep hearing about AI replacing jobs, and data analysis seems like an obvious target. But when I tried current Data Analyst tools of ChatGPT or LeChat for real data work, they're pretty far from doing the job. Still, they're improving fast, so I wanted to see for myself: could an AI agent realistically replace a talented junior data analyst in a few years?

**My take after building this: Probably yes, but there are some real structural problems to solve first.**

## What I Learned

Here's something that surprised me: data analysis doesn't really have systematic methods. You'd think for such an important business function, there would be clear frameworks for questions like "what's driving our revenue changes?" But no - most analysis still comes down to intuition, business knowledge, and experience.

So I decided to write down some basic methods that could be used consistently:
- **Describe additive metric evolution** - Understanding how sum-based metrics change over time
- **Explain additive metric evolution** - Identifying drivers behind those changes  
- **Describe ratio metric evolution** - Analyzing percentage and rate-based metrics
- **Explain ratio metric evolution** - Uncovering causes of ratio changes

These are pretty simple, but they actually cover a huge chunk of the analysis work that most companies need.

## Testing It Out

I tested my agent on the same dataset I used for a live data analysis interview at Onfido. The results were genuinely impressive - it performed like a competent junior analyst would.

## Where This Could Go Next

If I wanted to take this further, here's what I'd work on:

**More Analysis Types:**
- Finding anomalies and weird patterns
- Correlation analysis
- Seasonality detection  
- Revenue breakdowns (is it price changes or volume changes?)

**Real-World Implementation Issues:**
- **Beyond CSV files**: DA Agent will ultimately be connected directly to company data warehouses
- **Trust and accuracy**: How do you make sure the AI isn't making mistakes when manipulating the data? AI needs guidance from data catalogs, semantic layers, etc.
- **Business context**: Where / how do you build all the company-specific knowledge the AI needs?
- **Scale problems**: LLMs don't handle (hundred of) millions of rows efficiently or cheaply. Some data techniques need to be implemented to solve this.

The models will keep getting better, but some of these challenges - especially around processing massive datasets cost-effectively - are going to stick around for a while.


## Overview

This repository contains an AI-powered data analysis agent that can perform systematic data analysis tasks typically handled by junior data analysts. The agent implements structured analytical methods to analyze and explain metric evolutions in datasets.

## Features

- **Systematic Analytical Methods**:
  - Additive metric evolution analysis
  - Ratio metric evolution analysis
  - Metric driver analysis
  - Trend identification and explanation

## LLM

I used Anthropic API for this project but feel free to use any other model provider as Langchain integration greatly enables LLM interoperability.

## Requirements

- Python 3.8+
- Anthropic API key, or any other LLM key. You will have to adapt the LLM client (see Langchain documentation)
- Required Python packages (see `requirements.txt`):
  - pandas
  - numpy
  - openai
  - python-dotenv
  - matplotlib
  - seaborn

## Installation

Clone the repository:
```bash
git clone https://github.com/yourusername/data_analyst_agent.git
cd data_analyst_agent
```

Then create `.env` file and add your Anthropic API key:
```
my_anthropic_api=your_api_key_here
```

## Usage

1. Place your CSV data file in the `data` directory
2. Run the analysis:
```bash
python src/main.py --csv_path 'data/dataset.csv' --question 'Explain the main driver of the evolution of the tat_2_minutes (nb_reports_2_minutes / nb_reports)'
```
## Result

You can find the output of the above command in the outputs/results.html file.





