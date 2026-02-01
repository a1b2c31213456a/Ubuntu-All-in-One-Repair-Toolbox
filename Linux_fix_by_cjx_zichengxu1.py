# !/usr/bin/env python3


import os
import subprocess
import sys
import platform


def check_platform():
    os.system('clear')
    """检查操作系统平台"""
    system = platform.system().lower()
    if system != 'linux':
        print(f"警告: 此工具专为Linux系统设计，当前系统为{system}")
        response = input("是否继续运行? (y/N): ").strip().lower()
        if response not in ['y', 'yes']:
            print("程序已退出")
            return False
    return True


def check_root():
    os.system('clear')
    """检查是否具有root权限"""
    # Windows系统没有root概念，直接返回True
    if platform.system().lower() == 'windows':
        print("Windows系统无需检查root权限")
        return True

    # Linux系统检查root权限
    try:
        if os.geteuid() != 0:
            print("需要root权限来安装软件包，请使用sudo运行此脚本")
            return False
    except AttributeError:
        # 兜底处理，某些情况下可能没有geteuid方法
        print("无法检测root权限，假设已有足够权限继续执行")
    return True


def update_package_list():
    """更新软件包列表"""
    os.system('clear')
    print("正在更新软件包列表...")
    try:
        if platform.system().lower() == 'windows':
            print("Windows系统无需更新Linux软件包列表")
            return True
        subprocess.run(['apt-get', 'update'], check=True, stdout=subprocess.DEVNULL)
        print("软件包列表更新完成")
        return True
    except subprocess.CalledProcessError:
        print("软件包列表更新失败")
        return False
    except FileNotFoundError:
        print("未找到apt命令，请确保在Ubuntu/Debian系统上运行")
        return False


def install_window_manager(manager_name, package_name, description):
    """安装指定的窗口管理器"""
    os.system('clear')
    print(f"\n正在安装{description}...")
    try:
        if platform.system().lower() == 'windows':
            print(f"Windows系统模拟安装{description}...")
            print("(实际环境中请在Linux系统上运行)")
            return True
        # 安装窗口管理器
        result = subprocess.run(['apt-get', 'install', '-y', package_name],
                                check=True, capture_output=True, text=True)
        print(f"{description}安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{description}安装失败: {e}")
        return False
    except FileNotFoundError:
        print("未找到apt命令，请确保在Ubuntu/Debian系统上运行")
        return False


def install_xorg():
    """安装Xorg显示服务器"""
    os.system('clear')
    print("正在安装Xorg显示服务器...")
    try:
        if platform.system().lower() == 'windows':
            print("Windows系统模拟安装Xorg...")
            print("(实际环境中请在Linux系统上运行)")
            return True
        subprocess.run(['apt-get', 'install', '-y', 'xserver-xorg'],
                       check=True, stdout=subprocess.DEVNULL)
        print("Xorg显示服务器安装成功")
        return True
    except subprocess.CalledProcessError:
        print("Xorg显示服务器安装失败")
        return False
    except FileNotFoundError:
        print("未找到apt命令，请确保在Ubuntu/Debian系统上运行")
        return False


def install_login_manager():
    """安装登录管理器"""
    os.system('clear')
    print("正在安装登录管理器...")
    try:
        if platform.system().lower() == 'windows':
            print("Windows系统模拟安装登录管理器...")
            print("(实际环境中请在Linux系统上运行)")
            return True
        subprocess.run(['apt-get', 'install', '-y', 'lightdm'],
                       check=True, stdout=subprocess.DEVNULL)
        print("登录管理器安装成功")
        return True
    except subprocess.CalledProcessError:
        print("登录管理器安装失败")
        return False
    except FileNotFoundError:
        print("未找到apt命令，请确保在Ubuntu/Debian系统上运行")
        return False


