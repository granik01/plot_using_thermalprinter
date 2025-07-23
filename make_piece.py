from PIL import Image, ImageDraw, ImageFont
import numpy as np

def create_rotated_line_image(point1_temp, point2_temp, temp_range1,temp_range2, image_width=200, 
                            line_width=1, marker_size=3, height=384, font_size=16):
    """
    Создает и поворачивает изображение с графиком температуры:
    - point1_temp: (x, temperature) - первая точка
    - point2_temp: (x, temperature) - вторая точка
    - temp_range: (min_temp, max_temp) - диапазон температур
    Возвращает изображение, повернутое на 90° по часовой стрелке
    """
    # Преобразование температуры в координаты Y (с инверсией)
    back = 255 
    foreg =0  

    def temp_to_y(temp,temp_range):
        return height - int((temp - temp_range[0]) / (temp_range[1] - temp_range[0]) * height)
    
    # Координаты точек
    point1 = (point1_temp[0], temp_to_y(point1_temp[1],temp_range1))
    #point1 = point1_temp
    point2 = (point2_temp[0], temp_to_y(point2_temp[1],temp_range2))
    
    # Создаем изображение
    image = Image.new('L', (image_width, height), back)
    draw = ImageDraw.Draw(image)
    
    # Загружаем шрифт
    try:
        font = ImageFont.truetype("fonts/code2000.ttf", font_size)
    except Exception as e:
        print(e) 
        font = ImageFont.load_default()
    
    # Рисуем линию и маркеры
    draw.line([point1, point2], fill=foreg, width=line_width)
    
    def draw_marker(draw, center, diameter):
        radius = diameter / 2
        left_top = (center[0] - radius, center[1] - radius)
        right_bottom = (center[0] + radius, center[1] + radius)
        draw.ellipse([left_top, right_bottom], fill=foreg)
    
    draw_marker(draw, point1, marker_size)
    draw_marker(draw, point2, marker_size)
    
    # Подпись температуры у второй точки
    temp_text = f"{point2_temp[1]:.1f}°"
    #bbox = draw.textbbox((0, 0), temp_text, font=font)
    #text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
   
    if hasattr(font, 'getsize'):
        text_width, text_height = font.getsize(temp_text)
    else:
        # Самый старый способ (для очень старых версий)
        text_width = len(temp_text) * font_size
        text_height = font_size
 

    text_x = point2[0] - text_width
    text_y = point2[1] + text_height // 2
    draw.text((text_x, text_y), temp_text, fill=foreg, font=font)
    
    # Обрезаем и поворачиваем изображение
    right_bound = point2[0]# + marker_size//2
    left_bound = point1[0]# - marker_size//2
    cropped = image.crop((left_bound, 0, min(right_bound, image_width), height))
    
    # Поворот на 90° по часовой стрелке
    rotated = cropped.rotate(-90, expand=True)
    
    return rotated.convert('1')

