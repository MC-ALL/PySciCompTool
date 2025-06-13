import signal
import sys
from nicegui import ui
from calculator import ScientificCalculator

def signal_handler(sig, frame):
    """处理键盘中断信号"""
    print('\n🛑 收到中断信号，正在退出程序...')
    sys.exit(0)

def main():
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    
    # 设置应用配置
    ui.page_title = '高级科学计算器'
    
    try:
        # 创建计算器实例
        _ = ScientificCalculator()
        
        print('🚀 高级计算器启动中...')
        print('💡 在浏览器中访问: http://localhost:8080')
        print('⚡ 按 Ctrl+C 退出程序')
        
        # 启动应用
        ui.run(
            title='高级科学计算器',
            reload=False, 
            port=8080,
            show=True,
            favicon='🧮'
        )
    except KeyboardInterrupt:
        print('\n🛑 收到键盘中断，正在退出程序...')
        sys.exit(0)
    except Exception as e:
        print(f'❌ 程序运行出错: {str(e)}')
        sys.exit(1)
    finally:
        print('👋 程序已退出')

if __name__ == "__main__":
    main()
