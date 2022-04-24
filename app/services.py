from PIL import Image
import os
from dotenv import load_dotenv 
from pytesseract import pytesseract, Output
import pandas as pd


def parse_image(img: Image):
    """
    Returns formatted strings from DataFrame
    """
    load_dotenv()
    pytesseract.tesseract_cmd = os.getenv("TESSERACT_PATH") 
    data = pytesseract.image_to_data(img, output_type=Output.DICT)
    df = pd.DataFrame(data)

    # Clean up blanks
    df1 = df[(df.conf!="1")&(df.text!=" ")&(df.text!="")]
    # Sort blocks vertically
    sorted_blocks = df1.groupby("block_num").first().sort_values("top").index.to_list()

    text = ""

    for block in sorted_blocks:
        curr = df1[df1["block_num"]==block]
        sel = curr[curr.text.str.len() > 2]
        char_w = (sel.width/sel.text.str.len()).mean()
        prev_par, prev_line, prev_left = -1, 0, 0

        for _, ln in curr.iterrows():
            if prev_par != ln["par_num"]:
                text += "\n"
                prev_par = ln["par_num"]
                prev_line = ln["line_num"]
                prev_left = -1
            elif prev_line != ln["line_num"]:
                text += "\n"
                prev_line = ln["line_num"]
                prev_left = -1

            added = -1 
            if ln["left"]/char_w > prev_left + 0:
                added = int((ln["left"])/char_w) - prev_left
                text += " " * added
            text += ln["text"] + " "
            prev_left += len(ln["text"]) + added + 0
        text += "\n"

    return text