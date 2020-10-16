Данный модуль нужен для того, чтобы работа с NET библиотеками BinaryReader и BinaryWriter

Для передачи дробных чисел не стоит использовать метод add_float т.к. в BinaryReader (NET 4.8.03752) нет метода ReadFloat.
Лучше использовать тип Double