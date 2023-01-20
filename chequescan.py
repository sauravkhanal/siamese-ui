def extract_data_from_cheque(cheque_path ):
    #enter folder_path as : "A:/data"
    #enter cheque_path as : "A:/chequesample.png"
    import cv2
    import os

    folder_path = os.path.dirname(cheque_path)
    cheque = cv2.imread(cheque_path)
    ch_size = (1494,700)

    cheque = cv2.resize(cheque,ch_size)

    if os.path.isdir(folder_path) is False:
        os.makedirs(folder_path)

    sign1 = cheque[326:520, 705:1068]
    cv2.imwrite(f'{folder_path}/sign1.png',sign1)

    sign2 = cheque[326:520, 705+397:1068+397]
    cv2.imwrite(f'{folder_path}/sign2.png',sign2)

    amount = cheque[225:297, 1075:1468]
    cv2.imwrite(f'{folder_path}/amount.png',amount)

    name = cheque[145: 195, 310:310+1065]
    cv2.imwrite(f'{folder_path}/name.png',name)

    account_details = cheque[340:340+200, 95:95+370  ]
    cv2.imwrite(f'{folder_path}/account_details.png',account_details)

    amount_text = cheque[200:246, 156:156+905]
    cv2.imwrite(f'{folder_path}/amount_text.png',amount_text)

    #for date
    x,y = 45,71
    xo,yo = 1074,51
    margin = 7
    margin2 = 8
    margin3 = 15
    margin4 = 20
    d0 = cheque[yo:yo+y , xo:xo+x]
    d1 = cheque[yo:yo+y , xo+x*(2-1)+margin :xo+x*2 + margin]
    m0 = cheque[yo:yo+y , xo+x*(3-1)+margin2 :xo+x*3 + margin2]
    m1 = cheque[yo:yo+y , xo+x*(4-1)+margin2 :xo+x*4 + margin2]
    y0 = cheque[yo:yo+y , xo+x*(5-1)+margin3 :xo+x*5 + margin3]
    y1 = cheque[yo:yo+y , xo+x*(6-1)+margin3 :xo+x*6 + margin3]
    y2 = cheque[yo:yo+y , xo+x*(7-1)+margin4 :xo+x*7 + margin4]
    y3 = cheque[yo:yo+y , xo+x*(8-1)+margin4 :xo+x*8 + margin4]

    cv2.imwrite(f'{folder_path}/d0.png',d0)
    cv2.imwrite(f'{folder_path}/d1.png',d1)
    cv2.imwrite(f'{folder_path}/m0.png',m0)
    cv2.imwrite(f'{folder_path}/m1.png',m1)
    cv2.imwrite(f"{folder_path}/y0.png",y0)
    cv2.imwrite(f"{folder_path}/y1.png",y1)
    cv2.imwrite(f"{folder_path}/y2.png",y2)
    cv2.imwrite(f"{folder_path}/y3.png",y3)

    print('complete')