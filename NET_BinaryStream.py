from io import BytesIO
import struct

class BinaryWrite:
    def __init__(self):
        self._stream = BytesIO()

    def _add_7bit_int(self, value):
        temp =abs(value)
        byted = ""
        while temp >= 128:
           byted += chr(0x000000FF & (temp | 0x80))
           temp >>= 7
        byted += chr(temp)
        if len(byted) > 1:
            self._stream.write( (byted.encode())[1::] )
        else:
            self._stream.write( (byted.encode()))

    def add_string(self, value):
        self._add_7bit_int(len(bytes(value.encode('utf-8'))))
        self._stream.write( bytes(value.encode('utf-8')) )

    def add_int(self, value):
        self._stream.write(struct.pack("<i", value))

    def add_bool(self, value):
        self._stream.write(struct.pack("<?", value))

    def add_float(self, value):
        self._stream.write(struct.pack("<f", value))

    def add_double(self, value):
        self._stream.write(struct.pack("<d", value))

    def getValue(self):
        return self._stream.getvalue()

class BinaryRead:
        def __init__(self, buffer):
            self._buffer = buffer 
            self.__index = 0 #Позиция в буффере 

        def read_str(self):
            num = self.read_7bit_int(self.__index) #Читаем разделитель
            self.__index += num[1] #Пропускаем байты разделителя
            result = self._buffer[self.__index:self.__index+num[0]] #Значение
            self.__index += num[0] #Пропускам символы

            result = struct.unpack("<"+str(num[0])+"s", result)[0] #Распаковка значение
            return bytes(result).decode() #Декодирование в str

        def read_bool(self):
            local = self._buffer[self.__index:self.__index+1] #Читаем 1 байт для типа bool
            self.__index += 1 #Говорим объекту, что взяли 1 байт
            return struct.unpack("<?", local)[0] #Распаковка байтов

        def read_int(self):
            local = self._buffer[self.__index:self.__index+4] 
            self.__index += 4 
            return struct.unpack("<i", local)[0] 

        def read_float(self):
            local = self._buffer[self.__index:self.__index+4] 
            self.__index += 4 
            return struct.unpack("<f", local)[0] 

        def read_double(self):
            local = self._buffer[self.__index:self.__index+8] 
            self.__index += 8 
            return struct.unpack("<d", local)[0]

        def pull(self, count, index = 0):
            return self._buffer[index:index+count] #Вернуть определённый байт

        def read_7bit_int(self, __index = 0):
            value = 0 
            shift = 0 #Сдвиг
            numbyte =  0 #Кол-во использованных байтов
            while True:
                numbyte += 1
                val = ord(self.pull(1, __index))
                __index +=1
                if val & 128 == 0: 
                    break
                value |= (val & 0x7F) << shift
                shift += 7
                
            result = value | (val << shift) 
            return (result, numbyte)

        def read_list_str(self):
            num = self.read_7bit_int() #Разделитель сколько байтов прочитать, кол-во пропускаемых байтов
            callList = [] #Список с итоговыми str знвчениями
            strbytes = b'' #Массив байтов, который будет переделан в str
            f = BytesIO(self._buffer)
            position = 0 #Точная позиция потока в цикле
            breakpointposition = -num[1]  #Позиция при которой нужно заканчивать читать байты

            c = b'' #Перезаписываемая переменная для каждого байта
            while c != b'\x00': #Пока не упераемся в мусор
                c = f.read(1)  #Читаем 1 байт из потока 
                if breakpointposition >= num[0]: 
                    num = self.read_7bit_int(position) #Определяем реальное 
                    breakpointposition = -num[1] 
                    callList.append(strbytes.decode('utf-8')) #Добавляем в список строку из байтов
                    strbytes = b''
                elif breakpointposition >= 0: #Если breakpointposition >= 0, то это символ
                    strbytes += c  
                breakpointposition += 1
                position += 1
            return callList



if __name__ == "__main__":
    pass
