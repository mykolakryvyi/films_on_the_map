# Призначення модулю

Користувач вводить бажані координати, після чого для нього генерується
html-карта, на якій, за допомогою маркерів, зображені мітки - його локація
а також локації максимум 10 місць, які були використані для зйомки фільмів
у певному році(рік також вводить користувач). Також на мапі зображен шлях від
початкової локації, який проходить по всіх мітках, які є на карті. При натисканні
на кожну мітку відображаться назва фільму, який був відзнятий у тій локації.

# Короткий висновок

Програма дозволяє наочно проаналізувати, скільки фільмів і де сами були
відзняті у певний рік та біля певної локації. 

# Приклад запуску

### (49.651179, 24.2450), 2012

![Input](Ukraine.jpg?raw=true "Ukraine, 2012")

### (-22.071530, 122.475435), 2013

![Input](Australia.jpg?raw=true "Australia, 2013")

### (51.750641, 18.342718), 2012

![Input](Poland.jpg?raw=true "Poland, 2012")

# Опис структури html-файлу та тегів розмітки, які були згенеровані

Тег <!DOCTYPE html> відповідає за тип документа, тобто він вказує браузеру,
як правильно інтерпретувати дану веб-сторінку. 

У парному тегу <head></head> міститься інформація, яка допомогає браузеру з 
обробкою даних. Там міститься теги <style></style>, які визначають стиль файлу та
його дизайн. 

Тег <link> встановлює зв'язок між поточним документом та іншими документами(джерелами)

У тегах <body></body> містить інформацію про те, що відображається у вікні браузера
при відкритті даного файлу.

У тезі <script></script> міститься уся інформація про дії, які відбуваються у файлі.
Тобто це перенесення результатів виконня модулю main.py у JavaScript. 