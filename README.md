# ProgettoBCC
<p align="left">
    <img alt="AGPL-3.0 license" src="https://img.shields.io/github/license/AlBovo/ProgettoBCC">
    <img alt="GitHub issues" src="https://img.shields.io/github/issues/AlBovo/ProgettoBCC">
    <img alt="GitHub language count" src="https://img.shields.io/github/languages/count/albovo/ProgettoBCC">
</p>

This repository is about a project related to the _[BCC Bank's scholarship](https://www.labcc.it/)_ for the academic year 2023/2024. <br>

This project was designed to make communication between bank employees and customers faster and more effective, making consultations easily accessible and editable through a simple and clear style.
In the development of the website, many knowledge and techniques that the group studied at __[ITT Blaise Pascal](https://www.ispascalcomandini.it)__ over the years in various subjects were also implemented and used.<br>

## Run Locally

Clone the project and go inside the project directory

```bash
  git clone https://github.com/AlBovo/ProgettoBCC.git
  cd ProgettoBCC
```

Create the `.env` file and set `MYSQL_DATABASE` and `MYSQL_ROOT_PASSWORD` inside it, here it is an example

```env
MYSQL_DATABASE=database
MYSQL_ROOT_PASSWORD=f5hFaMuZRC7x9Qb27EdRCuDaz7CPFa
```

To start the site you now just have to run `docker compose up --build`.<br>
Additionally, you can use `cleanDocker.sh` script which will delete all the containers, images and volumes of this project. 

```bash
  ./scripts/cleanDocker.sh
```
