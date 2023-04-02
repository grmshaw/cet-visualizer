<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>CET-4 Visualization</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="shortcut icon" type="image/x-icon" href="/static/favicon.png">
    <link rel="stylesheet" href="/static/visual.css">
</head>
<body>
    <div class="analysis">
        <h2>{{result['classname']}}</h2>
        {{!result['analysis_text']}}
    </div>
    <hr>
    <div>
        <img src="data:image/png;base64,{{result['overall_rate_piechart']}}">
    </div>
    <hr>
    <div>
        <img src="data:image/png;base64,{{result['average_socre_table']}}">
    </div>
    <hr>
    <div>
        <img src="data:image/png;base64,{{result['section_fail_bar']}}">
    </div>
    <hr>
    <div>
        <img src="data:image/png;base64,{{result['section_improvement_bar']}}">
    </div>
</body>
</html>
