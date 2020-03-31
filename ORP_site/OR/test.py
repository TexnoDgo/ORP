import os
import tempfile
from pdf2image import convert_from_path

filename = 'media/pdf/3333.PDF'

with tempfile.TemporaryDirectory() as path:
    images_from_path = convert_from_path(filename, output_folder=path, last_page=1, first_page=0)

base_filename = os.path.splitext(os.path.basename(filename))[0] + '.jpg'

save_dir = 'your_saved_dir'

for page in images_from_path:
    page.save(os.path.join(save_dir, base_filename), 'JPEG')