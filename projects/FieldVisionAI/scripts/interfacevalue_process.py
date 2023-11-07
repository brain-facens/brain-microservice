import streamlit as st
import cv2
import numpy as np
from paddleocr import PaddleOCR, draw_ocr


class OCRInterface:
    def __init__(self):
        self.img_file_buffer = st.camera_input("Tirar foto")

    def ocr_process(self, img, phrases):
        ocr = PaddleOCR(use_angle_cls=True, lang="pt")  # Initialize PaddleOCR
        result = ocr.ocr(img, cls=True)  # Get OCR results for the input image

        # Extract relevant information from OCR results based on specified phrases
        coord = []
        text_lines = []
        text_lines_sec = []
        boxes = []
        boxes_sec = []

        for f in phrases:
            phrase = f.upper().replace(" ", "")

            for idx in result:
                for line in idx:
                    line_plus = line[1][0].upper().replace(" ", "")
                    line_plus = line_plus[: len(phrase)]

                    if line_plus == phrase:
                        coord.append({line[1][0]: line[0]})
                        text_lines.append(line[1][0])
                        boxes.append(line[0])

        # Process the found coordinates
        for comp in coord:
            produto = next(iter(comp.keys()))
            coordenada = comp[produto]

            xy_min = coordenada[0]
            xy_max = coordenada[2]

            print(f"\n\nCOORDENADA DO CAMPO ({produto}) {xy_min, xy_max}\n")
            for l in result:
                for axis in l:
                    _xy_min = axis[0][0]
                    _xy_max = axis[0][2]

                    compara_min = xy_min[1] / _xy_min[1]
                    compara_max = xy_max[1] / _xy_max[1]

                    diferente = False
                    if (
                        xy_min[0] != _xy_min[0]
                        and xy_max[0] != _xy_max[0]
                        and xy_min[0] < _xy_min[0]
                        and xy_max[0] < _xy_max[0]
                    ):
                        diferente = True

                    if (
                        (compara_min >= 0.95 and compara_min <= 1.05)
                        and (compara_max >= 0.95 and compara_max <= 1.05)
                        and (diferente == True) and (axis[0] not in boxes)
                    ):
                        print(
                            f"ACHOU, CAMPO ({axis[1][0]}), Coordenada {_xy_min, _xy_max}"
                        )
                        text_lines_sec.append(axis[1][0])
                        boxes_sec.append(axis[0])

        num_boxes = len(boxes)
        boxes = np.array(boxes).reshape(num_boxes, 4, 2).astype(np.int64)

        num_boxes_sec = len(boxes_sec)
        boxes_sec = np.array(boxes_sec).reshape(num_boxes_sec, 4, 2).astype(np.int64)

        all_boxes = np.concatenate((boxes, boxes_sec), axis=0)
        all_texts = np.concatenate((text_lines, text_lines_sec), axis=0)

        result = result[0]
        image = img
        font_path = "projects/FieldVisionAI/fonts/simfang.ttf"
        im_show = draw_ocr(image, all_boxes, all_texts, font_path=font_path)

        return im_show, all_texts

    def img_capture(self):
        if self.img_file_buffer is not None:
            bytes_data = self.img_file_buffer.getvalue()
            cv2_img = cv2.imdecode(
                np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR
            )
            phrases = ["CNPJ", "VALOR", "TOTAL", "PRODUTO"]
            img_result, txt = self.ocr_process(cv2_img, phrases)

            st.divider()
            st.caption("Imagem Processada:")
            st.image(cv2.cvtColor(img_result, cv2.COLOR_BGR2RGB))
            st.caption("Dados da Nota: ")
            st.table(txt)


if __name__ == "__main__":
    interface = OCRInterface()
    interface.img_capture()