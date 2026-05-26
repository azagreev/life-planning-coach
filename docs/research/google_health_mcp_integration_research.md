# **Архитектурная интеграция биометрических данных Google Health через Model Context Protocol в интеллектуальный коуч-ассистент Life Planning Coach**

Эффективное планирование жизни и управление долгосрочными целями требуют от интеллектуального ассистента глубокого понимания текущего физиологического состояния пользователя.1 Внедрение биометрического контекста в репозиторий life-planning-coach позволяет перевести планирование из реактивного формата в адаптивный, когда сложность задач и приоритеты динамически корректируются на основе реальных показателей здоровья.3 Для реализации бесшовного взаимодействия между ассистентом Claude и экосистемой медицинских данных Google оптимальным решением является открытый стандарт Model Context Protocol (MCP), разработанный компанией Anthropic.3 Данный подход позволяет преодолеть традиционные архитектурные барьеры интеграции, сводя архитектуру связи к единому стандартизированному интерфейсу.3

## **Резюме исследования (Executive Summary)**

* **Проблема:** Традиционная интеграция медицинских и фитнес-данных в ИИ-ассистенты сопряжена со сложностями безопасного хранения OAuth-токенов, фрагментацией API производителей носимых устройств и риском переполнения контекстного окна модели сырыми JSON-данными.6 Ситуация усложняется тем, что Google Fit REST API будет полностью отключен к концу 2026 года, а мобильный стандарт Google Health Connect не предоставляет облачного REST API.8  
* **Решение:** Протокол Model Context Protocol (MCP) решает проблему интеграции, предоставляя стандартизированный stdio/SSE интерфейс. Вместо отправки сырых токенов авторизации на сервер ИИ, MCP-сервер запускается локально на машине пользователя, безопасно выполняет запросы к Google Health API v4 (новому облачному стандарту Google), рассчитывает показатели здоровья и передает модели Claude только лаконичный агрегированный контекст.6  
* **Существующая экосистема:** В open-source сообществе уже развиваются зрелые проекты для интеграции носимых устройств с ИИ через MCP — *vytalLink*, *Delx Wellness* и *Open Wearables*.5 Каждое решение имеет свою архитектурную нишу (от мобильных приложений-прокси до полноценных self-hosted Docker-платформ).14  
* **Рекомендация для проекта:** Использование **Open Wearables** в качестве self-hosted инфраструктуры является наиболее масштабируемым и профессиональным решением.13 Платформа позволяет объединить Apple Health, Google Health Connect и облачные провайдеры (Garmin, Whoop) в один API, отдавая Claude чистый, агрегированный медицинский контекст.13

## **Архитектурное сопоставление технологий Google и выбор стратегии интеграции**

В процессе интеграции с биометрическими данными Google разработчик сталкивается с кардинальным изменением ландшафта API корпорации.8 Историческая платформа Google Fit API, включая ее REST-версию, официально выводится из эксплуатации к концу 2026 года.8 Новым стандартом для мобильных устройств на базе ОС Android выступает Health Connect, однако эта технология ориентирована исключительно на локальное хранение данных на физическом устройстве и не предоставляет публичного облачного REST API.10  
В качестве стратегического преемника облачного Fitbit Web API корпорация Google представила Google Health API (v4), который объединяет биометрические показатели носимых устройств Fitbit, Pixel Watch и сторонних интеграций в единое согласованное облачное хранилище.10 Поскольку проект life-planning-coach функционирует как программное окружение или облачный агент, взаимодействие должно быть построено через Google Health API по схеме «сервер-сервер» (Server-to-Server), что исключает жесткую зависимость от физического присутствия мобильного устройства пользователя в момент запуска сессии планирования.10

| Критерий архитектурного сравнения | Health Connect | Google Health API (v4) |
| :---- | :---- | :---- |
| **Системный статус** | Актуальный локальный стандарт для Android 8 | Актуальный облачный кроссплатформенный стандарт 10 |
| **Физическое размещение данных** | Локально на устройстве пользователя (On-device) 10 | Облачные серверы Google Cloud Platform 10 |
| **Протокол авторизации** | Нативные системные разрешения Android 7 | Google OAuth 2.0 (Restricted Scopes) 17 |
| **Сетевые требования** | Локальный межпроцессный доступ (IPC) 7 | HTTPS REST API (health.googleapis.com) 14 |
| **Унифицированный поток (Reconciled)** | Отсутствует, данные агрегируются клиентом 7 | Присутствует, автоматическое слияние дубликатов 10 |

## **Существующие open-source решения и альтернативы в экосистеме MCP**

Для проекта life-planning-coach разработчику не обязательно создавать коннектор с нуля. В сообществах GitHub и Reddit активно развиваются несколько проектов, которые уже успешно решили задачу бесшовной передачи данных здоровья в Claude через MCP:

1. **vytalLink (разработка Xmartlabs)** 14  
   * **Архитектура:** Гибридный подход. Мобильное приложение (Flutter) агрегирует данные локально из Apple Health и Google Health Connect, а затем проксирует их в Claude через собственный Node.js MCP-сервер (@xmartlabs/vytallink-mcp-server).  
   * **Авторизация:** Проект решает проблему сложной настройки OAuth в MCP-клиентах с помощью генерации временного кода «Слово \+ PIN» (например, HEALTH7 / sunset42) в мобильном приложении. Пользователю достаточно написать эти данные в чат Claude, чтобы установить безопасное соединение.  
   * **Интеграция:** Поддерживает дистрибуцию в виде официального бандла Claude Desktop (.mcpb) для установки расширения в один клик через интерфейс настроек.  
2. **Delx Wellness (разработчик davidmosiah)** 5  
   * **Архитектура:** Это децентрализованный реестр и каталог «local-first» MCP-коннекторов для 15 велнес-провайдеров, включая неофициальный коннектор google-health-mcp.5  
   * **Безопасность и хранение:** Все токены OAuth и файлы сессий сохраняются исключительно локально на машине пользователя в директории \~/.google-health-mcp/, полностью изолируя персональные данные от сторонних SaaS-хабов.5  
   * **Оптимизация:** Пакет поставляется с встроенными файлами AGENTS.md и манифестами инструментов, а также системными утилитами проверки (команда npx \-y google-health-mcp-unofficial doctor), которые помогают Claude быстро понимать границы доступных метрик здоровья.  
3. **Open Wearables (проект the-momentum)** 13  
   * **Архитектура:** Полноценная self-hosted платформа с открытым исходным кодом, которая объединяет API облачных вендоров (Garmin, Whoop, Oura) и локальные SDK (Samsung Health, Google Health Connect) в единый стандартизированный REST API.13  
   * **MCP-слой:** Отдельный модуль MCP-сервера связывается с вашим локальным или удаленным инстансом Open Wearables по API-ключам. Claude получает лаконичные инструменты для извлечения готовых сводок тренировок (workout\_events), сна (sleep\_data) и активности (activity\_summaries) без перегрузки контекстного окна сырыми JSON-структурами.  
4. **Withings MCP (автор akutishevsky)** 8  
   * **Архитектура:** Интересный паттерн удаленного MCP-сервера, развернутого на Deno Deploy и Supabase.8 Он реализует механизм *Double OAuth Flow*, где Claude Desktop авторизуется на промежуточном сервере, а тот безопасно авторизуется в API провайдера.8 Это позволяет анализировать данные даже в мобильном приложении Claude, где stdio-транспорт недоступен.8

### **Сравнительный анализ open-source решений в экосистеме MCP**

| Критерий сравнения | vytalLink | Delx Wellness | Open Wearables | Withings MCP |
| :---- | :---- | :---- | :---- | :---- |
| **Архитектурный тип** | Локальный / Гибридный (Мобильный клиент \+ Node.js MCP) 14 | Локальный (Local-first npm пакеты под каждое устройство) 5 | Централизованная self-hosted платформа (Docker / Railway) 13 | Удаленный (Remote SSE на Deno Deploy \+ Supabase) 8 |
| **Провайдеры данных** | Apple Health, Google Health Connect (через приложение) 14 | 15+ источников (Oura, Whoop, Garmin, Google Health, etc.) 5 | 8 провайдеров (Garmin, Whoop, Oura, Strava, Health Connect) | Исключительно экосистема Withings (весы, часы, сон) 8 |
| **Сложность авторизации** | Низкая (генерация Word \+ PIN в мобильном приложении) | Средняя (локальные токены и CLI-команда setup) | Высокая (необходимость OAuth / SDK ключей для self-hosted) 13 | Средняя (Double OAuth Flow: Claude \-\> Server \-\> Withings) 8 |
| **Оптимизация контекста** | Средняя (агрегированный composite readiness score) 17 | Высокая (встроенные мета-инструменты, privacy\_audit) 22 | Высокая (готовые сводки sleep\_data и activity\_summaries) | Средняя (прямые запросы к 12 инструментам) 8 |
| **Поддерживаемые клиенты** | Claude Desktop, ChatGPT, Cursor | Claude Desktop, Claude Code, Cursor, Codex 7 | Claude Desktop, Cursor, любые MCP-клиенты | Claude Desktop, мобильное приложение Claude 8 |

