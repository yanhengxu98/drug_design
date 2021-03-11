
def uchar_checksum(check_data, byteorder='little'):
    '''
    char_checksum 按字节计算校验和。每个字节被翻译为无符号整数
    @param check_data: 字节串
    @param byteorder: 大/小端
    '''
    length = len(check_data)
    checksum = 0
    for i in range(0, length):
        checksum += int.from_bytes(check_data[i:i + 1], byteorder, signed=False)
        checksum &= 0xFF  # 强制截断

    return checksum


print(uchar_checksum(br"\xA8\x50"))
