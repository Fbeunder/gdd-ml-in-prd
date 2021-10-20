from io import StringIO

import joblib
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse, HTMLResponse
from typing import List

import pandas as pd


app = FastAPI()

@app.get("/api/v1/ping")
def ping():
    return "pong"


@app.post("/api/v1/predict/")
def predict(file: UploadFile = File(...)):
    input_data = pd.read_csv(file.file)
    # TODO: Fill this in.
    predictions = input_data
    response = _convert_df_to_response(predictions)
    return response


def _convert_df_to_response(df: pd.DataFrame) -> StreamingResponse:
    """Convert a DataFrame to CSV response."""
    stream = StringIO()
    df.to_csv(stream, index=False)
    response = StreamingResponse(
        iter([stream.getvalue()]), media_type="text/csv"
    )
    return response


@app.post("/files/")
async def create_data_file(
        experiment: str = Form(...),
        file_type: str = Form(...),
        file_id: str = Form(...),
        data_file: UploadFile = File(...),
        ):
    print(pd.read_csv(data_file.file, sep='\t'))

    return {'filename': data_file.filename,
            'experiment':experiment,
            'file_type': file_type,
            'file_id': file_id}

# async def create_files(files: List[bytes] = File(...)):
#    return {"file_sizes": [len(file) for file in files]}

@app.get("/")
async def main():
    content = """
<body>
<form action="/files" enctype="multipart/form-data" method="post">
<input name="file" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
