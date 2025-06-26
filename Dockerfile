FROM python:3.12-slim-bookworm

# set working directory
WORKDIR /usr/app 

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 


# install UV
RUN pip install uv

# install python dependencies
COPY uv.lock .
COPY pyproject.toml .
RUN uv sync 

# add project
COPY . .

CMD ["uv", "run", "pytest", "--selenium_grid"]