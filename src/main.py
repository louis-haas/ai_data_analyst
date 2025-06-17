from analytics_tasks import describe_ratio_metric_evolution, describe_volume_metric_evolution, explain_ratio_metric_evolution, explain_volume_metric_evolution
from functions import select_analytics_methods, combine_findings, prepare_html_blocks, build_html_content, open_html_content
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--csv_path', type=str)
parser.add_argument('--question', type=str)
args = parser.parse_args()

question = args.question
csv_path = args.csv_path

if question == None or csv_path == None:

    print("You need to input both a question and a csv path.")

else:

    findings = []
    plots = []
    methods = select_analytics_methods(question)


    if methods == []:
        print("I am sorry, but there is currently no available analytical methods that can help answering your question.")

    if "describe_volume_metric_evolution" in methods:
        finding, plot = describe_volume_metric_evolution(csv_path, question)
        findings += finding
        plots += plot

    if "explain_volume_metric_evolution" in methods:
        finding, plot = explain_volume_metric_evolution(csv_path, question)
        findings += finding
        plots += plot

    if "describe_ratio_metric_evolution" in methods:
        finding, plot = describe_ratio_metric_evolution(csv_path, question)
        findings += finding
        plots += plot

    if "explain_ratio_metric_evolution" in methods:
        finding, plot = explain_ratio_metric_evolution(csv_path, question)
        findings += finding
        plots += plot

    executive_summary = combine_findings(findings, question)

    html_blocks_data = prepare_html_blocks(question, executive_summary, findings, plots)

    build_html_content('outputs/template.html', html_blocks_data)

    open_html_content('outputs/results.html')



