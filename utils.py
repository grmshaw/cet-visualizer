#!/usr/bin/env python3

import os
import io
import sys
import uuid
import base64
import xlrd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# Set font for Chinese characters
font_path = os.path.abspath('./static/SourceHanSansCN-Medium.otf')
font_prop = FontProperties(fname=font_path, size=14)

# Read the xlsx file
def read_xlsx(target_file):
    df = pd.read_excel(target_file)
    return df

# retrieve section names from df
def retrieve_section_names(df):
    sections = []
    for header in df.columns:
        if '作文' in header:
            sections.append('作文')
        elif '写作' in header:
            sections.append('写作')
        elif '听力' in header:
            sections.append('听力')
        elif '阅读' in header:
            sections.append('阅读')
        elif '翻译' in header:
            sections.append('翻译')
    return sections

# remove invalid rows
def remove_invalid_rows(df, writing_section_name):
    analysis_text = ''
    # analysis_text += '\n<h2>概况</h2>\n'
    invalid = len(df.index) - len(df.dropna().index)
    # analysis_text += f"所选样本共 {len(df.index)} 人，无效数据 {invalid} 条，"
    df = df[df[writing_section_name].notna()]
    df = df[df['听力'].notna()]
    df = df[df['阅读'].notna()]
    df = df[df['翻译'].notna()]
    df = df[df['总分'].notna()]
    return df, analysis_text

# calculate total score and pass rate
def calculate_total_score(df, sections, inherited_analysis_text):
    df['总分'] = df[sections].sum(axis=1)
    total_students = len(df)
    pass_students = len(df[df['总分'] >= 60])
    fail_students = total_students - pass_students
    overall_pass_rate = pass_students / total_students * 100
    overall_fail_rate = fail_students / total_students * 100
    # inherited_analysis_text += f"有效数据 {total_students} 条。\n"
    inherited_analysis_text += f"<br>总分及格率 {overall_pass_rate:.1f}%，未通过率 {overall_fail_rate:.1f}%。"
    return overall_pass_rate, overall_fail_rate, inherited_analysis_text

# create a pie chart for overall pass rate and fail rate
def create_pie_chart_for_overall_rates(overall_pass_rate, overall_fail_rate):
    fig, ax = plt.subplots(figsize=(9, 9))
    rates = [overall_pass_rate, overall_fail_rate]
    colors = ['#FFB800', '#E9E7E3']
    wedges, texts, autotexts = ax.pie(rates, colors=colors, autopct='%1.1f%%', startangle=90, wedgeprops=dict(width=0.5, edgecolor='w'))
    ax.axis('equal')
    ax.set_title('总分及格率', weight='bold', fontsize=20, fontproperties=font_prop)
    ax.legend(labels=['及格', '未通过'], loc='best', frameon=False, fontsize=14, prop=font_prop)

    # Add black border around percentage values
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontsize(18)
        autotext.set_bbox(dict(facecolor='none', edgecolor='none', pad=5))

    plt.tight_layout()
    # plt.savefig(output_folder + '0. 总分及格率.png', dpi=300)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=300)
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode()
    plt.close()

# calculte the average total score and the average score of each section
def calculate_total_and_section_average_score(df, sections):
    global analysis_text
    total_avg_score = df['总分'].mean()
    # analysis_text += f"总平均分为 {total_avg_score:.2f} 分。\n\n"
    section_avg_scores = []
    for section in sections:
        avg_score = df[section].mean()
        section_avg_scores.append(avg_score)
    return total_avg_score, section_avg_scores

# create a table to show average total score and average score of each section
def create_table_for_total_and_section_average_score(total_avg_score, section_avg_scores, writing_section_name):
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.axis('tight')
    ax.axis('off')
    ax.set_title('各项平均分', fontsize=16, weight='bold', fontproperties=font_prop, y=1.1)

    pass_scores = [60, 9, 21, 21, 9]
    table_data = [['名称', '平均分', '及格线'],
                  ['总分', f'{total_avg_score:.2f}', pass_scores[0]],
                  [writing_section_name, f'{section_avg_scores[0]:.2f}', pass_scores[1]],
                  ['听力', f'{section_avg_scores[1]:.2f}', pass_scores[2]],
                  ['阅读', f'{section_avg_scores[2]:.2f}', pass_scores[3]],
                  ['翻译', f'{section_avg_scores[3]:.2f}', pass_scores[4]]]

    table = ax.table(cellText=table_data, loc='center', cellLoc='center', colLabels=None, edges='closed', bbox=[0, 0, 1, 1])
    # Apply the custom font to each cell in the table
    for key, cell in table.get_celld().items():
        cell.set_text_props(fontproperties=font_prop)

    table.auto_set_font_size(False)
    table.set_fontsize(15)
    
    for _, cell in table.get_celld().items():
        cell.set_edgecolor('white')
        cell.set_linewidth(0.5)
    
    header_color = '#E9E7E4'
    row_colors = ['white', 'white']
    
    for key, cell in table.get_celld().items():
        if key[0] == 0:
            cell.set_text_props(weight='bold', color='black')
            cell.set_facecolor(header_color)
            cell.set_edgecolor(header_color)
        elif key[1] == 2:
            cell.set_text_props(weight='bold', color='black')
            cell.set_facecolor('white')
            cell.set_edgecolor('white')
        else:
            cell.set_facecolor(row_colors[key[0] % 2])
    
    table.scale(1, 2)
    plt.tight_layout()
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=300)
    buffer.seek(0)
    plt.close()
    
    return base64.b64encode(buffer.getvalue()).decode()

