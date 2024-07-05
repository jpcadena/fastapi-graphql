# fastapi-graphql

<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>

<!-- PROJECT SHIELDS -->
<!--
*** Markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
-->

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="assets/images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Fastapi GraphQL project</h3>

  <p align="center">
    Fastapi backend using GraphQL API
    <br />
    <a href="https://github.com/jpcadena/fastapi-graphql"><strong>Explore the
docs
»</strong></a>
    <br />
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
       <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#security">Security</a></li>
    <li><a href="#code-of-conduct">Code of Conduct</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

![Project][project-screenshot]

This backend project is a FastAPI-based template designed to serve as a robust,
reliable, and GraphQL API backend. It is crucial for facilitating user
authentication, real-time data processing, and deployment as serverless
functions.
By leveraging GraphQL, this API ensures flexible and efficient data retrieval,
addressing the limitations of REST APIs.

This project covers topics from basic GraphQL concepts to advanced features
like authentication, ORM integration, and deployment.


<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built with

This project is built using a suite of modern, powerful technologies and
frameworks to ensure high performance, ease of development, and robustness:

[![Python][python-shield]][python-url] [![FastAPI][fastapi-shield]][fastapi-url] [![Graphene][graphene-shield]][graphene-url] [![GraphQL Playground][graphql-playground-shield]][graphql-playground-url] [![Pydantic][pydantic-shield]][pydantic-url] [![Starlette][starlette-shield]][starlette-url] [![Uvicorn][uvicorn-shield]][uvicorn-url] [![postgresql][postgresql-shield]][postgresql-url] [![Redis][redis-shield]][redis-url] [![JWT][jwt-shield]][jwt-url] [![HTML5][html5-shield]][html5-url] [![CSS3][css3-shield]][css3-url] [![isort][isort-shield]][isort-url] [![Black][black-shield]][black-url] [![Ruff][ruff-shield]][ruff-url] [![MyPy][mypy-shield]][mypy-url] [![pre-commit][pre-commit-shield]][pre-commit-url] [![GitHub Actions][github-actions-shield]][github-actions-url] [![Poetry][poetry-shield]][poetry-url] [![Pycharm][pycharm-shield]][pycharm-url] [![Visual Studio Code][visual-studio-code-shield]][visual-studio-code-url] [![Markdown][markdown-shield]][markdown-url] [![Swagger UI][swagger-ui-shield]][swagger-ui-url] [![License: MIT][license-shield]][license-url]

### Components

The system is composed of the following main components, each playing a
crucial role in providing a scalable, maintainable, and robust application:

- **FastAPI Backend**: Serves as the core of the GraphQL API, handling incoming
  HTTP requests, processing data, and sending responses. It's designed for high
  performance and encourages standard API development practices.
- **Graphene**: A Python library for building GraphQL APIs, providing a simple
  and powerful way to define schemas and handle queries and mutations.
- **SQLAlchemy ORM**: Used for database interactions, providing a high-level
  and pythonic way to interact with relational databases.
- **JWT Authentication**: Implements secure authentication mechanisms using JSON
  Web Tokens (JWT), ensuring secure access to the API.

This project adheres to GraphQL design principles, ensuring an intuitive and
standard approach to API development. This design facilitates easy integration,
scalability, and interaction with various clients, including web and mobile
applications. The API provides flexible query and mutation capabilities, uses
JWT for secure, stateless authentication, and can be deployed as serverless
functions for scalability and cost-efficiency.


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting started

### Prerequisites

- [Python 3.11][python-docs]

### Installation

1. Clone the **repository**

   ```bash
   git clone https://github.com/jpcadena/fastapi-graphql.git
   ```

2. Change the directory to **root project**

   ```bash
   cd fastapi-graphql
   ```

3. Install **Poetry** package manager

   ```bash
   pip install poetry
   ```

4. Install the project's **dependencies**

   ```bash
   poetry install
   ```

