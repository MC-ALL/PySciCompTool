import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
import io
import base64

# 设置全局绘图参数
plt.rcParams['font.family'] = ['Microsoft YaHei', 'DejaVu Sans', 'Arial']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'

def safe_eval(expr):
    """安全评估数学表达式"""
    # 替换常见的数学符号
    expr = expr.replace('^', '**').replace('π', 'pi')
    
    try:
        # 安全地评估表达式
        result = eval(expr, {'__builtins__': None}, {
            'np': np, 
            'sin': np.sin, 
            'cos': np.cos, 
            'tan': np.tan, 
            'sqrt': np.sqrt,
            'log': np.log,
            'exp': np.exp,
            'pi': np.pi,
            'e': np.e,
            'abs': abs,
            'pow': pow
        })
        return result
    except Exception as e:
        raise ValueError(f'计算错误: {str(e)}')

def solve_equation(eq_str, var_str):
    """求解方程"""
    try:
        # 处理变量
        variables = [sp.Symbol(v.strip()) for v in var_str.split(',')]
        
        # 处理方程
        equations = []
        for part in eq_str.split(','):
            part = part.strip()
            # 替换常见符号
            part = part.replace('^', '**').replace('π', 'pi').replace('e', 'E')
            
            if '=' in part:
                lhs, rhs = part.split('=')
                equations.append(sp.Eq(sp.sympify(lhs.strip()), sp.sympify(rhs.strip())))
            else:
                equations.append(sp.sympify(part.strip()))
        
        # 求解方程
        if len(equations) == 1 and len(variables) == 1:
            # 一元方程
            solution = sp.solve(equations[0], variables[0])
            return solution
        else:
            # 方程组
            solution = sp.solve(equations, variables)
            return solution
    except Exception as e:
        raise ValueError(f'方程求解错误: {str(e)}')

def compute_fft(freq, duration, sample_rate, noise_level):
    """计算傅里叶变换"""
    # 生成时间序列
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    # 生成信号 (正弦波 + 噪声)
    signal = np.sin(2 * np.pi * freq * t)
    noise = noise_level * np.random.normal(size=t.size)
    signal += noise
    
    # 计算FFT
    yf = fft(signal)
    xf = fftfreq(len(t), 1 / sample_rate)
    
    return t, signal, xf, yf

def compute_derivative(func_str, var_str):
    """计算导数"""
    try:
        x = sp.Symbol(var_str)
        # 替换常见符号
        func_str = func_str.replace('^', '**').replace('π', 'pi').replace('e', 'E')
        f = sp.sympify(func_str)
        derivative = sp.diff(f, x)
        return derivative
    except Exception as e:
        raise ValueError(f'导数计算错误: {str(e)}')

def compute_integral(func_str, var_str, lower_str=None, upper_str=None):
    """计算积分"""
    try:
        x = sp.Symbol(var_str)
        # 替换常见符号
        func_str = func_str.replace('^', '**').replace('π', 'pi').replace('e', 'E')
        f = sp.sympify(func_str)
        
        if lower_str is not None and upper_str is not None and lower_str != '' and upper_str != '':
            # 定积分
            lower_str = lower_str.replace('π', 'pi').replace('e', 'E')
            upper_str = upper_str.replace('π', 'pi').replace('e', 'E')
            lower = sp.sympify(lower_str)
            upper = sp.sympify(upper_str)
            integral = sp.integrate(f, (x, lower, upper))
            return integral
        else:
            # 不定积分
            integral = sp.integrate(f, x)
            return integral
    except Exception as e:
        raise ValueError(f'积分计算错误: {str(e)}')

def compute_statistics(data_str):
    """计算统计量"""
    # 转换数据为浮点数列表
    data = [float(x.strip()) for x in data_str.split(',')]
    arr = np.array(data)
    
    # 计算统计量
    stats_dict = {
        'count': len(arr),
        'mean': np.mean(arr),
        'median': np.median(arr),
        'std': np.std(arr),
        'var': np.var(arr),
        'min': np.min(arr),
        'max': np.max(arr),
        'q1': np.percentile(arr, 25),
        'q3': np.percentile(arr, 75)
    }
    return stats_dict

