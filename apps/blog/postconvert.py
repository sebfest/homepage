import nbformat

from urllib.request import urlopen
from nbconvert.exporters import HTMLExporter
from nbconvert.writers import FilesWriter
from traitlets.config import Config


url = 'http://jakevdp.github.com/downloads/notebooks/XKCD_plots.ipynb'
response = urlopen(url).read().decode()
jake_notebook = nbformat.reads(response, as_version=4)

c = Config()
c.HTMLExporter.preprocessors = [
    'nbconvert.preprocessors.ExtractOutputPreprocessor',
    'nbconvert.preprocessors.ClearMetadataPreprocessor',
]

html_exporter = HTMLExporter(config=c)
html_exporter.template_file = 'basic'
html_file, html_recources = html_exporter.from_notebook_node(jake_notebook)

with open('notebook.html', 'w') as my_html:
    my_html.write(html_file)

all_figures = html_recources.get('outputs', {})
for filename, data in all_figures.items():
    with open(filename, 'wb') as figure:
        figure.write(data)


file_writer = FilesWriter()
file_writer.write(html_file, html_recources, notebook_name="whatever-notebook-name-you-desire")

