
from functions import init_duckdb, summarize_dataframe, write_sql_query, run_sql_query, perform_analytical_task, write_code_to_plot_chart, list_fields, how_calculate_ratio_metric, execute_chart_code
from analytics_methods import analytics_methods


def describe_volume_metric_evolution(csv_path: str, question: str):
    
    connection, df = init_duckdb(csv_path)

    sql_query = write_sql_query(df, analytics_methods['describe_volume_metric_evolution']['sql_plan'])

    df_task = run_sql_query(connection, sql_query)

    findings = [perform_analytical_task(question, analytics_methods['describe_volume_metric_evolution']['analytics_plan'], df_task)]

    code = write_code_to_plot_chart(analytics_methods['describe_volume_metric_evolution']['plot_guideline'],df_task)
    
    result = execute_chart_code(code, df_task)

    result.write_image("outputs/plot_method1.png") 

    plots = ["plot_method1.png"]

    return findings, plots



def describe_ratio_metric_evolution(csv_path: str, question: str):
    
    connection, df = init_duckdb(csv_path)

    df_summary = summarize_dataframe(df)
    
    how_ratio_metric = how_calculate_ratio_metric(question, df_summary)

    sql_query = write_sql_query(df, analytics_methods['describe_ratio_metric_evolution']['sql_plan'] + f'{how_ratio_metric}')

    df_task = run_sql_query(connection, sql_query)

    findings = [perform_analytical_task(question, analytics_methods['describe_ratio_metric_evolution']['analytical_plan'], df_task)]
    
    code = write_code_to_plot_chart(analytics_methods['describe_ratio_metric_evolution']['plot_guideline'],df_task)

    result = execute_chart_code(code, df_task)

    result.write_image("outputs/plot_method2.png")
    
    plots = ["plot_method2.png"]

    return findings, plots
      

def explain_volume_metric_evolution(csv_path: str, question: str):
    
    connection, df = init_duckdb(csv_path)

    df_summary = summarize_dataframe(df)

    categorical_dimensions = list_fields(df_summary, 'categorical dimension')

    findings = []
    plots = []

    for i, dimension in enumerate(categorical_dimensions):

        sql_query = write_sql_query(df, analytics_methods['explain_volume_metric_evolution']['sql_plan'] + f'. Use the following dimension: {dimension}')

        df_task = run_sql_query(connection, sql_query)

        findings.append(perform_analytical_task(question, analytics_methods['explain_volume_metric_evolution']['analytical_plan'], df_task))
                
        code = write_code_to_plot_chart(analytics_methods['explain_volume_metric_evolution']['plot_guideline'],df_task)
        
        result = execute_chart_code(code, df_task)
        
        result.write_image("outputs/plot_method3_{0}.png".format(i))

        plots = ["plot_method3_{0}.png".format(i)]
   
    return findings, plots
      

def explain_ratio_metric_evolution(csv_path: str, question: str):
    
    connection, df = init_duckdb(csv_path)

    df_summary = summarize_dataframe(df)

    categorical_dimensions = list_fields(df_summary, 'categorical dimension')

    findings = []
    plots = []

    how_ratio_metric = how_calculate_ratio_metric(question, df_summary)

    for i, dimension in enumerate(categorical_dimensions):

        sql_query = write_sql_query(df, analytics_methods['explain_ratio_metric_evolution']['sql_plan']  + f'. Use the following categorical dimension: {dimension}. {how_ratio_metric}')

        df_task = run_sql_query(connection, sql_query)

        findings.append(perform_analytical_task(question, analytics_methods['explain_ratio_metric_evolution']['analytical_plan'], df_task))
        
        code = write_code_to_plot_chart(analytics_methods['explain_ratio_metric_evolution']['plot_guideline'],df_task)
        
        result = execute_chart_code(code, df_task)
        
        result.write_image("outputs/plot_method4_{0}.png".format(i))
        
        plots = ["plot_method4_{0}.png".format(i)]
    
    return findings, plots


