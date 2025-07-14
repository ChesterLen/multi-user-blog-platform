class AppUserProfileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        self._user_profile_middleware(request, *args, **kwargs)
        return self.get_response(request, *args, **kwargs)

    def _user_profile_middleware(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                request.pet = request.user.profile
            except request.et.DoesNotExist:
                request.pet = None
        else:
            request.pet = None