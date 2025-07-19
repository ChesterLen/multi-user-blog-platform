const profileNavImg = document.getElementById('profile-nav-img');
const petPk = document.getElementById('pet_pk');
const profileDetailsUrl = Urls.profile_details(pk=petPk.value);

profileNavImg.addEventListener('click', () => {
    window.location.href = profileDetailsUrl;
});