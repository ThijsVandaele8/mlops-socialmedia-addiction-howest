from setuptools import setup, find_packages

setup(
    name="socialmedia_mlops",
    version="0.1.2",
    description="Package voor social media addiction ML project",
    author="Thijs Vandaele",
    packages=find_packages(where="src"),
    package_dir={"": "src"}, 
    install_requires=[
        "pandas",
        "numpy",
        "scikit-learn",
        "mlflow",
        "pycountry_convert"
    ],
    python_requires=">=3.11",
)
