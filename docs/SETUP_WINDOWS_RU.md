# Запуск на Windows 11 через Ubuntu в WSL 2

Персональные данные: Amir Sembi, IT2-2307, Student ID 37693.
18 октября 2026 года пользователь прислал успешный вывод `docker run --rm hello-world`.
Это подтверждает работу Docker Desktop. Запуск самого проекта и Jenkins ещё предстоит.

## 1 Ubuntu и папка проекта

**PowerShell Windows:**

```powershell
wsl -l -v
```

Должен быть дистрибутив Ubuntu с VERSION 2. `docker-desktop` — служебная среда
Docker, её не используем как рабочий терминал. Если Ubuntu отсутствует, выполни
`wsl --install -d Ubuntu` в PowerShell администратора и следуй сообщению установки.
Если дистрибутив имеет другое имя, используй точное имя из списка.

Открой Ubuntu через Пуск или `wsl -d Ubuntu`. При первом запуске создай Linux-
пользователя (например, `amir`) и пароль. Символы пароля при вводе не отображаются.
Если Ubuntu уже настроена, используй имеющуюся среду, не переустанавливай её.

В Docker Desktop открой Settings → Resources → WSL Integration, включи Ubuntu
и нажми Apply / Apply & restart. Docker Desktop должен оставаться запущенным.

**В Ubuntu, не в PowerShell:**

```bash
docker version
docker compose version
sudo apt-get update
sudo apt-get install -y git python3 unzip
mkdir -p ~/devops
cd ~/devops
explorer.exe .
```

`docker version` должен показать Client и Server. Если команды Docker нет,
проверь интеграцию Ubuntu и заново открой её терминал. Docker Engine отдельно
через apt не устанавливай: используем уже работающий Docker Desktop.

Скачай обновлённый `DevOps_Amir_Sembi_Package.zip` из чата. В открывшееся окно
Проводника скопируй этот ZIP. Это Linux-папка `~/devops`, доступная из Windows.
Затем в Ubuntu выполни:

```bash
unzip DevOps_Amir_Sembi_Package.zip
mv DevOps_Amir_Sembi/sembi_amir ./
cd ~/devops/sembi_amir
ls -la
```

Эти команды предназначены для первой распаковки. Если `sembi_amir` уже существует,
сначала проверь её содержимое и историю Git; не заменяй существующую работу.
Рабочие исходники остаются в файловой системе Linux. Это даёт корректные Linux-
права доступа и удобное монтирование в контейнер. Папки с отчётом остаются рядом
в `~/devops/DevOps_Amir_Sembi/report`.
Сборки требуют доступа к Docker Hub, репозиториям Debian и плагинам Jenkins.

## 2 Linux и персональные данные

**В Ubuntu WSL, из папки проекта:**

```bash
docker compose -f infra/linux-compose.yml run --build --rm linux
```

Откроется Bash внутри Linux под пользователем `student`. Там проект доступен
по адресу `/home/student/devops/sembi_amir`. Это соответствует
`~/devops/sembi_amir` для Linux-пользователя. Папка примонтирована из Ubuntu WSL:
изменения в файлах сохраняются после выхода.

**В открывшемся Linux Bash:**

```bash
pwd
uname -s
bash scripts/prepare_linux.sh
python3 scripts/personalize.py --group IT2-2307 --student-id 37693
python3 scripts/validate_personalization.py
cat Sembi_Amir_info.txt
./scripts/Sembi_Amir_system.sh
python3 -m unittest discover -s tests -v
```

Данные уже заполнены. Повторный запуск восстановит `.env` после клонирования.
Скрипт обновит JSON, текстовый
файл, `.env`, пример окружения и четыре переменные в Jenkinsfile.
Проверка не даст запустить Jenkins с незаполненным Student ID.
Файл `.env` не попадёт в Git, но по условиям задания Student ID также находится
в отслеживаемом файле с информацией. Можно выбрать приватный репозиторий и
дать преподавателю доступ.

## 3 История Git

Сначала прочитай `scripts/init_history.sh`, чтобы понимать будущие коммиты.
Скрипт добавляет разные группы реальных файлов поэтапно; пустых коммитов нет.
Он создаёт семь содержательных коммитов, затем коммит в `development`
и отдельный merge-коммит. История не задним числом: все коммиты создаются при запуске.

**В Linux Bash:**

