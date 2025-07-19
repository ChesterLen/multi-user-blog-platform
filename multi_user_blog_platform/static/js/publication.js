const formPopUp = document.getElementById('form-pop-up');
const profileContainer = document.getElementsByClassName('profile-container')[0];
const main = document.querySelector('main');

formPopUp.addEventListener('click', () => {
    if (formPopUp.style.position === 'absolute') {
        main.style.position = '';
        main.style.zIndex = '';

        formPopUp.style.position = '';
        formPopUp.style.zIndex = 1;
        formPopUp.style.width = '';
        formPopUp.style.height = '';
        formPopUp.style.backgroundColor = '';
        formPopUp.style.opacity = '';

        formPopUp.innerHTML = '';
        formPopUp.textContent = 'dsa';
    } else {
        main.style.position = 'relative';
        main.style.zIndex = 0;
        
        formPopUp.style.position = 'absolute';
        formPopUp.style.zIndex = 1;
        formPopUp.style.width = '100%';
        formPopUp.style.height = '100%';
        formPopUp.style.backgroundColor = '#000';
        formPopUp.style.backgroundColor = 'rgba(0, 0, 0, 0.4)';

        const formDiv = document.createElement('div');
        formDiv.style.width = '500px';
        formDiv.style.height = '500px';
        formDiv.style.backgroundColor = '#fff';
        formDiv.style.margin = '0 auto';

        const formBtn = document.createElement('button');
        formBtn.textContent = 'test';
        formBtn.addEventListener('click', ()=> {
            formDiv.style.backgroundColor = 'red';
        });

        formDiv.appendChild(formBtn);
        formPopUp.appendChild(formDiv);
    };
});