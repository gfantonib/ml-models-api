from pydantic import BaseModel


def eject_object(base_model_obj: BaseModel, filename: str):
    with open(filename, "w") as f:
        f.write(base_model_obj.model_dump_json())
