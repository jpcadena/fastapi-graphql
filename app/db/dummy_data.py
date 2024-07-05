"""
A module for dummy data in the app.db package.
"""

from pydantic import EmailStr, PositiveInt

employers: list[dict[str, int | str]] = [
    {
        "id": 1,
        "name": "MetaTechA",
        "contact_email": "contact@company-a.com",
        "industry": "Tech",
    },
    {
        "id": 2,
        "name": "MoneySoftB",
        "contact_email": "contact@company-b.com",
        "industry": "Finance",
    },
]
jobs: list[dict[str, int | str]] = [
    {
        "id": 1,
        "title": "Software Engineer",
        "description": "Develop web applications",
        "employer_id": 1,
    },
    {
        "id": 2,
        "title": "Data Analyst",
        "description": "Analyze data and create reports",
        "employer_id": 1,
    },
    {
        "id": 3,
        "title": "Accountant",
        "description": "Manage financial records",
        "employer_id": 2,
    },
]
users: list[dict[str, str | EmailStr]] = [
    {
        "username": "andybeak",
        "email": "andybeak@gmail.com",
        "password": "Password123.",
        "role": "admin",
    },
    {
        "username": "jpcadena",
        "email": "jpcadena@gmail.com",
        "password": "Clave123-",
        "role": "admin",
    },
    {
        "username": "ingi",
        "email": "ingi17@hotmail.com",
        "password": "Bimilbeonho11_",
        "role": "user",
    },
]
applications: list[dict[str, PositiveInt]] = [
    {
        "user_id": 1,
        "job_id": 1,
    },
    {
        "user_id": 1,
        "job_id": 2,
    },
    {
        "user_id": 2,
        "job_id": 1,
    },
    {
        "user_id": 2,
        "job_id": 2,
    },
    {
        "user_id": 2,
        "job_id": 3,
    },
]
