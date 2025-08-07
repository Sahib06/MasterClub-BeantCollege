from setuptools import setup, find_packages

setup(
    name="college_attendance",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "pydantic",
        "qrcode",
        "pillow",
        "python-multipart",
        "passlib",
        "python-dotenv",
    ],
) 