"""
Setup.py - Configuración del paquete
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="chatbot-turismo-huaraz",
    version="1.0.0",
    author="Tu Nombre",
    description="Chatbot turístico inteligente para Huaraz con IA agéntica",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "langchain>=0.1.0",
        "langchain-google-genai>=0.0.1",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0",
        "pydantic>=2.0.0",
    ],
)
