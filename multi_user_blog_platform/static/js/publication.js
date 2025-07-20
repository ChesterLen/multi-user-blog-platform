const publicationForm = document.getElementsByClassName('form-pop-up')[0];

publicationForm.addEventListener('click', () => {
    const popUp = document.createElement('div');
    popUp.style.cursor = 'auto';
    popUp.addEventListener('click', (e) => {
        e.stopPropagation();
    });

    popUp.className = 'pop-up';
    popUp.style.width = '100vw';
    popUp.style.height = '100vh';
    popUp.style.backgroundColor = 'rgba(0, 0, 0, 70%)';
    popUp.style.top = '50%';
    popUp.style.left = '50%';
    popUp.style.transform = 'translate(-50%, -50%)';
    popUp.style.position = 'fixed';

    const popUpInner = document.createElement('div');
    popUpInner.style.width = '300px';
    popUpInner.style.height = '300px';
    popUpInner.style.backgroundColor = 'red';
    popUpInner.style.position = 'fixed';
    popUpInner.style.top = '50%';
    popUpInner.style.left = '50%';
    popUpInner.style.transform = 'translate(-50%, -50%)';

    const form = document.createElement('form');
    form.method = 'post';

    const labelTitle = document.createElement('label');
    labelTitle.htmlFor = 'title';
    labelTitle.textContent = 'Title';
    const title = document.createElement('input');
    title.type = 'text';
    title.name = 'title';
    title.id = 'title';

    const labelText = document.createElement('label');
    labelText.htmlFor = 'text';
    labelText.textContent = 'Text';
    const text = document.createElement('textarea');
    text.name = 'text';
    text.id = 'text';

    const csrfToken = document.createElement('input');
    csrfToken.type = 'hidden';
    csrfToken.name = 'csrfmiddlewaretoken';
    csrfToken.value = CSRF_TOKEN;

    const formBtn = document.createElement('button');
    formBtn.type = 'submit';
    formBtn.textContent = 'Publish';
    formBtn.style.cursor = 'pointer';

    form.appendChild(labelTitle);
    form.appendChild(title);
    form.appendChild(labelText);
    form.appendChild(text);
    form.appendChild(csrfToken);
    form.appendChild(formBtn);

    const closeBtn = document.createElement('button');
    closeBtn.textContent = 'X';
    closeBtn.style.position = 'fixed';
    closeBtn.style.top = '29.2%';
    closeBtn.style.right = '38.6%';
    closeBtn.style.transform = 'translate(-50%, -50%)';
    closeBtn.style.padding = '0 0.3em';
    closeBtn.style.cursor = 'pointer';
    closeBtn.addEventListener('click', () => {
        publicationForm.removeChild(popUp);
    });
    
    
    popUpInner.appendChild(form);
    popUp.appendChild(popUpInner);
    popUp.appendChild(closeBtn);
    publicationForm.appendChild(popUp);
});

// const form = document.createElement('form');
// form.method = 'post';

// const labelTitle = document.createElement('label');
// labelTitle.htmlFor = 'title';
// labelTitle.textContent = 'Title';
// const title = document.createElement('input');
// title.type = 'text';
// title.name = 'title';
// title.id = 'title';

// const labelText = document.createElement('label');
// labelText.htmlFor = 'text';
// labelText.textContent = 'Text';
// const text = document.createElement('textarea');
// text.name = 'text';
// text.id = 'text';

// const csrfToken = document.createElement('input');
// csrfToken.type = 'hidden';
// csrfToken.name = 'csrfmiddlewaretoken';
// csrfToken.value = CSRF_TOKEN;

// const formBtn = document.createElement('button');
// formBtn.type = 'submit';
// formBtn.textContent = 'Publish';

// form.appendChild(labelTitle);
// form.appendChild(title);
// form.appendChild(labelText);
// form.appendChild(text);
// form.appendChild(csrfToken);
// form.appendChild(formBtn);

// publicationForm.appendChild(form);