import qrcode

url =   "https://andresgonzalezdev.me/"

img = qrcode.make(url)

img.save("qr_page.png")

print("QR code generated successfully!")