# Calculate average score and fail rate for each section
def calculate_section_score(df, sections, section_pass_scores):
    global analysis_text
    # analysis_text += '\n<h2>各项不及格情况</h2>\n'
    section_fail_rates = []
    total_students = len(df)
    for section in sections:
        pass_score = section_pass_scores[section]
        avg_score = df[section].mean()
        fail_students = len(df[df[section] < pass_score])
        fail_rate = fail_students / total_students * 100
        section_fail_rates.append(fail_rate)
        # analysis_text += f"{section}：{fail_students} 名学生不及格，不及格率 {fail_rate:.2f}%。\n<br>"
    return section_fail_rates

# create a bar chart to show the fail rate of the four sections from high to low
def create_section_fail_rate_chart(sections, section_fail_rates):
    fig, ax = plt.subplots()
    section_fail_rates, sections = zip(*zip(section_fail_rates, sections))
    bars = ax.bar(sections, section_fail_rates, width=0.6, align='center', color=['#4BD6FD', '#4F86FF', '#6C56FF', '#4AE2B1'])
    ax.set_title('各项不及格情况', pad=15, fontsize=16, weight='bold', fontproperties=font_prop)
    ax.title.set_position([0.5, 3])
    
    # Apply the custom font to the x-axis tick labels
    ax.set_xticks(range(len(sections)))
    ax.set_xticklabels(sections, fontproperties=font_prop, rotation=45)

    # Add describing numbers to the top of each bar
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.annotate(f'{height:.1f}%', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 6), textcoords='offset points', ha='center', fontsize=15, fontproperties=font_prop)
        
    # Set the maximum Y value to the maximum value in section_fail_rates + 10
    max_y = max(section_fail_rates) + 10
    ax.set_ylim(top=max_y)
    
    # plt.show()
    # plt.savefig(output_folder + '2. 各项不及格情况.png', dpi=300)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=300)
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode()
    plt.close()

# Calculate how many scores can be improved for each section, by comparing the average score of the section with its full marks
def calculate_score_improvement(df, sections, section_full_marks):
    global analysis_text
    # analysis_text += '\n<h2>各项可提分空间</h2>\n'
    section_improvements = []
    for section in sections:
        avg_score = df[section].mean()
        full_mark = section_full_marks[section]
        improvement = full_mark - avg_score
        section_improvements.append(improvement)
        # analysis_text += f"{section}平均分：{avg_score:.2f} 分，可提分空间：{improvement:.2f} 分。\n<br>"
    return section_improvements

# create a bar chart to show the improvement of the four sections from high to low, and add describing numbers to each bar
def create_section_improvement_chart(sections, section_improvements):
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.3)
    section_improvements, sections = zip(*zip(section_improvements, sections))
    bars = ax.bar(sections, section_improvements, width=0.6, align='center', color=['#C6C82D', '#B2E32E', '#F8D83A', '#F79636'])
    ax.set_title('各项可提分空间', pad=15, fontsize=16, weight='bold', fontproperties=font_prop)
    ax.title.set_position([0.5, 3])

    # Apply the custom font to the x-axis tick labels
    ax.set_xticks(range(len(sections)))
    ax.set_xticklabels(sections, fontproperties=font_prop, rotation=45)
    
    # Add describing numbers to the top of each bar
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.annotate(f'{height:.1f} 分', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 6), textcoords='offset points', ha='center', fontsize=15, fontproperties=font_prop)

    # Add a footnote-like annotation
    ax.text(0.5, -0.3, "*可提分空间 = 单项满分 - 单项平均", transform=ax.transAxes, fontsize=12, ha='left', color='gray', fontproperties=font_prop)

    # Set the maximum Y value to the maximum value in section_improvements + 20
    max_y = max(section_improvements) + 5
    ax.set_ylim(top=max_y)
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=300)
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode()
    plt.close()