## **Глубокий анализ платформы Open Wearables**

**Open Wearables** — это полноценная self-hosted платформа с открытым исходным кодом (лицензия MIT), созданная студией Momentum. Она разработана специально для создания ИИ-приложений в сфере здоровья и долголетия, беря на себя всю работу по интеграции разрозненных SDK, обработке OAuth-потоков и дедупликации данных.

### **Технологический стек и архитектура платформы**

* **Backend:** Написан на FastAPI (Python) с базой данных PostgreSQL для долгосрочного хранения нормализованных данных.  
* **Frontend:** Панель управления разработчика (Developer Portal) на React/Next.js.  
* **SDK для мобильных устройств:** Native iOS SDK (HealthKit), native Android SDK (Google Health Connect \+ Samsung Health), а также кроссплатформенные библиотеки для React Native (Expo) и Flutter.  
* **MCP Server:** Отдельный сервис (написанный на Python/Node), который связывается с бэкендом Open Wearables по REST API с использованием API-ключей, предоставляя Claude готовые высокоуровневые инструменты.

### **Ключевые преимущества для проекта Life Planning Coach:**

1. **Экономия бюджета на токены (Progressive Disclosure):** MCP-сервер Open Wearables не скармливает Claude мегабайты сырого JSON. Вместо этого он выполняет агрегацию данных на сервере и возвращает лаконичные структурированные сводки (например, get\_sleep\_data, get\_activity\_summary). Это экономит до 90% контекстного окна модели.  
2. **Нулевая плата за пользователей:** Коммерческие агрегаторы (Rook, Terra, Junction) берут плату за каждого подключенного пользователя (от 0.5 до 2 долларов в месяц). Open Wearables разворачивается на вашей инфраструктуре, поэтому вы платите только за хостинг (около 50–100 долларов в месяц за Docker-контейнеры), экономя значительные средства при масштабировании.  
3. **Открытые алгоритмы здоровья:** Платформа поставляется со встроенными и верифицированными алгоритмами расчета показателей сна и устойчивости к нагрузкам (resilience scores), разработанными доктором нейробиологии из Института Макса Планка. Вы можете использовать и дорабатывать их под логику Life Planning Coach.

## **Путь пользователя (End-User Customer Journey) в Life Planning Coach**

Этот сценарий описывает опыт обычного пользователя вашего коуча, который хочет подключить свои часы или телефон для автоматической корректировки планов.

\+--------------------+      \+--------------------+      \+--------------------+      \+-----------------------+  
|  1\. Инициация в    |      | 2\. Onboarding &    |      | 3\. Авторизация     |      | 4\. Фоновый сбор       |  
|    интерфейсе ИИ   | \---\> |    Ввод кода       | \---\> |    устройств (OAuth)| \---\> |    и синхронизация    |  
| (Claude/Telegram)  |      |   (Приглашение)    |      |   / Разрешения SDK |      | (Health Connect/Cloud)|  
\+--------------------+      \+--------------------+      \+--------------------+      \+-----------------------+  
                                                                                                |  
                                                                                                v  
                                                                                    \+-----------------------+  
                                                                                    | 5\. Получение умных    |  
                                                                                    |    рекомендаций ИИ    |  
                                                                                    |   (Коррекция задач)   |  
                                                                                    \+-----------------------+

### **Шаг 1\. Инициация в интерфейсе ассистента**

* **Действие:** Пользователь начинает сессию планирования в Telegram-боте, веб\-интерфейсе проекта или через Claude Desktop/Claude Code.3  
* **Опыт:** Коуч-ассистент видит, что у него нет актуальных данных о физиологии пользователя, и мягко предлагает: *«Привет\! Чтобы я мог составить максимально эффективный план дня, адаптированный под твой уровень энергии, давай подключим твои фитнес-данные».*

### **Шаг 2\. Onboarding и получение кода доступа**

* **Действие:** ИИ-коуч генерирует персонализированную ссылку для подключения (вызывая API Open Wearables для создания нового пользователя и получения Invitation Code).  
* **Опыт:** Пользователь переходит по ссылке на веб\-страницу Onboarding, брендированную под life-planning-coach. Система приветствует его сообщением о конфиденциальности: *«Твои медицинские данные хранятся на наших защищенных серверах, зашифрованы и никогда не передаются третьим лицам»*.

### **Шаг 3\. Авторизация устройств и источников данных**

* **Действие:** Пользователь выбирает свое устройство (например, Garmin, Oura, Pixel Watch/Health Connect или Apple Watch).  
  * **Для облачных сервисов (Garmin, Whoop, Oura, Fitbit):** Пользователь нажимает «Подключить» и перенаправляется на официальный сайт производителя (OAuth 2.0). Он авторизуется под своей учетной записью и дает согласие на передачу данных в ваше приложение.  
  * **Для мобильных датчиков (Google Health Connect на Android / Apple Health на iOS):** Пользователь делает это внутри вашего мобильного приложения-компаньона. На экране смартфона появляется системное окно: *«Разрешить приложению Life Planning Coach доступ к шагам, пульсу и сну в Health Connect»*.7 Пользователь одобряет доступ.7

### **Шаг 4\. Фоновая синхронизация данных (Invisible Sync)**

* **Действие:** После авторизации процесс синхронизации становится полностью невидимым для пользователя.  
  * Мобильные SDK (React Native / Flutter) в фоновом режиме раз в 15–30 минут считывают новые данные из Health Connect/HealthKit и отправляют их на ваш self-hosted сервер Open Wearables.  
  * Облачные интеграции автоматически отправляют вебхуки при завершении тренировок или пробуждении пользователя.

### **Шаг 5\. Получение адаптивных рекомендаций**

* **Действие:** Пользователь просыпается и открывает утренний чат с коучем.  
* **Опыт:** Claude в фоновом режиме обращается к MCP-серверу Open Wearables, запрашивает сводку сна за ночь и активность за вчера. На основе этих данных коуч рассчитывает Recovery Index (![][image1]) и перестраивает календарь:  
  * *«Я вижу, что твой глубокий сон сегодня составил всего 40 минут, а пульс в покое повысился до 74 уд/мин. Твой индекс восстановления снижен. Я рекомендую перенести сегодняшнюю тяжелую тренировку по боксу на завтра, а вместо этого добавить 20-минутную прогулку и лечь спать на час раньше. Изменил твое расписание\!»*

## **Путь разработчика (Developer Customer Journey) в Life Planning Coach**

Этот технический сценарий описывает шаги инженеров вашего проекта по развертыванию, настройке и интеграции Open Wearables в кодовую базу life-planning-coach.

  1\. Self-hosting Бэкенда (Docker Compose / Railway)  
                         │  
                         ▼  
  2\. Настройка Developer Portal (API ключи, OAuth вендоров)  
                         │  
                         ▼  
  3\. Интеграция SDK в клиентские приложения (React Native / Flutter)  
                         │  
                         ▼  
  4\. Настройка и запуск MCP Server (OPEN\_WEARABLES\_API\_KEY)  
                         │  
                         ▼  
  5\. Написание Системных Промптов (AGENTS.md) и Логики Recovery

### **Шаг 1\. Локальное и облачное развертывание бэкенда**

Разработчик разворачивает бэкенд Open Wearables на собственном сервере (например, AWS, DigitalOcean или Railway) с помощью Docker.

Bash  
\# Клонирование репозитория  
git clone https://github.com/the-momentum/open-wearables.git  
cd open-wearables

\# Копирование и настройка переменных окружения  
cp./backend/config/.env.example./backend/config/.env  
cp./frontend/.env.example./frontend/.env

\# Настройка ADMIN\_EMAIL и ADMIN\_PASSWORD в файле конфигурации бэкенда  
\# Запуск инфраструктуры в Docker  
docker compose up \-d

### **Шаг 2\. Конфигурация Developer Portal**

* Разработчик переходит по адресу http://localhost:3000 (или URL своего сервера), авторизуется под учетной записью администратора и попадает в панель управления.  
* В разделе **Credentials** генерирует приватный API-ключ вида ow\_prod\_api\_key\_... для бэкенда life-planning-coach.  
* В панели регистрирует OAuth-приложения для провайдеров. Например, для Google Health API v4 разработчик создает проект в Google Cloud Console, включает Google Health API, получает Client ID и Client Secret и прописывает их в кабинете Open Wearables.

### **Шаг 3\. Интеграция SDK в мобильные или веб\-клиенты коуча**

Для автоматического забора данных из Google Health Connect на Android разработчик интегрирует официальный React Native (Expo) или Flutter SDK в приложение-компаньон life-planning-coach.

TypeScript  
// Пример инициализации SDK в React Native приложении коуча  
import OpenWearables from 'open-wearables-react-native-sdk';

// Настройка хоста вашего self-hosted сервера  
OpenWearables.configure('https://wearables.yourdomain.com');

// Авторизация пользователя по токенам сессии вашего бэкенда  
await OpenWearables.signIn(userId, userAccessToken, userRefreshToken, apiKey);

