from fastapi import FastAPI, Form, Response
from exceptions import UserError
from handlers import convert 

app = FastAPI()


@app.post("/slack/actions", status_code=200)
async def img_to_text(response: Response, text: str = Form(0), channel_id: str = Form(...)): 
    output = convert(channel_id, text)
    if isinstance(output, UserError):
        response.status_code = output.status_code
        return {"error": output.error_msg}

    return {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"```{output}```"
                }
            }
        ]
    }
