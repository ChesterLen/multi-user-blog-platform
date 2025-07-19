const profileNavImg = document.getElementById('profile-nav-img');
const noProfileNavImg = document.getElementById('no-profile-img');

console.log(noProfileNavImg);

const petPk = document.getElementById('pet_pk');
const profileDetailsUrl = Urls.profile_details(pk=petPk.value);

if (profileNavImg) {
    profileNavImg.addEventListener('click', () => {
        window.location.href = profileDetailsUrl;
    });
} else if (noProfileNavImg) {
    noProfileNavImg.addEventListener('click', () => {
        window.location.href = profileDetailsUrl;
    });
}