5. Activate the **environment**

   ```bash
   poetry shell
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Usage

1. **Setting up environment variables:**

   If you find a `.env.sample` in the project directory, make a copy of it and
   rename to `.env`.

   ```bash
   cp .env.sample .env
   ```

   This `.env` file will be used to manage your application's environment
   variables.

2. **Configuring your credentials:**

   Open the `.env` file in a text editor and replace the placeholder values with
   your actual credentials.

   ```bash
   # .env file
   POSTGRES_USER=your_database_user
   SECRET_KEY=your_api_key
   ```

   Be sure to save the file after making these changes.

3. **Generating RSA keys**

   To ensure secure communication in this project, RSA keys are used. Before
   running the application, you need to generate a public and private RSA key
   pair.
   We've provided a Python script to automatically generate these keys. You can
   find the script at `app\services\infrastructure\encryption.py`. To generate
   your keys, simply run:

    ```bash
    python app\services\infrastructure\encryption.py
    ```

   This will create `public_key.pem` and `private_key.pem` files in your
   specified directory.

   Once the keys are generated, the application will use them for cryptographic
   operations. Ensure that these files are kept secure and are not exposed
   publicly. The default configuration expects these keys in the root directory
   of the project.

4. **Starting the server:**

   To start the local server on your machine, run the following command in your
   terminal:

   ```bash
   uvicorn main:app --reload
   ```

   The `--reload` flag enables hot reloading, which means the server will
   automatically update whenever you make changes to the code.

5. **Interacting with the app:**

   Once your server is running, you can interact with it using any API client
   like Postman or your web browser. You can send GraphQL queries and mutations
   to the API endpoints as defined in your main.py file. For example, to get all
   users, you can send a query to http://localhost:8000/graphql.

6. **Using GraphQL Playground:**

   FastAPI provides automatic interactive API documentation using GraphQL
   Playground. Once your server is up and running, you can go
   to http://localhost:8000/graphql in your web browser to access it. From
   there, you can explore and interact with your API directly.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTRIBUTING -->

## Contributing

[![GitHub][github-shield]][github-url]

Please read our [contributing guide](CONTRIBUTING.md) for details on our code of
conduct, and the process for submitting pull requests to us.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- SECURITY -->

## Security

For security considerations and best practices, please refer to
our [Security Guide](SECURITY.md) for a detailed guide.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CODE_OF_CONDUCT -->

## Code of Conduct

We enforce a code of conduct for all maintainers and contributors. Please read
our [Code of Conduct](CODE_OF_CONDUCT.md) to understand the expectations before
making any contributions.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->

## Contact

- [![LinkedIn][linkedin-shield]][linkedin-url]

- [![Outlook][outlook-shield]](mailto:jpcadena@espol.edu.ec?subject=[GitHub]fastapi-graphql)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[project-screenshot]: assets/images/project.png

[python-docs]: https://docs.python.org/3.11/

[linkedin-shield]: https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white

[outlook-shield]: https://img.shields.io/badge/Microsoft_Outlook-0078D4?style=for-the-badge&logo=microsoft-outlook&logoColor=white

[python-shield]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54

[fastapi-shield]: https://img.shields.io/badge/FastAPI-FFFFFF?style=for-the-badge&logo=fastapi

[pydantic-shield]: https://img.shields.io/badge/Pydantic-FF43A1?style=for-the-badge&logo=pydantic&logoColor=white

[starlette-shield]: https://img.shields.io/badge/Starlette-392939?style=for-the-badge&logo=starlette&logoColor=white

[uvicorn-shield]: https://img.shields.io/badge/Uvicorn-2A308B?style=for-the-badge&logo=uvicorn&logoColor=white

[redis-shield]: https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white

[html5-shield]: https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white

[jwt-shield]: https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens

[pycharm-shield]: https://img.shields.io/badge/PyCharm-21D789?style=for-the-badge&logo=pycharm&logoColor=white

[markdown-shield]: https://img.shields.io/badge/Markdown-000000?style=for-the-badge&logo=markdown&logoColor=white

[swagger-ui-shield]: https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white

[github-shield]: https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white

[ruff-shield]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json

[black-shield]: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge&logo=appveyor

[mypy-shield]: https://img.shields.io/badge/mypy-checked-2A6DB2.svg?style=for-the-badge&logo=appveyor

[visual-studio-code-shield]: https://img.shields.io/badge/Visual_Studio_Code-007ACC?style=for-the-badge&logo=visual-studio-code&logoColor=white

[poetry-shield]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/python-poetry/website/main/static/badge/v0.json

[postgresql-shield]: https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white

[isort-shield]: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336

[github-actions-shield]: https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white

[pre-commit-shield]: https://img.shields.io/badge/pre--commit-F7B93E?style=for-the-badge&logo=pre-commit&logoColor=white

[css3-shield]: https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white

[license-shield]: https://img.shields.io/badge/License-MIT-yellow.svg

[graphene-shield]: https://img.shields.io/badge/Graphene-FF6F3F?style=for-the-badge&logo=graphql&logoColor=white

[graphql-playground-shield]: https://img.shields.io/badge/GraphQL%20Playground-E535AB?style=for-the-badge&logo=graphql&logoColor=white

[linkedin-url]: https://linkedin.com/in/juanpablocadenaaguilar

[python-url]: https://docs.python.org/3.11/

[fastapi-url]: https://fastapi.tiangolo.com

[pydantic-url]: https://docs.pydantic.dev

[starlette-url]: https://www.starlette.io/

[uvicorn-url]: https://www.uvicorn.org/

[redis-url]: https://redis.io/

[html5-url]: https://developer.mozilla.org/en-US/docs/Glossary/HTML5

[jwt-url]: https://jwt.io/

[pycharm-url]: https://www.jetbrains.com/pycharm/

[markdown-url]: https://daringfireball.net/projects/markdown/

[swagger-ui-url]: https://swagger.io/

[github-url]: https://github.com/jpcadena/fastapi-graphql

[ruff-url]: https://beta.ruff.rs/docs/

[black-url]: https://github.com/psf/black

[mypy-url]: http://mypy-lang.org/

[visual-studio-code-url]: https://code.visualstudio.com/

[poetry-url]: https://python-poetry.org/

[postgresql-url]: https://www.postgresql.org/

[isort-url]: https://pycqa.github.io/isort/

[github-actions-url]: https://github.com/features/actions

[pre-commit-url]: https://pre-commit.com/

[css3-url]: https://developer.mozilla.org/en-US/docs/Web/CSS

[license-url]: https://opensource.org/licenses/MIT

[graphene-url]: https://docs.graphene-python.org/en/latest/

[graphql-playground-url]: https://github.com/graphql/graphql-playground
