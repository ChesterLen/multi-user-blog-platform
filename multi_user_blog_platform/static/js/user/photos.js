const main = document.querySelector('main');

const photoContainer = document.createElement('div');
photoContainer.className = 'photo-container';

const photoApiUrl = Urls.pet_image_api();
const photoCommentsApiUrl = Urls.pet_image_comment_api();

const fetchPhotos = fetch(photoApiUrl).then(res => res.json());
const fetchPhotosComments = fetch(photoCommentsApiUrl).then(res => res.json());

Promise.all([fetchPhotos, fetchPhotosComments])
    .then(([photos, comments]) => {
            const photosContainer = document.createElement('div');
            photosContainer.className = 'photos-container';

            const photoComments = document.createElement('div');
            photoComments.className = 'photo-comments';

            photosContainer.appendChild(displpayImages(photos));
            photosContainer.appendChild(photoComments);
            main.appendChild(photosContainer);
    });


function displpayImages(images) {
    const innerPhotos = document.createElement('div');
    innerPhotos.className = 'inner-photos';

    const innerPhotosContainer = document.createElement('div');
    innerPhotosContainer.className = 'inner-photos-container';

    for (const image of images) {
        const img = document.createElement('img');
        img.src = image.image;

        innerPhotosContainer.appendChild(img);
    };

    const mainPhoto = document.createElement('img');
    mainPhoto.className = 'main-photo';
    mainPhoto.src = images[0].image;

    innerPhotos.appendChild(mainPhoto);
    innerPhotos.appendChild(innerPhotosContainer);

    return innerPhotos;
};