# Сравнение сообществ VK

![vk_image](/images/vk_group.png)

* [Описание](##Description)
* [Установка](##Download)
* [Использование](##Usage)

## Description

С помощью данного приложения можно наглядно сравнивать группы и сообщества социальной сети [Вконтакте](https://vk.com), получать актуальную статистику и наблюдать динамику за любой период на графиках.

## Download

```console
git clone github.com/makarovNick/vk_group_analytics
pip install -r requirements.txt
```

## Usage

```console
usage: vkcompare.py [-h] [--groups GROUPS [GROUPS ...]] [-w] [-t TOKEN] [-d N_DAYS]
               [-mc] [-ma] [-iu] [-cu] [-ppd] [-vpp] [-lpp] [-l] [-s] [-c]
               [-u] [-tv] [-mv] [-tvis] [-mobr] [-tr] [-r] [-fvis] [-mvis]
               [-1v] [-2v] [-3v] [-4v] [-5v] [-6v] [-7v] [-RUv] [-NRv] [-fr]
               [-mr] [-1r] [-2r] [-3r] [-4r] [-5r] [-6r] [-7r] [-RUr] [-NRr]
               [--all]

optional arguments:
  -h, --help            show this help message and exit
  --groups GROUPS [GROUPS ...]
  -w, --web             Generate interactive web ui
  -t TOKEN, --token TOKEN
                        Access token
  -d N_DAYS, --n_days N_DAYS
                        Days for statistics
  -mc, --members_count  Show members count in table
  -ma, --mean_age       Show member's mean age in table
  -iu, --inactive_users
                        Show inactive_users in table
  -cu, --common_users   Show common_users of two groups in table
  -ppd, --posts_per_day
                        Show posts_per_day in table
  -vpp, --views_per_post
                        Show views_per_post in table
  -lpp, --likes_per_post
                        Show likes_per_post in table
  -l, --likes           Show daily count in table
  -s, --subscribed      Show subcribers daily in table
  -c, --comments        Show comments daily in table
  -u, --unsubscribed    Show unsubscribed count daily in table
  -tv, --total_views    Show total_views count daily in table
  -mv, --mobile_views   Show mobile_views count daily in table
  -tvis, --total_visitors
                        Show total_visitors count daily in table
  -mobr, --mobile_reach
                        Show mobile_reach count daily in table
  -tr, --total_reach    Show total_reach count daily in table
  -r, --reach_subscribers
                        Show reach_subscribers count daily in table
  -fvis, --f_visitors   Show f_visitors count daily in table
  -mvis, --m_visitors   Show m_visitors count daily in table
  -1v, --_18_21_visitors
                        Show 18_21_visitors count daily in table
  -2v, --_21_24_visitors
                        Show 21_24_visitors count daily in table
  -3v, --_24_27_visitors
                        Show 24_27_visitors count daily in table
  -4v, --_27_30_visitors
                        Show 27_30_visitors count daily in table
  -5v, --_30_35_visitors
                        Show 30_35_visitors count daily in table
  -6v, --_35_45_visitors
                        Show 35_45_visitors count daily in table
  -7v, --_45_100_visitors
                        Show 45_100_visitors count daily in table
  -RUv, --RU_visitors   Show RU_visitors count daily in table
  -NRv, --NOTRU_visitors
                        Show NOTRU_visitors count daily in table
  -fr, --f_reach        Show f_reach count daily in table
  -mr, --m_reach        Show m_reach count daily in table
  -1r, --_18_21_reach   Show 18_21_reach count daily in table
  -2r, --_21_24_reach   Show 21_24_reach count daily in table
  -3r, --_24_27_reach   Show 24_27_reach count daily in table
  -4r, --_27_30_reach   Show 27_30_reach count daily in table
  -5r, --_30_35_reach   Show 30_35_reach count daily in table
  -6r, --_35_45_reach   Show 35_45_reach count daily in table
  -7r, --_45_100_reach  Show 45_100_reach count daily in table
  -RUr, --RU_reach      Show RU_reach count daily in table
  -NRr, --NOTRU_reach   Show NOTRU_reach count daily in table
  --all                 Show all statistics table
```

|Название Аргумента|Описание|
|-----------------|-------|
|**h, --help**|Помощь|
|**-groups GROUPS [GROUPS ...]**|Список групп для анализа|
|**w, --web**|Использовать веб-интерфейс|
|**t, --token TOKEN**|VK API token|
|**d, --n_days**|Кол-во дней для усреднения статистики|
|**mc, --members_count**|Кол-во полььзователей в группе|
|**ma, --mean_age**|Средний возраст|
|**iu, --inactive_users**|Кол-во неактивных пользователей (>=30дней)|
|**cu, --common_users**|Кол-во общих подписчиков (для двух групп)|
|**ppd, --posts_per_day**|Кол-во постов в день|
|**vpp, --views_per_post**|Кол-во просмотров на пост|
|**lpp, --likes_per_post**|Кол-во лайков на пост|
|**l, --likes**   *|Лайков в день|
|**s, --subscribed**   *|Подписчиков в день|
|**c, --comments**    *|Комментариев|
|**u, --unsubscribed** *|Отписок в день|
|**tv, --total_views** *|Просмотров в день|
|**mv, --mobile_views** *|Просмотров с мобильных устройств в день|
|**tvis, --total_visitors** *|Общее кол-во посетителей в день|
|**mobr, --mobile_reach** *|Охват пользователей с мобильных устройств в день|
|**tr, --total_reach** *|Общий охват в день|
|**r, --reach_subscribers** *|Охват среди подписчиков в день|
|**fvis, --f_visitors** *|Посетителей женского пола в день|
|**mvis, --m_visitors** *|Посетителей мужского пола в день|
|**1v, --_18_21_visitors** *|Посетителей 18-21 год в день|
|**2v, --_21_24_visitors** *|Посетителей 21-24 год в день|
|**3v, --_24_27_visitors** *|Посетителей 24-27 год в день|
|**4v, --_27_30_visitors** *|Посетителей 27-30 год в день|
|**5v, --_30_35_visitors** *|Посетителей 30-35 год в день|
|**6v, --_35_45_visitors** *|Посетителей 35-45 год в день|
|**7v, --_45_100_visitors** *|Посетителей 45-100 год в день|
|**RUv, --RU_visitors** *|Посетителей из России в день|
|**NRv, --NOTRU_visitors** *|Посетителей не из России в день|
|**fr, --f_reach** *|Охват женского пола в день|
|**mr, --m_reach** *|Озват мужского пола в день|
|**1r, --_18_21_reach** *|Охват 18-21 в день|
|**2r, --_21_24_reach** *|Охват 21-24 в день|
|**3r, --_24_27_reach** *|Охват 24-27 в день|
|**4r, --_27_30_reach** *|Охват 27-30 в день|
|**5r, --_30_35_reach** *|Охват 30-35 в день|
|**6r, --_35_45_reach** *|Охват 35-45 в день|
|**7r, --_45_100_reach** *|Охват 45-100 в день|
|**RUr, --RU_reach** *|Охват пользователей из России в день|
|**NRr, --NOTRU_reach** *|Охват пользоваталей не из России в день|
|**-all**|Использовать все статистики|

* \* - Возможно только при открытой статистике группы, иначе будет отображенно "No Access"

## CLI

```console
test@test:~/$ python main.py --groups chamber13 kod neurohive
Working... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
Working... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
Working... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┓
┃ feature/screen_name ┃ chamber13          ┃ kod                ┃ neurohive          ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━┩
│ posts_per_day       │ 11.0               │ 8.5                │ 1.0                │
│ views_per_post      │ 2726.343434343434  │ 2702.8888888888887 │ 2291.6969696969695 │
│ likes_per_post      │ 205.7979797979798  │ 15.212121212121213 │ 23.0               │
│ members_count       │ 11901              │ 63786              │ 8926               │
│ mean_age            │ 29.963957759412306 │ 30.710679033778085 │ 29.756473287446738 │
│ inactive_users      │ 1772               │ 13789              │ 612                │
│ likes               │ 2296.8571428571427 │ 143.0              │ No access          │
│ subscribed          │ 8.0                │ 17.571428571428573 │ No access          │
│ unsubscribed        │ 4.428571428571429  │ 17.428571428571427 │ No access          │
│ RU_visitors         │ 343.85714285714283 │ 286.85714285714283 │ No access          │
└─────────────────────┴────────────────────┴────────────────────┴────────────────────┘
```
<!-- RU_visitors daily of chamber13
RU_visitors
       +------------------------------------------------+
  2500 |                    **********************      |
       |            ********                      ******|
       |    ********                                    |
  2000 |****                                            |
       |                                                |
       |                                                |
  1500 |                                                |
       |                                                |
       |                                                |
  1000 |                                                |
       |                                                |
   500 |                                                |
       |                                                |
       |                                                |
     0 +------------------------------------------------+
       3                     2                          1
                           days_ago
``` -->



## WEBUI
![webui](/images/webui.png)
<!-- ## GROUP GRAPH -->
<!-- ![group graph](/images/graph.png) -->
