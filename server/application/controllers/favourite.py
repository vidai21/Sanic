# from application.api import favourite
# from application.models.models import Favourite
# from application.server import json

# @favourite.get("/")
# async def get_favourite(request):
#     favourite = await Favourite.find(as_raw=True)
#     return json({
#         "status": "success",
#         "data": favourite.objects
#     })

# @favourite.post("/<post_id>")
# async def add_favourite(request, post_id):
#     favourite = await Favourite.find_one({"post_id": post_id}, as_raw=True)
#     if favourite is None:
#         new_favourite = await Favourite.insert_one({"_id": str(ObjectId()), "post_id": post_id})
#         created_favourite = await Favourite.find_one({"_id": new_favourite.inserted_id}, as_raw=True)
#         return json({
#             "status": "success",
#             "data": created_favourite
#         })
#     return json({
#             "status": "success",
#             "data": favourite
#         })

# @favourite.delete("/<post_id>")
# async def delete_favourite(request, post_id):
#     await Favourite.delete_one({"post_id": post_id})
#     return json({
#         "status": "success",
#         "message": "this post has been deleted from your favourite!"
#     })