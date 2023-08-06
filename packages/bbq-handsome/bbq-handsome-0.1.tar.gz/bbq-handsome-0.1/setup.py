from setuptools import setup,find_packages
setup(
    name="bbq-handsome",
    version="0.1",
    author="谢秉求，李亚成，郭高举",
    #url="ckh.handsome.com", 此网站需要存在且未被占用
    packages = find_packages("bbq"), # 模块的保存目录
    package_dir = {"":"bbq"}, # 告诉 setuptools 包都在 ckh 下
    package_data = {
        # 定义打包除了 .py 之外的文件类型，此处 .py 其实可以不写
        "":[".txt",".info","*.properties",".py"],
        # 包含 data 文件夹下所有的 *.dat 文件
        "":["data/*.*"],
    },
    # 取消所有测试包
    exclude = ["*.test","*.test.*","test.*","test"]
)
