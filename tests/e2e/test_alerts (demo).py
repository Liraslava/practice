from multiprocessing import Queue, Process
from multiprocessing.queues import Empty
from time import sleep
import data_input
import device

class Monitor(Process):
    def __init__(self, events_q: Queue):
        # вызываем конструктор базового класса
        super().__init__()
        self._events_q = events_q  # очередь событий для монитора (входящие сообщения)
        self._control_q = Queue()  # очередь управляющих команд (например, для остановки монитора)
        self._entity_queues = {}   # словарь очередей известных монитору сущностей
        self._force_quit = False   # флаг завершения работы монитора

    def _check_policies(self, event):
        print(f'[{self.__class__.__name__}] обрабатываем событие {event}')

        #  всё, что не разрешено, запрещено по умолчанию
        authorized = False
        # проверка на входе, что это экземпляр класса Event,

        if not isinstance(event, Event):
            return False

     # запрос на чтение данных из устройства
        if event.source == "Device" \
                and event.destination == "DataInput" \
                and event.operation == "read_request" \
                and event.parameters == "table_orders" \
                and event.data is None:
            authorized = True

        # ответ на запрос на чтение данных из устройства
        if event.source == "DataInput" \
                and event.destination == "Devise" \
                and event.operation == "read_response" \
                and event.parameters == "table_orders":
            authorized = True

    # выполнение разрешённого запроса
    # метод должен вызываться только после проверки политик безопасности
    def _proceed(self, event):
        print(f'[{self.__class__.__name__}] отправляем запрос {event}')
        try:
            # найдём очередь получателя события
            dst_q: Queue = self._entity_queues[event.destination]
            # и положим запрос в эту очередь
            dst_q.put(event)
        except  Exception as e:
            # например, запрос пришёл от или для неизвестной сущности
            print(f"[{self.__class__.__name__}] ошибка выполнение запроса {e}")

     # основной код работы монитора безопасности
    def run(self):
        print(f'[{self.__class__.__name__}] старт')

        # в цикле проверяет наличие новых событий,
        # выход из цикла по флагу _force_quit
        while self._force_quit is False:
            event = None
            try:
                # ожидание сделано неблокирующим,
                # чтобы можно было завершить работу монитора,
                # не дожидаясь нового сообщения
                event = self._events_q.get_nowait()
                # сюда попадаем только в случае получение события,
                # теперь нужно проверить политики безопасности
                authorized = self._check_policies(event)
                if authorized:
                    # если политиками запрос авторизован - выполняем
                    self._proceed(event)
            except Empty:
                # сюда попадаем, если новых сообщений ещё нет,
                # в таком случае немного подождём
                sleep(0.5)
            except Exception as e:
                # что-то пошло не так, выведем сообщение об ошибке
                print(f"[{self.__class__.__name__}] ошибка обработки {e}, {event}")
            self._check_control_q()
        print(f'[{self.__class__.__name__}] завершение работы')

    # запрос на остановку работы монитора безопасности для завершения работы
    # может вызываться вне процесса монитора
    def stop(self):
        # поскольку монитор работает в отдельном процессе,
        # запрос помещается в очередь, которая проверяется из процесса монитора
        request = ControlEvent(operation='stop')
        self._control_q.put(request)

monitor = Monitor(monitor_events_queue)


monitor.start()
device.start()
data_input.start()
data_input.send_data()
sleep(1)
data_input.read_data()
sleep(2)