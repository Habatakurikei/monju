import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="monju",
    version="0.1.0",
    author="Daisuke Yamaguchi",
    author_email="daicom0204@gmail.com",
    description="A python library for brainstorming by multiple LLMs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/monju/",
    project_urls={
        'Homepage': 'https://habatakurikei.com/',
        'GitHub': 'https://github.com/Habatakurikei/monju',
    },
    packages=setuptools.find_packages(include=['monju', 'monju.*']),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=[
        "llmmaster>=0.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "flake8>=6.0",
        ],
    },
)
