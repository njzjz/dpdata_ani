from setuptools import setup
setup(
    name="dpdata-ani",
    version="0.0.1",
    install_requires = [
        "dpdata>=0.2.5", # 0.2.7
        "torchani",
        "torch",
        "numpy",
    ],
    entry_points = {
        'dpdata.plugins': [
            'anidriver=dpdata_ani.anidriver:ANIDriver'
        ]
    },
    packages = ['dpdata_ani'],
)
