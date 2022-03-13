from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/upload-file/")
def create_upload_file(db, uploaded_file: UploadFile = File(...)):
    # TODO: get current user
    # Store file path in db

    file_location = f"static/{uploaded_file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())
    return {"info": f"file '{uploaded_file.filename}' saved at '{file_location}'"}