def install_window_managers():
    """提供窗口管理器选择菜单"""
    os.system('clear')
    managers = {
        '1': {'name': 'Openbox', 'package': 'openbox', 'description': '轻量级窗口管理器'},
        '2': {'name': 'Fluxbox', 'package': 'fluxbox', 'description': '快速轻量级窗口管理器'},
        '3': {'name': 'Blackbox', 'package': 'blackbox', 'description': '极简窗口管理器'},
        '4': {'name': 'Awesome', 'package': 'awesome', 'description': '高度可配置的动态窗口管理器'},
        '5': {'name': 'Enlightenment', 'package': 'enlightenment', 'description': '现代化窗口管理器'},
        '6': {'name': 'i3', 'package': 'i3', 'description': '平铺式窗口管理器'}
    }

    print("\n可用的窗口管理器:")
    for key, value in managers.items():
        print(f"{key}) {value['name']} - {value['description']}")

    print("0) 返回主菜单")

    choice = input("\n请选择要安装的窗口管理器 (0-6): ").strip()

    if choice == '0':
        return False

    if choice in managers:
        manager = managers[choice]
        print(f"\n安装选项:")
        print(f"1) 仅安装{manager['name']}")
        print(f"2) 安装{manager['name']} + Xorg + 登录管理器")
        sub_choice = input("请选择安装方式 (1-2): ").strip()

        if sub_choice == '1':
            # 仅安装窗口管理器
            return install_window_manager(manager['name'], manager['package'], manager['description'])
        elif sub_choice == '2':
            # 安装完整环境
            success = True
            if not install_xorg():
                success = False
            if not install_window_manager(manager['name'], manager['package'], manager['description']):
                success = False
            if not install_login_manager():
                success = False
            return success
        else:
            print("无效选择")
            return False
    else:
        print("无效选择")
        return False


def install_desktop_environment():
    """安装桌面环境"""
    os.system('clear')
    print("\n可选的桌面环境:")
    print("1) Xubuntu (Xfce)")
    print("2) Kubuntu (KDE)")
    print("3) Ubuntu Budgie")
    print("4) Ubuntu MATE")
    print("0) 返回主菜单")

    choice = input("\n请选择要安装的桌面环境 (0-4): ").strip()

    if choice == '0':
        return False

    desktop_envs = {
        '1': {'name': 'Xubuntu', 'package': 'xubuntu-desktop'},
        '2': {'name': 'Kubuntu', 'package': 'kubuntu-desktop'},
        '3': {'name': 'Ubuntu Budgie', 'package': 'ubuntu-budgie-desktop'},
        '4': {'name': 'Ubuntu MATE', 'package': 'ubuntu-mate-desktop'}
    }

    if choice in desktop_envs:
        env = desktop_envs[choice]
        print(f"\n正在安装{env['name']}...")
        try:
            if platform.system().lower() == 'windows':
                print(f"Windows系统模拟安装{env['name']}...")
                print("(实际环境中请在Linux系统上运行)")
                return True
            subprocess.run(['apt-get', 'install', '-y', env['package']],
                           check=True, stdout=subprocess.DEVNULL)
            print(f"{env['name']}安装成功")
            return True
        except subprocess.CalledProcessError:
            print(f"{env['name']}安装失败")
            return False
        except FileNotFoundError:
            print("未找到apt命令，请确保在Ubuntu/Debian系统上运行")
            return False
    else:
        print("无效选择")
        return False

def banben_by():
    os.system('clear')
    print('\n \n⚠ 注意：本程序为陈俊旭开发的Ubuntu常用快捷命令控制台的子程序！！！！！')
    print('子程序版本:version 1正式版')
def main():
    """主菜单"""
    os.system('clear')
    print("=" * 50)
    print("Ubuntu桌面专用修复子程序")
    print("=" * 50)

    if not check_platform():
        sys.exit(1)

    if not check_root():
        sys.exit(1)

    if not update_package_list():
        sys.exit(1)

    while True:
        os.system('clear')
        print("\n主菜单:")
        print('⚠ 注意：本程序为陈俊旭开发的Ubuntu常用快捷命令控制台的子程序！！！！！')
        print("1) 安装窗口管理器")
        print("2) 安装桌面环境")
        print("3) 安装Xorg显示服务器")
        print("4) 安装登录管理器")
        print('5) 子程序版本信息')
        print("0) 返回主程序")

        choice = input("\n请选择操作 (0-5): ").strip()

        if choice == '0':
            print("感谢使用子程序！即将退回主程序！！！")
            os.system('python3 Linux_fix_by_cjx.py')
            break
        elif choice == '1':
            install_window_managers()
        elif choice == '2':
            install_desktop_environment()
        elif choice == '3':
            install_xorg()
        elif choice == '4':
            install_login_manager()
        elif choice == '5':
            banben_by()
        else:
            print("无效选择，请重新输入")


        input("\n按回车键继续...")


if __name__ == "__main__":
    main()