// Запрос системных разрешений на чтение пульса, шагов и сна  
const granted \= await OpenWearables.requestAuthorization();

if (granted) {  
  // Запуск фоновой синхронизации данных с сервером  
  await OpenWearables.startBackgroundSync();  
}

### **Шаг 4\. Настройка и запуск MCP-сервера для Claude**

Разработчик разворачивает изолированный MCP-сервер, поставляемый в директории /mcp Open Wearables. Этот сервер будет проксировать запросы от Claude к вашему REST API.

1. Переходим в директорию MCP-сервера в проекте:  
   Bash  
   cd open-wearables/mcp  
   cp config/.env.example config/.env

2. Заполняем config/.env учетными данными вашего развернутого сервера:  
   Code snippet  
   OPEN\_WEARABLES\_API\_URL=https://wearables.yourdomain.com  
   OPEN\_WEARABLES\_API\_KEY=ow\_prod\_api\_key\_your\_actual\_key

3. Конфигурируем Claude Desktop на локальной машине или сервере разработки, прописывая запуск через утилиту uv (рекомендуемый быстрый инструмент запуска Python-пакетов от Astral):  
   JSON  
   {  
     "mcpServers": {  
       "open-wearables": {  
         "command": "uv",  
         "args": \[  
           "run",  
           "--frozen",  
           "--directory",  
           "/path/to/open-wearables/mcp",  
           "start"  
         \]  
       }  
     }  
   }

### **Шаг 5\. Обучение модели и написание системных инструкций**

Разработчик создает файл AGENTS.md (или CLAUDE.md) в корне репозитория life-planning-coach. Этот файл содержит мета-инструкции для Claude, описывающие, как правильно опрашивать MCP-сервер Open Wearables и интерпретировать полученные метрики здоровья.

# **Инструкции для ИИ-агента Life Planning Coach**

Ты — эмпатичный ИИ-коуч по планированию жизни. У тебя есть доступ к инструментам open-wearables.  
Всегда следуй этому протоколу перед планированием задач пользователя:

## **Шаг 1: Обнаружение пользователя и сбор контекста**

Вызови инструмент get\_users, чтобы сопоставить текущего собеседника.  
Вызови get\_sleep\_data и get\_activity\_summary за последние 24 часа.

## **Шаг 2: Расчет индекса готовности (Recovery Index)**

Используй следующую формулу для оценки физиологического состояния:  
![][image2]

## **Шаг 3: Адаптация планов**

* Если ![][image3]: Включи режим сохранения энергии. Предложи перенести дедлайны.  
* Если ![][image4]: Предложи сфокусироваться на ключевых сложных целях.

## **Интеграционный паттерн для репозитория Life Planning Coach**

Для того чтобы Claude мог использовать данные Google Health в качестве активного «скилла» непосредственно внутри проекта life-planning-coach, архитектура репозитория расширяется за счет добавления изолированного модуля MCP-сервера.4 Claude взаимодействует с кодовой базой проекта либо через десктопное приложение Claude Desktop, либо через консольный интерфейс Claude Code.27 Оба клиента поддерживают автоматическое обнаружение и запуск MCP-серверов, настроенных в границах проекта.27

| Компонент интеграции в репозитории | Роль в общей архитектуре системы | Техническое назначение |
| :---- | :---- | :---- |
| **/mcp-google-health/** | Изолированный пакет MCP-сервера | Содержит кодовую базу коннектора на Node.js/TypeScript. 28 |
| **├── src/server.ts** | Точка инициализации и запуска | Настраивает stdio-транспорт и создает экземпляр сервера. 3 |
| **├── src/tools.ts** | Декларация и логика инструментов | Описывает Zod-схемы входных параметров и выполняет запросы к API. 28 |
| **├── package.json** | Зависимости и скрипты сборки | Фиксирует библиотеки @modelcontextprotocol/server и axios. 28 |
| **/.mcp.json** | Конфигурация для Claude Code | Автоматически подключает инструменты к CLI-ассистенту при запуске. 27 |
| **/AGENTS.md** | Системные инструкции для Claude | Формирует мета-промпт, описывающий логику вызова биометрических инструментов. 12 |

Внедрение файла конфигурации .mcp.json непосредственно в корень репозитория обеспечивает переносимость окружения.27 При запуске Claude Code в контексте данной директории клиент инициализирует локальный процесс MCP-сервера по протоколу стандартного ввода-вывода (stdio), автоматически расширяя контекстное окно Claude доступными инструментами планирования активности на основе здоровья.3

## **Реализация протокола авторизации Google OAuth 2.0 с PKCE**

Безопасный доступ к медицинским данным в Google Health API строго регламентирован.17 Все области видимости (scopes), связанные с физической активностью, пульсом и сном, относятся к категории повышенной конфиденциальности (Restricted), что накладывает ограничения на публикацию приложения.17 Для персональной эксплуатации коуча в рамках проекта разработчик создает Desktop-клиент или Web-приложение в Google Cloud Console и переводит его в статус тестирования, добавив свой email в список доверенных лиц.19  
Реализация авторизации в контексте MCP-клиентов (таких как Claude Desktop или Claude Code) требует интеграции протокола OAuth 2.1 с использованием технологии Proof Key for Code Exchange (PKCE).25 Так как локальные консольные утилиты не могут безопасно хранить секреты клиента, PKCE защищает процесс обмена кодами авторизации.25 В момент инициализации авторизации MCP-клиент запускает временный локальный HTTP-сервер на локальном хосте для перехвата перенаправления.11  
Процесс получения авторизационного токена протекает без непосредственного участия модели в передаче секретных ключей.6 Пользователь подтверждает права доступа в веб\-интерфейсе Google, после чего его браузер производит перенаправление на http://localhost:\<порт\>/callback с параметром code.27 Локальный веб\-сервер принимает этот запрос, завершает обмен на access\_token и refresh\_token, сохраняя их в зашифрованный файл конфигурации, и завершает свою работу, гарантируя отсутствие утечки данных через контекстное окно модели.6

## **Спецификация эндпоинтов Google Health API v4 и маппинг биометрии**

Интеграция с Google Health API v4 требует полной переработки логики разбора данных, так как схема ответов новой платформы не имеет общих путей и полей с устаревшим Fitbit API.14 Платформа v4 предоставляет четыре метода агрегации данных: list (сырые точки), reconcile (согласованный поток), rollUp (физические интервалы времени) и dailyRollUp (интервалы гражданского времени).14

| Тип данных | Системный идентификатор | Категория (Kind) | Фильтр и особенности обработки схемы |
| :---- | :---- | :---- | :---- |
| **Пульс** | heart-rate 13 | **Sample** (Мгновенное измерение) 14 | Использует фильтр физического времени heart\_rate.sample\_time.physical\_time. Каждая точка содержит объект beatsPerMinute. 14 |
| **Шаги** | steps 13 | **Interval** (Протяженное событие) 14 | Использует фильтр steps.interval.start\_time. Агрегированные данные извлекаются через суммирующий узел countSum. 14 |
| **Сон** | sleep 13 | **Session** (Сессионное событие) 14 | Использует фильтр sleep.interval.end\_time. Стадии сна возвращаются в верхнем регистре (AWAKE, LIGHT, DEEP, REM) в массиве sleep.stages. 14 |

При построении фильтров для запросов критически важно учитывать специфику именования полей в зависимости от места их использования.33 В самом пути URL-запроса идентификаторы типов всегда указываются в kebab-case (например, body-fat), однако в строке параметров фильтрации те же сущности преобразуются в snake\_case (например, body\_fat.sample\_time.physical\_time).33 Кроме того, шесть базовых типов данных, включая расход калорий (total-calories) и зоны пульса, не поддерживают метод получения списка сырых точек :list, возвращая ошибку 400; для них необходимо осуществлять вызовы исключительно через методы :rollUp или :dailyRollUp.14

## **Математическая модель расчета индекса восстановления для коучинга**

Для предоставления качественных рекомендаций в рамках Life Planning Coach ассистент не должен анализировать сырые массивы JSON.6 Вместо этого MCP-сервер осуществляет первичную обработку и вычисляет интегральный индекс восстановления (![][image1]), используя нормализованные показатели сна, активности и пульса в покое.14 Расчет производится по следующей математической зависимости:  
![][image5]  
Где параметры определены следующим образом:

* ![][image6] — фактическая продолжительность сна в минутах, а ![][image7] — целевая продолжительность сна пользователя (например, 480 минут).14  
* ![][image8] и ![][image9] — суммарное время нахождения в фазах глубокого и быстрого сна соответственно.14  
* ![][image10] — количество шагов, зафиксированных за предыдущие сутки, а ![][image11] — ежедневная норма активности.14  
* ![][image12] — средний пульс в состоянии покоя за прошедшие сутки, а ![][image13] и ![][image14] — исторические пограничные показатели пульса пользователя.13  
* ![][image15] — весовые коэффициенты, определяющие вклад каждого фактора в общую оценку готовности организма к нагрузкам. При этом должно строго соблюдаться условие нормировки весов:

