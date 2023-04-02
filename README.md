# CET-4 Test Score Visualizer

This is a Python application built with the Bottle web framework to analyze and visualize CET-4 test scores. The app allows users to upload an Excel file containing test scores and generates charts and tables to help analyze the data.

## Installation

To run this application, you need to have Python 3 installed on your machine. To install the required dependencies, run the following command in your terminal:

```
pip3 install -r requirements.txt
```

## Usage

To start the application, run the following command in your terminal:

```
python3 main.py
```

Then open your web browser and go to `http://localhost:8787`.

### Uploading a file

To upload a file, click the "Choose File" button and select the Excel file containing the test scores. Then click the "Upload" button.

### Viewing the results

After uploading the file, the app will generate several charts and tables to help you analyze the data. The following visualizations are generated:

- A pie chart showing the overall pass and fail rates for the test.
- A table showing the average score for each section of the test.
- A bar chart showing the fail rate for each section of the test.
- A bar chart showing the improvement in score for each section of the test.

To export the visualizations, you can take a screenshot of the charts and tables and save them as images, or simply drag the images to your local folder.

## About the code

The code for this application is organized as follows:

- `main.py`: the main application file containing the Bottle routes and logic for processing the uploaded file and generating the visualizations.
- `utils.py`: a separate module containing utility functions for processing the data and generating the visualizations.
- `views/`: a directory containing the HTML templates for the different pages of the application.
- `static/`: a directory containing the CSS and JavaScript files for the application.

## License

This project is licensed under the MIT License.