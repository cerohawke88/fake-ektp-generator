from PIL import Image, ImageDraw, ImageFont, ImageFilter
# from datetime import date
import json

# font size list
size=[25,32,17,40,18.5,22]

# Open file data.json
f=open("data.json")
data=json.load(f)

# open template
tmp=Image.open("src/Template3.jpg")

# open second image for pas photo
pas_photo=Image.open(data["pas_photo"])

# Font list
font=["font/Ariall.ttf", "font/Sign.ttf","font/Ocr.ttf"]
# Font for provinsi
fprov=ImageFont.truetype(font[0], size[5])
# Font for NIK
fnik=ImageFont.truetype(font[2],size[1])
# Font for data
fdata=ImageFont.truetype(font[0],size[2])
# Font for signature
fsign=ImageFont.truetype(font[1],size[1])

# Crop + resize pas photo to fit the white placeholder box in Template2.jpg
BOX_XY = (515, 80)
BOX_WH = (175, 220)
ratio = BOX_WH[0] / BOX_WH[1]
pw, ph = pas_photo.size
if pw / ph > ratio:
    nw = int(ph * ratio)
    croped = pas_photo.crop(((pw - nw)//2, 0, (pw - nw)//2 + nw, ph))
else:
    nh = int(pw / ratio)
    croped = pas_photo.crop((0, (ph - nh)//2, pw, (ph - nh)//2 + nh))
csize = croped.resize(BOX_WH, Image.LANCZOS)
tmp.paste(csize, BOX_XY)

# sign
s = data["nama"].split()
sign=s[0]
print("[XXX]GENERATE FAKE E-KTP SUCCESS")
print(data)

# Draw in Image on a transparent text layer so the text can be blurred
BLUR_RADIUS = 1     # gaussian blur radius (softness); 0 = disable
SHARPEN_PERCENT = 20  # unsharp-mask amount (higher = sharper edges)
ALPHA_BOOST = 1.5     # text darkness / color-level boost (1.0 = none)
txt = Image.new("RGBA", tmp.size, (0, 0, 0, 0))
write = ImageDraw.Draw(txt)
write.text((380,25), f"PROVINSI {data['provinsi'].upper()}", fill=(14, 32, 61), font=fprov, anchor="ms")
write.text((380,50), f"KABUPATEN {data['kota'].upper()}", fill=(14, 32, 61), font=fprov, anchor="ms")
write.text((180,72), data["nik"], fill=(14, 32, 61), font=fnik, anchor="lt")
write.text((205,118), data["nama"].upper(), fill=(14, 32, 61), font=fdata, anchor="lt")
write.text((205,140), data["ttl"].upper(), fill=(14, 32, 61), font=fdata, anchor="lt")
write.text((205,160), data["jenis_kelamin"].upper(), fill=(14, 32, 61), font=fdata, anchor="lt")
write.text((488,161), data["golongan_darah"].upper(),fill=(14, 32, 61), font=fdata, anchor="lt")
write.text((205,180), data["alamat"].upper(), fill=(14, 32, 61), font=fdata, anchor="lt")
write.text((205,224), data["rt/rw"].upper(), fill=(14, 32, 61), font=fdata, anchor="lt")
write.text((205,245), data["kel/desa"].upper(), fill=(14, 32, 61), font=fdata, anchor="lt")
write.text((205,267), data["kecamatan"].upper(), fill=(14, 32, 61), font=fdata, anchor="lt")
write.text((205,287), data["agama"].upper(), fill=(14, 32, 61), font=fdata, anchor="lt")
write.text((205,308), data["status"].upper(), fill=(14, 32, 61), font=fdata, anchor="lt")
write.text((205,330), data["pekerjaan"].upper(), fill=(14, 32, 61), font=fdata, anchor="lt")
write.text((205,352), data["kewarganegaraan"].upper(), fill=(14, 32, 61), font=fdata, anchor="lt")
write.text((205,372), data["masa_berlaku"].upper(), fill=(14, 32, 61), font=fdata, anchor="lt")
write.text((543,310), f"{data['kota'].upper()}", fill=(14, 32, 61), font=fdata, anchor="lt")
write.text((560,330), data["terbuat"], fill=(14, 32, 61), font=fdata, anchor="lt")
write.text((550,350), sign, fill=(14, 32, 61), font=fsign, anchor="lt")
# blur, sharpen, and darken the text, then composite onto the template
if BLUR_RADIUS > 0:
    txt = txt.filter(ImageFilter.GaussianBlur(BLUR_RADIUS))
txt = txt.filter(ImageFilter.UnsharpMask(radius=2, percent=SHARPEN_PERCENT, threshold=2))
a = txt.getchannel("A").point(lambda v: min(255, int(v * ALPHA_BOOST)))
txt.putalpha(a)
tmp = Image.alpha_composite(tmp.convert("RGBA"), txt).convert("RGB")
tmp.save("src/result.png", quality=95)