![][image16]  
Полученный индекс восстановления масштабируется в диапазоне от 0.0 до 1.0. Если ![][image3], модель Claude получает сигнал о критической утомляемости пользователя, что активирует сценарий бережного планирования (перенос сложных когнитивных или интенсивных физических задач, предложение практик медитации и раннего отхода ко сну).4

## **Разработка TypeScript MCP-сервера для Life Planning Coach**

Техническая реализация MCP-сервера базируется на официальном программном пакете @modelcontextprotocol/server.26 В рамках расширения репозитория life-planning-coach создается исполняемый файл сервера, регистрирующий необходимые аналитические инструменты для Claude.28

TypeScript  
import { McpServer } from '@modelcontextprotocol/server';  
import { StdioServerTransport } from '@modelcontextprotocol/server/stdio';  
import { z } from 'zod';  
import axios from 'axios';

const server \= new McpServer({  
  name: 'life-planning-health-connector',  
  version: '1.0.0'  
});

const GOOGLE\_HEALTH\_API\_BASE \= 'https://health.googleapis.com/v4';

// Функция безопасного извлечения токена из переменных окружения  
function getAccessToken(): string {  
  const token \= process.env.GOOGLE\_HEALTH\_ACCESS\_TOKEN;  
  if (\!token) {  
    throw new Error('Критическая ошибка: Переменная GOOGLE\_HEALTH\_ACCESS\_TOKEN не настроена.');  
  }  
  return token;  
}

