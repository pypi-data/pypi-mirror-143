# Example Postify Usage


```python
# Imports
import postify
```

## Demo of usage on map.png


```python
# Load in the image

IMG = postify.open_file('./map.png')
postify.show(IMG)
```


    
![png](example/output_3_0.png)
    



```python
# Add padding
IMG_PAD = postify.pad_with_color_percent( IMG, pad=0.29, color=(1,1,1))
postify.show(IMG_PAD)
```


    
![png](example/output_4_0.png)
    



```python
# Add circle
postify.with_circle_precent(IMG_PAD, outside=(1,1,1), radius=0.30)
postify.with_circle_precent(IMG_PAD, outside=(0.7,0.7,0.7), radius=0.303)
postify.with_circle_precent(IMG_PAD, outside=(1,1,1), radius=0.306)
postify.show(IMG_PAD)
```


    
![png](example/output_5_0.png)
    



```python
# Crop
IMG_CROP = postify.crop_width_ratio(IMG_PAD, new_ratio = 0.8)
IMG_CROP = postify.pad_bottom_with_color_percent(IMG_CROP, color=(1,1,1), pad=0.2)
postify.show(IMG_CROP)
```


    
![png](example/output_6_0.png)
    



```python
# With borders
postify.with_borders_percent( IMG_CROP, width = 0.022, color=(0.7,0.7,0.7))
postify.with_borders_percent( IMG_CROP, width = 0.02, color=(1,1,1))
postify.show(IMG_CROP)
```


    
![png](example/output_7_0.png)
    



```python
# Add text
postify.with_text(IMG_CROP, font="Jura-Medium.ttf", text="New York, NY", x=0.5, y=0.8)
postify.with_line(IMG_CROP, y=0.85, color=(0.7,0.7,0.7), size=0.2)
postify.with_text(IMG_CROP, font="Jura-Medium.ttf", text="Latitude, Longitude", x=0.5, y=0.9, size=0.6)
postify.show(IMG_CROP)
```


    
![png](example/output_8_0.png)
    



```python
# Save
postify.save(IMG_CROP, './poster.png')
```
