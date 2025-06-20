from nicegui import ui
from utils import (
    safe_eval, solve_equation, compute_derivative, 
    compute_integral, compute_statistics,
    create_fft_plot, create_fitting_plot, create_visualization_plot
)

import pandas as pd
import io

class ScientificCalculator:
    def __init__(self):
        self.excel_data = None  # 存储Excel数据
        self.setup_styles()
        self.create_ui()
    
    def setup_styles(self):
        """设置自定义样式"""
        ui.add_head_html('''
        <style>
            .calculator-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 15px;
                padding: 20px;
                margin: 10px 0;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            }
            .result-card {
                background: #f8f9fa;
                border: 2px solid #e9ecef;
                border-radius: 10px;
                padding: 15px;
                margin: 10px 0;
            }
            .example-button {
                background: #17a2b8;
                color: white;
                border-radius: 8px;
                margin: 2px;
                transition: all 0.3s ease;
            }
            .example-button:hover {
                background: #138496;
                transform: translateY(-2px);
            }
            .title-gradient {
                background: linear-gradient(45deg, #667eea, #764ba2);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
        </style>
        ''')
    
    def create_ui(self):
        """创建用户界面"""
        # 页面标题和头部
        # ui.page_title('高级科学计算器')
        
        with ui.header(elevated=True).style('background: linear-gradient(90deg, #667eea 0%, #764ba2 100%)'):
            ui.label('🧮 高级科学计算器').classes('text-h5 text-white font-weight-bold')
        
        with ui.column().classes('w-full max-w-6xl mx-auto p-4'):
            # 欢迎信息
            with ui.card().classes('w-full calculator-card'):
                ui.label('欢迎使用高级科学计算器').classes('text-h5 text-white text-center')
                ui.label('支持基础运算、方程求解、傅里叶变换、微积分、统计分析等功能').classes('text-subtitle1 text-white text-center')
            
            # 创建选项卡
            with ui.tabs().classes('w-full') as tabs:
                basic_tab = ui.tab('🔢 四则运算')
                equation_tab = ui.tab('⚖️ 方程求解')
                fourier_tab = ui.tab('📊 傅里叶变换')
                calculus_tab = ui.tab('∫ 微积分')
                stats_tab = ui.tab('📈 统计分析')
                fitting_tab = ui.tab('📉 曲线拟合')
                visualization_tab = ui.tab('🎨 数据可视化')
            
            with ui.tab_panels(tabs, value=basic_tab).classes('w-full'):
                self.create_basic_tab(basic_tab)
                self.create_equation_tab(equation_tab)
                self.create_fourier_tab(fourier_tab)
                self.create_calculus_tab(calculus_tab)
                self.create_stats_tab(stats_tab)
                self.create_fitting_tab(fitting_tab)
                self.create_visualization_tab(visualization_tab)
        
        # 页脚
        with ui.footer().style('background: #343a40; color: white;'):
            ui.label('© 2025 高级科学计算器 - 基于 Python 和 NiceGUI 构建').classes('text-center w-full')
    
    def create_basic_tab(self, tab):
        """创建四则运算面板"""
        with ui.tab_panel(tab):
            with ui.card().classes('w-full'):
                ui.label('🔢 基本四则运算').classes('text-h5 mb-4')
                
                self.expr_input = ui.input('输入表达式', 
                                         placeholder='例如: (2+3)*4/2 - 5**2 + sin(π/2)').classes('w-full mb-4')
                
                with ui.row().classes('w-full gap-2 mb-4'):
                    ui.button('🧮 计算', on_click=self.calculate_expression).classes('bg-blue-500 text-white')
                    ui.button('🗑️ 清除', on_click=lambda: self.expr_input.set_value('')).classes('bg-gray-500 text-white')
                
                with ui.card().classes('result-card w-full'):
                    self.result_label = ui.label('🎯 结果将显示在这里').classes('text-h6')
                
                # 示例表达式
                ui.label('📝 示例表达式:').classes('text-subtitle1 font-weight-bold mt-4')
                with ui.row().classes('flex-wrap gap-2'):
                    examples = [
                        ('2+3*4', '2+3*4'),
                        ('(2+3)*4', '(2+3)*4'),
                        ('5²+√9', '5**2 + 9**0.5'),
                        ('sin(π/2)', 'sin(pi/2)'),
                        ('ln(e)', 'log(e)'),
                        ('√(16)', 'sqrt(16)')
                    ]
                    for label, expr in examples:
                        ui.button(label, 
                                on_click=lambda e=expr: self.expr_input.set_value(e)).classes('example-button')
    
    def calculate_expression(self):
        """计算表达式"""
        expr = self.expr_input.value
        if not expr:
            self.result_label.text = '❌ 请输入表达式'
            return
        
        try:
            result = safe_eval(expr)
            if isinstance(result, (int, float)):
                self.result_label.text = f'✅ 结果: {result:.6f}' if isinstance(result, float) else f'✅ 结果: {result}'
            else:
                self.result_label.text = f'✅ 结果: {result}'
        except Exception as e:
            self.result_label.text = f'❌ {str(e)}'
    
    def create_equation_tab(self, tab):
        """创建方程求解面板"""
        with ui.tab_panel(tab):
            with ui.card().classes('w-full'):
                ui.label('⚖️ 方程求解').classes('text-h5 mb-4')
                
                with ui.row().classes('w-full gap-4 mb-4'):
                    self.eq_input = ui.input('输入方程', 
                                           placeholder='例如: x**2 - 4 = 0').classes('flex-grow')
                    self.var_input = ui.input('变量', 
                                            placeholder='例如: x').classes('w-32')
                
                with ui.row().classes('w-full gap-2 mb-4'):
                    ui.button('🔍 求解', on_click=self.solve_equation).classes('bg-green-500 text-white')
                    ui.button('🗑️ 清除', on_click=lambda: [
                        self.eq_input.set_value(''), 
                        self.var_input.set_value('')
                    ]).classes('bg-gray-500 text-white')
                
                with ui.card().classes('result-card w-full'):
                    self.eq_result = ui.label('🎯 方程解将显示在这里').classes('text-h6')
                
                # 示例方程
                ui.label('📝 示例方程:').classes('text-subtitle1 font-weight-bold mt-4')
                with ui.row().classes('flex-wrap gap-2'):
                    examples = [
                        ('一元二次', 'x**2 - 4 = 0', 'x'),
                        ('二元线性', 'x + 2*y = 10, 3*x - y = 5', 'x,y'),
                        ('指数方程', 'exp(x) - 2 = 0', 'x'),
                        ('三角方程', 'sin(x) = 0.5', 'x')
                    ]
                    for label, eq, var in examples:
                        ui.button(label, on_click=lambda e=eq, v=var: [
                            self.eq_input.set_value(e), 
                            self.var_input.set_value(v)
                        ]).classes('example-button')
    
    def solve_equation(self):
        """求解方程"""
        eq_str = self.eq_input.value
        var_str = self.var_input.value
        
        if not eq_str or not var_str:
            self.eq_result.text = '❌ 请输入方程和变量'
            return
        
        try:
            solution = solve_equation(eq_str, var_str)
            self.eq_result.text = f'✅ 解: {solution}'
        except Exception as e:
            self.eq_result.text = f'❌ 错误: {str(e)}'
    
    def create_fourier_tab(self, tab):
        """创建傅里叶变换面板"""
        with ui.tab_panel(tab):
            with ui.card().classes('w-full'):
                ui.label('📊 傅里叶变换分析').classes('text-h5 mb-4')
                
                with ui.row().classes('w-full gap-4 mb-4'):
                    self.freq_input = ui.number('信号频率 (Hz)', value=5, min=0.1, max=100, step=0.1).classes('flex-1')
                    self.duration_input = ui.number('持续时间 (秒)', value=1, min=0.1, max=10, step=0.1).classes('flex-1')
                    self.sample_rate_input = ui.number('采样率 (Hz)', value=100, min=10, max=1000, step=10).classes('flex-1')
                
                with ui.row().classes('w-full gap-4 mb-4'):
                    ui.label('噪声水平').classes('w-full')
                    self.noise_level = ui.slider(min=0, max=1, value=0.1, step=0.01).props('label-always').classes('flex-grow')
                    ui.button('📈 计算并绘制', on_click=self.compute_fft_and_plot).classes('bg-purple-500 text-white')
                
                with ui.card().classes('w-full'):
                    self.fft_result = ui.html().classes('w-full')
                    self.fft_result.content = '<div class="text-center text-gray-500 p-8">📊 FFT图表将显示在这里</div>'
    
    def compute_fft_and_plot(self):
        """计算并绘制傅里叶变换结果"""
        freq = self.freq_input.value
        duration = self.duration_input.value
        sample_rate = self.sample_rate_input.value
        noise_level = self.noise_level.value
        
        try:
            img_base64 = create_fft_plot(freq, duration, sample_rate, noise_level)
            self.fft_result.content = f'''
            <div class="text-center">
                <h3 class="text-lg font-bold mb-4">傅里叶变换结果</h3>
                <img src="data:image/png;base64,{img_base64}" class="w-full h-auto rounded-lg shadow-lg">
            </div>
            '''
        except Exception as e:
            self.fft_result.content = f'<div class="text-red-500 text-center p-4">❌ 错误: {str(e)}</div>'
    
    def create_calculus_tab(self, tab):
        """创建微积分面板"""
        with ui.tab_panel(tab):
            with ui.card().classes('w-full'):
                ui.label('∫ 微积分计算').classes('text-h5 mb-4')
                
                with ui.row().classes('w-full gap-4 mb-4'):
                    self.func_input = ui.input('函数表达式', 
                                             placeholder='例如: sin(x) 或 x**2').classes('flex-grow')
                    self.var_integral = ui.input('变量', 
                                               placeholder='x', value='x').classes('w-24')
                
                with ui.row().classes('w-full gap-4 mb-4'):
                    self.lower_input = ui.input('下限', placeholder='例如: 0').classes('flex-1')
                    self.upper_input = ui.input('上限', placeholder='例如: pi').classes('flex-1')
                    ui.button('d/dx 求导', on_click=self.compute_derivative).classes('bg-blue-500 text-white')
                    ui.button('∫ 积分', on_click=self.compute_integral).classes('bg-green-500 text-white')
                
                with ui.card().classes('result-card w-full'):
                    self.calc_result = ui.label('🎯 计算结果将显示在这里').classes('text-h6')
                
                # 示例函数
                ui.label('📝 示例函数:').classes('text-subtitle1 font-weight-bold mt-4')
                with ui.row().classes('flex-wrap gap-2'):
                    examples = [
                        ('sin(x)', 'sin(x)', 'x'),
                        ('x²', 'x**2', 'x'),
                        ('eˣ', 'exp(x)', 'x'),
                        ('ln(x)', 'log(x)', 'x')
                    ]
                    for label, func, var in examples:
                        ui.button(label, on_click=lambda f=func, v=var: [
                            self.func_input.set_value(f), 
                            self.var_integral.set_value(v)
                        ]).classes('example-button')
    
    def compute_derivative(self):
        """计算导数"""
        func_str = self.func_input.value
        var_str = self.var_integral.value
        
        if not func_str or not var_str:
            self.calc_result.text = '❌ 请输入函数和变量'
            return
        
        try:
            derivative = compute_derivative(func_str, var_str)
            self.calc_result.text = f'✅ 导数: {derivative}'
        except Exception as e:
            self.calc_result.text = f'❌ 错误: {str(e)}'
    
    def compute_integral(self):
        """计算积分"""
        func_str = self.func_input.value
        var_str = self.var_integral.value
        lower_str = self.lower_input.value
        upper_str = self.upper_input.value
        
        if not func_str or not var_str:
            self.calc_result.text = '❌ 请输入函数和变量'
            return
        
        try:
            if lower_str and upper_str:
                integral = compute_integral(func_str, var_str, lower_str, upper_str)
                self.calc_result.text = f'✅ 定积分结果: {integral}'
            else:
                integral = compute_integral(func_str, var_str)
                self.calc_result.text = f'✅ 不定积分结果: {integral} + C'
        except Exception as e:
            self.calc_result.text = f'❌ 错误: {str(e)}'
    
    def create_stats_tab(self, tab):
        """创建统计分析面板"""
        with ui.tab_panel(tab):
            with ui.card().classes('w-full'):
                ui.label('📈 统计分析').classes('text-h5 mb-4')
                
                # Excel上传功能
                with ui.expansion('📊 Excel文件输入', icon='upload_file').classes('w-full mb-4'):
                    with ui.row().classes('w-full gap-4 mb-4'):
                        self.stats_excel_upload = ui.upload(
                            on_upload=self.handle_stats_excel_upload,
                            max_file_size=5_000_000,
                            multiple=False
                        ).props('accept=".xlsx,.xls"').classes('flex-1')
                        ui.label('支持 .xlsx 和 .xls 格式，最大5MB').classes('text-sm text-gray-600')
                    
                    with ui.row().classes('w-full gap-4'):
                        self.stats_column = ui.select(
                            options=[], 
                            label='选择数据列', 
                            on_change=self.update_stats_data
                        ).classes('flex-1')
                        ui.button('📋 预览数据', on_click=self.preview_stats_data).classes('bg-blue-500 text-white')
                
                # 手动输入功能
                with ui.expansion('✏️ 手动输入', icon='edit', value=True).classes('w-full mb-4'):
                    self.data_input = ui.textarea('输入数据 (逗号分隔)', 
                                                placeholder='例如: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10').classes('w-full h-32 mb-4')
                
                with ui.row().classes('w-full gap-2 mb-4'):
                    ui.button('📊 计算统计量', on_click=self.compute_statistics).classes('bg-blue-500 text-white')
                    ui.button('🗑️ 清除', on_click=lambda: self.data_input.set_value('')).classes('bg-gray-500 text-white')
                
                with ui.card().classes('result-card w-full'):
                    self.stats_result = ui.html('🎯 统计结果将显示在这里').classes('text-h6')
                
                # 数据预览区域
                with ui.card().classes('w-full'):
                    self.stats_preview = ui.html().classes('w-full')
                    self.stats_preview.content = '<div class="text-center text-gray-500 p-4">📋 数据预览将显示在这里</div>'
                
                # 示例数据
                ui.label('📝 示例数据:').classes('text-subtitle1 font-weight-bold mt-4')
                with ui.row().classes('flex-wrap gap-2'):
                    examples = [
                        ('整数序列', '1, 2, 3, 4, 5, 6, 7, 8, 9, 10'),
                        ('随机数据', '10.5, 12.3, 11.7, 9.8, 13.2, 8.9, 14.1, 11.0'),
                        ('正态分布', '100, 102, 98, 101, 99, 103, 97, 100, 102, 98'),
                    ]
                    for label, data in examples:
                        ui.button(label, on_click=lambda d=data: self.data_input.set_value(d)).classes('example-button')
    
    def handle_stats_excel_upload(self, e):
        """处理统计分析功能的Excel文件上传"""
        try:
            # 读取Excel文件
            content = e.content.read()
            df = pd.read_excel(io.BytesIO(content))
            self.excel_data = df
            
            # 更新列选择器选项，只显示数值列
            numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
            all_columns = df.columns.tolist()
            
            # 优先显示数值列，但也包含所有列
            self.stats_column.options = numeric_columns + [col for col in all_columns if col not in numeric_columns]
            
            # 显示成功消息
            ui.notify(f'✅ Excel文件上传成功！共{len(df)}行，{len(numeric_columns)}个数值列', type='positive')
            
            # 自动选择第一个数值列（如果存在）
            if numeric_columns:
                self.stats_column.value = numeric_columns[0]
                self.update_stats_data()
                
        except Exception as ex:
            ui.notify(f'❌ Excel文件读取失败: {str(ex)}', type='negative')
    
    def update_stats_data(self):
        """更新统计分析的数据"""
        if self.excel_data is not None and self.stats_column.value:
            try:
                # 获取选中列的数据，去除空值
                column_data = self.excel_data[self.stats_column.value].dropna()
                
                # 尝试转换为数值类型
                try:
                    numeric_data = pd.to_numeric(column_data, errors='coerce').dropna()
                    data_str = ', '.join(str(x) for x in numeric_data.tolist())
                    self.data_input.set_value(data_str)
                    
                    # 显示数据信息
                    ui.notify(f'✅ 已加载 {len(numeric_data)} 个有效数值', type='positive')
                    
                except Exception:
                    ui.notify(f'❌ 列 "{self.stats_column.value}" 包含非数值数据', type='negative')
                    
            except Exception as e:
                ui.notify(f'❌ 数据更新失败: {str(e)}', type='negative')
    
    def preview_stats_data(self):
        """预览统计分析的数据"""
        if self.excel_data is None:
            self.stats_preview.content = '<div class="text-red-500 text-center p-4">❌ 请先上传Excel文件</div>'
            return
        
        try:
            # 创建预览表格，重点显示数值列
            preview_df = self.excel_data.head(10)  # 只显示前10行
            numeric_columns = self.excel_data.select_dtypes(include=['number']).columns.tolist()
            
            html_table = '<div class="overflow-x-auto">'
            html_table += f'<h4 class="text-lg font-bold mb-2">数据预览 (数值列: {len(numeric_columns)}个)</h4>'
            html_table += '<table class="w-full border-collapse border border-gray-300">'
            html_table += '<thead><tr class="bg-gray-100">'
            for col in preview_df.columns:
                # 数值列用不同的背景色标识
                bg_class = "bg-green-200" if col in numeric_columns else "bg-gray-100"
                html_table += f'<th class="border border-gray-300 px-2 py-1 text-left {bg_class}">{col}</th>'
            html_table += '</tr></thead><tbody>'
            
            for _, row in preview_df.iterrows():
                html_table += '<tr>'
                for col, val in zip(preview_df.columns, row):
                    bg_class = "bg-green-50" if col in numeric_columns else ""
                    html_table += f'<td class="border border-gray-300 px-2 py-1 {bg_class}">{val}</td>'
                html_table += '</tr>'
            html_table += '</tbody></table></div>'
            
            total_rows = len(self.excel_data)
            html_table += f'<p class="text-sm text-gray-600 mt-2">显示前10行，共{total_rows}行数据</p>'
            html_table += f'<p class="text-sm text-green-600">绿色背景列为数值列，推荐用于统计分析</p>'
            
            self.stats_preview.content = html_table
            
        except Exception as e:
            self.stats_preview.content = f'<div class="text-red-500 text-center p-4">❌ 预览失败: {str(e)}</div>'
    
    def create_fitting_tab(self, tab):
        """创建曲线拟合面板"""
        with ui.tab_panel(tab):
            with ui.card().classes('w-full'):
                ui.label('📉 曲线拟合').classes('text-h5 mb-4')
                
                # Excel上传功能
                with ui.expansion('📊 Excel文件输入', icon='upload_file').classes('w-full mb-4'):
                    with ui.row().classes('w-full gap-4 mb-4'):
                        self.fit_excel_upload = ui.upload(
                            on_upload=self.handle_fitting_excel_upload,
                            max_file_size=5_000_000,
                            multiple=False
                        ).props('accept=".xlsx,.xls"').classes('flex-1')
                        ui.label('支持 .xlsx 和 .xls 格式，最大5MB').classes('text-sm text-gray-600')
                    
                    with ui.row().classes('w-full gap-4'):
                        self.fit_x_column = ui.select(
                            options=[], 
                            label='X轴数据列', 
                            on_change=self.update_fitting_x_data
                        ).classes('flex-1')
                        self.fit_y_column = ui.select(
                            options=[], 
                            label='Y轴数据列', 
                            on_change=self.update_fitting_y_data
                        ).classes('flex-1')
                        ui.button('📋 预览数据', on_click=self.preview_fitting_data).classes('bg-blue-500 text-white')
                
                # 手动输入功能
                with ui.expansion('✏️ 手动输入', icon='edit', value=True).classes('w-full mb-4'):
                    with ui.row().classes('w-full gap-4 mb-4'):
                        self.fit_x_input = ui.textarea('X 数据 (逗号分隔)', 
                                                     placeholder='例如: 1, 2, 3, 4, 5').classes('flex-1')
                        self.fit_y_input = ui.textarea('Y 数据 (逗号分隔)', 
                                                     placeholder='例如: 2, 4, 6, 8, 10').classes('flex-1')

                self.deg_input = ui.number('多项式次数', value=1, min=1, max=10, step=1).classes('w-32')

                with ui.row().classes('w-full gap-4 mb-4'):
                    ui.button('📈 执行拟合', on_click=self.curve_fitting).classes('bg-green-500 text-white')
                    ui.button('🗑️ 清除', on_click=lambda: [
                        self.fit_x_input.set_value(''), 
                        self.fit_y_input.set_value('')
                    ]).classes('bg-gray-500 text-white')
                
                with ui.card().classes('w-full'):
                    self.fit_result = ui.html().classes('w-full')
                    self.fit_result.content = '<div class="text-center text-gray-500 p-8">📉 拟合结果将显示在这里</div>'
                
                # 数据预览区域
                with ui.card().classes('w-full'):
                    self.fitting_preview = ui.html().classes('w-full')
                    self.fitting_preview.content = '<div class="text-center text-gray-500 p-4">📋 数据预览将显示在这里</div>'
    
    def handle_fitting_excel_upload(self, e):
        """处理拟合功能的Excel文件上传"""
        try:
            # 读取Excel文件
            content = e.content.read()
            df = pd.read_excel(io.BytesIO(content))
            self.excel_data = df
            
            # 更新列选择器选项
            columns = df.columns.tolist()
            self.fit_x_column.options = columns
            self.fit_y_column.options = columns
            
            # 显示成功消息
            ui.notify(f'✅ Excel文件上传成功！共{len(df)}行，{len(columns)}列', type='positive')
            
            # 自动选择前两列（如果存在）
            if len(columns) >= 2:
                self.fit_x_column.value = columns[0]
                self.fit_y_column.value = columns[1]
                self.update_fitting_x_data()
                self.update_fitting_y_data()
                
        except Exception as ex:
            ui.notify(f'❌ Excel文件读取失败: {str(ex)}', type='negative')
    
    def update_fitting_x_data(self):
        """更新拟合功能的X轴数据"""
        if self.excel_data is not None and self.fit_x_column.value:
            try:
                x_data = self.excel_data[self.fit_x_column.value].dropna().tolist()
                x_str = ', '.join(str(x) for x in x_data)
                self.fit_x_input.set_value(x_str)
            except Exception as e:
                ui.notify(f'❌ X轴数据更新失败: {str(e)}', type='negative')
    
    def update_fitting_y_data(self):
        """更新拟合功能的Y轴数据"""
        if self.excel_data is not None and self.fit_y_column.value:
            try:
                y_data = self.excel_data[self.fit_y_column.value].dropna().tolist()
                y_str = ', '.join(str(y) for y in y_data)
                self.fit_y_input.set_value(y_str)
            except Exception as e:
                ui.notify(f'❌ Y轴数据更新失败: {str(e)}', type='negative')
    
    def preview_fitting_data(self):
        """预览拟合功能的数据"""
        if self.excel_data is None:
            self.fitting_preview.content = '<div class="text-red-500 text-center p-4">❌ 请先上传Excel文件</div>'
            return
        
        try:
            # 创建预览表格
            preview_df = self.excel_data.head(10)  # 只显示前10行
            
            html_table = '<div class="overflow-x-auto"><table class="w-full border-collapse border border-gray-300">'
            html_table += '<thead><tr class="bg-gray-100">'
            for col in preview_df.columns:
                html_table += f'<th class="border border-gray-300 px-2 py-1 text-left">{col}</th>'
            html_table += '</tr></thead><tbody>'
            
            for _, row in preview_df.iterrows():
                html_table += '<tr>'
                for val in row:
                    html_table += f'<td class="border border-gray-300 px-2 py-1">{val}</td>'
                html_table += '</tr>'
            html_table += '</tbody></table></div>'
            
            total_rows = len(self.excel_data)
            html_table += f'<p class="text-sm text-gray-600 mt-2">显示前10行，共{total_rows}行数据</p>'
            
            self.fitting_preview.content = html_table
            
        except Exception as e:
            self.fitting_preview.content = f'<div class="text-red-500 text-center p-4">❌ 预览失败: {str(e)}</div>'
    
    def curve_fitting(self):
        """执行曲线拟合"""
        x_str = self.fit_x_input.value
        y_str = self.fit_y_input.value
        degree = self.deg_input.value
        
        if not x_str or not y_str:
            self.fit_result.content = '❌ 请输入X和Y数据'
            return
        
        try:
            img_base64, poly, r_squared = create_fitting_plot(x_str, y_str, degree)
            
            self.fit_result.content = f'''
            <div class="text-center">
                <h3 class="text-lg font-bold mb-2">曲线拟合结果</h3>
                <div class="bg-blue-100 p-3 rounded mb-4">
                    <p><strong>拟合多项式:</strong> {poly}</p>
                    <p><strong>R²相关系数:</strong> {r_squared:.6f}</p>
                    <p><strong>拟合质量:</strong> {'优秀' if r_squared > 0.95 else '良好' if r_squared > 0.8 else '一般' if r_squared > 0.6 else '较差'}</p>
                </div>
                <img src="data:image/png;base64,{img_base64}" class="w-full h-auto rounded-lg shadow-lg">
            </div>
            '''
        except Exception as e:
            self.fit_result.content = f'<div class="text-red-500 text-center p-4">❌ 错误: {str(e)}</div>'
    
    def create_visualization_tab(self, tab):
        """创建数据可视化面板"""
        with ui.tab_panel(tab):
            with ui.card().classes('w-full'):
                ui.label('🎨 数据可视化').classes('text-h5 mb-4')
                
                # Excel上传功能
                with ui.expansion('📊 Excel文件输入', icon='upload_file').classes('w-full mb-4'):
                    with ui.row().classes('w-full gap-4 mb-4'):
                        self.vis_excel_upload = ui.upload(
                            on_upload=self.handle_visualization_excel_upload,
                            max_file_size=5_000_000,
                            multiple=False
                        ).props('accept=".xlsx,.xls"').classes('flex-1')
                        ui.label('支持 .xlsx 和 .xls 格式，最大5MB').classes('text-sm text-gray-600')
                    
                    with ui.row().classes('w-full gap-4'):
                        self.vis_x_column = ui.select(
                            options=[], 
                            label='X轴数据列', 
                            on_change=self.update_visualization_x_data
                        ).classes('flex-1')
                        self.vis_y_column = ui.select(
                            options=[], 
                            label='Y轴数据列', 
                            on_change=self.update_visualization_y_data
                        ).classes('flex-1')
                        ui.button('📋 预览数据', on_click=self.preview_visualization_data).classes('bg-blue-500 text-white')
                
                # 手动输入功能
                with ui.expansion('✏️ 手动输入', icon='edit', value=True).classes('w-full mb-4'):
                    with ui.row().classes('w-full gap-4 mb-4'):
                        self.vis_x_input = ui.textarea('X 数据 (逗号分隔)', 
                                                     placeholder='例如: 1, 2, 3, 4, 5').classes('flex-1')
                        self.vis_y_input = ui.textarea('Y 数据 (逗号分隔)', 
                                                     placeholder='例如: 2, 4, 6, 8, 10').classes('flex-1')
                
                self.chart_type = ui.select(
                        ['散点图', '折线图', '柱状图', '饼图'], 
                        value='散点图', 
                        label='图表类型'
                    ).classes('w-48')

                with ui.row().classes('w-full gap-4 mb-4'):
                    ui.button('🎨 绘制图表', on_click=self.plot_data).classes('bg-purple-500 text-white')
                    ui.button('🗑️ 清除', on_click=lambda: [
                        self.vis_x_input.set_value(''), 
                        self.vis_y_input.set_value('')
                    ]).classes('bg-gray-500 text-white')
                
                with ui.card().classes('w-full'):
                    self.vis_result = ui.html().classes('w-full')
                    self.vis_result.content = '<div class="text-center text-gray-500 p-8">🎨 图表将显示在这里</div>'
                
                # 数据预览区域
                with ui.card().classes('w-full'):
                    self.visualization_preview = ui.html().classes('w-full')
                    self.visualization_preview.content = '<div class="text-center text-gray-500 p-4">📋 数据预览将显示在这里</div>'
    
    def handle_visualization_excel_upload(self, e):
        """处理可视化功能的Excel文件上传"""
        try:
            # 读取Excel文件
            content = e.content.read()
            df = pd.read_excel(io.BytesIO(content))
            self.excel_data = df
            
            # 更新列选择器选项
            columns = df.columns.tolist()
            self.vis_x_column.options = columns
            self.vis_y_column.options = columns
            
            # 显示成功消息
            ui.notify(f'✅ Excel文件上传成功！共{len(df)}行，{len(columns)}列', type='positive')
            
            # 自动选择前两列（如果存在）
            if len(columns) >= 2:
                self.vis_x_column.value = columns[0]
                self.vis_y_column.value = columns[1]
                self.update_visualization_x_data()
                self.update_visualization_y_data()
                
        except Exception as ex:
            ui.notify(f'❌ Excel文件读取失败: {str(ex)}', type='negative')
    
    def update_visualization_x_data(self):
        """更新可视化功能的X轴数据"""
        if self.excel_data is not None and self.vis_x_column.value:
            try:
                x_data = self.excel_data[self.vis_x_column.value].dropna().tolist()
                x_str = ', '.join(str(x) for x in x_data)
                self.vis_x_input.set_value(x_str)
            except Exception as e:
                ui.notify(f'❌ X轴数据更新失败: {str(e)}', type='negative')
    
    def update_visualization_y_data(self):
        """更新可视化功能的Y轴数据"""
        if self.excel_data is not None and self.vis_y_column.value:
            try:
                y_data = self.excel_data[self.vis_y_column.value].dropna().tolist()
                y_str = ', '.join(str(y) for y in y_data)
                self.vis_y_input.set_value(y_str)
            except Exception as e:
                ui.notify(f'❌ Y轴数据更新失败: {str(e)}', type='negative')
    
    def preview_visualization_data(self):
        """预览可视化功能的数据"""
        if self.excel_data is None:
            self.visualization_preview.content = '<div class="text-red-500 text-center p-4">❌ 请先上传Excel文件</div>'
            return
        
        try:
            # 创建预览表格
            preview_df = self.excel_data.head(10)  # 只显示前10行
            
            html_table = '<div class="overflow-x-auto"><table class="w-full border-collapse border border-gray-300">'
            html_table += '<thead><tr class="bg-gray-100">'
            for col in preview_df.columns:
                html_table += f'<th class="border border-gray-300 px-2 py-1 text-left">{col}</th>'
            html_table += '</tr></thead><tbody>'
            
            for _, row in preview_df.iterrows():
                html_table += '<tr>'
                for val in row:
                    html_table += f'<td class="border border-gray-300 px-2 py-1">{val}</td>'
                html_table += '</tr>'
            html_table += '</tbody></table></div>'
            
            total_rows = len(self.excel_data)
            html_table += f'<p class="text-sm text-gray-600 mt-2">显示前10行，共{total_rows}行数据</p>'
            
            self.visualization_preview.content = html_table
            
        except Exception as e:
            self.visualization_preview.content = f'<div class="text-red-500 text-center p-4">❌ 预览失败: {str(e)}</div>'
    
    def plot_data(self):
        """绘制数据图表"""
        x_str = self.vis_x_input.value
        y_str = self.vis_y_input.value
        chart_type = self.chart_type.value
        
        if not x_str or not y_str:
            self.vis_result.content = '❌ 请输入X和Y数据'
            return
        
        try:
            # 改进数据转换逻辑
            x_parts = [x.strip() for x in x_str.split(',')]
            y_parts = [y.strip() for y in y_str.split(',')]
            
            # 处理X数据
            x_data = []
            for i, x in enumerate(x_parts):
                try:
                    # 尝试转换为数字
                    x_data.append(float(x))
                except ValueError:
                    # 如果不能转换为数字，保留字符串
                    x_data.append(x)
            
            # 处理Y数据
            y_data = []
            for y in y_parts:
                try:
                    y_data.append(float(y))
                except ValueError:
                    raise ValueError(f"Y数据 '{y}' 不是有效数字")
            
            if len(x_data) != len(y_data):
                self.vis_result.content = '<div class="text-red-500 text-center p-4">❌ X和Y数据数量不一致</div>'
                return
            
            img_base64 = create_visualization_plot(x_data, y_data, chart_type)
            
            self.vis_result.content = f'''
            <div class="text-center">
                <h3 class="text-lg font-bold mb-4">{chart_type}可视化结果</h3>
                <img src="data:image/png;base64,{img_base64}" class="w-full h-auto rounded-lg shadow-lg">
            </div>
            '''
            
        except Exception as e:
            self.vis_result.content = f'<div class="text-red-500 text-center p-4">❌ 错误: {str(e)}</div>'
    
    def compute_statistics(self):
        """计算统计量"""
        data_str = self.data_input.value
        
        if not data_str:
            self.stats_result.content = '❌ 请输入数据'
            return
        
        try:
            stats = compute_statistics(data_str)
            
            # 创建统计结果的HTML表格
            html_content = '''
            <div class="bg-blue-50 p-4 rounded-lg">
                <h3 class="text-lg font-bold mb-4 text-center">📊 统计分析结果</h3>
                <div class="grid grid-cols-2 gap-4">
                    <div class="bg-white p-3 rounded border">
                        <p><strong>数据个数:</strong> {count}</p>
                        <p><strong>平均值:</strong> {mean:.6f}</p>
                        <p><strong>中位数:</strong> {median:.6f}</p>
                    </div>
                    <div class="bg-white p-3 rounded border">
                        <p><strong>标准差:</strong> {std:.6f}</p>
                        <p><strong>方差:</strong> {var:.6f}</p>
                        <p><strong>变异系数:</strong> {cv:.6f}</p>
                    </div>
                    <div class="bg-white p-3 rounded border">
                        <p><strong>最小值:</strong> {min:.6f}</p>
                        <p><strong>最大值:</strong> {max:.6f}</p>
                        <p><strong>极差:</strong> {range:.6f}</p>
                    </div>
                    <div class="bg-white p-3 rounded border">
                        <p><strong>第一四分位数:</strong> {q1:.6f}</p>
                        <p><strong>第三四分位数:</strong> {q3:.6f}</p>
                        <p><strong>四分位距:</strong> {iqr:.6f}</p>
                    </div>
                </div>
            </div>
            '''.format(
                count=stats['count'],
                mean=stats['mean'],
                median=stats['median'],
                std=stats['std'],
                var=stats['var'],
                cv=stats['std']/stats['mean'] if stats['mean'] != 0 else 0,
                min=stats['min'],
                max=stats['max'],
                range=stats['max'] - stats['min'],
                q1=stats['q1'],
                q3=stats['q3'],
                iqr=stats['q3'] - stats['q1']
            )
            
            self.stats_result.content = html_content
            
        except Exception as e:
            self.stats_result.content = f'<div class="text-red-500 text-center p-4">❌ 错误: {str(e)}</div>'
            self.visualization_preview.content = '<div class="text-center text-gray-500 p-4">📋 数据预览将显示在这里</div>'
    
    def handle_visualization_excel_upload(self, e):
        """处理可视化功能的Excel文件上传"""
        try:
            # 读取Excel文件
            content = e.content.read()
            df = pd.read_excel(io.BytesIO(content))
            self.excel_data = df
            
            # 更新列选择器选项
            columns = df.columns.tolist()
            self.vis_x_column.options = columns
            self.vis_y_column.options = columns
            
            # 显示成功消息
            ui.notify(f'✅ Excel文件上传成功！共{len(df)}行，{len(columns)}列', type='positive')
            
            # 自动选择前两列（如果存在）
            if len(columns) >= 2:
                self.vis_x_column.value = columns[0]
                self.vis_y_column.value = columns[1]
                self.update_visualization_x_data()
                self.update_visualization_y_data()
                
        except Exception as ex:
            ui.notify(f'❌ Excel文件读取失败: {str(ex)}', type='negative')
    
    def update_visualization_x_data(self):
        """更新可视化功能的X轴数据"""
        if self.excel_data is not None and self.vis_x_column.value:
            try:
                x_data = self.excel_data[self.vis_x_column.value].dropna().tolist()
                x_str = ', '.join(str(x) for x in x_data)
                self.vis_x_input.set_value(x_str)
            except Exception as e:
                ui.notify(f'❌ X轴数据更新失败: {str(e)}', type='negative')
    
    def update_visualization_y_data(self):
        """更新可视化功能的Y轴数据"""
        if self.excel_data is not None and self.vis_y_column.value:
            try:
                y_data = self.excel_data[self.vis_y_column.value].dropna().tolist()
                y_str = ', '.join(str(y) for y in y_data)
                self.vis_y_input.set_value(y_str)
            except Exception as e:
                ui.notify(f'❌ Y轴数据更新失败: {str(e)}', type='negative')
    
    def preview_visualization_data(self):
        """预览可视化功能的数据"""
        if self.excel_data is None:
            self.visualization_preview.content = '<div class="text-red-500 text-center p-4">❌ 请先上传Excel文件</div>'
            return
        
        try:
            # 创建预览表格
            preview_df = self.excel_data.head(10)  # 只显示前10行
            
            html_table = '<div class="overflow-x-auto"><table class="w-full border-collapse border border-gray-300">'
            html_table += '<thead><tr class="bg-gray-100">'
            for col in preview_df.columns:
                html_table += f'<th class="border border-gray-300 px-2 py-1 text-left">{col}</th>'
            html_table += '</tr></thead><tbody>'
            
            for _, row in preview_df.iterrows():
                html_table += '<tr>'
                for val in row:
                    html_table += f'<td class="border border-gray-300 px-2 py-1">{val}</td>'
                html_table += '</tr>'
            html_table += '</tbody></table></div>'
            
            total_rows = len(self.excel_data)
            html_table += f'<p class="text-sm text-gray-600 mt-2">显示前10行，共{total_rows}行数据</p>'
            
            self.visualization_preview.content = html_table
            
        except Exception as e:
            self.visualization_preview.content = f'<div class="text-red-500 text-center p-4">❌ 预览失败: {str(e)}</div>'
    
    def plot_data(self):
        """绘制数据图表"""
        x_str = self.vis_x_input.value
        y_str = self.vis_y_input.value
        chart_type = self.chart_type.value
        
        if not x_str or not y_str:
            self.vis_result.content = '❌ 请输入X和Y数据'
            return
        
        try:
            # 改进数据转换逻辑
            x_parts = [x.strip() for x in x_str.split(',')]
            y_parts = [y.strip() for y in y_str.split(',')]
            
            # 处理X数据
            x_data = []
            for i, x in enumerate(x_parts):
                try:
                    # 尝试转换为数字
                    x_data.append(float(x))
                except ValueError:
                    # 如果不能转换为数字，保留字符串
                    x_data.append(x)
            
            # 处理Y数据
            y_data = []
            for y in y_parts:
                try:
                    y_data.append(float(y))
                except ValueError:
                    raise ValueError(f"Y数据 '{y}' 不是有效数字")
            
            if len(x_data) != len(y_data):
                self.vis_result.content = '<div class="text-red-500 text-center p-4">❌ X和Y数据数量不一致</div>'
                return
            
            img_base64 = create_visualization_plot(x_data, y_data, chart_type)
            
            self.vis_result.content = f'''
            <div class="text-center">
                <h3 class="text-lg font-bold mb-4">{chart_type}可视化结果</h3>
                <img src="data:image/png;base64,{img_base64}" class="w-full h-auto rounded-lg shadow-lg">
            </div>
            '''
            
        except Exception as e:
            self.vis_result.content = f'<div class="text-red-500 text-center p-4">❌ 错误: {str(e)}</div>'
