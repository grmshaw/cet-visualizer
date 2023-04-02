#!/usr/bin/env python3

from utils import *
from bottle import route, run, static_file, template, request, redirect

results = {}
error_msg = """<pre style="font-size: 16px; margin: 3em;"><br>无法解析表单，请检查：

1）表头是否有空行或隐藏行，
2）栏目是否为'写作'、'听力'、'阅读'、'翻译'。
3）分数部分，是否有单元格包含「10 <strong>分</strong>」一类文字

<a href='/'>返回</a></pre>"""

@route('/static/<filename:path>')
def serve_static(filename):
    return static_file(filename, root='./static/')

@route('/')
def index():
    return template('index')

@route('/upload', method='POST')
def do_upload():
    upload = request.files.get('file')
    if not upload:
        return 'No file selected'

    filename = upload.filename
    classname = request.forms.get('classname')

    uuid_str = str(uuid.uuid4())
    file_path = 'uploads/' + uuid_str + '.xlsx'

    # Create the uploads directory if it doesn't exist
    os.makedirs('uploads', exist_ok=True)

    upload.save(file_path, overwrite=True)

    # Process the uploaded file
    df = pd.read_excel(file_path)
    sections = retrieve_section_names(df)

    try:
        df, analysis_text = remove_invalid_rows(df, sections[0])
    except IndexError:
        return error_msg
    except KeyError:
        return error_msg

    section_full_marks = {sections[0]: 15, '听力': 35, '阅读': 35, '翻译': 15}
    section_pass_scores = {sections[0]: 9, '听力': 21, '阅读': 21, '翻译': 9}

    # Generate the charts
    overall_pass_rate, overall_fail_rate, full_analysis_text = calculate_total_score(df, sections, analysis_text)
    overall_rate_piechart = create_pie_chart_for_overall_rates(overall_pass_rate, overall_fail_rate)

    total_and_section_avg_score = calculate_total_and_section_average_score(df, sections)
    average_socre_table = create_table_for_total_and_section_average_score(*total_and_section_avg_score, sections[0])

    section_fail_rates = calculate_section_score(df, sections, section_pass_scores)
    section_fail_bar = create_section_fail_rate_chart(sections, section_fail_rates)

    section_improvements = calculate_score_improvement(df, sections, section_full_marks)
    section_improvement_bar = create_section_improvement_chart(sections, section_improvements)

    # Store the results in a dictionary or a database using the UUID as a key
    results[uuid_str] = {
        'df': df,
        'classname' : classname,
        'title' : filename,
        'analysis_text' : full_analysis_text,
        'overall_rate_piechart': overall_rate_piechart,
        'average_socre_table': average_socre_table,
        'section_fail_bar': section_fail_bar,
        'section_improvement_bar': section_improvement_bar
    }
    print(analysis_text)
    os.remove(file_path)
    return redirect('/{}'.format(uuid_str))

@route('/<uuid_str>')
def show_visual(uuid_str):
    if uuid_str not in results:
        return redirect('/')
    result = results[uuid_str]
    return template('visual', result=result)

if __name__ == '__main__':
    run(host='0.0.0.0', port=8787, reloader=True)