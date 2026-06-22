"""
Generate sample construction document from template
"""
import argparse
import re
from datetime import datetime


def fill_template(template_path, project_data, output_path=None):
    """填充模板并生成文档"""
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换所有 {{variable}} 占位符
    for key, value in project_data.items():
        placeholder = '{{' + key + '}}'
        content = content.replace(placeholder, str(value))
    
    # 替换未填充的占位符为空字符串
    content = re.sub(r'\{\{[^}]+\}\}', '', content)
    
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Generated document: {output_path}")
    
    return content


def main():
    parser = argparse.ArgumentParser(description='Generate sample construction document')
    parser.add_argument('--template', '-t', required=True, help='Template file path')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--project', '-p', default='示例工程项目', help='Project name')
    
    args = parser.parse_args()
    
    # 示例项目数据
    project_data = {
        'project_name': args.project,
        'project_location': '北京市朝阳区',
        'owner_name': '某某房地产开发有限公司',
        'design_unit': '某某建筑设计研究院',
        'contractor_name': '某某建设集团有限公司',
        'supervisor_name': '某某监理有限公司',
        'building_area': '45000',
        'structure_type': '框架剪力墙结构',
        'floors': '28',
        'height': '99.5',
        'start_date': datetime.now().strftime('%Y-%m-%d'),
        'end_date': (datetime.now().replace(year=datetime.now().year + 1)).strftime('%Y-%m-%d'),
        'quality_target': '合格，争创"长城杯"',
        'safety_target': '零死亡、零重伤、零火灾',
        'schedule_target': '按期完工',
        'environment_target': '符合北京市环保要求',
        'crane_model': 'QTZ80',
        'crane_qty': '3',
        'preparer': '张三',
        'reviewer': '李四',
        'approver': '王五',
        'date': datetime.now().strftime('%Y年%m月%d日')
    }
    
    fill_template(args.template, project_data, args.output)


if __name__ == '__main__':
    main()
