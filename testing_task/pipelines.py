import logging

from itemadapter import ItemAdapter


class EmptyFieldsPipeline:
    """Ищет в элементе поля с None, если находит, то
       генерирует ошибку в лог.
    """
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        find_none = 0
        for key, value in adapter.items():
            if value == None:
                adapter[key] = 'NULL'
                find_none += 1
        if find_none:
            if find_none == 1:
                text = (f'При обработке записи обнаруженно '
                        f'пустое поле \n{item!r}')
            else:
                text = (f'При обработке записи обнаруженны '
                        f'пустые поля \n{item!r}')
            logging.warning(text)
        return item


class StatusBuildPipeline:
    """Обрабатывает поле status для удобства чтения."""
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['status'] == 0:
            adapter['status'] = 'Строится'
        elif adapter['status'] == 1:
            adapter['status'] = 'Сдан'
        elif adapter['status'] == 2:
            adapter['status'] = 'Проблемный'
        else:
            logging.warning(f'У новостройки с id {item["id_from_site"]} '
                            f'неизвестный статус = {item["status"]}.')
        return item


class ProcentSaleBuildPipeline:
    """Если у новостройки статус 'Строится', то пытается обработать
       поле 'распроданность квартир' для отображения в %.
    """
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['status'] == 'Строится':
            procent = adapter['sale_apartments']
            if procent != None:
                adapter['sale_apartments'] = int(procent * 100)
            else:
                logging.warning(
                    f'При обработке новостройки с id {item["id_from_site"]} '
                    f'не удалось найти "распроданность квартир"'
                )
        return item
