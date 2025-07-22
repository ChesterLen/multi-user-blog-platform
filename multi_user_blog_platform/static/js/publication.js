const formPopUp = document.getElementsByClassName('form-pop-up')[0];

const engagements = document.getElementsByClassName('engagement');
const commentPopUpBtns = document.getElementsByClassName('comment-btn');

if (formPopUp) {
    formPopUp.addEventListener('click', () => {
        const popUp = document.createElement('div');
        popUp.className = 'pop-up';
        popUp.style.cursor = 'auto';
        popUp.addEventListener('click', (e) => {
            e.stopPropagation();
        });

        popUp.style.width = '100vw';
        popUp.style.height = '100vh';
        popUp.style.backgroundColor = 'rgba(0, 0, 0, 70%)';
        popUp.style.top = '50%';
        popUp.style.left = '50%';
        popUp.style.transform = 'translate(-50%, -50%)';
        popUp.style.position = 'fixed';

        const popUpInner = document.createElement('div');
        popUpInner.className = 'pop-up-inner';
        popUpInner.style.width = '400px';
        popUpInner.style.height = 'auto';
        popUpInner.style.backgroundColor = '#F68537';
        popUpInner.style.position = 'fixed';
        popUpInner.style.top = '50%';
        popUpInner.style.left = '50%';
        popUpInner.style.transform = 'translate(-50%, -50%)';
        popUpInner.style.display = 'flex';
        popUpInner.style.flexDirection = 'column';
        popUpInner.style.alignItems = 'center';
        popUpInner.style.borderRadius = '5px';

        const form = document.createElement('form');
        form.method = 'post';
        form.style.padding = '1em';
        form.style.display = 'flex';
        form.style.flexDirection = 'column';
        form.style.alignItems = 'center';

        const labelTitle = document.createElement('label');
        labelTitle.htmlFor = 'title';
        labelTitle.textContent = 'Title';
        const title = document.createElement('input');
        title.type = 'text';
        title.name = 'title';
        title.id = 'title';
        title.required = 'true';

        const labelText = document.createElement('label');
        labelText.htmlFor = 'text';
        labelText.textContent = 'Text';
        const text = document.createElement('textarea');
        text.name = 'text';
        text.id = 'text';
        text.required = 'true';

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
        closeBtn.style.top = '21.5%';
        closeBtn.style.right = '35.4%';
        closeBtn.style.transform = 'translate(-50%, -50%)';
        closeBtn.style.padding = '0 0.3em';
        closeBtn.style.borderRadius = '5px';
        closeBtn.style.cursor = 'pointer';
        closeBtn.addEventListener('click', () => {
            formPopUp.removeChild(popUp);
        });
        
        
        popUpInner.appendChild(form);
        popUp.appendChild(popUpInner);
        popUp.appendChild(closeBtn);
        formPopUp.appendChild(popUp);
    });
};

for (const engagement of engagements) {
    const btn = engagement.children[1].children[1];
    btn.addEventListener('click', () => {
        const pubPK = engagement.children[1].children[0].children[0].value;

        const commentForm = document.createElement('form');
        commentForm.className = 'comment';
        const commentFormAction = Urls.comment(pk=pubPK);
        commentForm.action = commentFormAction;
        commentForm.method = 'post';

        const input = document.createElement('textarea');
        input.id = 'comment';
        input.name = 'comment';

        const divFormBtns = document.createElement('div');
        divFormBtns.className = 'form-btns';

        const commentBtn = document.createElement('button');
        commentBtn.textContent = 'Comment';

        const cancelBtn = document.createElement('div');
        cancelBtn.textContent = 'Cancel';
        cancelBtn.className = 'cancel';
        cancelBtn.addEventListener('click', () => {
            engagement.removeChild(commentForm);
        });

        const csrfToken = document.createElement('input');
        csrfToken.type = 'hidden';
        csrfToken.name = 'csrfmiddlewaretoken';
        csrfToken.value = CSRF_TOKEN;

        divFormBtns.appendChild(commentBtn);
        divFormBtns.appendChild(cancelBtn);

        commentForm.appendChild(input);
        commentForm.appendChild(csrfToken);
        commentForm.appendChild(divFormBtns);

        engagement.appendChild(commentForm);
    });
};

const replyBtns = document.querySelectorAll('.reply');
const comments = document.querySelectorAll('.comment-p');

if (comments && replyBtns) {
    for (const comment of comments) {
        const replyDiv = document.createElement('div');
        replyDiv.className = 'reply-div';

        const replyBtn = comment.querySelector('.reply');

        replyDiv.appendChild(comment.removeChild(replyBtn));
        comment.appendChild(replyDiv)

        replyBtn.addEventListener('click', () => {
            replyDiv.removeChild(replyBtn);
            const replyForm = document.createElement('form');
            replyForm.className = 'reply-form';

            const reply = document.createElement('input');
            reply.type = 'text';
            reply.name = 'reply';
            reply.id = 'reply';
            
            const postBtn = document.createElement('button');
            postBtn.textContent = 'Post';

            const cancelPostBtn = document.createElement('button');
            cancelPostBtn.textContent = 'Cancel';
            cancelPostBtn.addEventListener('click', () => {
                replyDiv.removeChild(replyForm);
                replyDiv.removeChild(cancelPostBtn);
                replyDiv.appendChild(replyBtn);
            });

            const csrfToken = document.createElement('input');
            csrfToken.type = 'hidden';
            csrfToken.name = 'csrfmiddlewaretoken';
            csrfToken.value = CSRF_TOKEN;

            replyForm.appendChild(reply);
            replyForm.appendChild(csrfToken);
            replyForm.appendChild(postBtn);

            replyDiv.appendChild(replyForm);
            replyDiv.appendChild(cancelPostBtn);
            // comment.appendChild(replyDiv)
        });
    };
};