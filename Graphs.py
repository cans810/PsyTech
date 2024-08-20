import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import base64
from PIL import Image
import os


class GraphsManager:
    def __init__(self, db, answers_ref):
        self.db = db
        self.answers_ref = answers_ref

    def generate_graph_and_save(self, test_id ,Bil, Lie, F, K, Hs, D, Hy, Pd, Mf, Pa, Pt, Sc, Ma, Si):
        x = np.arange(1, 15, 1)
        y = [Bil, Lie, F, K, Hs, D, Hy, Pd, Mf, Pa, Pt, Sc, Ma, Si]

        plt.figure(figsize=(10, 8))
        plt.plot(x, y, 'r-', linewidth=0.5)
        plt.plot(x, y, 'rD', markersize=5)
        x_labels = ['?', 'L', 'F', 'K', 'Hs+5K', 'D', 'Hy', 'Pd+4K', 'Mf', 'Pa', 'Pt+1K', 'Sc+1K', 'Ma+2K', 'Si']
        plt.xticks(x, x_labels, ha='center', va='top')
        y_ticks = [0, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120]
        plt.yticks(y_ticks)
        plt.ylim(15, 120)
        plt.ylabel('Y Ekseni')
        plt.title('Nokta ve Çizgi ile Veri Görselleştirme')
        for i in range(len(x)):
            plt.text(x[i], 7, str(y[i]), ha='center')
        plt.grid(True)


        # Save the plot as a PNG file
        graph_tempfile_png = 'temp_graph.png'
        plt.savefig(graph_tempfile_png)
        plt.close()

        # Convert the PNG to webp using Pillow
        graph_tempfile_webp = 'temp_graph.webp'
        Image.open(graph_tempfile_png).save(graph_tempfile_webp, 'webp')

        # Read the webp file and encode it to base64
        with open(graph_tempfile_webp, 'rb') as f:
            image_data = f.read()
        encoded_image = base64.b64encode(image_data).decode('utf-8')

        # Remove the temporary files
        os.remove(graph_tempfile_png)
        os.remove(graph_tempfile_webp)

        try:
            # iterate through answer documents in answers_ref
            for answer_doc in self.answers_ref.stream():
                answer_data = answer_doc.to_dict()

                # check if the test_id matches the patient's test_id
                if answer_data.get('test_id') == test_id:
                    # update answer_data with the encoded image
                    answer_data['generated_graph'] = encoded_image

                    # update the answer document in answers_ref
                    answer_doc.reference.update(answer_data)
                    return
        except Exception as e:
            print(f"Error occurred while retrieving generated graph: {e}")



"""
# Veri noktalarını tanımla
x = np.arange(1, 15, 1)  # 1'den 14'e kadar olan tam sayılar
# Eksik veri noktalarını NaN ile doldur
y = [39, 41, 25, 7, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

plt.figure(figsize=(10,8))
# Noktaları birleştiren çizgiyi çiz
plt.plot(x, y, 'r-', linewidth=0.5)  # 'r-' ince kırmızı renkte bir çizgi çizer

# Nokta olarak verileri çiz (eşkenar dörtgen şeklinde)
plt.plot(x, y, 'rD', markersize=5)  # 'rD' kırmızı renkte ve eşkenar dörtgen şeklinde çizim yapar

# X eksenindeki veri isimlerini özelleştir
x_labels = ['?', 'L', 'F', 'K', 'Hs+5K', 'D', 'Hy', 'Pd+4K', 'Mf', 'Pa', 'Pt+1K', 'Sc+1K', 'Ma+2K', 'Si']
plt.xticks(x, x_labels, ha='center', va='top')  # X eksenindeki metinlerin hizalamasını belirle


# Y eksenindeki özel değerleri belirle
y_ticks = [0,15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120]
plt.yticks(y_ticks)


plt.ylim(15, 120)

# Eksen etiketlerini ve başlığı ekle
plt.ylabel('Y Ekseni')
plt.title('Nokta ve Çizgi ile Veri Görselleştirme')

# Y veri noktalarını X ekseninin altına yazdır
for i in range(len(x)):
    plt.text(x[i], 7, str(y[i]), ha='center')

# Arkaplan çizgilerini göster
plt.grid(True)

# Çizimi göster
plt.show()
"""