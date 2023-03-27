import qrcode

def make_qr_code(mesage,save_path=False):
    img = qrcode.make(mesage)
    if save_path!=False:
        img.save(save_path)
    return img
