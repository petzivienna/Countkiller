from PIL import Image
#how to install pil:
#https://pillow.readthedocs.io/en/stable/installation.html
## gimp effect: fx-foundry -> photo -> effects -> old photo

im_original = Image.open("map1.png")
im_fog = Image.open("map1_fog.png")

w,h  = im_original.size

village = (777,900,1555,1500)
ghost = (1400,600,2100,950)

im_new = Image.new("RGBA",(w,h))


#crop: (left, upper) and (right, lower) pixel values.
im_village = im_original.crop(village)
im_ghost = im_original.crop(ghost)
im_new.paste(im_fog) # everything is foggy
im_new.paste(im_village, (village[0], village[1])) # explore village
im_new.paste(im_ghost, (ghost[0], ghost[1]))       # explore ghost
im_new.show()

