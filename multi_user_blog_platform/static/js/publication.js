const formPopUp = document.getElementById('form-pop-up');
formPopUp.style.cursor = 'pointer';

const main = document.querySelector('main');

function toggleForm() {
    formPopUp.style.marginTop = '-1em';
    const existingForm = document.getElementById('form-container');

    if (existingForm) {
        main.style.position = '';
        main.style.zIndex = '';

        formPopUp.style.position = '';
        formPopUp.style.zIndex = 1;
        formPopUp.style.width = '';
        formPopUp.style.height = '';
        formPopUp.style.backgroundColor = '';
        formPopUp.innerHTML = '';
        formPopUp.textContent = "What's on your mind?";
    } else {
        formPopUp.innerHTML = '';
        main.style.position = 'relative';
        main.style.zIndex = 0;

        formPopUp.style.position = 'absolute';
        formPopUp.style.zIndex = 1;
        formPopUp.style.width = '100%';
        formPopUp.style.height = '100%';
        formPopUp.style.backgroundColor = 'rgba(0, 0, 0, 0.4)';

        formPopUp.style.display = 'flex';
        formPopUp.style.alignItems = 'center';
        formPopUp.style.justifyContent = 'center';

        const formDiv = document.createElement('div');
        formDiv.id = 'form-container';
        formDiv.style.width = '500px';
        formDiv.style.height = '500px';
        formDiv.style.backgroundColor = '#fff';
        formDiv.style.padding = '20px';
        formDiv.style.boxShadow = '0 0 10px rgba(0,0,0,0.2)';
        formDiv.style.position = 'relative';

        formDiv.addEventListener('click', (e) => {
            e.stopPropagation();
        });

        const form = document.createElement('form');
        form.action = popUpFormAction;
        form.method = 'post';
        
        const imgLabel = document.createElement('label');
        imgLabel.textContent = 'Image';
        imgLabel.htmlFor = 'image';
        const img = document.createElement('input');
        img.type = 'file';
        img.name = 'image';
        img.id = 'image';

        const title = document.createElement('input');
        const titleLabel = document.createElement('label');
        titleLabel.htmlFor = 'title';
        titleLabel.textContent = 'Title:';
        title.type = 'text';
        title.name = 'title';
        title.id = 'title';

        const text = document.createElement('input');
        const textLabel = document.createElement('label');
        textLabel.htmlFor = 'text';
        textLabel.textContent = 'Text';
        text.type = 'text';
        text.name = 'text';
        text.id = 'text';

        const csrfToken = document.createElement('input');
        csrfToken.type = 'hidden';
        csrfToken.name = 'csrfmiddlewaretoken';
        csrfToken.value = CSRF_TOKEN;

        const formBtn = document.createElement('button');
        formBtn.textContent = 'test';

        form.appendChild(imgLabel);
        form.appendChild(img);
        form.appendChild(titleLabel);
        form.appendChild(title);
        form.appendChild(textLabel);
        form.appendChild(text);
        form.appendChild(csrfToken);
        form.appendChild(formBtn);

        const closeBtn = document.createElement('button');
        closeBtn.textContent = '×';
        closeBtn.style.position = 'absolute';
        closeBtn.style.top = '10px';
        closeBtn.style.right = '10px';
        closeBtn.style.border = 'none';
        closeBtn.style.background = 'transparent';
        closeBtn.style.fontSize = '24px';
        closeBtn.style.cursor = 'pointer';
        closeBtn.addEventListener('click', toggleForm);

        formDiv.appendChild(form);

        formDiv.appendChild(closeBtn);
        formPopUp.appendChild(formDiv);
    };
};

formPopUp.addEventListener('click', toggleForm);