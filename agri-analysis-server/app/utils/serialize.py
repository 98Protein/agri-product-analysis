def serialize(model):
    if isinstance(model, list):
        return [serialize(x) for x in model]

    return model.to_dict()