```bash
read -r -p "Git email из твоего GitHub: " lab_git_email
bash scripts/init_history.sh "Amir Sembi" "$lab_git_email"
git config user.name
git config user.email
git config --global user.name
git config --global user.email
git status
git log --oneline --graph --all
git branch
git check-ignore -v logs/application.log backup/demo.txt .env
git ls-files -- logs/application.log backup/demo.txt .env
```

Если глобальные команды не вывели значения, это нормально: скрипт задаёт
личность локально для проекта и не меняет глобальные настройки. Последняя
команда не должна вывести файлов. Это проверка отсутствия их в индексе.
Скрипт не перезаписывает существующий `.git`. Если репозиторий уже создан,
работай с ним обычными `git add` и `git commit`, не удаляй историю ради повторного запуска.

## 4 GitHub

Подключённый аккаунт для этой работы: `s1mbaq`.
Нужный репозиторий: `sembi-amir-devops`.

1. Открой https://github.com/new под своим аккаунтом.
2. Владелец: `s1mbaq`; Repository name: `sembi-amir-devops`.
3. Выбери Public либо Private с последующим доступом преподавателю.
4. Не добавляй README, `.gitignore` и лицензию при создании: они уже есть локально.
5. Нажми Create repository. Если репозиторий уже существует, проверь его
   содержимое; не перезаписывай чужие или прежние файлы.

Выйди из Linux командой `exit`. **В Ubuntu WSL:**

```bash
cd ~/devops/sembi_amir
git remote add origin https://github.com/s1mbaq/sembi-amir-devops.git
git remote -v
git push -u origin main
git push -u origin development
```

Если `origin` уже существует, сначала посмотри `git remote -v` и сравни URL.
Для HTTPS GitHub использует токен или настроенный credential helper, а не
обычный пароль аккаунта. Не вставляй токен в URL репозитория, файлы или видео.
Можно выполнить push через уже авторизованный GitHub Desktop.

После push проверь файлы, ветки и коммиты в браузере. Git установлен в Ubuntu
командой apt выше. HTTPS-токен вводи только в скрытый запрос пароля Git.
Если нужно настроить вход, остановись на этом шаге и настрой доступ к своему
аккаунту; не используй чужой аккаунт и не записывай секреты в историю команд.

## 5 Docker вручную

**В Ubuntu WSL:**

```bash
cd ~/devops/sembi_amir
docker build -t sembi-amir-devops .
docker images sembi-amir-devops
docker run -d --name sembi-amir-container -p 127.0.0.1:8080:8080 sembi-amir-devops
docker ps
docker ps -a
docker logs sembi-amir-container
curl http://localhost:8080/health
curl http://localhost:8080/api/student
```

Открой http://localhost:8080. Контейнер продолжает работать, потому что Python
обслуживает HTTP-запросы. `-d` запускает его в фоне. Проброс порта `-p` даёт
доступ из браузера; инструкция `EXPOSE` сама порт не публикует.

Демонстрация переменных окружения и жизненного цикла:

```bash
docker stop sembi-amir-container
docker start sembi-amir-container
docker exec sembi-amir-container whoami
docker stop sembi-amir-container
docker rm sembi-amir-container
set -a
source .env
set +a
docker run -d --name sembi-amir-container -p 127.0.0.1:8080:8080 \
  -e STUDENT_NAME -e STUDENT_SURNAME -e STUDENT_GROUP -e STUDENT_ID \
  sembi-amir-devops
docker logs sembi-amir-container
curl http://localhost:8080/api/student
```

Форма `-e STUDENT_NAME` передаёт текущее значение переменной из Ubuntu.
Для отдельной демонстрации переопределения можно указать
`-e STUDENT_GROUP=DEMO-GROUP`, затем вернуть настоящую группу.
Не оставляй демонстрационное значение для сдачи.

## 6 Docker Compose

Перед Compose освободи имя, занятое контейнером ручного запуска:

```bash
docker stop sembi-amir-container
docker rm sembi-amir-container
docker compose config
docker compose up --build -d
docker compose ps
docker compose logs app
curl http://localhost:8080/health
docker compose down
```

`.env` читается Compose автоматически для подстановки `${...}`. Наличие `.env`
само по себе не передаёт все значения контейнеру: для этого в YAML есть
раздел `environment`. `down` удаляет контейнер Compose и его сеть; образ остаётся.

## 7 Jenkins

**В Ubuntu WSL, из корня проекта:**

