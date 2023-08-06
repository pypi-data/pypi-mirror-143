from setuptools import setup, find_packages

VERSION = '0.0.5a8'
DESCRIPTION = 'Web-based point of sale system.'

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="openwebpos",
    version=VERSION,
    url="https://github.com/baezfb/openwebpos",
    author="Javier Baez",
    author_email="baezdevs@gmail.com",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages('src', exclude=['test*']),
    include_package_data=True,
    package_dir={'': 'src'},
    install_requires=[
        "flask ~= 2.0",
        "Flask-SQLAlchemy ~= 2.5",
        "Flask-WTF ~= 1.0",
        "Flask-Login ~=0.5",
        "Flask-Migrate ~= 3.1",
        "mysqlclient ~= 2.1",
        "python-dotenv ~= 0.19"
    ],
    keywords=['python', 'pos', 'point-of-sale'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Framework :: Flask",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    extras_require={
        "dev": [
            "markdown ~= 3.3"
        ]
    },
)
