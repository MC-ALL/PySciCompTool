import pytest
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from io import StringIO
from utils import (
    safe_eval,
    solve_equation,
    compute_derivative,
    compute_integral,
    compute_statistics,
    curve_fitting,
    compute_fft,
    create_fft_plot,
    create_fitting_plot,
    create_visualization_plot,
    plot_to_base64
)

class TestCoreFunctions:
    """测试utils.py所有核心函数（修正版）"""

    # 1. 基础计算测试
    def test_safe_eval(self):
        """测试安全表达式求值"""
        assert safe_eval("2+3*4") == 14
        assert safe_eval("sin(np.pi/2) + log(e**2)") == pytest.approx(3)
        assert safe_eval("2^3 + 3^2") == 17  # 测试^转**
        with pytest.raises(ValueError, match="计算错误"):
            safe_eval("__import__('os').system('ls')")

    # 2. 方程求解测试（修正版）
    def test_solve_equation(self):
        """测试方程求解功能"""
        # 一元方程
        res = solve_equation("x**2 - 4 = 0", "x")
        assert sorted([float(x) for x in res]) == pytest.approx([-2.0, 2.0])
        
        # 方程组（使用SymPy符号比较）
        x, y = sp.symbols('x y')
        sol = solve_equation("x + y - 5, x - y - 1", "x,y")
        assert str(sol) == "{x: 3, y: 2}"       

    # 3. 傅里叶变换测试
    def test_fft(self):
        """测试FFT计算"""
        t, signal, xf, yf = compute_fft(5, 1, 100, 0.1)
        assert len(t) == 100
        assert len(signal) == 100
        assert np.argmax(np.abs(yf[:50])) == 5
    
    # 4. 微积分测试
    def test_calculus(self):
        """测试微积分功能"""
        # 导数
        assert str(compute_derivative("x**3 + sin(x)", "x")) == "3*x**2 + cos(x)"
        # 不定积分
        assert str(compute_integral("3*x**2 + cos(x)", "x")) == "x**3 + sin(x)"
        # 定积分
        assert compute_integral("sin(x)", "x", "0", "pi/2") == pytest.approx(1)

    # 5. 统计分析测试
    def test_statistics(self):
        """测试统计分析功能"""
        stats = compute_statistics("1,2,3,4,5,6,7,8,9,10")
        assert stats["mean"] == 5.5
        assert stats["std"] == pytest.approx(2.87228, rel=1e-4)
        with pytest.raises(ValueError):
            compute_statistics("")

    # 6. 曲线拟合测试
    def test_curve_fitting(self):
        """测试曲线拟合"""
        # 线性拟合
        poly, r2, _, _ = curve_fitting("1,2,3,4", "2,4,6,8", 1)
        assert r2 > 0.999
        assert abs(poly(2.5) - 5) < 0.001
        
        # 二次拟合
        poly, r2, _, _ = curve_fitting("1,2,3,4", "1,4,9,16", 2)
        assert r2 > 0.99
        assert abs(poly(2.5) - 6.25) < 0.1

    # 7. 可视化功能测试（修正版）
    def test_plot_generation(self):
        """测试图表生成"""
        # FFT图（检查Base64数据长度）
        fft_img = create_fft_plot(5, 1, 100, 0.1)
        assert len(fft_img) > 1000
        
        # 散点图
        scatter_img = create_visualization_plot([1,2,3], [1,4,9], "散点图")
        assert scatter_img.startswith("iVBOR")
        
        # 拟合图
        fit_img, _, _ = create_fitting_plot("1,2,3", "2,4,6", 1)
        assert len(fit_img) > 1000


 
  

if __name__ == "__main__":
    pytest.main(["-v", __file__])