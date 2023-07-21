from PySide6.QtCore import QByteArray

# qba = QByteArray('aa')
qba = QByteArray('$2b$12$3qGuFDjGEvLGcIgmPTGX8OOECLYRvuC5jd/fPu1VRbmgcvhOd5oYq')
print(f'QByteArray:\t\t\t\t {qba}')
qba_hex = qba.toHex()
print('QByteArray to hex QByteArray')
print(f'QByteArray to hex:\t\t {qba_hex}')
print('QByteArray from hex QByteArray')
print(f'QByteArray from hex:\t {QByteArray.fromHex(qba_hex)}')

print('\n')
# ba = b'aa'
ba = b'$2b$12$3qGuFDjGEvLGcIgmPTGX8OOECLYRvuC5jd/fPu1VRbmgcvhOd5oYq'
print(f'bytes:\t\t\t\t\t {ba}')
ba_hex = ba.hex()
print('bytes to hex string')
print(f'bytes to hex:\t\t\t {ba_hex}')
print('bytes from hex string')
print(f'bytes from hex:\t\t\t {bytes.fromhex(ba_hex)}')
print('\n')

# QByteArray to PyByte
# difference is at "to hex() and " from hex"
# QByteArray: toHex() returns QByteArray, fromHex() takes QByteArray as a parameter
# bytes: hex() returns str, fromhex() takes str as a parameter
qba_str = qba.toStdString()
print(f'QByteArray to str:\t\t {qba_str}')
# print(f'bytes from hex:\t\t\t {bytes.fromhex(qba_str)}')
print(f'bytes from str:\t\t\t {bytes.fromhex("6161")}')
print(f'bytes from str:\t\t\t {bytes.fromhex("aa")}')
print('\n')

# To convert QByteArray to bytes, need to convert it to Hex and then to str and
# then finally calls fromhex(str)
qba_hex_str = qba_hex.toStdString()
print(f'bytes from QByteArray hex str:\t\t {bytes.fromhex(qba_hex_str)}')

# This is the function that does everything
qba_data = qba.data()
print(f'QByteArry.data: {qba_data}({type(qba_data)})')
