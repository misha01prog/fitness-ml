define e = Character('Персональный тренер', color="#4400ff")
default povid = config.save_directory
default povsex = 0
default check_data = None


image blank = "gui/overlay/game_menu.png"


label start:

    scene blank
    show screen quick_menu
    show trainer with dissolve
    # show bca
    # hide bca
    label check_sleep:
                menu:
                    e "Сколько часов вы сегодня спали?"
                    "8 и больше":
                        $ povsleep = 8
                        jump control
                    "7":
                        $ povsleep = 7
                        jump control
                    "6":
                        $ povsleep = 6
                        jump control
                    "5":
                        $ povsleep = 5
                        jump control
                    "4 и меньше":
                        $ povsleep = 4
                        jump control
    #-------------------------------------------------------------------------------------------#
    # Проверка, есть ли в БД запись о пользователе
    # Если записи нет, то приложение собират данные пользователя и отправляет их в бд

    label control:
        python:
            import requests
            from requests.adapters import HTTPAdapter
            from urllib3.util import Retry

            user_id = povid

            class Server:
                server_url = "http://158.160.4.195:8080"
                session = requests.Session()
                retry_strategy = Retry(
                    total=3,
                    backoff_factor=1,
                    status_forcelist=[413, 429, 500, 502, 503, 504],
                )
                default_timeout = 10  # 10s for timeout
                adapter = HTTPAdapter(max_retries=retry_strategy)
                session.mount("http://", adapter)

                # Возвращает None если пользователь не найден или его данные, если найден
                def get_user_or_none(self, user_id: str) -> dict | None:
                    response = self.session.get(self.server_url + f'/get/{user_id}', timeout=10)
                    if response.status_code == 200:
                        return response.json()
                    elif response.status_code == 404:
                        print(f"Нет записей для пользователя с user_id '{user_id}'")
                        return None
                    else:
                        print("Ошибка при запросе сервера, код:", response.status_code)
                        return None
                        
                # Возвращает количество отжиманий и подтягиваний для пользователя + сохраняет введенные данные в базу данных
                def score_user_data(self, user_data: dict):
                    data = {
                        "id": user_id,
                        "age": user_data.get('age', 0),
                        "sex": user_data.get('sex', 0),
                        "weight": user_data.get('weight', 0),
                        "height": user_data.get('height', 0),
                        "fat": user_data.get('fat', 0),
                        "sleep": povsleep,
                        "cls": user_data.get('class', 0)
                    }

                    response = self.session.post(self.server_url + '/score', json=data, timeout=15)
                    if response.status_code != 200:
                        print("Ошибка при запросе сервера, код:", response.status_code)
                        return None, None, None
                    content = response.json()
                    print("successful response with content:", content)
                    pushups, pullups, squats = round(content["pushups"]), round(content["pullups"]), round(content["squats"])
                    print(f"predicted pushups: {pushups} pullups: {pullups} and squats: {squats}")
                    return pushups, pullups, squats
                
                # Сохранение сделанных упражнений
                def save_made_excersises(self, excercise: dict):

                    response = self.session.post(self.server_url + '/train', json=excercise, timeout=15)
                    if response.status_code != 200:
                        print("Ошибка при сохранении упражнения запросе сервера, код:", response.status_code)
                    else:
                        print("Упражнения сохранены")
                    return response.json().get('motivation')

            # main logic
            server = Server()

            user_data = server.get_user_or_none(user_id)
            if user_data is not None:
                print("Найдены данные пользователя в базе данных:", user_data)
                povsex = user_data['sex']
                check_data = True
            else:
                check_data = False
            
        jump process
 
    #-------------------------------------------------------------------------------------------#

    label process:

        if check_data == True:

            python:
                # Отправка данных для получения кол-ва упражнений
                print("Отправка данных для получения кол-ва упражнений")
                pushups, pullups, squats = server.score_user_data(user_data)
                if pullups or pushups or squats is None:
                    print("Не смогли получить кол-во отжиманий. Сорян")

                print(f"Вам предсказано pushups={pushups}, pullups={pullups} и squats={squats}")
                adaptive_pushups = int(pushups)
                adaptive_pullups = int(pullups)
                adaptive_squats = int(squats)

            jump workout
        
        elif check_data == False:

            menu:
                e "Какой у Вас пол?"
                "Мужской":
                    $ povsex = 1
                    jump choice_fat
                "Женский":
                    $ povsex = 2
                    jump choice_fat

            label choice_fat:
                menu:
                    e "Какая у Вас степень полноты?"
                    "Низкая":
                        $ povprocfat = 1
                        jump choice_cls
                    "Среднияя":
                        $ povprocfat = 2
                        jump choice_cls
                    "Высокая":
                        $ povprocfat = 3
                        jump choice_cls

            label choice_cls:
                menu:
                    e "Как вы оцениваете ваши силовые показатели?"
                    "Низкие":
                        $ povclass = 1
                    "Средние":
                        $ povclass = 2
                    "Высокие":
                        $ povclass = 3
                if povsleep != None:
                    jump choice_other
                else:
                    jump choice_sleep
            
            label choice_sleep:
                menu:
                    e "Сколько часов вы сегодня спали?"
                    "8 и больше":
                        $ povsleep = 8
                        jump choice_other
                    "7":
                        $ povsleep = 7
                        jump choice_other
                    "6":
                        $ povsleep = 6
                        jump choice_other
                    "5":
                        $ povsleep = 5
                        jump choice_other
                    "4 и меньше":
                        $ povsleep = 4
                        jump choice_other

            
            label choice_other:
                
                python:

                    povage = ""
                    while povage == "":
                        povage = renpy.input("Сколько вам лет?", allow="1234567890", length=2)
                        povage = povage.strip()
                    
                    povheight = ""
                    while povheight == "":
                        povheight = renpy.input("Какой у вас рост?", allow="1234567890", length=3)
                        povheight = povheight.strip()
                    
                    povweight = ""
                    while povweight == "":
                        povweight = renpy.input("Какой у вас вес?", allow="1234567890", length=3)
                        povweight = povweight.strip()

                    
                
                python:
                    user_data = {
                        "id": povid,
                        "age": povage,
                        "sex": povsex,
                        "weight": povweight,
                        "height": povheight,
                        "fat": povprocfat,
                        "sleep": povsleep,
                        "cls": povclass
                    }

                    # Отправка данных для получения кол-ва упражнений
                    print("Отправка данных для получения кол-ва упражнений")
                    pushups, pullups, squats = server.score_user_data(user_data)
                    if pullups or pushups or squats is None:
                        print("Не смогли получить кол-во повторений. Сорян")

                    print(f"Вам предсказано pushups={pushups}, pullups={pullups} и squats={squats}")
                    adaptive_pushups = pushups
                    adaptive_pullups = pullups
                    adaptive_squats = squats

                jump workout
        
        else:
            e "Ошибка сервера! Куда-то потерялись ваши данные..."

        # -------------------------------------------------------------------------------------------------------------------- #
        
        label workout:

        image pushUps_image = "images/pushUps.png"
        hide trainer
        show pushUps_image

        e "1-е упражнение - отжимания от пола"

        python:
            podhod_push = 1
            adaptive_pushups += 3

        init:
            $ podhod_push = 1
        
        $ max_count_push = 0
        $ sum_count_push = 0

        while podhod_push <= 3:
            
            e "[podhod_push]-й подход. Сделайте [adaptive_pushups] отжиманий"
            
            python:

                fact_count_push = ""
                while fact_count_push == "":
                    fact_count_push = renpy.input("Сколько раз получилось отжаться?", allow="1234567890", length=2)
                    fact_count_push = fact_count_push.strip()

                fact_count_push = int(fact_count_push)

                if fact_count_push == adaptive_pushups:
                    adaptive_pushups = int(adaptive_pushups)
                else:
                    adaptive_pushups = int(fact_count_push)
                
                if fact_count_push > max_count_push:
                    max_count_push = fact_count_push

                sum_count_push += fact_count_push
                
                podhod_push += 1
        
        
        if povsex == 1:
            image pullUps_image = "images/pullUps.png"
            show pullUps_image

            e "2-е упражнение - подтягивания на перекладине"

            python:
                podhod_pull = 1
                adaptive_pullups += 1

            init:
                $ podhod_pull = 1

            $ max_count_pull = 0
            $ sum_count_pull = 0

            while podhod_pull <= 3:
                            
                e "[podhod_pull]-й подход. Сделайте [adaptive_pullups] подтягиваний"
                
                python:

                    fact_count_pull = ""
                    while fact_count_pull == "":
                        fact_count_pull = renpy.input("Сколько раз получилось подтянуться?", allow="1234567890", length=2)
                        fact_count_pull = fact_count_pull.strip()

                    fact_count_pull = int(fact_count_pull)

                    if fact_count_pull == adaptive_pullups:
                        adaptive_pullups = int(adaptive_pullups)
                    else:
                        adaptive_pullups = int(fact_count_pull)
                    
                    if fact_count_pull > max_count_pull:
                        max_count_pull = fact_count_pull
                    
                    sum_count_pull += fact_count_pull

                    podhod_pull += 1
        else:
            python:
                sum_count_pull = 0
                max_count_pull = 0

        image squats_image = "images/squats.png"
        show squats_image

        e "3-е упражнение - приседания"

        python:
            podhod_squats = 1
            adaptive_pullups += 3

        init:
            $ podhod_squats = 1

        $ max_count_squats = 0
        $ sum_count_squats = 0

        while podhod_squats <= 3:
                        
            e "[podhod_squats]-й подход. Сделайте [adaptive_squats] приседаний"
            
            python:

                fact_count_squats = ""
                while fact_count_squats == "":
                    fact_count_squats = renpy.input("Сколько раз получилось присесть?", allow="1234567890", length=2)
                    fact_count_squats = fact_count_squats.strip()

                fact_count_squats = int(fact_count_squats)

                if fact_count_squats == adaptive_squats:
                    adaptive_squats = int(adaptive_squats)
                else:
                    adaptive_squats = int(fact_count_squats)
                
                if fact_count_squats > max_count_squats:
                    max_count_squats = fact_count_squats
                
                sum_count_squats += fact_count_squats

                podhod_squats += 1

        python:
            exercise_made = {
                "id": povid,
                "pull_ups": max_count_pull,
                "push_ups": max_count_push,
                "squats": max_count_squats,
                "sum_pullups": sum_count_pull,
                "sum_pushups": sum_count_push,
                "sum_squats": sum_count_squats
            }
            motivation = server.save_made_excersises(exercise_made)
        
        python:
            size_mativation = len(motivation)
            i = 0

        init:
            $ i = 0

        while i < size_mativation:
            if len(motivation) != 0:
                $ item = motivation[i]
                e "[item]"
            python:
                i += 1

        e "Вы закончили тренировку, поздравляю! Приходите послезавтра"

    return