def curve_fitting(x_str, y_str, degree):
    """曲线拟合"""
    # 转换数据
    x_data = np.array([float(x.strip()) for x in x_str.split(',')])
    y_data = np.array([float(y.strip()) for y in y_str.split(',')])
    
    # 多项式拟合
    coeffs = np.polyfit(x_data, y_data, degree)
    poly = np.poly1d(coeffs)
    
    # 计算R平方
    residuals = y_data - poly(x_data)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y_data - np.mean(y_data))**2)
    r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
    
    # 返回拟合结果
    return poly, r_squared, x_data, y_data

def plot_to_base64(fig):
    """将matplotlib图像转换为base64字符串"""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=100, facecolor='white')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return img_base64

def create_fft_plot(freq, duration, sample_rate, noise_level):
    """创建FFT图表并返回base64图像"""
    t, signal, xf, yf = compute_fft(freq, duration, sample_rate, noise_level)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # 原始信号
    ax1.plot(t, signal, 'b-', linewidth=1)
    ax1.set_title('原始信号 (含噪声)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('时间 [s]')
    ax1.set_ylabel('幅度')
    ax1.grid(True, alpha=0.3)
    
    # FFT结果
    ax2.plot(xf[:len(xf)//2], 2.0/len(t) * np.abs(yf[:len(yf)//2]), 'r-', linewidth=2)
    ax2.set_title('傅里叶变换频谱', fontsize=14, fontweight='bold')
    ax2.set_xlabel('频率 [Hz]')
    ax2.set_ylabel('幅度')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return plot_to_base64(fig)

def create_fitting_plot(x_str, y_str, degree):
    """创建曲线拟合图表并返回base64图像和结果"""
    poly, r_squared, x_data, y_data = curve_fitting(x_str, y_str, degree)
    x_fit = np.linspace(min(x_data), max(x_data), 100)
    y_fit = poly(x_fit)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(x_data, y_data, color='blue', s=50, alpha=0.7, label='原始数据')
    ax.plot(x_fit, y_fit, 'r-', linewidth=2, label=f'{degree}次多项式拟合')
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    ax.set_title('曲线拟合结果', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return plot_to_base64(fig), poly, r_squared

def create_visualization_plot(x_data, y_data, chart_type):
    """创建数据可视化图表并返回base64图像"""
    try:
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # 处理x_data，确保数据类型正确
        if isinstance(x_data[0], str):
            # 如果是字符串数据，使用索引作为x轴
            x_values = list(range(len(x_data)))
            x_labels = x_data
        else:
            x_values = x_data
            x_labels = [str(x) for x in x_data]
        
        if chart_type == '散点图':
            ax.scatter(x_values, y_data, color='blue', s=50, alpha=0.7)
            ax.set_title('散点图', fontsize=14, fontweight='bold')
        elif chart_type == '折线图':
            ax.plot(x_values, y_data, 'o-', color='blue', linewidth=2, markersize=6)
            ax.set_title('折线图', fontsize=14, fontweight='bold')
        elif chart_type == '柱状图':
            ax.bar(x_values, y_data, color='skyblue', alpha=0.7)
            ax.set_title('柱状图', fontsize=14, fontweight='bold')
            # 设置x轴标签
            if isinstance(x_data[0], str):
                ax.set_xticks(x_values)
                ax.set_xticklabels(x_labels, rotation=45)
        elif chart_type == '饼图':
            # 饼图需要特殊处理
            labels = x_labels if isinstance(x_data[0], str) else [f'X{i}' for i in range(len(x_data))]
            # 确保y_data都是正数
            y_positive = [abs(y) for y in y_data]
            ax.pie(y_positive, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.set_title('饼图', fontsize=14, fontweight='bold')
            return plot_to_base64(fig)
        
        ax.set_xlabel('X', fontsize=12)
        ax.set_ylabel('Y', fontsize=12)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        return plot_to_base64(fig)
    except Exception as e:
        raise ValueError(f'图表绘制错误: {str(e)}')
