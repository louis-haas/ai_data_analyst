analytics_methods = {
    "describe_additive_metric_evolution": 
        
        {"sql_plan": 
            """
    
            Create a time series plot showing the additive metric's evolution.
            
            **SQL Template:**
            ```sql
            SELECT time_dimension, SUM(additive_metric) AS additive_metric 
            FROM data_table
            GROUP BY time_dimension
            ORDER BY time_dimension
            ```

            """, 

         "analytical_plan" : 
            """
            1. Identify significant changes in the additive metrics
            2. Quantify the magnitude of key changes (both in absolute and relative values)
            """,

        "plot_guideline":
            """
            Plot the evolution of the {additive metric} with a line chart .

            Coding Rules: 
            1. Create only ONE relevant plot and assign the plotly figure to a variable named `result`. Don't show the plot.
            2. Set width=900, height=600. 
            3. Add title.
            4. Show legend below the plot (legend=dict(orientation="h",yanchor="top", y=-0.1, xanchor="center", x=0.5))
            5. Use the actual names of fields of df_task, not generic terms like {additive metric}.
            """
        },
    
    "explain_additive_metric_evolution":
        
        {"sql_plan": 
            """
    
            Create a time series plot with the additive metric broken down by categorical dimension
            
            **SQL Template:**
            ```sql
            SELECT time_dimension, categorical_dimension, SUM(additive_metric) AS additive_metric 
            FROM data_table
            GROUP BY time_dimension, categorical_dimension
            ORDER BY time_dimension, categorical_dimension
            ```

            """, 

         "analytical_plan" : 
            """
            1. Analyze how different categories contribute to overall additive metric changes

            """,

        "plot_guideline":
            """
            Plot the evolution of the {additive metric} by category with a line chart.

            Coding Rules: 
            1. Create only ONE relevant plot and assign the plotly figure to a variable named `result`. Don't show the plot.
            2. Set width=900, height=600. 
            3. Add title.
            4. Show legend below the plot (legend=dict(orientation="h",yanchor="top", y=-0.1, xanchor="center", x=0.5))
            5. Use the actual names of fields of df_task, not generic terms like {additive metric}.
            """
        },

    "describe_ratio_metric_evolution": 
        
        {"sql_plan": 
            """
    
            Create a time series plot showing the ratio metric's evolution
            
            **SQL Template:**
            ```sql
            SELECT time_dimension, SUM(metric_1) / SUM(metric_2) AS ratio_metric 
            FROM data_table
            GROUP BY time_dimension
            ORDER BY time_dimension
            ```

            """, 

         "analytical_plan" : 
            """
            1. Identify significant changes in the ratio metric
            2. Quantify the magnitude of key changes (in percentage points)

            """,

        "plot_guideline":
            """
            Plot the evolution of the {ratio metric} with a line chart.

            Coding Rules: 
            1. Create only ONE relevant plot and assign the plotly figure to a variable named `result`. Don't show the plot.
            2. Set width=900, height=600. 
            3. Add title.
            4. Show legend below the plot (legend=dict(orientation="h",yanchor="top", y=-0.1, xanchor="center", x=0.5))
            5. Use the actual names of fields of df_task, not generic terms like {ratio metric}.
            """
        }, 

    "explain_ratio_metric_evolution":
        
        {"sql_plan": 
            """
    
            Plot the time serie, broken down by a dimension "categorical_dimension", of:
                - the {ratio metric} ({metric_1} / {metric_2})
                - and the contribution {metric_2} to the periodic total of {metric_2}
            
            **SQL Template:**
            ```sql
            WITH total_volume AS (
                SELECT time_dimension, SUM(metric_2) AS total_metric_2
                FROM data_table
                GROUP BY time_dimension
            )

            SELECT 
                data_table.time_dimension, 
                data_table.categorical_dimension,
                ROUND(SUM(data_table.metric_2) / AVG(total_volume.total_metric_2), 3) AS volume_contribution,
                SUM(data_table.metric_1) / SUM(data_table.metric_2) AS ratio_metric
            FROM data_table
            LEFT JOIN total_volume ON data_table.time_dimension = total_volume.time_dimension
            GROUP BY data_table.time_dimension, data_table.categorical_dimension
            ORDER BY data_table.time_dimension, data_table.categorical_dimension
            ```

            **Coding Rule:**
            Use the actual names of fields of your dataset, not generic terms like "ratio metric," "metric_1,", "metric_2", etc


            """, 

         "analytical_plan" : 
            """
            1. Analyze:
            - Performance effect: What is the evolution of the ratio metric per category?
            - Mix effect: How does the contribution of each category to the overall volume evolve over time?
            2. Assess the contribution of each category to the overall ratio metric changes by combining the performance effect and mix effect analysis
            """,

        "plot_guideline":

            """
            Use side by side subplots (fig = make_subplots(rows=1, cols=2)) to plot:
               1. Plot the evolution of the {ratio metric} by category with a line chart.
               2. Plot the evolution of the volume contribution by category with another line chart. 
            
            Coding Rules: 
            1. Create only ONE relevant plot and assign the plotly figure to a variable named `result`. Don't show the plot.
            2. Set width=900, height=600. by using fig.update_layout(height=600, width=800)
            3. Add title with a smaller police to the subplots. NO title for the chart.
            4. Show legend below the plot (legend=dict(orientation="h",yanchor="top", y=-0.1, xanchor="center", x=0.5))
            5. Use the actual names of fields of df_task, not generic terms like {ratio metric}.


            """
        }
}