```bash
docker compose -f infra/jenkins-compose.yml up --build -d
docker compose -f infra/jenkins-compose.yml ps
docker compose -f infra/jenkins-compose.yml logs --tail=80 jenkins
docker compose -f infra/jenkins-compose.yml exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Последняя команда нужна только для первого входа. Не показывай этот пароль
в записи. Открой http://localhost:8081, разблокируй Jenkins, установи
предложенные плагины, создай локального администратора. В Jenkins URL укажи
`http://localhost:8081/`. Данные хранятся в именованном Docker volume.

Создай job:

1. New Item → имя **Sembi_Amir_DevOps** → **Pipeline** → OK.
2. В разделе Pipeline выбери **Pipeline script from SCM**.
3. SCM: **Git**.
4. Repository URL: `https://github.com/s1mbaq/sembi-amir-devops.git`.
5. Для публичного репозитория Credentials можно оставить пустым. Для приватного
   добавь **Username with password**: логин GitHub и токен с доступом на чтение
   этого репозитория в поле Password. Сохраняй его в Jenkins Credentials.
6. Branch Specifier: `*/main`.
7. Script Path: `Jenkinsfile`.
8. Save → Build Now.

Открой сборку и Console Output. Должны пройти Checkout, Build, Test,
Docker Build и Docker Run. В конце сам Jenkins должен вывести **Finished: SUCCESS**.
Открой http://localhost:8082 и проверь реальные персональные данные.

Проверить окружение Jenkins и результаты:

```bash
docker compose -f infra/jenkins-compose.yml exec jenkins python3 --version
docker compose -f infra/jenkins-compose.yml exec jenkins docker version
docker compose -f infra/jenkins-compose.yml exec jenkins docker images sembi-amir-devops
docker compose -f infra/jenkins-compose.yml exec jenkins docker ps
docker compose -f infra/jenkins-compose.yml exec jenkins docker logs sembi-amir-container
```

Jenkins использует **отдельный Docker daemon** внутри сервиса `docker`.
Поэтому обычный `docker ps` на Windows не показывает вложенный контейнер приложения:
смотри его через `exec jenkins docker ps`. Порт 8082 Windows перенаправлен на 8080
этого daemon-контейнера, где опубликован порт приложения.
Jenkins обращается к Docker по TLS на порту 2376 внутри сети Compose.
Порт 2376 наружу не открыт. `privileged: true` нужен только Docker-in-Docker.

Job запускается кнопкой Build Now. Автозапуск после push здесь не настроен и
не требуется заданием. При желании включи Poll SCM с расписанием `H/5 * * * *`;
оно проверяет изменения примерно каждые пять минут. Для локального Jenkins
это проще, чем GitHub webhook, которому нужен доступный извне адрес.

## 8 Сохранение и выключение

```bash
git status
git add config/student.json Sembi_Amir_info.txt Jenkinsfile .env.example
git commit -m "Update student configuration"
git push
docker compose -f infra/jenkins-compose.yml stop
```

Коммит нужен только если перечисленные файлы действительно изменились.
Повторный запуск: `docker compose -f infra/jenkins-compose.yml start`.
Не добавляй флаг `-v` к `down`, если хочешь сохранить Jenkins job и настройки.
Папка проекта остаётся в Ubuntu WSL, GitHub хранит отправленные коммиты, а Jenkins
хранит свои данные отдельно в Docker volume.

## 9 Частые ошибки

| Ошибка | Что проверить |
| --- | --- |
| Cannot connect to Docker daemon | Docker Desktop запущен; `docker version` показывает Server |
| Port is already allocated | На 8080 может работать Spring Boot; останови его или измени левый порт публикации |
| Container name is already in use | Останови и удали только старый `sembi-amir-container` перед новым способом запуска |
| Personalization is incomplete | Заполни ID, сделай commit и push; Jenkins читает GitHub, а не незакоммиченные файлы Ubuntu |
| Repository not found | Проверь URL и доступ токена к приватному репозиторию |
| Docker недоступен внутри Jenkins | Проверь сервис `docker`, сертификаты и `exec jenkins docker version` |
| Очередь Jenkins не запускается | У built-in node должен быть хотя бы 1 executor для этой локальной лабораторной |
| free не найден | Команда выполняется в PowerShell; открой Ubuntu или предоставленный Linux Bash |
| permission denied при запуске скрипта | Выполни `bash scripts/prepare_linux.sh` внутри Linux |
| Нет logs или backup после clone | Запусти `bash scripts/prepare_linux.sh` |
| Docker Hub или apt недоступны | Проверь интернет и повтори сборку после восстановления доступа |

Проверяй первый красный этап Jenkins. Не меняй тесты на безусловный успех:
сначала прочитай конкретное сообщение об ошибке.
