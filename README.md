# Demoblaze E2E Test Automation with Selenium, Pytest And Docker
This is an end-to-end UI test automation project for [www.demoblaze.com](https://www.demoblaze.com/), built with **Selenium WebDriver**, **Pytest**, and **Allure Reporting**. It follows the **Page Object Model (POM)** design pattern for maintainable and scalable test architecture. The tests support local execution on Chrome and Firefox, as well as remote execution via **Selenium Grid** using Docker. A **CI pipeline with Github Actions** builds, runs, and publishes the Allure test report to Github Pages: [https://andreiiav.github.io/Demoblaze-Selenium-Automation](https://andreiiav.github.io/Demoblaze-Selenium-Automation).

# Features
- Cross-browser testing: Chrome & Firefox 
- Dockerized Selenium Grid support
- Page Object Model (POM) architecture for clean and maintainable code
- Modular Pytest fixture structure
- CI pipeline with Github Actions
- Automated Allure report deployment to Github Pages

# Setup
**Requirements**
- Python 3.10 or higher
- UV
- Docker & Docker Compose (to run tests with Docker)
- Chrome, Firefox and ChromeDriver, GeckoDriver (to run tests without Docker)

**Steps to run:**

**Clone the repository**:\
`git clone https://github.com/AndreiIav/Demoblaze-Selenium-Automation.git`\
`cd Demoblaze-Selenium-Automation`

**Install Dependencies**\
`uv sync`

**Running tests locally**\
`uv run pytest`

**Running tests using Selenium Grid (with Docker)**

**Start Selenium Grid and the test container**\
`docker compose up --build`

**To tear everything down**\
`docker compose down`


# Custom Pytest CLI Options
| Option            | Description                    |
| ----------------- | ------------------------------ |
| `--headless`      | Run browser in headless mode   |
| `--selenium_grid` | Use Selenium Grid (via Docker) |

# Tools and Technologies
- Python + Pytest
- Selenium WebDriver
- Selenium Grid
- Docker and Docker Compose
- Github Actions
- Allure Reports


