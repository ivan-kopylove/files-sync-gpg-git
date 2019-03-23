# Current development status: work in progress. Script is unstable.

# Roadmap
- viewing file history based on git repo
- viewing deleted files based on git repo
- desktop / mobile frontend to prevent having unencrypted the notes at the filesystem. Frontend just runs python script.

# Warning
Локальные заметки хранятся в незашифрованном виде. Если кто-то получит доступ к вашему устройству, на котором хранятся данные, заметки будут скомпрометированы.

# Системные требования
- консольная команда git установлена (пуск - выполнить - cmd - git --version)
- консольная команда gpg установлена (пуск - выполнить - cmd - gpg --version)

# Как работает
- Первичная синхронизация выполняется, если отсутствует каталог .git в remote директории

# Ограничения
- Звёздочки в именах файлах не поддерживаются и будут убраны

# Синхронизация
Скрипт автоматически синхронизирует заметки.
- Синхронизация двустороняя - локальные заметки закачиваются в репозиторий, репозиторные заметки скачиваются в локальные
- [+] Коммитятся только измененные файлы.
- [] Программа выполняется если установлена версия git не ниже той что была у меня на момент разработки
- [] Программа выполняется если установлена версия gpg не ниже той что была у меня на момент разработки
- [] Программа выполняется если есть права на запись и удаление файлов в оба каталога
- [] делать коммит если доступен репозиторий (скачивать какую-нибудь инфу с удаленного репозитория)
- [] делать коммит только после успешного pull
- [] коммитятся все файлы, кроме тех, которые имеют расширение .gpg
- [] При конфликте, конфликтующая заметка переименовывается и коммитятся обе заметки 
- [] Если в репозиторий подложить незашифрованный файл, то при первой синхронизации файл зашифруется и удалится с сервера
- [] Если файл уже имеет расширение gpg, он будет зашифрован второй раз и будет иметь расширение myfile.txt.gpg.gpg


# Конфликтующие заметки
- Конфликт заметок сведен к минимуму, поскольку коммитятся только измененные файлы.
- Конфликтующий локальный файл переименовывается в имя_CURRENT_TIMESTAMP

# Шифрование
- шифрование выполнено путем делегирования задачи команде gpg 
- файлы шифруются на локальной машине, кладутся в папку на удаленном сервере и коммитятся
- 

# Точки возникновения конфликтов
- [] Склонировал репозиторий, а файл в НЕрепозитории конфликтует с тем что находится в склонированном репозитории
