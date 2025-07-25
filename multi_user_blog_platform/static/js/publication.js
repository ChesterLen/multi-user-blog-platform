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
    const btn = engagement.children[0].children[1].children[1];
    btn.addEventListener('click', () => {
        console.log('It Works!');
        const pubPK = engagement.children[0].children[1].children[0].children[0].value;

        const commentForm = document.createElement('form');
        commentForm.className = 'comment';
        const commentFormAction = Urls.comment(pk=pubPK);
        commentForm.action = commentFormAction;
        commentForm.method = 'post';

        const input = document.createElement('textarea');
        input.id = 'comment';
        input.name = 'comment';
        input.required = true;

        const divFormBtns = document.createElement('div');
        divFormBtns.className = 'form-btns';

        const commentBtn = document.createElement('button');
        commentBtn.textContent = 'Comment';

        const cancelBtn = document.createElement('div');
        cancelBtn.textContent = 'Cancel';
        cancelBtn.className = 'cancel';
        cancelBtn.addEventListener('click', () => {
            engagementDiv.removeChild(commentForm);
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

        const engagementDiv = engagement.querySelector('.engagement-div');
        if (!engagementDiv.querySelector('.comment')) {
            engagementDiv.appendChild(commentForm);
        };
    });
};

const commentCards = document.querySelectorAll('.comment-card');

for (const card of commentCards) {
    const replyBtn = document.createElement('a');
    replyBtn.className = 'reply-btn';
    const replyBtnI = document.createElement('i');
    replyBtnI.className = 'fa-solid fa-reply';
    replyBtn.appendChild(replyBtnI);
    replyBtn.innerHTML += ' Reply';

    const editBtn = document.createElement('a');
    editBtn.className = 'edit-btn';
    const editBtnI = document.createElement('i');
    editBtnI.className = 'fa-solid fa-edit';
    editBtn.appendChild(editBtnI);
    editBtn.innerHTML += ' Edit';

    const deleteBtn = document.createElement('a');
    deleteBtn.className = 'delete-btn';
    const comPK = document.querySelector('#com-pk').value;
    const deleteCommentUrl = Urls.comment_delete(pk=comPK);
    deleteBtn.href = deleteCommentUrl;

    const deleteBtnI = document.createElement('i');
    deleteBtnI.className = 'fa-solid fa-times';

    deleteBtn.appendChild(deleteBtnI);
    deleteBtn.innerHTML += ' Delete';


    replyBtn.addEventListener('click', () => {
        const replyFormCommentForm = document.createElement('form');
        const comPK = comment.parentNode.querySelector('#com-pk');
        const pubPK = comment.parentNode.querySelector('#pub-pk').value;
        const replyFormCommentFormAction = Urls.reply(pk=pubPK);
        replyFormCommentForm.action = replyFormCommentFormAction;
        replyFormCommentForm.method = 'post';

        const pubPkHidden = document.createElement('input');
        pubPkHidden.type = 'hidden';
        pubPkHidden.value = pubPK;
        pubPkHidden.name = 'pub_pk';
        pubPkHidden.id = 'pub-pk';

        const comPKHidden = document.createElement('input');
        comPKHidden.type = 'hidden';
        comPKHidden.value = comPK.value;
        comPKHidden.name = 'com_pk';
        comPKHidden.id = 'com-pk';

        const replyInput = document.createElement('input');
        replyInput.type = 'text';
        replyInput.name = 'reply';
        replyInput.id = 'reply';
        replyInput.required = true;

        const replyFormCommentFormCsrfToken = document.createElement('input');
        replyFormCommentFormCsrfToken.type = 'hidden';
        replyFormCommentFormCsrfToken.value = CSRF_TOKEN;
        replyFormCommentFormCsrfToken.name = 'csrfmiddlewaretoken';

        const replyFormCommentFormBtn = document.createElement('button');
        const replyFormCommentFormBtnI = document.createElement('i');
        replyFormCommentFormBtnI.className = 'fa-solid fa-reply';
        replyFormCommentFormBtn.appendChild(replyFormCommentFormBtnI);

        replyFormCommentForm.appendChild(pubPkHidden);
        replyFormCommentForm.appendChild(comPKHidden);
        replyFormCommentForm.appendChild(replyInput);
        replyFormCommentForm.appendChild(replyFormCommentFormCsrfToken);
        replyFormCommentForm.appendChild(replyFormCommentFormBtn);

        const referenceNode = card.children[1];
        const formDiv = document.createElement('div');
        formDiv.className = 'form-div';

        const cancelBtn = document.createElement('button');
        const cancelBtnI = document.createElement('i');
        cancelBtnI.className = 'fa-solid fa-times';
        cancelBtn.appendChild(cancelBtnI);

        cancelBtn.addEventListener('click', () => {
            card.removeChild(formDiv);
        });

        formDiv.appendChild(replyFormCommentForm);
        formDiv.appendChild(cancelBtn);
        
        if (!card.querySelector('.form-div')) {
            card.insertBefore(formDiv, referenceNode);
        };
    });

    editBtn.addEventListener('click', () => {
        const commentP = comment.querySelector('p');

        const editCommentForm = document.createElement('form');
        const comPK = document.querySelector('#com-pk').value;
        const editCommentFormAction = Urls.comment_edit(pk=comPK);
        editCommentForm.action = editCommentFormAction
        editCommentForm.method = 'post';

        const editInput = document.createElement('input');
        editInput.value = commentP.textContent;
        editInput.name = 'comment_edit';
        editInput.id = 'comment-edit';

        const editCommentFormCsrfToken = document.createElement('input');
        editCommentFormCsrfToken.type = 'hidden';
        editCommentFormCsrfToken.value = CSRF_TOKEN;
        editCommentFormCsrfToken.name = 'csrfmiddlewaretoken';

        const editFormBtn = document.createElement('button');
        editFormBtn.className = 'form-edit-btn';
        const editFormBtnI = document.createElement('i');
        editFormBtnI.className = 'fa-solid fa-check';
        editFormBtn.appendChild(editFormBtnI);

        const editFormCancelBtn = document.createElement('button');
        const editFormCancelBtnI = document.createElement('i');
        editFormCancelBtnI.className = 'fa-solid fa-times';
        editFormCancelBtn.appendChild(editFormCancelBtnI);
        editFormCancelBtn.addEventListener('click', () => {
            comment.removeChild(editFormDiv);
            comment.prepend(commentP);
        });

        const editFormDiv = document.createElement('div');
        editFormDiv.className = 'edit-form-div';


        editCommentForm.appendChild(editInput);
        editCommentForm.appendChild(editCommentFormCsrfToken);
        editCommentForm.appendChild(editFormBtn);

        editFormDiv.appendChild(editCommentForm);
        editFormDiv.appendChild(editFormCancelBtn);

        comment.removeChild(commentP);
        comment.prepend(editFormDiv);
    });

    const comment = card.querySelector('.comment');

    const divBtns = document.createElement('div');
    divBtns.className = 'comment-btns';

    divBtns.appendChild(replyBtn);
    divBtns.appendChild(editBtn);
    divBtns.appendChild(deleteBtn);

    comment.appendChild(divBtns);
};

const replyCards = document.querySelectorAll('.reply-card');

for (const replyCard of replyCards) {
    const reply = replyCard.querySelector('.reply');

    const replyBtn = document.createElement('button');
    const replyBtnI = document.createElement('i');
    replyBtnI.className = 'fa-solid fa-reply';
    replyBtn.appendChild(replyBtnI);
    replyBtn.innerHTML += ' Reply';

    replyBtn.addEventListener('click', () => {
        const replyForm = document.createElement('form');
        const pubPK = replyCard.querySelector('#pub-pk').value;
        const comPK = replyCard.querySelector('#com-pk').value;
        const replyFormAction = Urls.reply(pk=pubPK);
        replyForm.action = replyFormAction;
        replyForm.method = 'post';

        const hiddenInputPubPK = document.createElement('input');
        hiddenInputPubPK.type = 'hidden';
        hiddenInputPubPK.value = pubPK;
        hiddenInputPubPK.name = 'pub_pk';
        hiddenInputPubPK.id = 'pub-pk';

        const hiddenInput = document.createElement('input');
        hiddenInput.type = 'hidden';
        hiddenInput.value = comPK;
        hiddenInput.name = 'com_pk';
        hiddenInput.id = 'com-pk';

        const hiddenToPet = document.createElement('input');
        hiddenToPet.type = 'hidden';
        const toPet = replyCard.querySelector('#to-pet').value;
        hiddenToPet.value = toPet;
        hiddenToPet.name = 'to_pet';
        hiddenToPet.id = 'to-pet';

        const replyInput = document.createElement('input');
        replyInput.type = 'text';
        replyInput.name = 'reply';
        replyInput.id = 'reply';
        replyInput.required = true;

        const replyCsrfToken = document.createElement('input');
        replyCsrfToken.type = 'hidden';
        replyCsrfToken.value = CSRF_TOKEN;
        replyCsrfToken.name = 'csrfmiddlewaretoken';

        const replyBtn = document.createElement('button');
        const replyBtnI = document.createElement('i');
        replyBtnI.className = 'fa-solid fa-reply';
        replyBtn.appendChild(replyBtnI);

        const cancelBtn = document.createElement('button');
        const cancelBtnI = document.createElement('i');
        cancelBtnI.className = 'fa-solid fa-times';
        cancelBtn.appendChild(cancelBtnI);
        cancelBtn.addEventListener('click', () => {
            replyCard.removeChild(replyDiv);
        });

        const replyDiv = document.createElement('div');
        replyDiv.className = 'reply-reply-div';

        replyForm.appendChild(hiddenInputPubPK);
        replyForm.appendChild(hiddenInput);
        replyForm.appendChild(hiddenToPet);
        replyForm.appendChild(replyInput);
        replyForm.appendChild(replyCsrfToken);
        replyForm.appendChild(replyBtn);

        replyDiv.appendChild(replyForm);
        replyDiv.appendChild(cancelBtn);

        if (!replyCard.querySelector('.reply-reply-div')) {
            replyCard.appendChild(replyDiv);
        };
    });

    const editBtn = document.createElement('button');
    const editBtnI = document.createElement('i');
    editBtnI.className = 'fa-solid fa-edit';
    editBtn.appendChild(editBtnI);
    editBtn.innerHTML += ' Edit';

    editBtn.addEventListener('click', () => {
        let replyP = reply.querySelector('.reply p');
        console.log(replyP.textContent);

        const editForm = document.createElement('form');
        editForm.className = 'reply-edit-form';
        const repPK = replyCard.querySelector('#to-pet').value;
        const editFormAction = Urls.reply_edit(pk=repPK);
        editForm.action = editFormAction;
        editForm.method = 'post';

        const editInput = document.createElement('input');
        editInput.name = 'edit_input';
        editInput.id = 'edit-input';
        editInput.value = replyP.textContent;

        const csrfToken = document.createElement('input');
        csrfToken.type = 'hidden';
        csrfToken.value = CSRF_TOKEN;
        csrfToken.name = 'csrfmiddlewaretoken';

        const editBtn = document.createElement('button');
        const editBtnI = document.createElement('i');
        editBtnI.className = 'fa-solid fa-check';
        editBtn.appendChild(editBtnI);

        const cancelBtn = document.createElement('button');
        const cancelBtnI = document.createElement('i');
        cancelBtnI.className = 'fa-solid fa-times';
        cancelBtn.appendChild(cancelBtnI);
        cancelBtn.addEventListener('click', () => {
            reply.removeChild(editForm);
            reply.removeChild(cancelBtn);
            reply.insertBefore(replyP, referenceNode);
        })

        editForm.appendChild(editInput);
        editForm.appendChild(csrfToken);
        editForm.appendChild(editBtn);

        const referenceNode = reply.children[2];
        reply.insertBefore(editForm, referenceNode);
        reply.insertBefore(cancelBtn, referenceNode);
        reply.removeChild(replyP);
    });

    const deleteBtn = document.createElement('a');
    deleteBtn.className = 'delete-btn';
    const repPK = replyCard.querySelector('#to-pet').value;
    const deleteReplytUrl = Urls.reply_delete(pk=repPK);
    deleteBtn.href = deleteReplytUrl;

    const deleteBtnI = document.createElement('i');
    deleteBtnI.className = 'fa-solid fa-times';

    deleteBtn.appendChild(deleteBtnI);
    deleteBtn.innerHTML += ' Delete';

    const divBtns = document.createElement('div');
    divBtns.className = 'reply-div-btns';

    divBtns.appendChild(replyBtn);
    divBtns.appendChild(editBtn);
    divBtns.appendChild(deleteBtn);

    reply.appendChild(divBtns);
};