// Регистрация инструмента анализа восстановления  
server.registerTool(  
  'get\_recovery\_context',  
  {  
    targetDate: z.string().regex(/^\\d{4}-\\d{2}-\\d{2}$/).describe('Целевая дата анализа в формате YYYY-MM-DD')  
  },  
  async ({ targetDate }) \=\> {  
    try {  
      const token \= getAccessToken();  
      const startTime \= \`${targetDate}T00:00:00Z\`;  
      const endTime \= \`${targetDate}T23:59:59Z\`;

      // Параллельный запрос шагов и пульса для оптимизации времени ответа  
      const \= await Promise.all();

      let totalSteps \= 0;  
      if (stepsResponse.data.dataPoints) {  
        for (const point of stepsResponse.data.dataPoints) {  
          totalSteps \+= parseInt(point.steps?.countSum || '0', 10);  
        }  
      }

      const restingHrPoint \= heartResponse.data.dataPoints?.;  
      const restingHr \= restingHrPoint?.dailyRestingHeartRate?.beatsPerMinute || 70;

      // Текстовый синтез данных для сохранения лимитов контекстного окна  
      const contextualSummary \= \`Физиологический статус на дату ${targetDate}: зарегистрировано шагов: ${totalSteps}; средний пульс в покое: ${restingHr} уд/мин. Данные нормализованы и готовы для корректировки планов.\`;

      return {  
        content:  
      };  
    } catch (error: any) {  
      return {  
        content: \[{ type: 'text', text: \`Ошибка сбора медицинского контекста: ${error.message}\` }\],  
        isError: true  
      };  
    }  
  }  
);

async function runServer() {  
  const transport \= new StdioServerTransport();  
  await server.connect(transport);  
}

runServer().catch((err) \=\> {  
  console.error('Сбой инициализации MCP stdio-транспорта:', err);  
  process.exit(1);  
});

## **Методы подключения и настройки скилла в клиентах Claude**

Подключение созданного MCP-сервера в качестве активного скилла ассистента Claude выполняется в зависимости от используемого рабочего окружения разработчика.27

### **Интеграция в Claude Code через проектную конфигурацию**

При локальной разработке и использовании консольного агента Claude Code в корне репозитория life-planning-coach создается файл .mcp.json.27 Это гарантирует, что любой запуск сессии автоматизации в этой директории немедленно подгрузит инструменты здоровья.27

JSON  
{  
  "mcpServers": {  
    "life-planning-health": {  
      "command": "node",  
      "args": \["./mcp-google-health/dist/server.js"\],  
      "env": {  
        "GOOGLE\_HEALTH\_ACCESS\_TOKEN": "ya29.a0Axoo..."  
      }  
    }  
  }  
}

Для проверки успешности подключения в консоли Claude Code выполняется команда claude mcp list, которая должна вернуть статус активности сервера и перечень зарегистрированных инструментов.29

### **Системное подключение в Claude Desktop**

Если взаимодействие с коучем осуществляется через десктопное приложение Claude Desktop, конфигурация прописывается в глобальном конфигурационном файле приложения.29 Разработчику необходимо открыть файл настроек напрямую из меню настроек разработчика (Settings \-\> Developer \-\> Edit Config) и импортировать блок конфигурации локального сервера.35

JSON  
{  
  "mcpServers": {  
    "life-planning-health-desktop": {  
      "command": "node",  
      "args": \["/Users/username/projects/life-planning-coach/mcp-google-health/dist/server.js"\],  
      "env": {  
        "GOOGLE\_HEALTH\_ACCESS\_TOKEN": "ya29.a0Axoo..."  
      }  
    }  
  }  
}

После сохранения файла требуется осуществить полный перезапуск приложения Claude Desktop.35 Индикатором корректной привязки скилла служит появление иконки электрической вилки или молотка в правом нижнем углу интерфейса чата, при клике на которую отображается инструмент get\_recovery\_context.23

## **Безопасность и предотвращение перегрузки контекстного окна**

Интеграция произвольного кода через stdio-транспорт MCP несет потенциальные риски безопасности, связанные с возможностью выполнения несанкционированных команд операционной системы.36 Уязвимости в реализации обработки ввода могут привести к компрометации локальной машины разработчика.36 Для защиты инфраструктуры MCP-сервер проекта должен придерживаться строгих мер изоляции 4:

* **Жесткая валидация схем:** Использование библиотек валидации типов (например, Zod) для входных параметров инструментов гарантирует, что модель не сможет передать деструктивные экранирующие последовательности в аргументах запуска.4  
* **Принцип прогрессивного раскрытия данных (Progressive Disclosure):** Прямая передача массивных сырых JSON-ответов от API Google перегружает контекстное окно модели, вызывая рост финансовых затрат на токены и увеличивая вероятность галлюцинаций модели.6 Логика MCP-инструментов должна агрегировать, фильтровать и форматировать данные на стороне сервера.6 Модели должны отдаваться исключительно лаконичные выжимки или числовые индексы.6  
* **Маскирование конфиденциальных данных (PII):** В случае работы с медицинскими записями или геолокационными треками тренировок, MCP-сервер обязан токенизировать или полностью удалять персональную информацию (такую как точные географические координаты или персональные идентификаторы устройств) до отправки ответа клиенту.6 Это исключает утечку приватных данных в облачное окружение Anthropic.6

## **Архитектурные выводы и рекомендации для Life Planning Coach**

Анализ кодовой базы life-planning-coach и текущей экосистемы Model Context Protocol позволяет выделить три альтернативных пути интеграции данных здоровья в Claude-скилл:

### **Рекомендация 1\. Интеграция через self-hosted Open Wearables (Наиболее масштабируемый путь)**

Если в будущем планируется поддержка не только Google Health/Fitbit, но и других девайсов (Garmin, Oura, Whoop) без переписывания бэкенда:

* **Что делать:** Развернуть Open Wearables в Docker-контейнере (или в один клик через Railway) в качестве единого хаба данных.13  
* **Интеграция в скилл:** Подключить официальный open-wearables MCP-сервер по API-ключам. Это позволит Claude оперировать высокоуровневыми абстракциями (сводками сна, активности и тренировок) напрямую через REST API платформы.

### **Рекомендация 2\. Локальный MVP на базе Delx Wellness (Самый быстрый путь для прототипирования)**

Если необходимо проверить концепцию персонального коучинга с минимальными временными затратами и локальным хранением:

* **Что делать:** Использовать пакет google-health-mcp от Delx Wellness.5  
* **Интеграция в скилл:** Сконфигурировать .mcp.json в корне репозитория для автоматического запуска этого локального коннектора через npx.5 Данные будут храниться строго в директории \~/.google-health-mcp/.5

### **Рекомендация 3\. Разработка собственного TypeScript MCP-сервера (Максимальный контроль и точность)**

Если ключевой фичей коуча является уникальный расчет биометрической готовности пользователя к задачам дня (например, на основе выведенной математической формулы ![][image1]):

* **Что делать:** Реализовать собственный легковесный Node.js MCP-сервер по приведенному в исследовании шаблону, используя библиотеку @modelcontextprotocol/server.28  
* **Интеграция в скилл:** Поместить код сервера в поддиректорию /mcp-google-health/ репозитория life-planning-coach.28 Это позволит кастомизировать фильтрацию данных, вычислять коэффициент восстановления ![][image1] на бэкенде и отдавать Claude исключительно компактные и безопасные структурированные выводы, экономя до 90% токенов контекстного окна.6

#### **Works cited**

1. start-my-day install and usage guide \- Agent Skills Finder, accessed May 20, 2026, [https://agentskillsfinder.com/skills/start-my-day](https://agentskillsfinder.com/skills/start-my-day)  
2. How to Transform Lives as a Coach \- Garrain Asé & Angel Martin Cordova \- YouTube, accessed May 20, 2026, [https://www.youtube.com/watch?v=ARw3wjutPhM](https://www.youtube.com/watch?v=ARw3wjutPhM)  
3. What is Model Context Protocol (MCP)? A guide | Google Cloud, accessed May 20, 2026, [https://cloud.google.com/discover/what-is-model-context-protocol](https://cloud.google.com/discover/what-is-model-context-protocol)  
4. Specification \- What is the Model Context Protocol (MCP)?, accessed May 20, 2026, [https://modelcontextprotocol.io/specification/2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25)  
5. Model Context Protocol \- Wikipedia, accessed May 20, 2026, [https://en.wikipedia.org/wiki/Model\_Context\_Protocol](https://en.wikipedia.org/wiki/Model_Context_Protocol)  
6. Code execution with MCP: building more efficient AI agents \- Anthropic, accessed May 20, 2026, [https://www.anthropic.com/engineering/code-execution-with-mcp](https://www.anthropic.com/engineering/code-execution-with-mcp)  
7. Google Health Connect API Integration \- Open Wearables, accessed May 20, 2026, [https://openwearables.io/integrations/google-health-connect](https://openwearables.io/integrations/google-health-connect)  
8. Google Fit Migration FAQ | Android health & fitness, accessed May 20, 2026, [https://developer.android.com/health-and-fitness/health-connect/migration/fit/faq](https://developer.android.com/health-and-fitness/health-connect/migration/fit/faq)  
9. Fit migration guide | Android health & fitness, accessed May 20, 2026, [https://developer.android.com/health-and-fitness/health-connect/migration/fit](https://developer.android.com/health-and-fitness/health-connect/migration/fit)  
10. Health Connect comparison guide | Android health & fitness \- Android Developers, accessed May 20, 2026, [https://developer.android.com/health-and-fitness/health-connect/comparison-guide](https://developer.android.com/health-and-fitness/health-connect/comparison-guide)  
11. Implementing MCP OAuth: A Technical Deep-Dive | Upstash Blog, accessed May 20, 2026, [https://upstash.com/blog/mcp-oauth-implementation](https://upstash.com/blog/mcp-oauth-implementation)  
12. Get started | Google Health API, accessed May 20, 2026, [https://developers.google.com/health/get-started](https://developers.google.com/health/get-started)  
13. Migration guide | Google Health API, accessed May 20, 2026, [https://developers.google.com/health/migration](https://developers.google.com/health/migration)  
14. The complete guide: How the new Google Health API works, accessed May 20, 2026, [https://tryterra.co/blog/everything-you-need-to-know-about-google-health-new-api](https://tryterra.co/blog/everything-you-need-to-know-about-google-health-new-api)  
15. How to Connect an MCP Server to Claude Desktop (No Developer Experience Required), accessed May 20, 2026, [https://www.adventuresincre.com/how-to-connect-mcp-server-claude-desktop/](https://www.adventuresincre.com/how-to-connect-mcp-server-claude-desktop/)  
16. Migrating Users from Google Fit SDK to Health Connect \- Validic Technical Documentation, accessed May 20, 2026, [https://helpdocs.validic.com/docs/native-android-mobile-inform-sdk-migrating-users-from-google-fit-sdk-to-health-connect](https://helpdocs.validic.com/docs/native-android-mobile-inform-sdk-migrating-users-from-google-fit-sdk-to-health-connect)  
17. About the Google Health API, accessed May 20, 2026, [https://developers.google.com/health/about](https://developers.google.com/health/about)  
18. How We're Preparing for Google's New API \- Fitabase Blog, accessed May 20, 2026, [https://www.fitabase.com/blog/post/google-health-api-announcement/](https://www.fitabase.com/blog/post/google-health-api-announcement/)  
19. Set up Google Cloud and OAuth \- Health API, accessed May 20, 2026, [https://developers.google.com/health/setup](https://developers.google.com/health/setup)  
20. Health Connect | Android health & fitness \- Android Developers, accessed May 20, 2026, [https://developer.android.com/health-and-fitness/health-connect](https://developer.android.com/health-and-fitness/health-connect)  
21. Health API \- Google for Developers, accessed May 20, 2026, [https://developers.google.com/health/reference/rest](https://developers.google.com/health/reference/rest)  
22. Accessing Samsung Health Data through Health Connect \- Samsung Developer, accessed May 20, 2026, [https://developer.samsung.com/health/blog/en/accessing-samsung-health-data-through-health-connect](https://developer.samsung.com/health/blog/en/accessing-samsung-health-data-through-health-connect)  
23. Connect to local MCP servers \- Model Context Protocol, accessed May 20, 2026, [https://modelcontextprotocol.io/docs/develop/connect-local-servers](https://modelcontextprotocol.io/docs/develop/connect-local-servers)  
24. Make your first Google Health API call, accessed May 20, 2026, [https://developers.google.com/health/codelabs/make-your-first-api-call](https://developers.google.com/health/codelabs/make-your-first-api-call)  
25. MCP OAuth: How OAuth 2.1 Works in the Model Context Protocol \- Prefect, accessed May 20, 2026, [https://www.prefect.io/resources/mcp-oauth](https://www.prefect.io/resources/mcp-oauth)  
26. The official TypeScript SDK for Model Context Protocol servers and clients \- GitHub, accessed May 20, 2026, [https://github.com/modelcontextprotocol/typescript-sdk](https://github.com/modelcontextprotocol/typescript-sdk)  
27. Connect Claude Code to tools via MCP, accessed May 20, 2026, [https://code.claude.com/docs/en/mcp](https://code.claude.com/docs/en/mcp)  
28. MCP Server Boilerplate \- LobeHub, accessed May 20, 2026, [https://lobehub.com/mcp/vltansky-mcp-boilerplate](https://lobehub.com/mcp/vltansky-mcp-boilerplate)  
29. github-mcp-server/docs/installation-guides/install-claude.md at main, accessed May 20, 2026, [https://github.com/github/github-mcp-server/blob/main/docs/installation-guides/install-claude.md](https://github.com/github/github-mcp-server/blob/main/docs/installation-guides/install-claude.md)  
30. AGENTS.md \- rudrankriyam/Google-Health-CLI \- GitHub, accessed May 20, 2026, [https://github.com/rudrankriyam/Google-Health-CLI/blob/main/AGENTS.md](https://github.com/rudrankriyam/Google-Health-CLI/blob/main/AGENTS.md)  
31. OAuth Authentication \- FastMCP, accessed May 20, 2026, [https://gofastmcp.com/clients/auth/oauth](https://gofastmcp.com/clients/auth/oauth)  
32. Method: users.dataTypes.dataPoints.list | Google Health API, accessed May 20, 2026, [https://developers.google.com/health/reference/rest/v4/users.dataTypes.dataPoints/list](https://developers.google.com/health/reference/rest/v4/users.dataTypes.dataPoints/list)  
33. Endpoints \- Health API \- Google for Developers, accessed May 20, 2026, [https://developers.google.com/health/endpoints](https://developers.google.com/health/endpoints)  
34. Method: users.dataTypes.dataPoints.dailyRollUp | Google Health API, accessed May 20, 2026, [https://developers.google.com/health/reference/rest/v4/users.dataTypes.dataPoints/dailyRollUp](https://developers.google.com/health/reference/rest/v4/users.dataTypes.dataPoints/dailyRollUp)  
35. How to Set Up MCP Servers in Claude Desktop (Complete Guide) \- Octave HQ, accessed May 20, 2026, [https://octavehq.com/post/how-to-set-up-mcp-servers-claude-desktop](https://octavehq.com/post/how-to-set-up-mcp-servers-claude-desktop)  
36. The 200,000 Server Question: Is Anthropic’s MCP Design Flaw a Bug or a Feature? | by Jiten Oswal | Apr, 2026, accessed May 20, 2026, [https://medium.com/@jiten.p.oswal/the-200-000-server-question-is-anthropics-mcp-design-flaw-a-bug-or-a-feature-b120294f93a5](https://medium.com/@jiten.p.oswal/the-200-000-server-question-is-anthropics-mcp-design-flaw-a-bug-or-a-feature-b120294f93a5)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACUAAAAaCAYAAAAwspV7AAAB4UlEQVR4Xu2UPyhGYRTGj1CKkoiEJKWUmP0bCGUgZikTMmERsTFIFjaRDDaLwmQwKqUUESmK0aIo5M/zdN7Xd538/XI/g+9XT9+9z/nufc8973mPSJw44ZIM5UC5Rn9KmmgSl9AzVOzuqSrnPUIJ/oFYciuagGVS1K+1gbBhFbjwhQ2AQdHYkg2ETYbowus2AFZEYz02EDYd0BPUYPx00YT2jR8T5kW3Ll8ip7EPOhftqdTIX2NDBXQNjQS8RNETdx/wgrAH29yvpU60ups28BO4dXyJ3bpF52can/BD2H8pNuBg1Ses+RN2RBe3C/gGLzX+d7iS6J575Uben0+nor6d7gVQs/EIt7xFtB+3RIey95tE+7IEanT+h3w2n+hT/uWsKAcot3MIKnQ+OYaG3XUX1Oqux0Wf4Yfx0JSLVtG/8w1MpgzqFV34SHSR4J/vXIwzjKxC1aJjYhtKcj5/+VFF7p4J+60bFW0Lf5h4sjtdLCqYOMs9B40F/BnoMHDPLfODNQ86i4Re4aFhpUODCTGxKShbNCnfYzXQA1QJDUCzUDd0IJoY+bKnomEPWhPdRsKK0luA2kWn/7ToVu1Cy1A/dAJtQPX62O/CxbKMx15k1QjjPHGE/eR9Xns/Tpz/yQvW+VifH2NB1gAAAABJRU5ErkJggg==>

[image2]: <data:image/png;base64,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>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFsAAAAaCAYAAADYMiBQAAADRklEQVR4Xu2XS8hNURTHl1BeeUdC8izyKEoRE6HkFVHKCInkUSaijIwMRIqBlIyUUJLyGtwYUAYor5SBYqIkQpHX+rXOdrflnr5zzr0f383+1b97ztrnnHv2eu19RBKJRCLRrvRUDVeNcEp0Av3EnPtK9UM1PjtHczPbN1W3cEObs1R1T7VJ9VD17vfhQuCLI6rTfqAon8Qc6zkoZp/vB9qQ2aq3qgHZOb83MnsZFoklYCVnEykc+tIPKLvFxio9+C/QX8yBa/1AAz7Ln3Mcp/qomuXseeCrC6o7UtEng8QcetkPKOfExrb4gS7AMdUX1RQp1uaYx3Nno12WmR8VPl1Vk4rOXq/6rlro7JQZL0Jv6wrgUCb6VczRZWBtYi61HHujRPMcUJ0Vu6cmFZ19Uqy8Rkl9d7JN9UKsZ/etX/rPwNG3VR9UQ9xYETpytrc34pFqgjTh7Bmq96p9ka272AJAieaxQSwwHvoiL9+KAPF8Av5atdGNlSXPqXn2GAK9V9U7O6/sbFoIf+ZbyKnM3iiLyHyiPNQPiFWHX4SqsEbMyeukcVDLkufUPHsMu5XH0XllZ98V+7Nezh4WxsnO3hF7VG+8sSJU2BNpTWYD87nlbCQMdlppHuxWuCZPRXcyvx7kYdXG7r8myfQlzgYEZblYkGqRfbRqWXbMvf55HYHDF4h9iOyS5toT86EtxRTZjawUq7SgzWLbzZvZ+eD6pfnQi/ijRmUfokbJABUwU2yBWKGak9nHqJ5JfevFPYwDm/9g5z8ISJk9rSfsRlhLyu5G4IrYriuGd70k9X4MrFfMo0dkiyFABK1QG+Glp6q2ij30qZjTgmMhLHTsweGiaqJY/zwj9a8wjuNg0UJC69mZ/ZKNZDwvT5aQrc0wVmxNQRwXJXxBhkxkfbmf2WN8osUMVO0QSxoSkCpvek0hIJNUJ1T7IzvlxgsH4hIcqToajQXInnne2CLKfEEGuPa4arG0wFGdCaXIBwBbxWlizg49HIeuFmsxBItFjewgAAQCDqv6ZMetgorJK/m25lom2g5sVz1QXVetUl1VHRLLGHoawaHsaCPnM3uiIPRbv78me0MfZiwc8xu2lMOi40QikUgkEv8zPwGF7LW4ewDpHgAAAABJRU5ErkJggg==>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFsAAAAaCAYAAADYMiBQAAADUklEQVR4Xu2XS8hNURTHl1BekUckJM9SHkWImCHyCillhELyKBMlDMwMpAwMpL6MTBhIymtwy8DAAEWkDIiJkgihPNavfXZ3W/ece/Y5fff7Puxf/bvnrn3PuWfvtddjiyQSiUTib2WgapxqvFGiAwwTt7hvVL9U07LvaGlm+6Hq52/oIU6oTlljN7BW9UC1S/VY9eHP4VwGqC6LW4s8HWn+NI4v4m60MGHsy+1Ah5mo6so0xYzVZZHqvWpE9p3PO5m9HSNV96V1kb1WNn9aDruWm17bAeWwuLGLdqAHGS3O6fdUi81YFb5J6xynqj6rFhh7yELVQ2tUzotzViXwHAt63Q5IM3z22IFe4JC4sN+o6m/GYmAeL4yNdFk2v/WSvzY8a7o1lrFd9VO1wtgJM16E3NaXoKhvU71V7TRjRVCbmEujwJ63mEUMVl2TmnXsgrjwIk/67mSf6qW48B3a/Gmfgh3+VHVA3AK0o2yxrb0de6U1HUUxT/VRdTSwEaJ0IN8Dm2WHOMdYyIu8fKcdxK66pfoqLqeXUbSoRfZ28PsN1hgDKYSbbQrpyux5E2HnP1GNsQPioqOW1ytAS0qxPKYabsaKKFrUInsRzP2dapYdiMG3NIOM3RfGqg+l5+RluhuiiLSG8iIqBuZz19jYMNhJpTGcFecYnFQZ2h7+zEKlxW5Pk+z0NcYGOIWqjZMagX2Sal12zb32eWWQiymCFMO6XYiH+eCskJhuxOP77YbUWOx2/TV25B/Kn8wX1+qQr5Zk9smq59KszNzj8xnNvrfzHzikrKf17FZ9Us2VmlU/hxviuq4Q3pXOIiyw1CvmwckxhPfm/SudOXj52eKqKg99Jm7RQm/5Qoc34apqhrgQviTNUxjXobPCfHYw+6RYsuN5+djdOUdq9LAl+BPkqOw79YXDij1B2o3mIXKxV1rsGHDITHGnpOOBnXDjhT1hCE4Ql9Ms7J5l1tiLbFWdU62SavmfTbJF8huDjkAocgCgVWT3sdg+h7Ogm8WlGJxFrmV34AAcAWdUQ7LrRAn0toi0A/tVj1S3VZtUN1Wnxe0Ywg3ncOggjVzJ7DGcVL2KFMV8tbvt34JQsmHE7vV5mDF/zadvKccG14lEIpFIJP5nfgOumb0DlsvjJgAAAABJRU5ErkJggg==>

[image5]: <data:image/png;base64,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>

[image6]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC0AAAAaCAYAAAAjZdWPAAAB/ElEQVR4Xu2WSygFURzG/0J5LYhIyKuUKCk2kghJWUh2bGVv4bWysZAsiI0dZUG2SlZ3IZSFlRXqKmUlO5E8vq//ue5x7nCvR9eo+dXXnfOdM+ee+c83Z0YkICDAN+xCL9A4NGi0ZbxZy7s0ni+4gaasdhq0DV1DVZbfAT1a7T8jExp2vFbRxbHKNg3QqeP9CbVQpeNNiMagy/HZPnA83xAWXXSG4/saRsM3D1wisLpc8JXbEYd50fNG3Y5kUCL65ztuRwLcQc2umQz4ED5L7EMYjzzRbZLbZVJhNFhhRqPU6bPhuHaozPK4C3lFownqd02J9bmdtkEpUA2Ub/V9CqvLKk+7HRbc14fM8YNEF7oEFZhjVnsZOjNtMmZ+vXwWgdsu52gx/obEiWgxVA/tieZ5RbQKRVC6NY5wLMexMp1Qtmg0jiUajW7oCZoRPb8HKjd9Xn6h6BwhiW6zjNqFOf4V+qB10Ul5Yay8/Xpnhfidwgu04YK8fNIreucicD5W/scwPvdWm690RoKT83gSqhO9tSEo522kSJZoXr18wk+GsOXfQo1W+9vwVu5Dq6J/zmiQEdGPqwHT5q2fg06gTejI+OQjn+czYmvQuegF/hqczCvruU6bsKJ2VSN4+cw67yTzner0+Q4usBo6NL//ggpoUTRyC++7AgK+zCuGAVytUuj8tgAAAABJRU5ErkJggg==>

[image7]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADQAAAAaCAYAAAD43n+tAAACPElEQVR4Xu2WuYsVQRDGS1TwwgM8WBSvQBAEBY9IhQWDXUQQMTDQRFMjQUUx0MBkEyMT/wMPUFBBFHZdhE2MBUGFFQQjUwPF4/tR3UxZ+3CfsixvYH7w8Wa+7lcz3V3VPWYdHR0dPXgm/ZIuSSeL7hXvZvA+Fm/g+SJdCfeLpAfSZ2l78Iel7+F+IFkqnU7eQfMXZ3Uiu6U3yRs4dkrbknfZPLWOJJ/7qeS1gmnzAS1Jfmsh3VpR/P3AqjCYT7mhrWw0H9DT3BAYl85kcx44K73I5mywIfy0mRtCJG/n8wVZk3fev0K6sTL8cVNqg/XSFmnCZu6Mq6Qd0oLgDUmjxaNtZWiDhdJeaXnyYYN0WFosrTCPRW2fKl5fsCqsztXcEKBPXD1e9p20VVojvTZ/ARgxHxCHNi/EGba2tB2w5vw7b/5c4KyjP3HXWZP6dbL72nl52C7puXn93JaOm89Sng0GG9ONGb5erun/oVzztUHc2p84+0obh/lj8/5AGpEV1a+rz3tcLNdkzD+lWz8QNO5+rMRLa2b9gvlnVCX3r5ywP48FapKB1wzpRZ7IOYEH/ijXh6wZUK0Bvv9eSWPSZvP+30pb5Jj0NdwTk777kw/LrEk3nsNK96rv/4LCfis9kfYUj+AM5JF0TXpvXh9wV3pYrjPU1rT5/2JtEPe+dEe6ZT4I6umGeTx+5xRmKNcVu1/dCFYHH2+2IiaNOCoixEOZGHugoH7OmX8Ys6J5glpHrbVJ6Whq6+hoE78BlLNg56vbAwMAAAAASUVORK5CYII=>

[image8]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC4AAAAaCAYAAADIUm6MAAAB/ElEQVR4Xu2WTyhlYRjGX2lKTDERiXLNlC0iRWGjsJGFnbKexaxsRBY2FpQFWUnJwkIsbGysbs2CUjNLGhRFSkkpU5I/z9P7HT5vx9m4p3vk/uqXe9/nXuft+977nSOSI8fn4gusgJXGEv9DSaRAtNEz+Ah/uPeBW64+BPPcdxLFf9EGLflwFN7CdpNlHa4kmz61gQfzG1vMNt9EG9u0gQfzsB3JKoPwAXbZwCORjS+Kjkm1DTwS13g9vIZjNvBoEm161wagEK6J5r0mixWOCS8aNSa/RD8zYeo+5/C7LcYJV5FN8TwPo0d0/n/awKMKztli3PCIi5rdf6I577CWYtEx6oR9JmuG/aZGbJ2j2iF6JNfBUi97k6jzuwHuwSVYZDJ+7wCmRC/0B3512bzLAoYj6tzlWtHdanP1FYk4lnnhFtHtZ+P7cMCTP1TWL9xnLa3yMu8ck+PnROReNOMOdcOaiHq56D0kLS+jug6P3OuMwpVNwzL3fgReute8+InoM47PW3XCk4iPEwF3EtPvJWg8GB+u0G84LbqKzIKxITwuuWthdTIpr3fsCjZ67zMKb1RseAOOw0PR0SNT8C9chTuuFlXnMcqTbVn0/4SNZkbhfAYraJ/dWfdXNyCsztnnPYT/j0+iiYdN8tl/2/39MKTgLFyAM6+jHDnexRPLr2Q8Cre5/wAAAABJRU5ErkJggg==>

[image9]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACwAAAAaCAYAAADMp76xAAAB2UlEQVR4Xu2WzytFQRTHj6QIIQpFRFkpyo9SyMKCBVlYKGXDgliwkLCxtVRWUv4B2dlI+bW0FpEdKRulKBt8v50zvTGel8V73RvvU5/e3DnjOjP3zNwrkiXL3yIPVsLqwFJ/UJzIF03wHn7ARrt2Hlj/BMyxv4kFr6KJheTCZfgGe4JYZHDlmOxdGPBg/CXsjIoy0YT2w4AH48meQCSMw3fYHwY8YpXwtmg51IQBj9gk3AKf4UoY8GgTTfY8DEQBy4HJpCqHOdExa0F/JHDVmAzP42QMiNb3dBiICh5VqWrzWjTON6KDx2Cv9fG324sRTn4Ilts1z3KWFX/r4Yi1CcfxHr8i1fnbCi/hDiz0+gvghuhG5WQHJTHhIngKS+x6U/S1z/GH8Mn6CZ/aorWZNCf0I0y0U/Qx859dwVFPbkD2P9pYn1q4Cs/gLqyCsxbj/caszVf5HmyHU6KLsm4xPoFj0QmSJdhg7YzBV3mHd10BLySRRMiDJJLiBh+2drN8XfmMweSYpKNYdNV9XN1zRVkSrrT8FeUJxIS74IL1pZ06OBl2itbuCdyCR7DJ+plMn7VZ07fWJvPwBs7I9/JLG7yx2+Uh/I7mZ6kPx/rJuE3piO23d5Ys/5JPlRhTBD6O2HIAAAAASUVORK5CYII=>

[image10]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADEAAAAaCAYAAAAe97TpAAACIUlEQVR4Xu2Wv0tVYRjHv6KGYVaCFIIiGg3h0ODgouBQUYO6KBqFBIUtTUn4FzhIaxC4iIOIFBSIBSJ6dZKMwEFscXBqCkHQJSq/X57n3PPe0xVB1O6B84Ev973P+5xz3+fXORfIyMg4CSPUXtKYJiqov67U0omUB/GY2oC1UmqD2KQGqB1YEGWF26VPG9Xu6xwsiNr8bgq4SM0hznwOFkR95JAGNAeah4gpWBCqTipQ9r9QN2GZl8ZhQXQEfsdxC/ZkO3cqqUnYuyGkGxbE84T9KJSIafynGbpLbSeNiIMYTW4492A+Qolopb7DqngpcnK6EPuKB1QjVQ27T3mwJ1TRviL2oshpi7qe3IDNwj5sNkLk+9XXg9QdX6tiP30d8YlaDb7r8PLXIeWrh4nYdbt4AeuKK9Q8VeX2f1Dp+6kF2A2eFW7jKvWa+gPLbg/im0XB3YAFpCoItdK6ryN0vQLVtUOwgz2B3e937IZf1EtfK2mqQg3VlPc4Ay5TH2DtppYQB9SjvAdQB3tMJ1tLLFLvfa2sqyqqjlCCx2AvW1XuTFAG7/taPxZVSH9TblMPqV5YJpOteME/fyCetWbqLSyYb9Rnt7cgbrFTR+8THW6NehXYdbBZqiGwzVAr1EdqObCrhXW99qKKiDfUEvUOhf6njh4G1/wzRBWRPYnmKxxOtZcGVkNdrNVkK2YvGXS4YdiQK7hU8pSacOmplZFRChwCMkRbK7okLM0AAAAASUVORK5CYII=>

[image11]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADcAAAAaCAYAAAAT6cSuAAACVUlEQVR4Xu2WTahOURSGl1BEIfJTRIoSRSEpMsFl4LckkZGYMDJQRkoGkkKZSMnAwMgAA1dxMyGUDERkoJSRlGJggPex1nbWd/pck3u53+m89XT23uv8rb99jlmrVq1Goo6Kz/XFJmiM+BE0Tmutoc7tE8/NS7Jxzr0Qu8U7c+dGdZp7V8vFqhgPmDs35be1hzVe3LQqUwPmzs0qJ/Sy6DP6reiquXNks6dFth6LBeaZgtPmzq1J5xUtMt9R/7Wmi3v1xcE0Vlwx/7ZlbTF37lBtnUBcs//Ti8fFh/riYNog3tYXrXLuWFojEIvFK/PsTkw2srkxzdFo88xznCCWWufuy3ihmJrWinjWdjHH/HqydlfcF5PTeX8UF70UM+oG8177Yt57WWTyY5rPFa+temkCstX8nufFNPPgzQtbqQSuO2l+3SbxPdapoDfm56PDcUTfxPo07ypuuEv0i0/iQKf5V2TOmD+QLPGy48JGST6JMbos3qc5jpPFFeb3nS1Ohe2geQZ5/jmxJNb3iq8xppJOxLhP3IkxoiTnp/mQi5fgZYpyNsjWhWRD9AkOZq20yhlEsAgaAbxt3T8/OUjDJn7L6J09Ypu5c5vDRn/tFKtjXl62ZL2olHwRYwJUNqvcy7QOohzLc47EcchFaVy3Khv0BN9Imn2HeRmdDRtOUvbdtMz8F4/r+OWjNxEbyTNxSTwS62KdjeeGuBXzYRFZYOfKItIlwrxkGXP82ycDO5+ivItyv26lyXNxfkSLUia7M8UDManT3Nu6KB6Kp2J/zdaqVdP0EziQZWtZaqQtAAAAAElFTkSuQmCC>

[image12]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAD0AAAAaCAYAAAAEy1RnAAAChElEQVR4Xu2YTahNURTHl1C+PyJS6kkMFFE+ShkKLzEQUqZiQBlJmRmYGCEjM8qIMpAU4uVNmMhESQyUGEgyoKTw/1l7c85659wnvdvd6fzq371nrXX23R/rrHXeM+vo6PifmSbNi8Z/YEmDGLtIZplP8IP0Q1qTrjN83558o+maeyLVuCvpGu2Q7kifpZ2/owvhm/mEm9ht7jsSHYE95nEHg31qsr+VVgTfwJhiPql30WF+qiPSM2lh3VUjx5ENs+uuXzA+Ohkdg4LFMKFb0SGWm2/GVWlS8FXJcReiQ8w3H/+7tDX4BgZp2zahM+YT3hgdgRy3KtiHpBfSbWlu8A0MUvu6+aJvSJeCOD0W0yu14Z55XE5tithq6VMSz3UxbDEvYpxUE/lZHI8YN106Lb2XNlTsRUBqM9mm1AZ8X6KxAeJoe1UobtjJoH5yV1oQjb2gKjOxmdFhXpzwUcR6keNiEcsFjN/oF0utPUtbmYj+nOPo01XWJvtIsE82f6z4ZLOJq3aGxdIuG1sHKJJ7ze8D6sY+6YD5PX9Fv/szPZnxL6frzdJj6bz5mK+kZSmGjWXx1IC8AbTQvJhj5vOlA2DnFRfl7+PCoJuko+Y/+Fxaab4AdnGRdEL6mnz7bezAMe6htM3qcZwA49Md+M1zSYesnpaHzU/8pvQm2VgsY+cNYOM4ZTZ2KNkYI8cXxXrzKn5cmlOxnzKfdBXaZtsbG4tnk15Lw8nGGE1ZWiRtaUmX4FnOzDDPqCfmLzdA0cydhjF4P+DZP5tsxcKz/TEaxTrpqflL0SP701EuSvela9KDZAMy6GX6jEWvODg92lkTuVbkCp2h3jT9STsR/wvo6OjoKJ+fBpyHeNbFA0gAAAAASUVORK5CYII=>

[image13]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAD4AAAAaCAYAAADv/O9kAAACp0lEQVR4Xu2WTahNURTH/0IRhYhEPYRSpHyVj2QgTEgGIiMMKKYoMjAwMDQiKaUwUUyUMLhloowUMRFKjKQMFPKxfq29vX2W826v6+kevfOrf3d/rLvPXnuvvfaWWlpaRhMTTFNjYw/MMs0OmlyxaBhMjkl+MP00LUv1DOWtqe9hqtc5RPtyVe3QOtNV03fT0d/WDeKbfNJ17JD3HYodgdVyu7OhfUxq/xLa+844+cTexw757nZMz0wzql0VcO6K6a1pbugDxh9qYfsGDjGpO7HDWCBfkGty54ZimumxfAzyRkle2MY5Tgj/MG2OHfKwZcKEcTf2ye3iGFNMD0xPTQOhr6+wGzfljt8yXQpit3GoW5jDZbldDnOy/CLTG9NX06TU3hg2yBNbTEiZ4YboJ1XtxpoOyp3eVbT3ynrT/tj4NxDmdSGaoe9zbKwBO6KmJGfzJ6G9F17KE+yIwWBMri4USWz0kdi6QWLDLibHnNR4IzSOkbi/V8rtToZ2zjntnPMSImGjabzcZnsqw5akkumqPqo4RnyT33mmnak8bP71/Y1DjN9J9fmmFabz8mTIay6D3YVUxin+CxdNC+XHba18ofh/x/Qx2QD1uhdlBSa7xnRE/sEX8gzMH1m5maZj8pcWfbv1593MGOzEYdM7DdqVH2eijM/9DtjynVPyZy23SOa1aU4qE2kkXcCWaHgkvxpXmfbKF/pcsmFuXJl1x7VvLDYdN51WNVw5Ytm5JaYTqcyOPlf1scRRW1rUgSglB8Ee+SL/F5ClcRLKHd4mvwI5FuzoRNNd+a7mHFLuMMf1hjwaDqT+xjIgv+OByeMEDgBn+5XpjDzEOTr3TLc1+PJjdzelMjbXTfflx6DREMZlFo5JKdaxzVk/18ujQDnmoJaWlpbRwS+oyok+CdLCKgAAAABJRU5ErkJggg==>

[image14]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAAAaCAYAAAAHfFpPAAACqklEQVR4Xu2YTahNURTH/0IR5TMSeQhlIEVekYx8TRgYmBjKRzFFkfIGkiET9XovpcwUA2YGtwyNFDEglBiZKAr5WL/W3u456553eoneVudX/94+a6+77157r732uU/q6Ojo6DPLND8a/4ClpmVBc2sehcIkmewH00/TxvScob039T1Mz02BYd+kuh/abrpp+m469du7QL7JJ9/EAXnf8dgR2Cr3uxTs05L9S7AXwwz5BN/HDvlu90xPTYvrXTUI8obprWlF6APGn2iBpxwCY3L3Y4exRr4wt+RBTsQC0yP5GNSVKnmBi10AUvuHaVfskKczEye92zgs94tjzDM9MD0xDYW+ImB3bssX4I5pNIjdJ7C29IcxuV9Of26FdaY3pq+mOcleHDvkBTAWrsxkU/ej6n7TTUfkwR+s2IuD9G9K3Qx9n6OxAfzIoiq5+j8O9qKgujPJphSlANJHAWyDAohfLKK5+PGOUSx/4/7fIvc7F+zUAezUgSpkxk7TTLnP/tSGPUkRiin2eBPxuTwWx44jzd9J8a/vfwJj/F56Xm3abLoqL5q8HWbwu57aLCifBcY/Y1qVnrlqe6k927Q2tT+ZLsqPIfNphUGHTSflX/xcXrEJmtVbYjotf3Oj75AG73bGWGQ6YXqnvl/1NXmbfHwmDfjyPeflr8vcOpnXpuWpTeaxk8BiEFzmpelaaufggbnymWMa3IgpZb18By+o/huDo5eD3GA6m9ociWfqp3pPnoUZ6gn+VVh0rnIy+r+BnSRYqO74PvnVyXG5Il8AXqSAAMmchaaV8p3erfoCHlVzDSmKIfk7AnD7EGDePc7+K9OIvLARJEHfNV02vTDdS74sGjcUZ54sGddgdhQJ6V2t1PHndXzGN9v430W1nzrEeNhod3R0dHS08QtU1o0qKLMIYQAAAABJRU5ErkJggg==>

[image15]: <data:image/png;base64,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>

[image16]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAmwAAAAxCAYAAABnGvUlAAAEC0lEQVR4Xu3cS6htcxwH8L9QXnnklSgxkyKJUoxMTChGZCgxMTGgSJ2J8ohEKIkMyGNgQglplwEhpTxG6pIyMBChXM//t/X/n73uss++++ic3XV8PvXr/1jr3L32Prf2t9/a+5QCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADAKm6bbkwcX+uJWsdODwAAe9/Z0409IOHmv+LFWr/X+mt6YOTSWm+3eR8BgP+R2XRjD7hzunGIu7gsD2y/1jqrzc8tw/kAwBqcV+uHMu9wfVHr5Fr7aj3U9tZhNt1Y4Jta+0frV9v482jvULJKYPu0VSQMfdLmy4LTblkW2I4rw7GMff36/DAAsJteqvVhrVtqHVaGN+WMd5T1viHPphsTj5Thur5t6wSGHoieauOh5mCB7dZaR5Z5SHq2VWTvqDbfrq+X1Fuj86a2G9hmm0cBgF3X36RvLEN4i9NrXdjmU3dNN/6FK8sQtHp9N1kfPT91U27D/dbm99Y6os23us5FrmhjfmZZIE2AjTzOqsHpgnLgc/hosj51fuqmk8rwukd+D1nHB22MHlJ327LAli8ZTAPbstcPANhhszb2TlskqGwlwWmnzaYbCzxd5h2ocYh5eTRfJh26HohW9ct0YxsO1mGL28s8BI3D0kYbzyzLfxeLTLtqO9Fhixw7o80z9v8rAMAaPN/G72td3eYvtDFeq/V4GQLPOKy9X+v6Wq+M1neXoTuW8+8rQ/cot/0OZjbdWOC5Mu/u/dnGXNNGm+dx8ngfl6FDGO/VeqzWRbXeLPPbp7m+fFYvP5PrjnzzMet72jphKp2/+8vwGn3e9vM6rWKVwJZz8hxiHJZ69zDH36n1ZRnOS7jLZ/merHVOO2enLApsWV/T5m/UuqrNs7eoCwoA7JKElMva/MRa54+ORd60n2nzfhsstxTTsXmgDEHix7Yef3Mw3aG4brS3ldl0Ywu5PZlrjMtrHT461m+X5tuM0UNd99loPu6cJQBF7xhttDHypYxIgOrBbtVbwqsEtsjrdFqb509njAPuH23cN9obP491y63RR8tqIRwAWJN0q/Im/VVb7691U61LNs8o5ZhyYABKiOqduHSBerdomROmG9uUzlM6ZHmsd8sQJMffHu2h8oa2Tuh4sM17sOrXmee4UeuUtn64DEG0dx9XvSW86mfflpm1MWHx5jZ3KxIA+If+uaUYh5B0hcYdrt4lilkZbjmuU7+W3oGLra69h7HI/vhY/0zZeJ7Qmn/32tGxdei3S9f9WgIAe1z/ExB7yU9l+MzW+NubAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGzlb17UoY9lf/p1AAAAAElFTkSuQmCC>