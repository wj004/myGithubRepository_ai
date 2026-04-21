import sys

def crc16_ccitt(data: bytes, poly=0x1021, init_crc=0xFFFF) -> int:
    crc = init_crc
    for byte in data:
        crc ^= (byte << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ poly
            else:
                crc <<= 1
            crc &= 0xFFFF  # 保持为16位
    return crc

def append_crc16_to_file(filename):
    with open(filename, "rb") as f:
        data = f.read()

    crc = crc16_ccitt(data)
    print(f"CRC-16 (CCITT): 0x{{crc:04X}}")

    # 以小端序方式写入（低字节在前）
    crc_bytes = crc.to_bytes(2, byteorder="little")

    with open(filename, "ab") as f:
        f.write(crc_bytes)
    print(f"已将CRC添加到文件 {{filename}} 尾部。")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python crc16_append.py <filename>")
        sys.exit(1)
    append_crc16_to_file(sys.argv[1])