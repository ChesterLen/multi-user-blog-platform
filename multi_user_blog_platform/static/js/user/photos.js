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

            const innerPhotos = displpayImages(photos);

            const mainPhoto = document.createElement('img');
            mainPhoto.className = 'main-photo';
            mainPhoto.src = photos[0].image;

            const images = innerPhotos.querySelectorAll('.inner-photos-container img');
            for (const image of images) {
                image.addEventListener('click', () => {
                    mainPhoto.src = image.src;
                });
            };

            const mainPhotoDiv = document.createElement('div');
            mainPhotoDiv.className = 'main-photo-div';

            mainPhotoDiv.addEventListener('click', () => {
                mainPhotoDiv.style.backgroundColor = 'rgba(0, 0, 0, 70%)';
                
                mainPhotoDiv.style.position = 'fixed';
                mainPhotoDiv.style.width = '500px';
                mainPhotoDiv.style.height = '500px';
                mainPhotoDiv.style.top = '50%';
                mainPhotoDiv.style.left = '50%';
                mainPhotoDiv.style.transform = 'translate(-50%, -50%)';
            });

            mainPhotoDiv.appendChild(mainPhoto);
            innerPhotos.appendChild(mainPhotoDiv);

            photosContainer.appendChild(innerPhotos);
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

    innerPhotos.appendChild(innerPhotosContainer);

    return innerPhotos;
};