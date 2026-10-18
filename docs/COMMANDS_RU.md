# Команды для демонстрации заданий

Команды выполняются по порядку после настройки из SETUP_RU.md.
Linux и Git показывай в Linux Bash; Docker запускай из Ubuntu WSL или Terminal macOS.

## Задание 1 Файлы и каталоги

```bash
pwd
ls -la
cd ~/devops/sembi_amir
mkdir -p app scripts config logs backup
touch logs/application.log
cat Sembi_Amir_info.txt
cp Sembi_Amir_info.txt backup/info-copy.txt
mv backup/info-copy.txt backup/info-renamed.txt
head -n 3 Sembi_Amir_info.txt
tail -n 2 Sembi_Amir_info.txt
rm backup/info-renamed.txt
```

| Команда | Что делает |
| --- | --- |
| pwd | Показывает абсолютный путь текущей папки |
| ls | Перечисляет файлы; `-a` включает скрытые, `-l` даёт подробности |
| cd | Меняет рабочую папку текущей оболочки |
| mkdir -p | Создаёт каталоги, включая недостающие родительские |
| touch | Создаёт пустой файл или обновляет время существующего, не стирая содержимое |
| cp | Копирует файл |
| mv | Перемещает или переименовывает файл |
| rm | Удаляет указанный файл |
| cat | Печатает содержимое файла |
| head / tail | Показывают начало / конец файла |

## Задание 2 Поиск и обработка

```bash
find . -type f -name 'application.log'
cat logs/application.log
grep 'ERROR' logs/application.log
grep 'WARNING' logs/application.log
grep -c 'ERROR' logs/application.log
tail -n 5 logs/application.log
```

В исходном учебном логе 10 строк, 2 строки ERROR и 2 WARNING.
Это специально подготовленный пример лога, а не журнал реальной базы данных.
`grep -c` считает подходящие строки. Здесь по одному ERROR на строку,
поэтому результат также равен количеству сообщений об ошибке.

## Задание 3 Права доступа

```bash
chmod 600 private.txt
chmod 644 public.txt
chmod 755 scripts/Sembi_Amir_system.sh
ls -l private.txt public.txt scripts/Sembi_Amir_system.sh
```

`r` = чтение (4), `w` = запись (2), `x` = выполнение (1).
Первые три бита относятся к владельцу, следующие к группе, последние к остальным.
600 = `rw-------`; 644 = `rw-r--r--`; 755 = `rwxr-xr-x`.
Первый файл доступен только владельцу, второй можно читать другим пользователям.
Имя private не шифрует файл; внутри только учебный текст без секретов.
Для каталогов `x` означает возможность прохода к содержимому, а не запуск программы.
Git хранит признак исполняемости, но не различие между 600 и 644: после clone
права устанавливает prepare_linux.sh.

## Задание 4 Bash

```bash
chmod +x scripts/Sembi_Amir_system.sh
./scripts/Sembi_Amir_system.sh
mv Sembi_Amir_info.txt backup/Sembi_Amir_info.txt
./scripts/Sembi_Amir_system.sh
mv backup/Sembi_Amir_info.txt Sembi_Amir_info.txt
```

Последние три команды показывают обе ветви проверки файла. Обязательно верни
файл на место. Скрипт использует `[ -f ... ]`, `whoami`, `hostname`, `date`,
`uname -a`, `df -h` и `free -h`. Путь вычисляется относительно самого скрипта,
поэтому он работает и при запуске из другой папки.

## Задание 5 Процессы

```bash
sleep 300 &
lab_pid=$!
ps
ps aux
ps -p "$lab_pid" -o pid,user,pcpu,pmem,comm
top
kill "$lab_pid"
```

Из top выйди клавишей `q`, затем выполни kill. Процесс — выполняющаяся
программа, PID — его числовой идентификатор. `ps` показывает снимок состояния,
`top` обновляет данные. `sleep` почти не использует CPU, поэтому 0.0% нормально.
Контейнер видит процессы в своём PID namespace; это не полный список процессов
Windows или macOS. `free` и `df` описывают Linux-среду Docker, а не точный мониторинг всего компьютера.

## Задания 6–10 Git и GitHub

После `init_history.sh`:

```bash
git status
git config user.name
git config user.email
git log
git log --oneline
git branch
git log --oneline --graph --all
git show development:docs/WORKFLOW.md
git show --stat development
git check-ignore -v logs/application.log backup/demo.txt .env
git ls-files -- logs/application.log backup/demo.txt .env
git remote -v
```

Из просмотра `git log` выйди клавишей `q`. Покажи merge-коммит и изменение
WORKFLOW.md. Если преподаватель просит новую ветку, используй уникальное имя:

```bash
git switch -c defense-demo
git branch
git switch main
```

Историю и слияние `development` уже создаёт init_history.sh. Для пояснения
можно открыть сам скрипт: `git branch development`, `git switch development`,
изменение документа, `git add`, `git commit`, `git switch main`, `git merge --no-ff`.
`.gitignore` предотвращает добавление ещё не отслеживаемых файлов. Он не
удаляет файлы с диска и не прекращает отслеживание уже закоммиченного файла.
`git pull` получает изменения и интегрирует их; `git push` отправляет локальные
коммиты. Ветка позволяет менять проект отдельно от основной линии.

## Задания 11–15 Docker

Открой Dockerfile и объясни FROM, WORKDIR, COPY, RUN, EXPOSE и CMD.
FROM задаёт базовый образ; WORKDIR — рабочую папку; COPY переносит файлы;
RUN выполняется при сборке; CMD запускает процесс при старте контейнера.
EXPOSE документирует порт, `-p` публикует его. USER задаёт непривилегированного
пользователя приложения. HEALTHCHECK проверяет HTTP-доступность.

Все команды build/run, `docker images`, `docker ps`, `docker ps -a`,
передача `-e`, logs, stop, start, rm, exec и Compose приведены в SETUP_RU.md.
Выполни их в том же порядке, чтобы не столкнуться с занятым именем контейнера.
Образ — шаблон файловой системы и настроек. Контейнер — созданный из образа
экземпляр с собственным состоянием; он может быть запущен или остановлен.
Переменные окружения — пары имя–значение, доступные процессу. Они позволяют
менять конфигурацию без пересборки. Секреты нельзя встраивать в образ; обычные
env также не являются защищённым хранилищем и доступны через инспекцию контейнера.

## Задания 16–20 Jenkins

Покажи Dashboard, имя Sembi_Amir_DevOps, Git URL в Configure, Jenkinsfile,
этапы Pipeline, Console Output, строку с данными студента, реальные образы и
контейнеры, результат Finished: SUCCESS и полный commit SHA из build/commit.txt.
Сравни этот SHA с коммитом в GitHub. Build компилирует Python в байткод и
проверяет персонализацию; Test выполняет десять проверок; Docker Build создаёт
образ; Docker Run проверяет здоровье контейнера и данные HTTP API.

## Задание 21 Полный процесс

Linux даёт рабочую среду. Git фиксирует изменения. GitHub хранит удалённую
версию проекта. Jenkins получает определённый коммит, проверяет код и создаёт
образ. Docker запускает приложение из этого образа. Успех означает, что
прошли все этапы, включая HTTP-проверку уже запущенного контейнера.
Если Test или Docker Build завершается с ошибкой, последующие этапы не
выполняются. При ошибке Test старый контейнер не заменяется. Если ошибка
произойдёт уже в Docker Run после удаления старого контейнера, автоматического
отката в этой учебной реализации нет — проблему нужно исправить и перезапустить job.
