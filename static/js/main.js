"use strict"


let buttons = document.querySelectorAll('.article-button')
let articles = document.querySelectorAll('.art-body')
for (let i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener('click', function () {
        let elem = articles[i]
        if (elem.getAttribute('hidden') === null) {
            elem.setAttribute('hidden', true);
            buttons[i].innerText = 'Развернуть';
        } else {
            elem.removeAttribute('hidden');
            buttons[i].innerText = 'Свернуть';
        }
    })
}
