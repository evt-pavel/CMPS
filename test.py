from app import session
from app.models import *



# part = session.query(Part).filter(Part.model_id == 1)

# type = session.query(Model).filter_by(id=1)

# for p in part:
#     print(p.model_id, p.model)


# for t in type:
#     print(t.type.type_name)


# part = session.query(Model).join(Part).filter(Model.brand_id == 1).first()

# part = session.query(Model).join(Brand).join(Part).filter(Model.brand_id == 2)


# for p in part:
#     print(p.type.type_name)
#     print(p.brand.brand_name)
#     print(p.model_name)



image = session.query(Element).get(1)

print(image.image_id)

