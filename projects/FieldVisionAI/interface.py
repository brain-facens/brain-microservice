import streamlit as st
import re
import cv2
import numpy as np
from paddleocr import PaddleOCR, draw_ocr
import matplotlib.pyplot as plt


class OCR_interface:
    def __init__(self):
        self.img_file_buffer    = st.camera_input("Tirar foto")
        self.total_value        = {'subtotal': None,
                                   'total': None}
        self.im_show            = None
        self.txts               = None
        self.boxes              = None
        self.font_path          = "projects/FieldVisionAI/fonts/simfang.ttf"                        # Replace this with the path to your preferred TrueType font file.
        self.cv2_img            = None

    def ocr_process(self):

        ocr = PaddleOCR(use_angle_cls=True)                                                  # need to run only once to download and load the model into memory
        self.result = ocr.ocr(self.cv2_img, cls=True)
        for idx in range(len(self.result)):
            res = self.result[idx]
            for line in res:
                print(line)
        # Draw result
        self.result     = self.result[0]
        self.boxes      = [line[0] for line in self.result]  
        self.txts       = [line[1][0] for line in self.result]
        self.scores     = [line[1][1] for line in self.result]
        self.im_show    = draw_ocr(self.cv2_img, self.boxes, self.txts, self.scores, font_path = self.font_path)
        
    @staticmethod
    def is_float(value):
        try:
            float_value = float(value)
            return float_value, True
        except:
            return -0.0, False
    
    
    def process_values(self):
        aux = 0
        for i in self.txts:
            if i.upper() == 'SUBTOTAL':
                subtotal, sun_result = self.is_float(self.txts[aux + 1])
                
                if sun_result:
                    self.total_value['subtotal'] = subtotal
                
            if i.upper() == 'TOTAL':
                total, total_result = self.is_float(self.txts[aux + 1])
                
                if total_result:
                    self.total_value['total'] = total
                     
            aux += 1
        

    def img_capture(self):
        try:
            if self.img_file_buffer is not None:
                # To read image file buffer with OpenCV:
                self.cv2_img     = cv2.imdecode(np.frombuffer(self.img_file_buffer.getvalue(), np.uint8), cv2.IMREAD_COLOR)
                self.ocr_process()   
                self.process_values()

                st.divider()
                st.caption("Imagem Processada:")
                st.image(cv2.cvtColor(self.im_show, cv2.COLOR_BGR2RGB))
                st.caption("Dados da Nota:")
                st.table(self.txts)
                st.table(self.total_value)
        except OSError:
            st.write("OCR processing failed. No results found!")
            
            
if __name__ == "__main__":
    interface = OCR_interface()
    interface.img_capture()