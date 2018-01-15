import serpy
from ezonseller.settings import URL, MEDIA_URL


class ProfileUserSerializers(serpy.Serializer):
    id = serpy.Field()
    username = serpy.Field()
    first_name = serpy.Field()
    first_name = serpy.Field()
    last_name = serpy.Field()
    email = serpy.Field()
    photo = serpy.MethodField()

    def get_photo(sefl, obj):
        if not obj.photo:
            return(str(obj.photo))
        return(URL+MEDIA_URL+str(obj.photo))
